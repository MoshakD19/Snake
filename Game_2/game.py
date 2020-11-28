import pygame
import random


pygame.init()

win = pygame.display.set_mode((500, 700))
pygame.display.set_caption('Snake Game')

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
BODY_VERTICAL = pygame.image.load('Images/Snake_Body_Vertical.png')
BODY_HORIZONTAL = pygame.image.load('Images/Snake_Body_Horizontal.png')
BODY_UP = pygame.image.load('Images/Snake_Body_Up.png')
BODY_RIGHT = pygame.image.load('Images/Snake_Body_Right.png')
BODY_DOWN = pygame.image.load('Images/Snake_Body_Down.png')
BODY_LEFT = pygame.image.load('Images/Snake_Body_Left.png')

# Snake Tail
TAIL_UP = pygame.image.load('Images/Snake_Tail_Up.png')
TAIL_RIGHT = pygame.image.load('Images/Snake_Tail_Right.png')
TAIL_DOWN = pygame.image.load('Images/Snake_Tail_Down.png')
TAIL_LEFT = pygame.image.load('Images/Snake_Tail_Left.png')

# RGB values
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def new_highscore(score):
    f = open("Highscore.txt", "w")
    f.write(f"{score}")
    f.close()


def get_highscore():
    f = open("Highscore.txt", "r")
    highscore = int(f.read())
    return highscore


def check_highscore(snake):
    if snake.score > get_highscore():
        new_highscore(snake.score)


def redraw_game_window(snake, food):
    win.fill(BLACK)
    for part in snake.length.values():
        part.draw()
    food.draw(snake)
    pygame.draw.line(win, BLUE, (0, 195), (500, 195), 5)
    draw_score(snake)
    draw_highscore()
    pygame.display.update()


def game_over(snake):
    run = True

    check_highscore(snake)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_r]:
            main()
        elif keys[pygame.K_q]:
            pygame.quit()


def draw_score(snake, text_size=32, location=(300, 100)):
    font = pygame.font.Font('SIXTY.TTF', text_size)
    text = font.render(f'Score: {snake.score}', True, WHITE, BLACK)
    win.blit(text, location)


def draw_highscore(text_size=32, location=(50, 100)):
    font = pygame.font.Font('SIXTY.TTF', text_size)
    text = font.render(f'Highscore: {get_highscore()}', True, WHITE, BLACK)
    win.blit(text, location)


class Snake:
    def __init__(self):
        self.length = {"0": Segment(head=True), "1": Segment(), "2": Segment(tail=True)}
        self.head = self.length["0"]
        self.pressed_log = ["down", "down", "down"]
        self.vel = 20
        self.speed = 100
        self.score = 0
        self.count_down = 0
        self.crash = False

    def increase_length(self):
        self.length[str(len(self.length) - 1)].tail = False
        self.length[str(len(self.length))] = Segment(self.length[str(len(self.length) - 1)].path[0],
                                                     self.length[str(len(self.length) - 1)].path[1], tail=True)
        self.log_pressed(self.pressed_log[len(self.length) - 2])

    def increase_speed(self):
        if self.speed > 30:
            self.speed -= 2
        else:
            self.speed = 30

    def hit(self):
        self.increase_length()
        self.increase_speed()
        self.score_up(150 - self.speed)

    def score_up(self, num=1):
        self.count_down += num
        while self.count_down > 10:
            self.count_down -= 10
            self.score += 1

    def log_pressed(self, direction):
        if direction == "up":
            self.pressed_log.insert(0, "up")
        elif direction == "down":
            self.pressed_log.insert(0, "down")
        elif direction == "right":
            self.pressed_log.insert(0, "right")
        elif direction == "left":
            self.pressed_log.insert(0, "left")
        if len(self.pressed_log) > len(self.length):
            self.pressed_log.pop()

    # Movements

    def move_up(self):
        self.head.pressed = 'up'
        self.head.record_path()
        if self.head.y == 200:
            self.crash = True
        self.head.y -= self.vel
        self.log_pressed("up")
        self.move_body()
        self.update_hitbox()

    def move_down(self):
        self.head.pressed = 'down'
        self.head.record_path()
        if self.head.y == 680:
            self.head.y = 200
            self.crash = True
        self.head.y += self.vel
        self.log_pressed("down")
        self.move_body()
        self.update_hitbox()

    def move_right(self):
        self.head.pressed = 'right'
        self.head.record_path()
        if self.head.x == 480:
            self.crash = True
        self.head.x += self.vel
        self.log_pressed("right")
        self.move_body()
        self.update_hitbox()

    def move_left(self):
        self.head.pressed = 'left'
        self.head.record_path()
        if self.head.x == 0:
            self.crash = True
        self.head.x -= self.vel
        self.log_pressed("left")
        self.move_body()
        self.update_hitbox()

    def move_body(self):
        for num in range(1, len(self.length)):
            self.length[str(num)].record_path()
            self.length[str(num)].x = self.length[str(num - 1)].path[0]
            self.length[str(num)].y = self.length[str(num - 1)].path[1]
            self.length[str(num)].pressed = self.pressed_log[num]
            if num < len(self.length) - 1:
                self.turned(num)



    def move(self):
        if self.head.pressed == "up":
            self.move_up()
        elif self.head.pressed == "down":
            self.move_down()
        elif self.head.pressed == "left":
            self.move_left()
        elif self.head.pressed == "right":
            self.move_right()

    def crashed(self):
        for num in range(1, len(self.length)):
            if self.head.hitbox == self.length[str(num)].hitbox:
                return True

        if self.crash:
            return True
        return False

    def update_hitbox(self):
        for num in range(len(self.length)):
            self.length[str(num)].hitbox[0] = self.length[str(num)].x
            self.length[str(num)].hitbox[1] = self.length[str(num)].y

    def turned(self, num):
        if self.length[str(num - 1)].pressed == "up" and self.length[str(num + 1)].pressed == "left":
            self.length[str(num)].pressed = "left_and_up"
        elif self.length[str(num - 1)].pressed == "down" and self.length[str(num + 1)].pressed == "right":
            self.length[str(num)].pressed = "down_and_right"

        elif self.length[str(num - 1)].pressed == "up" and self.length[str(num + 1)].pressed == "right":
            self.length[str(num)].pressed = "up_and_right"
        elif self.length[str(num - 1)].pressed == "left" and self.length[str(num + 1)].pressed == "down":
            self.length[str(num)].pressed = "left_and_down"

        elif self.length[str(num - 1)].pressed == "right" and self.length[str(num + 1)].pressed == "up":
            self.length[str(num)].pressed = "right_and_up"
        elif self.length[str(num - 1)].pressed == "down" and self.length[str(num + 1)].pressed == "left":
            self.length[str(num)].pressed = "down_and_left"

        elif self.length[str(num - 1)].pressed == "right" and self.length[str(num + 1)].pressed == "down":
            self.length[str(num)].pressed = "right_and_down"
        elif self.length[str(num - 1)].pressed == "up" and self.length[str(num + 1)].pressed == "left":
            self.length[str(num)].pressed = "up_and_left"




