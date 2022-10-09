import pygame
from pygame.locals import *
import random
import os
import time
from enum import Enum, auto


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    RIGHT = auto()
    LEFT = auto()


STEP = 40
BACKGROUND_COLOR = (100, 165, 67)


def _get_random_position(image_width, image_height, surface_width, surface_height):
    width = int(surface_width / image_width)
    height = int(surface_height / image_height)
    random_x = random.randint(0, width - 1)*STEP
    random_y = random.randint(0, height - 1)*STEP
    return random_x, random_y


class Apple:
    def __init__(self, surface):
        self.parent_screen = surface
        self.apple = pygame.image.load(f"{os.getcwd()}\\resources\\apple.jpg").convert()
        self.apple_height = self.apple.get_height()
        self.apple_width = self.apple.get_width()
        self.surface_width, self.surface_height = pygame.display.get_surface().get_size()
        self.x, self.y = _get_random_position(self.apple_width, self.apple_height, self.surface_width,
                                              self.surface_height)

    def move(self):
        self.x, self.y = _get_random_position(self.apple_width, self.apple_height, self.surface_width,
                                              self.surface_height)

    def draw(self):
        self.parent_screen.blit(self.apple, (self.x, self.y))
        pygame.display.flip()


class Snake:
    def __init__(self, surface):
        self.parent_screen = surface
        self.block = pygame.image.load(f"{os.getcwd()}\\resources\\block.jpg").convert()
        self.length = 1
        initial_x = 0
        initial_y = 100
        self.x = [initial_x] * self.length
        self.y = [initial_y] * self.length
        self.direction = Direction.RIGHT

    def move_up(self):
        self.direction = Direction.UP

    def move_down(self):
        self.direction = Direction.DOWN

    def move_right(self):
        self.direction = Direction.RIGHT

    def move_left(self):
        self.direction = Direction.LEFT

    def draw(self):
        self.parent_screen.fill(BACKGROUND_COLOR)
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def walk(self):

        # Update rest of snake
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # Update head
        if self.direction == Direction.UP:
            self.y[0] -= STEP
        if self.direction == Direction.DOWN:
            self.y[0] += STEP
        if self.direction == Direction.RIGHT:
            self.x[0] += STEP
        if self.direction == Direction.LEFT:
            self.x[0] -= STEP
        self.draw()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # Snake eats apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.increase_length()
            self.apple.move()

        # Snake collides with itself
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "Snake bit itself"

        # Snake lands on
        surface_width, surface_height = pygame.display.get_surface().get_size()
        x_out_of_range_bool = self.snake.x[0] > surface_width or self.snake.x[0] < 0
        y_out_of_range_bool = self.snake.y[0] > surface_height or self.snake.y[0] < 0

        if x_out_of_range_bool or y_out_of_range_bool:
            raise "Snake landed on edge"

    def is_collision(self, x1, y1, x2, y2):
        return x2 <= x1 < x2 + STEP and y2 <= y1 < y2 + STEP

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, (200, 200, 200))
        self.surface.blit(score, (850, 10))

    def show_game_over(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))

        pygame.display.flip()

    def run(self):
        running = True
        pause = False

        while running:
            self.apple.draw()
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pause = False

                    if event.key == K_UP and self.snake.direction != Direction.DOWN:
                        self.snake.move_up()
                    if event.key == K_DOWN and self.snake.direction != Direction.UP:
                        self.snake.move_down()
                    if event.key == K_RIGHT and self.snake.direction != Direction.LEFT:
                        self.snake.move_right()
                    if event.key == K_LEFT and self.snake.direction != Direction.RIGHT:
                        self.snake.move_left()
                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.2)


if __name__ == '__main__':
    game = Game()
    game.run()
