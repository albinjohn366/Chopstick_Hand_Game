import pygame
import sys
from Chopstick import *

# Initializing pygame
pygame.init()

# Defining pygame appearance
size = (width, height) = (400, 600)
window = pygame.display.set_mode(size)
window.fill((255, 255, 255))
pygame.display.set_caption('Chopstick(Hand Game)')
player_turn = True

# Making instances
game = Chopstick([(1, 1), (1, 1)])
ai = Chopstick_AI()
training_done = False
ai.train(10000)

# Fonts
instruction_font = pygame.font.Font(pygame.font.get_default_font(), 20)

# images
one = pygame.transform.scale(pygame.image.load('pictures/1.png'), (120, 160))
two = pygame.transform.scale(pygame.image.load('pictures/2.png'), (80, 160))
three = pygame.transform.scale(pygame.image.load('pictures/3.png'), (140, 160))
four = pygame.transform.scale(pygame.image.load('pictures/4.png'), (140, 160))

while True:
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

    # Updating player turns
    if game.player:
        status = instruction_font.render('Players Turn', True, (0, 0, 0))
    else:
        status = instruction_font.render('AIs Turn', True, (0, 0, 0))
    status_rect = status.get_rect()
    status_rect.center = (width / 2, 10)
    window.blit(status, status_rect)

    pygame.display.update()
