import pygame, os

width = 1500
height = 900

pygame.init()
ejecucion = True
screen = pygame.display.set_mode((width, height))
mouse_sobre_boton = False
icon_path = os.path.join(os.path.dirname(__file__), "LOGO3.ico")
menuassets_path = os.path.join(os.path.join(os.path.dirname(__file__), "Assets"), "Menu")
game_state = "Menu_Principal"
icono = pygame.image.load(icon_path)
pygame.display.set_icon(icono)
collision = pygame.Rect(0, 0, 50, 50)
clock = pygame.time.Clock()

class button:
    def __init__(self, pos, surf_normal, surf_hover=None):
        self.surf_normal = surf_normal
        self.surf_hover = surf_hover if surf_hover else surf_normal
        self.pos = pos
        self.rect = self.surf_normal.get_rect(topleft=pos)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            screen.blit(self.surf_hover, self.pos)
        else:
            screen.blit(self.surf_normal, self.pos)

def draw_menu_quickplay():
    pass

menu = []
background = pygame.image.load(os.path.join(menuassets_path, "FONDO.png")).convert_alpha()
logo = pygame.image.load(os.path.join(menuassets_path, "LOGO3.png")).convert_alpha()
boton_quickplay = pygame.image.load(os.path.join(menuassets_path, "QUICK PLAY SIN PRESIONAR.png")).convert_alpha()
boton_campaign = pygame.image.load(os.path.join(menuassets_path, "CAMPAIGN SIN PRESIONAR.png")).convert_alpha()
boton_opciones = pygame.image.load(os.path.join(menuassets_path, "OPCIONES SIN PRESIONAR.png")).convert_alpha()
boton_salir = pygame.image.load(os.path.join(menuassets_path, "SALIR SIN PRESIONAR.png")).convert_alpha()
boton_quickplay_presionado = pygame.image.load(os.path.join(menuassets_path, "QUICK PLAY PRESIONADO.png")).convert_alpha()
boton_salir_presionado = pygame.image.load(os.path.join(menuassets_path, "SALIR PRESIONADO.png")).convert_alpha()
boton_campaign_presionado = pygame.image.load(os.path.join(menuassets_path, "CAMPAIGN PRESIONADO.png")).convert_alpha()
boton_opciones_presionado = pygame.image.load(os.path.join(menuassets_path, "OPCIONES PRESIONADO.png")).convert_alpha()
var1 = button((width/2-logo.get_width()/2, -2),logo)
var2 = button((width/2-boton_quickplay.get_width()/2, 400), boton_quickplay, boton_quickplay_presionado)
var3 = button((width/2-boton_campaign.get_width()/2, 500), boton_campaign, boton_campaign_presionado)
var4 = button((width/2-boton_opciones.get_width()/2,600), boton_opciones, boton_opciones_presionado)
var5 = button((width/2-boton_salir.get_width()/2, 700), boton_salir, boton_salir_presionado)
menu.extend([var1, var2, var3, var4, var5])
    

def upt_assets():
    screen.fill("black")
    for obj in menu:
        obj.update()

while ejecucion:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecucion = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if var2.rect.collidepoint(event.pos):
                game_state = "Quickplay"
            elif var3.rect.collidepoint(event.pos):
                game_state = "Campaign"
            elif var4.rect.collidepoint(event.pos):
                game_state = "Opciones"
            elif var5.rect.collidepoint(event.pos):
                ejecucion = False
    pygame.display.flip()
    upt_assets()
    pygame.display.update()
    clock.tick(60)
pygame.quit()