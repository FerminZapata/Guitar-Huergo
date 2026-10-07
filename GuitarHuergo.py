import pygame, os

width = 1500
height = 900

pygame.init()
window = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

assets = os.path.join(os.path.dirname(__file__), "Assets")

notecol = pygame.surface.Surface((500,100))

notecol.set_alpha(90)

notecol.fill((255,255,255))

keys_dict = {pygame.K_a :"G_press",
             pygame.K_s:"R_press",
             pygame.K_j:"Y_press",
             pygame.K_k:"B_press",
             pygame.K_l:"O_press",
             pygame.K_SPACE:"Open"}

n_pressed = {"G_press":False,
             "R_press":False,
             "Y_press":False,
             "B_press":False,
             "O_press":False,
             "Open":False}

n_held = {"G_press":False,
          "R_press":False,
          "Y_press":False,
          "B_press":False,
          "O_press":False,
          "Open":False}

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

HN = {} # Este diccionario guarda todas las notas normales

for img in data:
    HN[img[:-4]] = pygame.image.load(os.path.join(hamon_path,img)).convert_alpha()

# Creacion de un diccionario con los assets de las notas Pull off
pulloff_path = os.path.join(note_assets, "Pull-off")

data = os.listdir(pulloff_path)

PO = {} # Este diccionario guarda las notas iluminadas

for img in data:
    PO[img[:-4]] = pygame.image.load(os.path.join(pulloff_path,img)).convert_alpha()

# Creacion de un diccionario con los assets de las notas Tap
tap_path = os.path.join(note_assets, "Pull-off")

data = os.listdir(tap_path)

TN = {} # Este diccionario guarda las notas transparentes

for img in data:
    TN[img[:-4]] = pygame.image.load(os.path.join(tap_path,img)).convert_alpha()

long_path = os.path.join(note_assets, "Long")

data = os.listdir(long_path)

LN = {} # Este diccionario guarda las notas largas

for img in data:
    LN[img[:-4]] = pygame.image.load(os.path.join(long_path,img)).convert_alpha()

notes = {"hammer":HN,
         "pull":PO,
         "tap":TN}

startNotePos = {
    "Green":(655,420),
    "Red":(695,420),
    "Yellow":(730,420),
    "Blue":(765,420),
    "Orange":(800,420),
    "Open":(653,435)
}
longNotePos = {
    "Green":(380,435),
    "Red":(457,435),
    "Yellow":(530,435),
    "Blue":(605,435),
    "Orange":(680,435),
}

rowList = ["Green","Red","Yellow","Blue","Orange","Open"]
specialList = ["hammer","pull","tap"]
posChangeList = [-4.5,-2.8,-1,1,2.7,-4.2]

class long:
    def __init__(self, surf, pos, span):
        self.spd = bpm/60
        self.add = 0.1
        self.pos = pos
        self.surf = surf
        self.end = pygame.time.get_ticks() + span
        self.lcut = 0
        self.cuty = 0

    def move(self):
        self.start = pygame.time.get_ticks()
        if self.start <= self.end:
            if self.lcut <= 430:
                self.lcut += 8*self.spd
        elif self.start >= self.end:
            self.cuty += 8*self.spd
            self.pos = (self.pos[0],self.pos[1]+8*self.spd)
            if self.pos[1] + self.lcut <= 800:
                self.lcut += 8*self.add
        self.add += 0.005*self.spd
        self.spd += 0.005
        cut = pygame.Rect(0,self.cuty,self.surf.get_width(),self.lcut)
        window.blit(self.surf,self.pos,cut)

class Note_Class:
    def __init__(self, note, row, span, special):
        self.spd = bpm/60
        self.note = note
        self.span = span
        self.row = row
        self.special = special
        if row != 7:
            self.add = 0.1
            self.type = rowList[row]
        else:
            self.add = 0.48
            self.type = rowList[row-2]
        specialTemp = specialList[special]
        self.pos = startNotePos[self.type]
        type = notes[specialTemp]
        if row != 7:
            self.surf = type[self.type]
        else:
            self.surf = open_note
        self.middle = self.surf.get_height() / 2
        if span != 0 and self.row != 7:
            self.lsurf = LN[self.type]
            self.long = long(self.lsurf,longNotePos[self.type],span)

    def update(self):
        if self.pos[1] != 900:
            note = pygame.transform.scale(self.surf, (int(self.surf.get_width()*self.add), int(self.surf.get_height()*self.add)))
            self.middle = note.get_height() / 2
            if self.row != 7:
                self.pos = (self.pos[0]+posChangeList[self.row]*self.spd,self.pos[1]+8*self.spd)
            elif self.row == 7:
                self.pos = (self.pos[0]+posChangeList[self.row-2]*self.spd,self.pos[1]+8*self.spd)
            if self.row != 7:
                self.add += 0.005*self.spd
                self.spd += 0.005
            else:
                self.add += 0.022*self.spd
                self.spd += 0.005
            if self.span != 0 and self.row != 7:
                self.long.move()
            window.blit(note,self.pos)

