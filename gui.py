from game_of_nim import GameOfNim
from games import *

import pygame
import sys

pygame.init()

BACKGROUND_COLOR = (202, 228, 241)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (61, 117, 69)
RED = (245, 90, 66)
WIDTH = 0
HEIGHT = 0
MARGIN = 100
SPACING = 10
SCREEN_WIDTH = 490
SCREEN_HEIGHT = 490
BASE_FONT = pygame.font.SysFont('arial', 25)

modified = -1  # -1 when player hasn't taken their turn, row # when player has modified it
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Game of Nim')

text_box = pygame.Rect(220, (SCREEN_HEIGHT/2+35), 50, 35)
start_button = pygame.Rect(200, (SCREEN_HEIGHT/2+125), 90, 35)
done_button = pygame.Rect(200, (SCREEN_HEIGHT/2+155), 90, 35)
row_rects = []  # store row rects to register clicks

# Start Menu


def start():
    start = True
    input = ''
    blocks = []
    output = ''

    while start:
        # handle events
        for event in pygame.event.get():
            # quit game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # if user clicks start
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if (start_button.collidepoint(pos)):
                    if len(blocks) > 0:
                        start = False
                        return blocks
            # user types input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input = input[:-1]
                elif event.key == pygame.K_RETURN:
                    if len(blocks) < 8:
                        blocks.append(int(input))
                        input = ''
                        print(blocks)
                else:
                    if len(input) < 1:
                        input += event.unicode

        # displayer title and game rules
        screen.fill((115, 171, 199))
        font = pygame.font.SysFont('arial', 40, bold=True)
        title = font.render('Game of Nim', True, WHITE)
        textRect = title.get_rect()
        textRect.center = (SCREEN_WIDTH/2, (SCREEN_HEIGHT/2-100))
        screen.blit(title, textRect)

        text = BASE_FONT.render(
            'Enter number(0-5) of objects to add to row', True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2-40))
        screen.blit(text, text_rect)

        text = BASE_FONT.render(
            'Press |START| when ready to start', True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2-10))
        screen.blit(text, text_rect)

        pygame.draw.rect(screen, WHITE, text_box)
        text = BASE_FONT.render(input, True, BLACK)
        screen.blit(text, (text_box.x+18, text_box.y+5))

        # display user input
        output = str(blocks)
        text = BASE_FONT.render(output, True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2+90))
        screen.blit(text, text_rect)

        # start button
        pygame.draw.rect(screen, GREEN, start_button)
        text = BASE_FONT.render('START', True, WHITE)
        screen.blit(text, (start_button.x+4, start_button.y+3))

        # update the screen
        pygame.display.update()

# calculates WIDTH and HEIGHT based off of the number of columns and rows
# + add rects to row_rects based on HEIGHT / row count


def setup(blocks):
    global WIDTH, HEIGHT

    # calculate width and height of rectangles before entering loops
    WIDTH = (SCREEN_WIDTH - 2 * MARGIN -
             (max(blocks) - 1) * SPACING) / max(blocks)
    HEIGHT = (SCREEN_HEIGHT - 2 * MARGIN -
              (len(blocks) - 1) * SPACING) / len(blocks)

    for row in range(len(blocks)):
        row_rects.append(pygame.Rect(MARGIN, MARGIN + (HEIGHT + SPACING) * row,
                                     SCREEN_WIDTH - 2 * MARGIN, HEIGHT))

# Set blocks in board to green if user inputs a number of objects for a row


def set_blocks(blocks, player):
    won = False
    actions = []
    color = GREEN if player == 1 else RED

    won = all(row == 0 for row in blocks)

    if won == True:
        return won

    for idx, row in enumerate(blocks):
        for column in range(row):
            # draw the objects
            obj_rect = pygame.Rect(MARGIN + (WIDTH + SPACING) * column,
                                   MARGIN + (HEIGHT + SPACING) * idx, WIDTH, HEIGHT)
            pygame.draw.rect(screen, color, obj_rect)

    text = BASE_FONT.render((f'Player {player} moves'), True, color)
    text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/6-10))
    screen.blit(text, text_rect)

    pygame.draw.rect(screen, color, done_button)
    text = BASE_FONT.render('DONE', True, WHITE)
    screen.blit(text, (done_button.x+8, done_button.y+3))
    pygame.display.flip()

# Handles events on game board


def board_events(event, blocks):
    global modified
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        for idx, rect in enumerate(row_rects):
            if(rect.collidepoint(pos) and (modified == idx or modified == -1)):
                if blocks[idx] > 0:
                    modified = idx
                    blocks[idx] -= 1


def actions(blocks):
    moves = []
    r = 1

    for idx, row in enumerate(blocks):
        for n in range(1, row + 1):
            moves.append([idx, n])

    print(moves)
    return moves

# Game screen


def game(blocks):
    run = True
    won = False
    player = 1

    while run:
        if player == 2:
            # grab player 2's best move
            nim = GameOfNim(board=blocks, to_move=0)
            move = alpha_beta_search(nim.initial, nim)
            # modify the current blocks array
            blocks[move[0]] -= move[1]
            for block in blocks:
                if block is not 0:
                    player = 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            board_events(event, blocks)
            if event.type == pygame.MOUSEBUTTONDOWN:
                global modified
                pos = pygame.mouse.get_pos()
                # handles player handoff when user clicks 'done' button
                if(done_button.collidepoint(pos) and modified != -1):
                    modified = -1
                    player = 2 if player == 1 else 1

        won = set_blocks(blocks, player)
        if won == True:
            run = False
        screen.fill(BACKGROUND_COLOR)

    return player


def end(player):
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                return run

        color = GREEN if player == 1 else RED

        text = BASE_FONT.render((f'Player {player} wins'), True, color)
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(text, text_rect)

        pygame.display.flip()


blocks = start()
setup(blocks)
player = game(blocks)
end(player)

pygame.quit()
