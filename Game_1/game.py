import pygame
import random


pygame.init()

win = pygame.display.set_mode((500, 700))
pygame.display.set_caption('Snake Game')

# music = pygame.mixer.music.load('music.mp3')
# pygame.mixer.music.play(-1)

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
        self.length = {"0": Segment()}
        self.head = self.length["0"]
        self.vel = 20
        self.speed = 100
        self.pressed = 'down'
        self.score = 0
        self.count_down = 0
        self.crash = False

    def increase_length(self):
        self.length[str(len(self.length))] = Segment(self.length[str(len(self.length) - 1)].path[0],
                                                     self.length[str(len(self.length) - 1)].path[1])

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

    # Movements

    def move_up(self):
        self.pressed = 'up'
        self.head.record_path()
        if self.head.y == 200:
            self.crash = True
        self.head.y -= self.vel
        self.move_body()
        self.update_hitbox()

    def move_down(self):
        self.pressed = 'down'
        self.head.record_path()
        if self.head.y == 680:
            self.head.y = 200
            self.crash = True
        self.head.y += self.vel
        self.move_body()
        self.update_hitbox()

    def move_right(self):
        self.pressed = 'right'
        self.head.record_path()
        if self.head.x == 480:
            self.crash = True
        self.head.x += self.vel
        self.move_body()
        self.update_hitbox()

    def move_left(self):
        self.pressed = 'left'
        self.head.record_path()
        if self.head.x == 0:
            self.crash = True
        self.head.x -= self.vel
        self.move_body()
        self.update_hitbox()

    def move_body(self):
        if len(self.length) > 1:
            for num in range(1, len(self.length)):
                self.length[str(num)].record_path()
                self.length[str(num)].x = self.length[str(num - 1)].path[0]
                self.length[str(num)].y = self.length[str(num - 1)].path[1]

    def move(self):
        if self.pressed == "up":
            self.move_up()
        elif self.pressed == "down":
            self.move_down()
        elif self.pressed == "left":
            self.move_left()
        elif self.pressed == "right":
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


class Segment:
    def __init__(self, x=100, y=200, colour=RED):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.colour = colour
        self.path = [0, 200]
        self.hitbox = [self.x, self.y]

    def draw(self):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))

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
            pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))
        else:
            self.move(snake)
            pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))

    def move(self, snake):
        self.x = random.randrange(0, 500, 20)
        self.y = random.randrange(200, 700, 20)
        for part in snake.length.values():
            if self.x == part.x and self.y == part.y:
                print("Success")
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

        if keys[pygame.K_LEFT] and snake.pressed != 'right':
            snake.move_left()

        elif keys[pygame.K_RIGHT] and snake.pressed != 'left':
            snake.move_right()

        elif keys[pygame.K_UP] and snake.pressed != 'down':
            snake.move_up()

        elif keys[pygame.K_DOWN] and snake.pressed != 'up':
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
