import pygame

width = 1000
height = 1000

pygame.init()
window = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
    clock.tick(60)