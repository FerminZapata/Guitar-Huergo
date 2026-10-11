import pygame, os

width = 1500
height = 900

ejecucion = True

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# IMPLEMENTACION DEL ICONO EN LA VENTANA
icon_path = os.path.join(os.path.dirname(__file__), "LOGO3.ico")
icono = pygame.image.load(icon_path)
pygame.display.set_icon(icono)

# MENU ACTUAL
state = "main"

# DEFINICION DE LA CLASE BOTON
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

# CARGA DE ASSETS
menuassets_path = os.path.join(os.path.join(os.path.dirname(__file__), "Assets"), "Menu")
game_state = "Menu_Principal"

bgnd = pygame.image.load(os.path.join(menuassets_path, "FONDO.png")).convert_alpha()
logo = pygame.image.load(os.path.join(menuassets_path, "LOGO3.png")).convert_alpha()
quick = pygame.image.load(os.path.join(menuassets_path, "QUICK PLAY SIN PRESIONAR.png")).convert_alpha()
campaign = pygame.image.load(os.path.join(menuassets_path, "CAMPAIGN SIN PRESIONAR.png")).convert_alpha()
options = pygame.image.load(os.path.join(menuassets_path, "OPCIONES SIN PRESIONAR.png")).convert_alpha()
salir = pygame.image.load(os.path.join(menuassets_path, "SALIR SIN PRESIONAR.png")).convert_alpha()
quick_p = pygame.image.load(os.path.join(menuassets_path, "QUICK PLAY PRESIONADO.png")).convert_alpha()
salir_p = pygame.image.load(os.path.join(menuassets_path, "SALIR PRESIONADO.png")).convert_alpha()
campaign_p = pygame.image.load(os.path.join(menuassets_path, "CAMPAIGN PRESIONADO.png")).convert_alpha()
options_p = pygame.image.load(os.path.join(menuassets_path, "OPCIONES PRESIONADO.png")).convert_alpha()

var1 = button((width/2-logo.get_width()/2, -2),logo)
var2 = button((width/2-quick.get_width()/2, 400), quick, quick_p)
var3 = button((width/2-campaign.get_width()/2, 500), campaign, campaign_p)
var4 = button((width/2-options.get_width()/2,600), options, options_p)
var5 = button((width/2-salir.get_width()/2, 700), salir, salir_p)

# DICCIONARIO QUE ALMACENA TODOS LOS BOTONES (UTILIZAR ESTO POR FAVOR)
menus = {"main":[var1, var2, var3, var4, var5],
         "quickplay":[var5],
         "campaign":[var5],
         "options":[var5],}

def upt_assets(): # FUNCION QUE REFRESCA LAS IMAGENES DE LA VENTANA
    screen.fill("black")
    for obj in menus[state]:
        obj.update()

while ejecucion:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecucion = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if state == "main":
                if var2.rect.collidepoint(event.pos):
                    state = "quickplay"
                elif var3.rect.collidepoint(event.pos):
                    state = "campaign"
                elif var4.rect.collidepoint(event.pos):
                    state = "options"
                elif var5.rect.collidepoint(event.pos):
                    ejecucion = False
            elif state != "main":
                if var5.rect.collidepoint(event.pos):
                    state = "main"
    upt_assets()
    pygame.display.update()
    clock.tick(60)
pygame.quit()