
from __future__ import with_statement
import pygame
import sys
import math
from pygame import MOUSEBUTTONDOWN, gfxdraw
from board import Board
from solver import Solver

BLUE = (72, 63, 161)
BLACK = (0,0,0)
RED = (153, 0, 0)
YELLOW = (230, 202, 25)
WHITE = (250,250,250)
EMPTY = 0
RED_PIECE = 1
YELLOW_PIECE = 2
DEPTH = 6


ROW_COUNT = 6
COLUMN_COUNT = 7

AI_PIECE = YELLOW_PIECE


def make_move(col):

	global Color, game_over, screen, nodesvisited
	if  board.canPlay(col):
			
		board.drop_piece(col)
		Board.current_piece = 3 - Board.current_piece

		if board.winning_move(3-board.current_piece):
			Color = YELLOW if board.current_piece == RED_PIECE else RED
			winstring = "Player "+ str(3 - board.current_piece) +" wins!!"
			label = myfont.render( winstring , True, Color)
			screen.blit(label, (20,5))
			game_over = True
		elif board.boardfilled():
			label = myfont.render( "Draw!!" , True, Color)
			screen.blit(label, (30,10))
			game_over = True
	
		Board.moves = Board.moves + str(col+1)
		board.print_board()
		print("eval: " , evaluation)
		print("ends in  :" , 42 - board.nbMoves() - abs(evaluation))
		draw_board(board)

board = Board()
solver = Solver()
board.print_board()
game_over = False


pygame.init()

SQUARESIZE = 100

ACTIVE_COLOR = pygame.Color('dodgerblue1')
INACTIVE_COLOR = pygame.Color('dodgerblue4')
FONT = pygame.font.SysFont("arial", 20)
# Font(None, 32)
AI_Enabled = True

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height+50)

RADIUS = int(SQUARESIZE/2 - 5)

evalbarfont = pygame.font.SysFont("monospace", 23)
evalstr = "0-0"
evalsurf = FONT.render(evalstr, True, WHITE)

screen = pygame.display.set_mode(size)


def draw_button(button, screen):
    """Draw the button rect and the text surface."""
    pygame.draw.rect(screen, button['color'], button['rect'])
    screen.blit(button['text'], button['text rect'])


def create_button(x, y, w, h, text, callback):
    """A button is a dictionary that contains the relevant data.

    Consists of a rect, text surface and text rect, color and a
    callback function.
    """
    # The button is a dictionary consisting of the rect, text,
    # text rect, color and the callback function.
    text_surf = FONT.render(text, True, WHITE)
    button_rect = pygame.Rect(x, y, w, h)
    text_rect = text_surf.get_rect(center=button_rect.center)
    button = {
        'rect': button_rect,
        'text': text_surf,
        'text rect': text_rect,
        'color': INACTIVE_COLOR,
        'callback': callback,
        }
    return button

def toggleAi():
	global AI_Enabled
	AI_Enabled = not AI_Enabled
	if not AI_Enabled:
		btnAiToggle['text'] = FONT.render("Manual", True, WHITE)
		btnAiToggle['text rect'] = btnAiToggle['text'].get_rect(center = btnAiToggle['rect'].center)
	else:
		btnAiToggle['text'] = FONT.render("AI", True, WHITE)
		btnAiToggle['text rect'] = btnAiToggle['text'].get_rect(center = btnAiToggle['rect'].center)

def retryGame():
	global game_over 
	game_over = False

def depthincr():
	global DEPTH
	DEPTH += 1

def depthdecr():
	global DEPTH
	DEPTH -= 1 

def draw_board(board):
	
	boord = board.getArrayRep()
	global evaluation
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			gfxdraw.aacircle(screen, int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2), RADIUS, BLACK)
			gfxdraw.filled_circle(screen, int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2), RADIUS, BLACK)

	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if boord[r][c] == 1:
				gfxdraw.filled_circle(screen, int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE+SQUARESIZE/2), RADIUS-5, RED)
				gfxdraw.aacircle(screen, int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE+SQUARESIZE/2), RADIUS-5, RED)
			elif boord[r][c] == 2: 
				gfxdraw.aacircle(screen, int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE+SQUARESIZE/2), RADIUS-5, YELLOW)
				gfxdraw.filled_circle(screen, int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE+SQUARESIZE/2), RADIUS-5, YELLOW)

	if evaluation >100  or evaluation <-100 or  board.move_number> 17:
		if evaluation == 0:
			msg = "Draw in "
		else:
			msg = "You lose in " if evaluation >0 else "You win in "

		evalstr = msg + str(42 - board.nbMoves() - abs(evaluation)) + " moves"	
	else :
		evalstr = str(board.move_number) +"  |  Evaluation = " + str(evaluation) 

	nodestr = "|  Nodes visited = " + str(Solver.nodesvisited)
	dpthstr = "|  Depth = " + str(DEPTH)
	nodebar = FONT.render(nodestr, True, WHITE)
	dpthbar = FONT.render(dpthstr, True, WHITE)
	evalbar = FONT.render(evalstr, True, WHITE)
	barlen = (evaluation)/50
	yelobarlen = max(0, barlen)
	redbarlen = min(0, barlen)
	evalsurf = pygame.Surface((width, 50))
	evalsurf.blit(evalbar, (10,2))
	evalsurf.blit(dpthbar, (200,2))
	evalsurf.blit(nodebar, (350,2))

	pygame.draw.rect(evalsurf, RED, (0, 30, width/2 + width, 10 ))
	pygame.draw.rect(evalsurf, YELLOW, (0, 30, width/2 + width * (yelobarlen +redbarlen), 10 ))
	pygame.display.update()

	screen.blit(evalsurf, (0, height))
	
	
	for button in buttonlist:
		draw_button(button, screen)

	pygame.display.update()


