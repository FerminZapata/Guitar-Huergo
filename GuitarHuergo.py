import pygame, os

width = 1500
height = 900

pygame.init()
window = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

assets = os.path.join(os.path.dirname(__file__), "Assets")

notecol = pygame.Rect(500,750,500,2)

keys_dict = {pygame.K_a :"g_press",
             pygame.K_s:"r_press",
             pygame.K_j:"y_press",
             pygame.K_k:"b_press",
             pygame.K_l:"o_press",
             pygame.K_SPACE:"space"}

n_pressed = {"g_press":False,
             "r_press":False,
             "y_press":False,
             "b_press":False,
             "o_press":False,
             "space":False}

n_held = {"g_press":False,
          "r_press":False,
          "y_press":False,
          "b_press":False,
          "o_press":False,
          "space":False}

class Note_Class:
    def __init__(self, surf, row, bpm, note, typ):
        self.spd = (bpm/60)
        self.row = row
        self.surf = surf
        self.type = typ
        self.note = note
        if row != 5:
            self.add = 0.1
        else:
            self.add = 0.48
        self.rect = pygame.Rect(0,0,self.surf.get_width(),self.surf.get_height())
        if row == 0:
            self.pos = (655,420)
        elif row == 1:
            self.pos = (695,420)
        elif row == 2:
            self.pos = (730,420)
        elif row == 3:
            self.pos = (765,420)
        elif row == 4:
            self.pos = (800,420)
        elif row == 5:
            self.pos = (653,435)

    def update(self):
        if self.pos[1] != 900:
            # Actualizacion de la imagen de la nota
            note = pygame.transform.scale(self.surf, (int(self.surf.get_width()*self.add), int(self.surf.get_height()*self.add)))
            if self.row == 0:
                self.pos = (self.pos[0]-4.5*self.spd,self.pos[1]+8*self.spd)
            elif self.row == 1:
                self.pos = (self.pos[0]-2.8*self.spd,self.pos[1]+8*self.spd)
            elif self.row == 2:
                self.pos = (self.pos[0]-1*self.spd,self.pos[1]+8*self.spd)
            elif self.row == 3:
                self.pos = (self.pos[0]+1*self.spd,self.pos[1]+8*self.spd)
            elif self.row == 4:
                self.pos = (self.pos[0]+2.7*self.spd,self.pos[1]+8*self.spd)
            elif self.row == 5:
                self.pos = (self.pos[0]-4.2*self.spd,self.pos[1]+8*self.spd)
            if self.row != 5:
                self.add += 0.005*self.spd
                self.spd += 0.005
            else:
                self.add += 0.022*self.spd
                self.spd += 0.005

            # Actualizacion de la colision de la nota
            self.rect.x = self.pos[0]
            self.rect.y = self.pos[1]
            self.rect.width = note.get_width()
            self.rect.height = note.get_height()

            window.blit(note,self.pos)

class Fret:
    def __init__(self, surf, bpm):
        self.spd = (bpm/60)
        self.surf = surf
        self.add = 0.42
        self.pos = (650,445)

    def update(self):
        if self.pos[1] < 900:
            note = pygame.transform.scale(self.surf, (int(self.surf.get_width()*self.add), int(self.surf.get_height()*self.add)))
            self.pos = (self.pos[0]-4.3*self.spd,self.pos[1]+9*self.spd)
            self.add += 0.02*self.spd
            self.spd += 0.005
            window.blit(note,self.pos)

# Background assets
bgnd_assets = os.path.join(assets, "Background")  # acceso a la ruta con los assets

background = pygame.image.load(os.path.join(bgnd_assets,"Back.png")).convert_alpha()  # carga y guarda la imagen

