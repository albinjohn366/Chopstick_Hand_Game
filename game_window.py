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
game = Chopstick([(2, 4), (1, 3)])
ai = Chopstick_AI()
training_done = False

# images
one = pygame.transform.scale(pygame.image.load('pictures/1.png'), (140, 160))
two = pygame.transform.scale(pygame.image.load('pictures/2.png'), (140, 160))
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
            x_coordinate = width / 3 + (side * width / 3)
            y_coordinate = height / 4 + (row * height / 2)
            picture_rect[row, side].center = (x_coordinate, y_coordinate)
            window.blit(picture, picture_rect[row, side])

    # Displaying while training is in process
    if not training_done:
        ai.train(100)
        training_done = True

    pygame.display.update()