class Segment:
    def __init__(self, x=100, y=200, colour=RED, head=False, tail=False):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.colour = colour
        self.path = [0, 200]
        self.hitbox = [self.x, self.y]
        self.head = head
        self.tail = tail
        self.pressed = "down"
        self.pressed_log = "down"

    def draw(self):
        if self.head == True:
            self.head_check()
        elif self.tail == True:
            self.tail_check()
        else:
            self.straight_body_check()

    def head_check(self):
        if self.pressed == "down":
            win.blit(HEAD_DOWN, (self.x, self.y))
        elif self.pressed == "up":
            win.blit(HEAD_UP, (self.x, self.y))
        elif self.pressed == "left":
            win.blit(HEAD_LEFT, (self.x, self.y))
        elif self.pressed == "right":
            win.blit(HEAD_RIGHT, (self.x, self.y))

    def tail_check(self):
        if self.pressed == "down":
            win.blit(TAIL_DOWN, (self.x, self.y))
        elif self.pressed == "up":
            win.blit(TAIL_UP, (self.x, self.y))
        elif self.pressed == "left":
            win.blit(TAIL_LEFT, (self.x, self.y))
        elif self.pressed == "right":
            win.blit(TAIL_RIGHT, (self.x, self.y))

    def straight_body_check(self):
        if self.pressed == "left_and_up" or self.pressed == "down_and_right":
            win.blit(BODY_RIGHT, (self.x, self.y))
        elif self.pressed == "up_and_right" or self.pressed == "left_and_down":
            win.blit(BODY_DOWN, (self.x, self.y))
        elif self.pressed == "right_and_up" or self.pressed == "down_and_left":
            win.blit(BODY_UP, (self.x, self.y))
        elif self.pressed == "right_and_down" or self.pressed == "up_and_left":
            win.blit(BODY_LEFT, (self.x, self.y))
        elif self.pressed == "up" or self.pressed == "down":
            win.blit(BODY_VERTICAL, (self.x, self.y))
        elif self.pressed == "right" or self.pressed == "left":
            win.blit(BODY_HORIZONTAL, (self.x, self.y))

    def record_path(self):
        self.path[0] = self.x
        self.path[1] = self.y

    def update_hitbox(self):
        self.hitbox[0] = self.x
        self.hitbox[1] = self.y


class Food:
    def __init__(self, colour=BLUE):
        self.x = random.randrange(0, 500, 20)
        self.y = random.randrange(200, 700, 20)
        self.width = 20
        self.height = 20
        self.colour = colour
        self.eaten = False

    def draw(self, snake):
        if not self.eaten:
            win.blit(APPLE, (self.x, self.y))
        else:
            self.move(snake)
            win.blit(APPLE, (self.x, self.y))

    def move(self, snake):
        self.x = random.randrange(0, 500, 20)
        self.y = random.randrange(200, 700, 20)
        for part in snake.length.values():
            if self.x == part.x and self.y == part.y:
                self.move(snake)
        self.eaten = False

    def hit(self):
        self.eaten = True

def main():
    run = True

    snake = Snake()
    food = Food()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.time.delay(snake.speed)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and snake.head.pressed != 'right':
            snake.move_left()

        elif keys[pygame.K_RIGHT] and snake.head.pressed != 'left':
            snake.move_right()

        elif keys[pygame.K_UP] and snake.head.pressed != 'down':
            snake.move_up()

        elif keys[pygame.K_DOWN] and snake.head.pressed != 'up':
            snake.move_down()

        else:
            snake.move()

        if snake.head.x == food.x and snake.head.y == food.y:
            food.hit()
            snake.hit()

        snake.score_up()

        if snake.crashed():
            # pygame.time.delay(1000)
            # pygame.quit()
            game_over(snake)

        redraw_game_window(snake, food)


print(main())

pygame.quit()
