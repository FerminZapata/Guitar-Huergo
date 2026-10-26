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

class quick_button:
    def __init__(self,size,text,pos):
        self.pos = pos
        self.font = pygame.font.SysFont(None, 30)
        self.surf = pygame.Rect(pos[0],pos[1],size[0],size[1])
        self.outline = pygame.Rect(pos[0]-5,pos[1]-5,size[0]+10,size[1]+10)
        self.text = text
    
    def update(self):
        text = self.font.render(self.text,True,(255,255,255))
        pygame.draw.rect(screen,(255,255,255),self.outline)
        pygame.draw.rect(screen,(50,50,50),self.surf)
        screen.blit(text,(self.pos[0],self.pos[1]+self.surf.height/2-text.get_height()/2))
        pygame.display.flip()

class campaign_button:
    def __init__(self,size,text,pos):
        self.pos = pos
        self.font = pygame.font.SysFont(None, 30)
        self.surf = pygame.Rect(pos[0],pos[1],size[0],size[1])
        self.outline = pygame.Rect(pos[0]-5,pos[1]-5,size[0]+10,size[1]+10)
        self.text = text
    
    def update(self):
        text = self.font.render(self.text,True,(255,255,255))
        pygame.draw.rect(screen,(255,255,255),self.outline)
        pygame.draw.rect(screen,(50,50,50),self.surf)
        screen.blit(text,(self.pos[0],self.pos[1]+self.surf.height/2-text.get_height()/2))
        pygame.display.flip()

menuassets_path = os.path.join(os.path.join(os.path.dirname(__file__), "Assets"), "Menu")
game_state = "Menu_Principal"

bgnd = pygame.image.load(os.path.join(menuassets_path, "FONDO.png")).convert_alpha()
logo = pygame.image.load(os.path.join(menuassets_path, "LOGO3.png")).convert_alpha()
quick = pygame.image.load(os.path.join(menuassets_path, "QUICK PLAY SIN PRESIONAR.png")).convert_alpha()
campaign = pygame.image.load(os.path.join(menuassets_path, "CAMPAIGN SIN PRESIONAR.png")).convert_alpha()
options = pygame.image.load(os.path.join(menuassets_path, "OPCIONES SIN PRESIONAR.png")).convert_alpha()
salir = pygame.image.load(os.path.join(menuassets_path, "SALIR SIN PRESIONAR.png")).convert_alpha()
musica = pygame.image.load(os.path.join(menuassets_path, "MUSICA SIN PRESIONAR.png")).convert_alpha()
gamepad = pygame.image.load(os.path.join(menuassets_path, "MODO GAMEPAD SIN PRESIONAR.png")).convert_alpha()
quick_p = pygame.image.load(os.path.join(menuassets_path, "QUICK PLAY PRESIONADO.png")).convert_alpha()
salir_p = pygame.image.load(os.path.join(menuassets_path, "SALIR PRESIONADO.png")).convert_alpha()
campaign_p = pygame.image.load(os.path.join(menuassets_path, "CAMPAIGN PRESIONADO.png")).convert_alpha()
options_p = pygame.image.load(os.path.join(menuassets_path, "OPCIONES PRESIONADO.png")).convert_alpha()
musica_p = pygame.image.load(os.path.join(menuassets_path, "MUSICA PRESIONADO.png")).convert_alpha()
gamepad_p = pygame.image.load(os.path.join(menuassets_path, "MODO GAMEPAD PRESIONADO.png")).convert_alpha()

var1 = button((width/2-logo.get_width()/2, -2),logo)
var2 = button((width/2-quick.get_width()/2, 500), quick, quick_p)
var3 = button((width/2-campaign.get_width()/2, 400), campaign, campaign_p)
var4 = button((width/2-options.get_width()/2,600), options, options_p)
var5 = button((width/2-salir.get_width()/2, 700), salir, salir_p)
var6 = button((width/5-musica.get_width()/5, 250), musica, musica_p)
var7 = button((width/5-gamepad.get_width()/5, 500), gamepad, gamepad_p)

quickity = quick_button((1200,800),"",(width/2-600,height/2-400))
campaignb = campaign_button((1200,800),"",(width/2-600,height/2-400))

# DICCIONARIO QUE ALMACENA TODOS LOS BOTONES (UTILIZAR ESTO POR FAVOR)
menus = {"main":[var1, var2, var3, var4, var5],
         "quickplay":[quickity,var5],
         "campaign":[campaignb,var5],
         "options":[var5, var6, var7],}

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
    pygame.display.flip()
    clock.tick(60)
pygame.quit()