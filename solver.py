from transposition import Transposition
from moveSorter import MoveSorter
from board import Board
import copy
import math

EMPTY = 0
class Solver:
    
	columnOrder = []
	nodesvisited = 0
	def __init__(self):
		self.table = Transposition()
		
		for i in range( Board.COLUMN_COUNT): 
			Solver.columnOrder.append(int(Board.COLUMN_COUNT/2) + (1-2*(i%2))*int((i+1)/2))

	def negamax_solverr(self, board, alpha, beta):
		
		
		Solver.nodesvisited +=1
  
		next = board.possibleNonLoosingMoves()
		if next ==0 :
			return -(Board.COLUMN_COUNT* Board.ROW_COUNT - board.nbMoves())/2
  
		if board.boardfilled():
			return  0 
		
		min = -int((Board.COLUMN_COUNT* Board.ROW_COUNT -2 - board.move_number)/2)
		if alpha < min : 
			alpha = min
			if alpha >= beta:
				return alpha

		max = int((Board.COLUMN_COUNT* Board.ROW_COUNT -1 - board.move_number)/2)
		if board.key() in self.table.ttable:
			max = self.table.get(board.key()) + Board.MIN_SCORE -1
			
		if beta > max:
			beta = max
			if alpha >= beta:
				return beta

		moves = MoveSorter()

		for i in range(Board.COLUMN_COUNT-1,-1,-1):
			if move:= next & Board.column_mask(Solver.columnOrder[i]):
				moves.add(move, board.moveScore(move))
    
		while (next := moves.getNext()):
		
			board2 = copy.deepcopy(board)
			board2.play(next)
			new_score=  self.negamax_solverr(board2 , -beta,-alpha)
			new_score = -new_score

			if new_score>= beta:
				
				return new_score

			if new_score> alpha:
				alpha = new_score
		
		self.table.put(board.key(), alpha - Board.MIN_SCORE+1)
	
		return alpha
		
	def window_eval(window, piece):
		score = 0
		# if window.count(piece) == 4:
		# 	score += 80
		if window.count(piece) == 3 and window.count(EMPTY) == 1:
			score += 5
		elif window.count(piece) == 2 and window.count(EMPTY) == 2:
			score+= 1
		elif window.count(piece) == 0 and window.count(EMPTY) == 1:
			score -= 4
		return score

	def score_position( board , piece):
		score = 0
		
		if board.boardfilled():
			return 0
		
		boord = board.getArrayRep()

		#score horizontal
		for c in range(Board.COLUMN_COUNT-3):
			for r in range(Board.ROW_COUNT):
				window = [int(i) for i in boord[r, c:c+4]]
				score += Solver.window_eval(window, piece)
		
		#score vertical
		for c in range(Board.COLUMN_COUNT):
			for r in range(Board.ROW_COUNT-3):
				window = [int(i) for i in boord[r:r+4,c]]
				score += Solver.window_eval(window, piece)

		#score l to r
		for c in range(Board.COLUMN_COUNT-3):
			for r in range(Board.ROW_COUNT-3):
				window = [boord[r+i][c+i] for i in range(4)]
				score += Solver.window_eval(window, piece)

		#score r to l
		for c in range(Board.COLUMN_COUNT-3):
			for r in range(Board.ROW_COUNT-3):
				window = [boord[r-i][c+i] for i in range(4)]
				score += Solver.window_eval(window, piece)
		
		return score

	def minimax1(self,board, depth,alpha, beta):

		Solver.nodesvisited +=1
		next = board.possibleNonLoosingMoves()		
  
		if depth == 0 or board.boardfilled(): 
			return None ,( -Solver.score_position(board, 3- board.current_piece) + Solver.score_position(board, board.current_piece) )* (1+ 0.001*depth)

		bestScore = -math.inf

		
		bestcol = Solver.columnOrder[0]
			
		for col in Solver.columnOrder:
			if next & Board.column_mask(col) :

				if board.isWinningMove(col):
					score = 100000* (1 + 0.001* depth)
					
					return col ,score

		for col in Solver.columnOrder:
			if next & Board.column_mask(col) :

				board2 = copy.deepcopy(board)
				board2.drop_piece(col)
				
				k ,new_score  = self.minimax1(board2,  depth-1,-beta,-alpha)
				new_score = - new_score

				if new_score> bestScore:
					bestScore = new_score
					bestcol = col
					

				if new_score> alpha:
					alpha = new_score
					if alpha >= beta:
						break
		return bestcol, bestScore


	def solve(self, board, weak = False):

		if(board.canWinNext()):
			return int((Board.COLUMN_COUNT* Board.ROW_COUNT +1 - board.move_number)/2)
		min = int(-(Board.COLUMN_COUNT* Board.ROW_COUNT - board.move_number)/2)
		max = int((Board.COLUMN_COUNT* Board.ROW_COUNT +1 - board.move_number)/2)
		
		if weak:
			min = -1
			max = 1
		while min < max:
			med = min + int((max - min)/2)
			if(med <= 0 and int(min/2) < med) :
				med = int(min/2)
			elif med >= 0 and int(max/2) > med:
				med = int(max/2)
			r = self.negamax_solverr(board, med, med+1 )
	
			if(r <= med):
				max = r
			else:
				min = r
		return min

	def analyze(self, board, weak = False):
		score = {}
		Solver.nodesvisited = 0
		for col in Solver.columnOrder:
			if board.canPlay(col):
				board2 = copy.deepcopy(board)
				board2.playCol(col)
				score[col] = - self.solve(board2, weak)
			if board.canWinNext():
				if board.isWinningMove(col):
					score[col] = int((Board.COLUMN_COUNT* Board.ROW_COUNT +1 - board.move_number)/2)
					break
		return score
