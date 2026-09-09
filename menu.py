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
collision = pygame.Rect(0, 0, 50, 50)
clock = pygame.time.Clock()

def update_quick_play():
    pass

def draw_assets():
    background = pygame.image.load(os.path.join("E:\Github desklol\Guitar-Huergo\Assets\Menu", "FONDO.png")).convert_alpha()
    logo = pygame.image.load(os.path.join("E:\Github desklol\Guitar-Huergo\Assets\Menu", "LOGO3.png")).convert_alpha()
    boton_quickplay = pygame.image.load(os.path.join("E:\Github desklol\Guitar-Huergo\Assets\Menu", "QUICK PLAY SIN PRESIONAR.png")).convert_alpha()
    boton_campaign = pygame.image.load(os.path.join("E:\Github desklol\Guitar-Huergo\Assets\Menu", "CAMPAIGN SIN PRESIONAR.png")).convert_alpha()
    boton_opciones = pygame.image.load(os.path.join("E:\Github desklol\Guitar-Huergo\Assets\Menu", "OPCIONES SIN PRESIONAR.png")).convert_alpha()
    boton_salir = pygame.image.load(os.path.join("E:\Github desklol\Guitar-Huergo\Assets\Menu", "SALIR SIN PRESIONAR.png")).convert_alpha()
    boton_quickplay_presionado = pygame.image.load(os.path.join("E:\Github desklol\Guitar-Huergo\Assets\Menu", "QUICK PLAY PRESIONADO.png")).convert_alpha()
    screen.blit(background, (0,0))
    screen.blit(logo, (width/2-logo.width/2, 0))
    screen.blit(boton_quickplay, (width/2-boton_quickplay.width/2, 400))
    screen.blit(boton_campaign, (width/2-boton_campaign.width/2, 500))
    screen.blit(boton_opciones, (width/2-boton_opciones.width/2,600))
    screen.blit(boton_salir, (width/2-boton_salir.width/2, 700))
    

def menu_opciones():
    pass

while ejecucion:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecucion = False
    pygame.draw.rect(screen, (255,0,0), collision)
    mouse = pygame.mouse.get_pos()
    collision.x = mouse[0]
    collision.y = mouse[1]
    pygame.display.flip()
    draw_assets()
    pygame.display.update()
    clock.tick(60)
pygame.quit()





    