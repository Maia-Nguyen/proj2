import pygame
import sys

pygame.init()

BACKGROUND_COLOR = (202, 228, 241)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (61, 117, 69)
RED = (245, 90, 66)
WIDTH = 50
HEIGHT = 50
MARGIN = 10
SCREEN_WIDTH = 490
SCREEN_HEIGHT = 490
BASE_FONT = pygame.font.SysFont('arial',25)

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Game of Nim')

text_box = pygame.Rect(220,(SCREEN_HEIGHT/2+35), 50, 35)
start_button = pygame.Rect(200,(SCREEN_HEIGHT/2+125), 90, 35)
done_button = pygame.Rect(200,(SCREEN_HEIGHT/2+155), 90, 35)
r1_rect = pygame.Rect(WIDTH*2, HEIGHT*2, 530, HEIGHT)
r2_rect = pygame.Rect(WIDTH*2, (MARGIN + HEIGHT) + (HEIGHT*2), 530, HEIGHT)
r3_rect = pygame.Rect(WIDTH*2, (MARGIN + HEIGHT) * 2 + (HEIGHT*2), 530, HEIGHT)
r4_rect = pygame.Rect(WIDTH*2, (MARGIN + HEIGHT) * 3  + (HEIGHT*2), 530, HEIGHT)
r5_rect = pygame.Rect(WIDTH*2, (MARGIN + HEIGHT) * 4 + (HEIGHT*2), 530, HEIGHT)
r6_rect = pygame.Rect(WIDTH*2, (MARGIN + HEIGHT) * 5 + (HEIGHT*2), 530, HEIGHT)
r7_rect = pygame.Rect(WIDTH*2, (MARGIN + HEIGHT) * 6 + (HEIGHT*2), 530, HEIGHT)
r8_rect = pygame.Rect(WIDTH*2, (MARGIN + HEIGHT) * 7 + (HEIGHT*2), 530, HEIGHT)
r9_rect = pygame.Rect(WIDTH*2, (MARGIN + HEIGHT) * 8 + (HEIGHT*2), 530, HEIGHT)

# Create board
grid = []
for row in range(5):
    grid.append([])
    for column in range(5):
        grid[row].append(0)

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
                if event.key == pygame.K_RETURN:
                    if len(blocks) < 5:
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

        text = BASE_FONT.render('Enter number(0-5) of objects to add to row', True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2-40))  
        screen.blit(text, text_rect)

        text = BASE_FONT.render('Press |START| when ready to start', True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2-10))  
        screen.blit(text, text_rect)

        pygame.draw.rect(screen, WHITE, text_box)
        text = BASE_FONT.render(input, True, BLACK)
        screen.blit(text, (text_box.x+18,text_box.y+5))

        # display user input
        output = str(blocks)
        text = BASE_FONT.render(output, True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2+90))
        screen.blit(text, text_rect)

        # start button
        pygame.draw.rect(screen, GREEN, start_button)
        text = BASE_FONT.render('START', True, WHITE)
        screen.blit(text, (start_button.x+4, start_button.y+3))
        
        # update the screen
        pygame.display.update()

# Set blocks in board to green if user inputs a number of objects for a row
def set_blocks(blocks, player):
    r = 0
    won = False
    actions = []

    won = all(row == 0 for row in blocks)
    
    if won == True:
        return won

    # create empty grid
    for row in range(5):
        for column in range(5):
            grid[row][column] = 0

    # for each index from user input, populate row with number 1
    # example, user inputs [1,2,1]
    # row 1 col 1 = 1, row 2 col 1 = 1, row 2 col 2 = 1, row 3 col 1 = 1
    for row in blocks:
        c = 0
        while c < row:
            grid[r][c] = 1
            c += 1
        r+=1

    for row in range(5):
        for column in range(5):
            color = WHITE
            # since we populated the grid with 1's depending on user input, set the board
            # by creating color blocks
            if grid[row][column] == 1:
                if player == 1:
                    color = GREEN
                else:
                    color = RED
            # draw the objects
            obj_rect = pygame.Rect((MARGIN + WIDTH) * column + (WIDTH*2),
                            (MARGIN + HEIGHT) * row + (HEIGHT*2), WIDTH, HEIGHT)
            pygame.draw.rect(screen, color, obj_rect)

    color = GREEN if player == 1 else RED
    text = BASE_FONT.render((f'Player {player} moves'), True, color)
    text_rect = text.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/6-10))  
    screen.blit(text, text_rect)

    pygame.draw.rect(screen, color, done_button)
    text = BASE_FONT.render('DONE', True, WHITE)
    screen.blit(text, (done_button.x+8, done_button.y+3))
    pygame.display.flip()

# Handles events on game board
def board_events(event,blocks):
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        for r in range(0, len(blocks)):
            if r == 0:
                if(r1_rect.collidepoint(pos)):
                    if blocks[r] > 0:
                        blocks[r] -= 1
                    print(blocks[r])
            if r == 1:
                if(r2_rect.collidepoint(pos)):
                    if blocks[r] > 0:
                        blocks[r] -= 1
                    print(blocks[r])
            if r == 2:
                if(r3_rect.collidepoint(pos)):
                    if blocks[r] > 0:
                        blocks[r] -= 1
                    print(blocks[r])
            if r == 3:
                if(r4_rect.collidepoint(pos)):
                    if blocks[r] > 0:
                        blocks[r] -= 1
                    print(blocks[r])
            if r == 4:
                if(r5_rect.collidepoint(pos)):
                    if blocks[r] > 0:
                        blocks[r] -= 1
                    print(blocks[r])

def actions(blocks):
    moves = []
    r = 1

    for row in blocks:
        if row != 0:
            n = 1
            while n <= row:
                moves.append([r, n])
                n += 1
        r += 1
    
    print(moves)
    return moves

# Game screen
def game(blocks):
    run = True
    won = False
    player = 1

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            board_events(event, blocks)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # handles player handoff when user clicks 'done' button
                if(done_button.collidepoint(pos)):
                    if player == 1:
                        player = 2
                    elif player == 2:
                        player = 1

        pos_actions = actions(blocks)

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

        text = BASE_FONT.render((f'Player {player} loses'), True, color)
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))  
        screen.blit(text, text_rect)

        pygame.display.flip()   

blocks = start()   
player = game(blocks)
end(player)

pygame.quit()