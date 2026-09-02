import pygame, os

width = 1500
height = 900

pygame.init()
ejecucion = True
screen = pygame.display.set_mode((width, height))
mouse_sobre_boton = False
icon_path = os.path.join(os.path.dirname(__file__), "LOGO3.ico")
icono = pygame.image.load(icon_path)
pygame.display.set_icon(icono)
background = pygame.image.load(os.path.join("E:\Github desklol\Guitar-Huergo\Assets\Menu", "FONDO.png")).convert_alpha()
logo = pygame.image.load(os.path.join("E:\Github desklol\Guitar-Huergo\Assets\Menu", "LOGO3.png")).convert_alpha()
boton_quickplay = pygame.image.load(os.path.join("E:\Github desklol\Guitar-Huergo\Assets\Menu", "QUICK PLAY SIN PRESIONAR.png")).convert_alpha()
boton_opciones = pygame.image.load(os.path.join("E:\Github desklol\Guitar-Huergo\Assets\Menu", "OPCIONES SIN PRESIONAR.png")).convert_alpha()
boton_salir = pygame.image.load(os.path.join("E:\Github desklol\Guitar-Huergo\Assets\Menu", "SALIR SIN PRESIONAR.png")).convert_alpha()
screen.blit(background, (0,0))
screen.blit(logo, (500, 0))
screen.blit(boton_quickplay, (100,25))
screen.blit(boton_opciones, (100,250))
screen.blit(boton_salir, (100, 375))
collision = pygame.draw.rect(screen, "white", (0, 0, 50, 50))

clock = pygame.time.Clock()

while ejecucion:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecutando = False    
    pygame.display.flip()
    clock.tick(60)
    mouse = pygame.mouse.get_pos()
    collision.x = mouse[0]
    collision.y = mouse[1]
pygame.quit()

def menu_opciones():
    pass