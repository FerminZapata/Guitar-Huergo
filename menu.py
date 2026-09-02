import pygame, os

width = 1500
height = 900

pygame.init()
ejecucion = True
screen = pygame.display.set_mode((width, height))
background = pygame.image.load(os.path.join("E:\Github desklol\Guitar-Huergo\Assets\Menu", "FONDO Y LOGO.png")).convert_alpha()
boton_quickplay = 
screen.blit(background, (0,0))
clock = pygame.time.Clock()

while ejecucion:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecutando = False
    pygame.display.flip()
    clock.tick(60)
pygame.quit()

def menu_opciones():
    