def draw_background():
    window.fill("black") # CONVIERTE EL FONDO EN NEGRO

    window.blit(notecol,(500,700))

    pos_def = (width/2 - background.get_width()/2,height - background.get_height())

    if len(frets) != 0:
        for surf in frets:
            if surf.pos[1] >= 900:
                del surf
            else:
                surf.update()

    window.blit(background,pos_def)

    teclas = pygame.key.get_pressed()

    pressed = False

    for key in keys_dict:
        if key != pygame.K_SPACE:
            if teclas[key] and space_pressed or teclas[key] and gamepad_mode:
                window.blit(spkr_s[keys_dict[key][0]], pos_def)
                pressed = True
            elif teclas[key]:
                window.blit(spkr_h[keys_dict[key][0]], pos_def)
            else:
                window.blit(spkr[keys_dict[key][0]], pos_def)
        elif key == pygame.K_SPACE:
            if teclas[pygame.K_SPACE] and pressed != True or teclas[pygame.K_SPACE] and gamepad_mode:
                for key in spkr_s:
                    window.blit(spkr_s[key],pos_def)

def draw_notes(lista):
    if len(lista) != 0:
        for i in lista:
            if i.pos[1] >= 900:
                del i
            else:
                i.update()

def draw_frets():
    if pygame.time.get_ticks() - o_time  >= 0:
        o_time = pygame.time.get_ticks() + (bpm * 60)/4
        if current_fret != 3:
            current_fret += 1
        else:
            current_fret = 0
        temp = Fret(fret[current_fret],bpm)
        frets.insert(0,temp)

def check_pressed(dicc):
    temp = False
    for item in dicc:
        if dicc[item]:
            temp = True
    return temp

drawable_notes = [] # Lista que almacena las notas actuales

gamepad_mode = False

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
            for key in keys_dict:
                n_pressed[keys_dict[key]] = "none"
                n_held[keys_dict[key]] = "none"
            if event.key == pygame.K_SPACE:
                space_pressed = False
        elif event.type == pygame.KEYDOWN:
            pos_def = (width/2 - background.get_width()/2,height - background.get_height())
            if event.key == pygame.K_q:
                note = Note_Class("N",0,200,0)
                drawable_notes.append(note)
            elif event.key == pygame.K_w:
                note = Note_Class("N",1,200,0)
                drawable_notes.append(note)
            elif event.key == pygame.K_u:
                note = Note_Class("N",2,200,0)
                drawable_notes.append(note)
            elif event.key == pygame.K_i:
                note = Note_Class("N",3,200,0)
                drawable_notes.append(note)
            elif event.key == pygame.K_o:
                note = Note_Class("N",4,200,0)
                drawable_notes.append(note)
            elif event.key == pygame.K_z:
                note = Note_Class("N",0,200,1)
                drawable_notes.append(note)
            elif event.key == pygame.K_x:
                note = Note_Class("N",1,200,1)
                drawable_notes.append(note)
            elif event.key == pygame.K_n:
                note = Note_Class("N",2,200,1)
                drawable_notes.append(note)
            elif event.key == pygame.K_m:
                note = Note_Class("N",3,200,1)
                drawable_notes.append(note)
            elif event.key == pygame.K_COMMA:
                note = Note_Class("N",4,200,1)
                drawable_notes.append(note)
            elif event.key == pygame.K_KP_DIVIDE:
                note = Note_Class("N",7,0,0)
                drawable_notes.append(note)
            if event.key == pygame.K_SPACE:
                keys = pygame.key.get_pressed()
                space_pressed = False

                for code, name in keys_dict.items():
                    if name != pygame.K_SPACE and keys[code]:
                        n_pressed[name] = "normal"
                        n_held[name] = "normal"
                        space_pressed = True
                    if not space_pressed:
                        n_pressed["Open"] = "normal"
                        n_held["Open"] = "normal"
            elif event.key in keys_dict:
                pressed = keys_dict[event.key]
                if space_pressed or gamepad_mode:
                    n_pressed[pressed] = "normal"
                    n_held[pressed] = "normal"
                else:
                    n_pressed[pressed] = "light"
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
        print(n_pressed[press],press)
        if n_pressed[press] == "normal":
            if len(drawable_notes) != 0:
                for n in drawable_notes[:]:
                    if n.type[0] != press[0]:
                        continue
                    elif n.pos[1] + n.middle >= 650 and n.pos[1] + n.middle <= 750:
                            drawable_notes.remove(n)
                            n_pressed["Open"] = "none"
                            space_pressed = False
                            point += 1
            n_pressed[press] = "none"
        elif n_pressed[press] == "light":
            temp = False
            if len(drawable_notes) != 0:
                for n in drawable_notes[:]:
                    if n.type[0] != press[0] or n.special != 1:
                        continue
                    elif n.pos[1] + n.middle >= 650 and n.pos[1] + n.middle <= 750:
                        n_pressed["Open"] = "none"
                        space_pressed = False
                        point += 1
                        drawable_notes.remove(n)
            n_pressed[press] = "none"
    
    if len(drawable_notes) != 0:
        for n in drawable_notes:
            if n.pos[1] >= 750:
                drawable_notes.remove(n)

    draw_notes(drawable_notes)

    pygame.display.update()
    clock.tick(60)