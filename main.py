import pygame
from pygame.locals import *
import random
import os

class Apple:
    def __init__(self, surface):
        self.parent_screen = surface
        self.apple = pygame.image.load(f"{os.getcwd()}\\resources\\apple.jpg").convert()
        apple_height = self.apple.get_height()
        apple_width =  self.apple.get_width()
        width, height = pygame.display.get_surface().get_size()
        self.x = random.randint(apple_width, width - apple_width)
        self.y = random.randint(apple_height, height - apple_height)


    def draw(self):
        self.parent_screen.blit(self.apple, (self.x, self.y))
        pygame.display.flip()

class Snake:
    def __init__(self, surface):
        self.parent_screen = surface
        self.block = pygame.image.load(f"{os.getcwd()}\\resources\\block.jpg").convert()

        self.x = 100
        self.y = 100

    def move_up(self):
        self.y -= 10
        self.draw()

    def move_down(self):
        self.y += 10
        self.draw()

    def move_right(self):
        self.x += 10
        self.draw()

    def move_left(self):
        self.x -= 10
        self.draw()

    def draw(self):
        self.parent_screen.fill((0, 122, 51))
        self.parent_screen.blit(self.block, (self.x, self.y))
        pygame.display.flip()



class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((500, 500))
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_UP:
                        self.snake.move_up()
                    if event.key == K_DOWN:
                        self.snake.move_down()
                    if event.key == K_RIGHT:
                        self.snake.move_right()
                    if event.key == K_LEFT:
                        self.snake.move_left()


if __name__ == '__main__':
    game = Game()
    game.run()
