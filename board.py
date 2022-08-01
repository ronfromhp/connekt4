import random
from numpy import zeros, flip
import numpy

def bottom( width, height) : 
		return  0  if width==0 else bottom(width-1, height) | 1 << (width-1)*(height+1)

class Board:
    
	ROW_COUNT = 6
	COLUMN_COUNT = 7
	RED_PIECE = 1
	YELLOW_PIECE = 2
	current_piece = 0  
	MIN_SCORE = -(ROW_COUNT* COLUMN_COUNT)/2 +3
	MAX_SCORE = (ROW_COUNT * COLUMN_COUNT)/2 -3
	moves = ""

	def __init__(self , move_number=0) -> None:
		# self.board = board
		self.move_number = move_number

		Board.current_piece = random.choice((Board.YELLOW_PIECE, Board.RED_PIECE))
		self.current_position = 0
		self.mask = 0

	def create_board():
		board = zeros((Board.ROW_COUNT,Board.COLUMN_COUNT))
		return board

	def drop_piece(self , col):

		self.playCol(col)


	def print_board(self):
		print(self.nbMoves())
		print(flip(self.getArrayRep(), 0))
		print(Board.moves)

	def boardfilled(self):
		if self.nbMoves() == Board.ROW_COUNT* Board.COLUMN_COUNT:
			return True
		return False


	def winning_move(self, piece):
		
		boord = self.getArrayRep()

		# Check horizontal locations for win
		for c in range(Board.COLUMN_COUNT-3):
			for r in range(Board.ROW_COUNT):
				for k in range(4):
					if boord[r][c+k] != piece:
						break
					if k ==3 : return True

		# Check vertical locations for win
		for c in range(Board.COLUMN_COUNT):
			for r in range(Board.ROW_COUNT-3):
				for k in range(4):
					if boord[r+k][c] != piece:
						break
					if k ==3 : return True

		# Check positively sloped diaganols
		for c in range(Board.COLUMN_COUNT-3):
			for r in range(Board.ROW_COUNT-3):
				for k in range(4):
					if boord[r+k][c+k] != piece:
						break
					if k ==3 : return True

		# Check negatively sloped diaganols
		for c in range(Board.COLUMN_COUNT-3):
			for r in range(3, Board.ROW_COUNT):
				for k in range(4):
					if boord[r-k][c+k] != piece:
						break
					if k ==3 : return True

	def getArrayRep(board):
		bpos = board.current_position
		bmask = board.mask

		board = zeros((Board.ROW_COUNT + 1,Board.COLUMN_COUNT))
		for i in range(Board.COLUMN_COUNT):
			for j in range(Board.ROW_COUNT+ 1):
				if bmask & pow(2, i*7 + j):
					if bpos & pow(2, i*7+ j):
						board[j][i] = Board.current_piece
					else:
						board[j][i] = 3- Board.current_piece
		board = numpy.delete(board, (6), axis = 0)
		return board

	def getBitmaskRep(move):
		board = zeros((Board.ROW_COUNT + 1,Board.COLUMN_COUNT))
		for i in range(Board.COLUMN_COUNT):
			for j in range(Board.ROW_COUNT+ 1):
				if move & pow(2, i*7 + j):
					board[j][i] = 1
		board = numpy.delete(board, (6), axis = 0)
		return board

	def canPlay(self, col): 
		return (self.mask & Board.top_mask_col(col)) == 0

	def play(self, move):
      
		self.current_position ^= self.mask
		self.mask |= move
		self.move_number += 1
  

	def playCol(self, col):
		if self.canPlay(col):
			self.play((self.mask + Board.bottom_mask_col(col)) & Board.column_mask(col))
		else : print("errrrrrrrrrrrrrrrrror")
  
	def isWinningMove(self, col):
		return self.winning_position() & self.possible() & Board.column_mask(col)

	def canWinNext(self):
		return self.winning_position() & self.possible()

	def nbMoves(self):
		return self.move_number

	def key(self):
		return self.current_position + self.mask

	def alignment(pos):
        # // horizontal 
		m = pos & (pos >> (Board.ROW_COUNT+1))
		if(m & (m >> (2*(Board.ROW_COUNT+1)))):
			return True

        # // diagonal 1
		m = pos & (pos >> Board.ROW_COUNT)
		if(m & (m >> (2*Board.ROW_COUNT))):
			return True

        # // diagonal 2 
		m = pos & (pos >> (Board.ROW_COUNT+2))
		if(m & (m >> (2*(Board.ROW_COUNT+2)))) :
			return True

        # // vertical
		m = pos & (pos >> 1)
		if(m & (m >> 2)) :
			return True

		return False

	def possibleNonLoosingMoves(self) :

		possible_mask = self.possible()
		opponent_win = self.opponent_winning_position()
		forced_moves = possible_mask & opponent_win
		if(forced_moves) :
			if(forced_moves & (forced_moves - 1)):
				return 0
			else: possible_mask = forced_moves   
		return possible_mask & ~(opponent_win >> 1)


	bottom_mask = bottom(COLUMN_COUNT, ROW_COUNT)
	board_mask = bottom_mask * ((1 << ROW_COUNT)-1)


	def winning_position(self) :
		return Board.compute_winning_position(self.current_position, self.mask)

    #   /*
    #    * Return a bitmask of the possible winning positions for the opponent
    #    */

	def opponent_winning_position(self) :
		return Board.compute_winning_position(self.current_position ^ self.mask, self.mask)

	def possible(self): 
		return (self.mask + Board.bottom_mask) & Board.board_mask

	def moveScore(self, move):
		return Board.popcount( Board.compute_winning_position(self.current_position | move, self.mask))

	def popcount(m):
		c = 0 
		while m:
			m &= m-1
			c += 1
		return c

	def compute_winning_position(position, mask):
		r = (position << 1) & (position << 2) & (position << 3)
		
		p = (position << (Board.ROW_COUNT+1)) & (position << 2*(Board.ROW_COUNT+1))
		r |= p & (position << 3*(Board.ROW_COUNT+1))
		r |= p & (position >> (Board.ROW_COUNT+1))
		p = (position >> (Board.ROW_COUNT+1)) & (position >> 2*(Board.ROW_COUNT+1))
		r |= p & (position << (Board.ROW_COUNT+1))
		r |= p & (position >> 3*(Board.ROW_COUNT+1))

		p = (position << Board.ROW_COUNT) & (position << 2*Board.ROW_COUNT)
		r |= p & (position << 3*Board.ROW_COUNT)
		r |= p & (position >> Board.ROW_COUNT)
		p = (position >> Board.ROW_COUNT) & (position >> 2*Board.ROW_COUNT)
		r |= p & (position << Board.ROW_COUNT)
		r |= p & (position >> 3*Board.ROW_COUNT)

		p = (position << (Board.ROW_COUNT+2)) & (position << 2*(Board.ROW_COUNT+2))
		r |= p & (position << 3*(Board.ROW_COUNT+2))
		r |= p & (position >> (Board.ROW_COUNT+2))
		p = (position >> (Board.ROW_COUNT+2)) & (position >> 2*(Board.ROW_COUNT+2))
		r |= p & (position << (Board.ROW_COUNT+2))
		r |= p & (position >> 3*(Board.ROW_COUNT+2))

		return r & (Board.board_mask ^ mask)

	def top_mask_col(col):
		return ((1) << (Board.ROW_COUNT - 1)) << col*(Board.ROW_COUNT+1)
      
    #   // return a bitmask containg a single 1 corresponding to the bottom cell of a given column
	def bottom_mask_col(col):
		return (1) << col*(Board.ROW_COUNT+1)
    
    #  return a bitmask 1 on all the cells of a given column
	def column_mask(col):
		return (((1) << Board.ROW_COUNT)-1) << col*(Board.ROW_COUNT+1)