btnAiToggle = create_button(width - 130, height + 2, 90, 25, 'AI', toggleAi)
btnRetry = create_button( screen.get_rect().centery -150 ,300,200,75, 'Retry', retryGame)
btnDepthincr = create_button( 300, height+1, 13, 13,"+", depthincr)
btnDepthdecr = create_button(300, btnDepthincr['rect'].bottom +1 ,13,13, "-", depthdecr )
buttonlist = [btnAiToggle, btnDepthdecr ,btnDepthincr]

pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)
nodesvisited = 0
livedepth = 0
evaluation = 0
draw_board(board)

while not game_over:

	playernotdone = True
	if board.current_piece == RED_PIECE:
		Color = RED
	else:  Color = YELLOW

	for event in pygame.event.get():

	
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			posx = event.pos[0]
			pygame.draw.circle(screen, Color, (posx, int(SQUARESIZE/2)), RADIUS)
			for button in buttonlist:
				if button['rect'].collidepoint(event.pos):
					button['color'] = ACTIVE_COLOR
				else:
					button['color'] = INACTIVE_COLOR
					
		pygame.display.update()
		#screen.blit(evalbar, (40,10))

		
		#get the position of user mouseclick
		if (event.type == pygame.MOUSEBUTTONDOWN or event.type ==pygame.KEYDOWN) and playernotdone:

			if event.type == pygame.MOUSEBUTTONDOWN:
				clicked = False
				for button in buttonlist:
					# `event.pos` is the mouse position.
					if button['rect'].collidepoint(event.pos):
						# Increment the number by calling the callback
						# function in the button list.
						button['callback']()
						clicked = True	
				
				if not clicked:

					pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
					posx = event.pos[0]
					col = int(math.floor(posx/SQUARESIZE))
					# make_move(col)
					# nodesvisited = 0
					playernotdone = False

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:
					col = 0
					playernotdone = False
				if event.key == pygame.K_2:
					col = 1
					playernotdone = False
				if event.key == pygame.K_3:
					col = 2
					playernotdone = False
				if event.key == pygame.K_4:
					col = 3
					playernotdone = False
				if event.key == pygame.K_5:
					col = 4
					playernotdone = False
				if event.key == pygame.K_6:
					col = 5
					playernotdone = False
				if event.key == pygame.K_7:
					col = 6
					playernotdone = False
				# AI test
				if board.move_number <20 :
					col, evaluation ,livedepth = solver.minimax1(board, 0, DEPTH,-math.inf , math.inf)
				else:
					col, evaluation = solver.negamax_solverr(board, -math.inf , math.inf )
				evaluation =-evaluation

			if playernotdone == False:
				make_move(col)
				nodesvisited = 0
				playernotdone = False

	if board.current_piece == AI_PIECE and AI_Enabled and not game_over:

		livedepth = 0
		
		#piece = YELLOW_PIECE         
		# pygame.time.wait(800)
		if board.move_number <15 :
			col , evaluation ,livedepth = solver.minimax1(board, 0 ,DEPTH, -math.inf, math.inf)
		else:
			analysis  = solver.analyze(board)
			print(analysis)  # logging , delete later
			col = max(analysis, key= lambda x : analysis[x])
			evaluation = analysis[col]	

		make_move(col)

	if game_over:

		draw_button(btnRetry, screen)
		pygame.display.update()
		madedec = False
		while not madedec:
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					if btnRetry['rect'].collidepoint(event.pos):
						game_over = False
						board = Board()
						Board.moves = ""
						nodesvisited = 0
					madedec = True
					
		pygame.time.wait(2000)
	draw_board(board)