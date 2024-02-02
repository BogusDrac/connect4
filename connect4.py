import numpy as np
import pygame
import sys
import math

BLUE = (0, 0, 225)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7

def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Check horizontal location for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # Check Vertical location for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

def display_winner(winner_text, color):
    label = myfont.render(winner_text, 1, color)
    screen.blit(label, (40, 10))
    pygame.display.update()

def restart_game():
    global board, game_over, turn
    board = create_board()
    draw_board(board)
    game_over = False
    turn = 0



board = create_board()
game_over = False
turn = 0

print_board(board)



pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            col = int(math.floor(posx / SQUARESIZE))

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, turn + 1)

                if winning_move(board, turn + 1):
                    winner_text = f"Player {turn + 1} wins!!"
                    display_winner(winner_text, RED if turn == 0 else YELLOW)
                    game_over = True

                print_board(board)
                draw_board(board)

                turn += 1
                turn %= 2

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            restart_game()
            pygame.time.wait(1000)  # Add a delay to prevent immediate key presses from restarting the game

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            sys.exit()
