import pygame, os

width = 1500
height = 900

pygame.init()
screen = pygame.display.set_mode((width, height))
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))
clock = pygame.time.Clock()

while True:
    pygame.display.update()
    clock.tick(60)