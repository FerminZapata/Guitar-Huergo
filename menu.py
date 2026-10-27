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

class quick_surface:
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

logo_path = os.path.join(menuassets_path,"Logo")

img = pygame.image.load(os.path.join(logo_path,"Logo.png")).convert_alpha()

Logo = button((width/2-img.get_width()/2, -2),img)

campaign_path = os.path.join(menuassets_path,"Campaign")

normal = None
pressed = None

for img in os.listdir(campaign_path):
    if img[-5] == "P":
        normal = pygame.image.load(os.path.join(campaign_path,img))
    else:
        pressed = pygame.image.load(os.path.join(campaign_path,img))

Campaign = button((width/2-normal.get_width()/2, 400), pressed, normal)

quick_path = os.path.join(menuassets_path,"Quickplay")

normal = None
pressed = None

for img in os.listdir(quick_path):
    if img[-5] == "P":
        normal = pygame.image.load(os.path.join(quick_path,img))
    else:
        pressed = pygame.image.load(os.path.join(quick_path,img))

Quickplay = button((width/2-normal.get_width()/2, 500), pressed, normal)

exit_path = os.path.join(menuassets_path,"Exit")

normal = None
pressed = None

for img in os.listdir(exit_path):
    if img[-5] == "P":
        normal = pygame.image.load(os.path.join(exit_path,img))
    else:
        pressed = pygame.image.load(os.path.join(exit_path,img))

Exit = button((width/2-normal.get_width()/2, 700), pressed, normal)

option_path = os.path.join(menuassets_path,"Options")

normal = None
pressed = None

for img in os.listdir(option_path):
    if img[-5] == "P":
        normal = pygame.image.load(os.path.join(option_path,img))
    else:
        pressed = pygame.image.load(os.path.join(option_path,img))

Option = button((width/2-normal.get_width()/2,600), pressed, normal)

gamepad_path = os.path.join(menuassets_path,"Gamepad")

normal = None
pressed = None

for img in os.listdir(gamepad_path):
    if img[-5] == "P":
        normal = pygame.image.load(os.path.join(gamepad_path,img))
    else:
        pressed = pygame.image.load(os.path.join(gamepad_path,img))

Gamepad = button((width/5-normal.get_width()/5, 500), pressed, normal)

music_path = os.path.join(menuassets_path,"Music")

normal = None
pressed = None

for img in os.listdir(music_path):
    if img[-5] == "P":
        normal = pygame.image.load(os.path.join(music_path,img))
    else:
        pressed = pygame.image.load(os.path.join(music_path,img))

Music = button((width/5-normal.get_width()/5, 250), pressed, normal)

quickity = quick_surface((1200,800),"",(width/2-600,height/2-400))

# DICCIONARIO QUE ALMACENA TODOS LOS BOTONES (UTILIZAR ESTO POR FAVOR)
menus = {"main":[Logo, Campaign, Quickplay, Option,Exit],
         "quickplay":[quickity,Exit],
         "campaign":[Exit],
         "options":[Music, Gamepad, Exit],}

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
                if Quickplay.rect.collidepoint(event.pos):
                    state = "quickplay"
                elif Campaign.rect.collidepoint(event.pos):
                    state = "campaign"
                elif Option.rect.collidepoint(event.pos):
                    state = "options"
                elif Exit.rect.collidepoint(event.pos):
                    ejecucion = False
            elif state != "main":
                if Exit.rect.collidepoint(event.pos):
                    state = "main"
    upt_assets()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()