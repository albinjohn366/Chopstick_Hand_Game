import pygame
import sys
from Chopstick import *

# Initializing pygame
pygame.init()

# Defining pygame appearance
size = (width, height) = (400, 600)
window = pygame.display.set_mode(size)
pygame.display.set_caption('Chopstick(Hand Game)')

# Making instances
game = Chopstick([(1, 1), (1, 1)])
ai = Chopstick_AI()
training_done = False
ai.train(10000)
mine = None
his = None

# Fonts
instruction_font = pygame.font.Font(pygame.font.get_default_font(), 20)

# images
one = pygame.transform.scale(pygame.image.load('pictures/1.png'), (120, 160))
two = pygame.transform.scale(pygame.image.load('pictures/2.png'), (80, 160))
three = pygame.transform.scale(pygame.image.load('pictures/3.png'), (140, 160))
four = pygame.transform.scale(pygame.image.load('pictures/4.png'), (140, 160))

while True:
    window.fill((255, 255, 255))
    # To exit from the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Displaying fingers
    picture_rect = dict()
    for row, player in enumerate(game.states):
        for side, number in enumerate(player):
            if number == 0:
                continue
            picture = one if number == 1 else two if number == 2 else three if \
                number == 3 else four
            picture_rect[row, side] = picture.get_rect()
            x_coordinate = width / 3 + (side * (width / 3 + 10))
            y_coordinate = height / 4 + (row * height / 2)
            picture_rect[row, side].center = (x_coordinate, y_coordinate)
            window.blit(picture, picture_rect[row, side])

    if not game.over:
        # Updating player turns
        if game.player:
            status = instruction_font.render('Players Turn', True, (0, 0, 0))

            # Checking if the game is over
            if game.states[1] == (0, 0):
                game.over = True
                continue

            # Checking for collide_point:
            left_1, _, _ = pygame.mouse.get_pressed()
            if left_1 == 1 and not mine:
                x, y = pygame.mouse.get_pos()
                for item in [(1, 0), (1, 1)]:
                    if game.states[item[0]][item[1]] == 0:
                        continue
                    if picture_rect[item].collidepoint(x, y):
                        mine = item
            if left_1 == 1 and mine:
                x, y = pygame.mouse.get_pos()
                for item in [(0, 0), (0, 1)]:
                    if game.states[item[0]][item[1]] == 0:
                        continue
                    if picture_rect[item].collidepoint(x, y):
                        his = item
                        game.move((mine, his))
                        mine = None
                        his = None
                        break
        else:
            status = instruction_font.render('AIs Turn', True, (0, 0, 0))
            action = ai.best_action(game.states, game.player)
            if not action:
                game.over = True
                continue
            game.move(action)
        status_rect = status.get_rect()
        status_rect.center = (width / 2, 10)
        window.blit(status, status_rect)
    else:
        if game.player:
            status = instruction_font.render('AI won', True, (0, 0, 0))
        else:
            status = instruction_font.render('Player Won', True, (0, 0, 0))
        status_rect = status.get_rect()
        status_rect.center = (width / 2, 10)
        window.blit(status, status_rect)

    pygame.display.update()
