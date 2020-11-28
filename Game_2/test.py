import pygame
import random

win = pygame.display.set_mode((500, 700))


# RGB values
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Images

# Food
APPLE = pygame.image.load('Images/Apple.png')
TOXIC = pygame.image.load('Images/Toxic.png')

# Snake Head
HEAD_UP = pygame.image.load('Images/Snake_Head_Up.png')
HEAD_RIGHT = pygame.image.load('Images/Snake_Head_Right.png')
HEAD_DOWN = pygame.image.load('Images/Snake_Head_Down.png')
HEAD_LEFT = pygame.image.load('Images/Snake_Head_Left.png')

# Snake Body
BODY_STRAIGHT = pygame.image.load('Images/Snake_Body_Straight.png')
BODY_UP = pygame.image.load('Images/Snake_Body_Up.png')
BODY_RIGHT = pygame.image.load('Images/Snake_Body_Right.png')
BODY_DOWN = pygame.image.load('Images/Snake_Body_Down.png')
BODY_LEFT = pygame.image.load('Images/Snake_Body_Left.png')

# Snake Tail
TAIL_UP = pygame.image.load('Images/Snake_Tail_Up.png')
TAIL_RIGHT = pygame.image.load('Images/Snake_Tail_Right.png')
TAIL_DOWN = pygame.image.load('Images/Snake_Tail_Down.png')
TAIL_LEFT = pygame.image.load('Images/Snake_Tail_Left.png')


def main():
    win.fill(BLACK)
    draw_image()
    pygame.display.update()


def draw_image():
    win.blit(APPLE, (250, 350))

run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.time.delay(100)

    keys = pygame.key.get_pressed()

    redraw_game_window(snake, food)