fret = {0:pygame.image.load(os.path.join(bgnd_assets,"Traste0.png")).convert_alpha(),
        1:pygame.image.load(os.path.join(bgnd_assets,"Traste0.png")).convert_alpha(),
        2:pygame.image.load(os.path.join(bgnd_assets,"Traste0.png")).convert_alpha(),
        3:pygame.image.load(os.path.join(bgnd_assets,"Traste1.png")).convert_alpha()}

# Ruta de los altavoces
key_assets = os.path.join(assets, "Keys") # ruta de la carpeta de assets

# Creacion de un diccionario con los altavoces
spkr_path = os.path.join(key_assets,"Normal") # ruta de los assets

data = os.listdir(spkr_path)

spkr = {}

for img in data:
    spkr[img[0]] = pygame.image.load(os.path.join(spkr_path,img)).convert_alpha()

# Creacion de un diccionario con los altavoces cuando los presionas
spkrh_path = os.path.join(key_assets,"Hit") # guarda la ruta de los assets

data = os.listdir(spkrh_path)

spkr_h = {}

for img in data:
    spkr_h[img[0]] = pygame.image.load(os.path.join(spkrh_path,img)).convert_alpha()

# Creacion de un diccionario con los altavoces cuando los presionas junto a la strumbar
spkrs_path = os.path.join(key_assets,"HitStrum") # guarda la ruta de los assets

data = os.listdir(spkrs_path)

spkr_s = {}

for img in data:
    spkr_s[img[0]] = pygame.image.load(os.path.join(spkrs_path,img)).convert_alpha()

# Ruta de las notas
note_assets = os.path.join(assets, "Notes")

# Creacion de la nota open
open_note = pygame.image.load(os.path.join(note_assets,"Open.png")).convert_alpha()

# Creacion de un diccionario con los assets de las notas Hammer on
hamon_path = os.path.join(note_assets, "Hammer-on")

data = os.listdir(hamon_path)

HN = {}

for img in data:
    HN[img[0]] = pygame.image.load(os.path.join(hamon_path,img)).convert_alpha()

# Creacion de un diccionario con los assets de las notas Pull off
pulloff_path = os.path.join(note_assets, "Pull-off")

data = os.listdir(pulloff_path)

PO = {}

for img in data:
    PO[img[0]] = pygame.image.load(os.path.join(pulloff_path,img)).convert_alpha()

# Creacion de un diccionario con los assets de las notas Tap
tap_path = os.path.join(note_assets, "Pull-off")

data = os.listdir(tap_path)

TN = {}

for img in data:
    TN[img[0]] = pygame.image.load(os.path.join(tap_path,img)).convert_alpha()

def draw_background():
    window.fill("black") # CONVIERTE EL FONDO EN NEGRO

    pos_def = (width/2 - background.get_width()/2,height - background.get_height())

    if len(frets) != 0:
        for surf in frets:
            if surf.pos[1] >= 900:
                del surf
            else:
                surf.update()

    window.blit(background,pos_def)

    pygame.draw.rect(window, (255,255,255), notecol)

    teclas = pygame.key.get_pressed()

    for key in keys_dict:
        if key != pygame.K_SPACE:
            if teclas[key] and teclas[pygame.K_SPACE] or teclas[key] and gamepad_mode:
                window.blit(spkr_s[keys_dict[key][0]], pos_def)
            elif teclas[key]:
                window.blit(spkr_h[keys_dict[key][0]], pos_def)
            else:
                window.blit(spkr[keys_dict[key][0]], pos_def)
        elif key == pygame.K_SPACE:
            if teclas[pygame.K_SPACE]:
                for key in spkr_s:
                    window.blit(spkr_s[key],pos_def)

def draw_notes(lista):
    if len(lista) != 0:
        for i in lista:
            if i.pos[1] >= 900:
                del i
            else:
                i.update()

drawable_notes = [] # Lista que almacena las notas actuales

gamepad_mode = True

space_pressed = False

current_fret = 2

frets = [] # Lista con los trastes que salen en pantalla

o_time = pygame.time.get_ticks()

bpm = 60

point = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                space_pressed = False
            for key in keys_dict:
                if event.key == key and space_pressed or  event.key == key and gamepad_mode:
                    n_pressed[keys_dict[key]] = "none"
                    n_held[keys_dict[key]] = "none"
        elif event.type == pygame.KEYDOWN:
            pos_def = (width/2 - background.get_width()/2,height - background.get_height())
            if event.key == pygame.K_SPACE:
                n_pressed["space"] = "normal"
                space_pressed = True
            if event.key == pygame.K_KP0:
                note = Note_Class(HN["G"],0,bpm,"g","nn")
                drawable_notes.insert(0,note)
            elif event.key == pygame.K_KP1:
                note = Note_Class(HN["R"],1,bpm,"r","nn")
                drawable_notes.insert(0,note)
            elif event.key == pygame.K_KP2:
                note = Note_Class(HN["Y"],2,bpm,"y","nn")
                drawable_notes.insert(0,note)
            elif event.key == pygame.K_KP3:
                note = Note_Class(HN["B"],3,bpm,"b","nn")
                drawable_notes.insert(0,note)
            elif event.key == pygame.K_KP4:
                note = Note_Class(HN["O"],4,bpm,"o","nn")
                drawable_notes.insert(0,note)
            elif event.key == pygame.K_KP5:
                note = Note_Class(PO["G"],0,bpm,"g","nl")
                drawable_notes.insert(0,note)
            elif event.key == pygame.K_KP6:
                note = Note_Class(PO["R"],1,bpm,"r","nl")
                drawable_notes.insert(0,note)
            elif event.key == pygame.K_KP7:
                note = Note_Class(PO["Y"],2,bpm,"y","nl")
                drawable_notes.insert(0,note)
            elif event.key == pygame.K_KP8:
                note = Note_Class(PO["B"],3,bpm,"b","nl")
                drawable_notes.insert(0,note)
            elif event.key == pygame.K_KP9:
                note = Note_Class(PO["O"],4,bpm,"o","nl")
                drawable_notes.insert(0,note)
            elif event.key == pygame.K_KP_DIVIDE:
                note = Note_Class(open_note,5,bpm,"s","sn")
                drawable_notes.insert(0,note)
            for key in keys_dict:
                if event.key == key and space_pressed or  event.key == key and gamepad_mode:
                    n_pressed[keys_dict[key]] = "normal"
                    n_held[keys_dict[key]] = "normal"
                elif event.key == key and space_pressed:
                    n_pressed[keys_dict[key]] = "light"
            if event.key == pygame.K_p:
                if gamepad_mode:
                    gamepad_mode = False
                else:
                    gamepad_mode = True

    if pygame.time.get_ticks() - o_time  >= 0:
        o_time = pygame.time.get_ticks() + (bpm * 60)/4
        if current_fret != 3:
            current_fret += 1
        else:
            current_fret = 0
        temp = Fret(fret[current_fret],bpm)
        frets.insert(0,temp)

    draw_background()

    for press in n_pressed:
        if n_pressed[press] == "normal":
            if len(drawable_notes) != 0:
                for n in drawable_notes:
                    if n.note[0] != press[0]:
                        continue
                    elif notecol.colliderect(n.rect):
                        drawable_notes.remove(n)
                        point += 1
            n_pressed[press] = "none"
        elif n_pressed[press] == "light":
            temp = False
            if len(drawable_notes) != 0:
                for n in drawable_notes:
                    if n.note[0] != press[0] or n.type != "nl":
                        continue
                    elif notecol.colliderect(n.rect):
                        drawable_notes.remove(n)
                        temp = True
            if temp == True:
                point += 1
            n_pressed[press] = "none"

    if len(drawable_notes) != 0:
        for n in drawable_notes:
            if n.pos[1] >= 900:
                drawable_notes.remove(n)

    draw_notes(drawable_notes)

    pygame.display.update()
    clock.tick(60)