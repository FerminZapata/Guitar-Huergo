import pygame, os

width = 1500
height = 900

pygame.init()
window = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

assets = os.path.join(os.path.dirname(__file__), "Assets")

notecol = pygame.Rect(500,750,500,2)

n_pressed = {"g_press":False,
             "r_press":False,
             "y_press":False,
             "b_press":False,
             "o_press":False}

n_held = {"g_press":False,
          "r_press":False,
          "y_press":False,
          "b_press":False,
          "o_press":False}

class Note_Class:
    def __init__(self, surf, row, bpm, note, typ):
        self.spd = (bpm/60)
        self.row = row
        self.surf = surf
        self.type = typ
        self.note = note
        self.add = 0.1
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
            self.add += 0.005*self.spd
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

# Teclas
key_assets = os.path.join(assets, "Keys") # ruta de la carpeta de assets

# Teclas sin ser presionadas
normal_keys = os.path.join(key_assets,"Normal") # ruta de los assets

G_K = pygame.image.load(os.path.join(normal_keys,"Green.png")).convert_alpha()
R_K = pygame.image.load(os.path.join(normal_keys,"Red.png")).convert_alpha()
Y_K = pygame.image.load(os.path.join(normal_keys,"Yellow.png")).convert_alpha()
B_K = pygame.image.load(os.path.join(normal_keys,"Blue.png")).convert_alpha()
O_K = pygame.image.load(os.path.join(normal_keys,"Orange.png")).convert_alpha()

# Teclas cuando son presionadas
hit_keysN = os.path.join(key_assets,"HitNormal") # guarda la ruta de los assets

G_KHN = pygame.image.load(os.path.join(hit_keysN,"Green.png")).convert_alpha()
R_KHN = pygame.image.load(os.path.join(hit_keysN,"Red.png")).convert_alpha()
Y_KHN = pygame.image.load(os.path.join(hit_keysN,"Yellow.png")).convert_alpha()
B_KHN = pygame.image.load(os.path.join(hit_keysN,"Blue.png")).convert_alpha()
O_KHN = pygame.image.load(os.path.join(hit_keysN,"Orange.png")).convert_alpha()

# Teclas cuando son presionadas con la strum bar
hit_keysB = os.path.join(key_assets,"HitBar") # guarda la ruta de los assets

G_KHB = pygame.image.load(os.path.join(hit_keysB,"Green.png")).convert_alpha()
R_KHB = pygame.image.load(os.path.join(hit_keysB,"Red.png")).convert_alpha()
Y_KHB = pygame.image.load(os.path.join(hit_keysB,"Yellow.png")).convert_alpha()
B_KHB = pygame.image.load(os.path.join(hit_keysB,"Blue.png")).convert_alpha()
O_KHB = pygame.image.load(os.path.join(hit_keysB,"Orange.png")).convert_alpha()

# Notas
note_assets = os.path.join(assets, "Notes")

# Notas normales
note_folder = os.path.join(note_assets, "Normal")

notes = {"G":pygame.image.load(os.path.join(note_folder,"Green.png")).convert_alpha(),
         "R":pygame.image.load(os.path.join(note_folder,"Red.png")).convert_alpha(),
         "Y":pygame.image.load(os.path.join(note_folder,"Yellow.png")).convert_alpha(),
         "B":pygame.image.load(os.path.join(note_folder,"Blue.png")).convert_alpha(),
         "O":pygame.image.load(os.path.join(note_folder,"Orange.png")).convert_alpha()}

# Notas brillantes
notel = os.path.join(note_assets, "Normal Light")

Lnotes = {"G":pygame.image.load(os.path.join(notel,"Green.png")).convert_alpha(),
         "R":pygame.image.load(os.path.join(notel,"Red.png")).convert_alpha(),
         "Y":pygame.image.load(os.path.join(notel,"Yellow.png")).convert_alpha(),
         "B":pygame.image.load(os.path.join(notel,"Blue.png")).convert_alpha(),
         "O":pygame.image.load(os.path.join(notel,"Orange.png")).convert_alpha()}

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

    if teclas[pygame.K_a] and teclas[pygame.K_SPACE] or teclas[pygame.K_a] and gamepad_mode:
        window.blit(G_KHB, pos_def)
    elif teclas[pygame.K_a]:
        window.blit(G_KHN, pos_def)
    else:
        window.blit(G_K, pos_def)
    if teclas[pygame.K_s] and teclas[pygame.K_SPACE] or teclas[pygame.K_s] and gamepad_mode:
        window.blit(R_KHB, pos_def)
    elif teclas[pygame.K_s]:
        window.blit(R_KHN, pos_def)
    else:
        window.blit(R_K, pos_def)
    if teclas[pygame.K_j] and teclas[pygame.K_SPACE] or teclas[pygame.K_j] and gamepad_mode:
        window.blit(Y_KHB, pos_def)
    elif teclas[pygame.K_j]:
        window.blit(Y_KHN, pos_def)
    else:
        window.blit(Y_K, pos_def)
    if teclas[pygame.K_k] and teclas[pygame.K_SPACE] or teclas[pygame.K_k] and gamepad_mode:
        window.blit(B_KHB, pos_def)
    elif teclas[pygame.K_k]:
        window.blit(B_KHN, pos_def)
    else:
        window.blit(B_K, pos_def)
    if teclas[pygame.K_l] and teclas[pygame.K_SPACE] or teclas[pygame.K_l] and gamepad_mode:
        window.blit(O_KHB, pos_def)
    elif teclas[pygame.K_l]:
        window.blit(O_KHN, pos_def)
    else:
        window.blit(O_K, pos_def)

def draw_notes(lista):
    if len(lista) != 0:
        for i in lista:
            if i.pos[1] >= 900:
                del i
            else:
                i.update()

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
            if event.key == pygame.K_SPACE:
                space_pressed = False
            if event.key == pygame.K_a or event.key == pygame.K_a and gamepad_mode:
                n_pressed["g_press"] = "none"
                n_held["g_press"] = "none"
            if event.key == pygame.K_s or event.key == pygame.K_s and gamepad_mode:
                n_pressed["r_press"] = "none"
                n_held["r_press"] = "none"
            if event.key == pygame.K_j or event.key == pygame.K_j and gamepad_mode:
                n_pressed["y_press"] = "none"
                n_held["y_press"] = "none"
            if event.key == pygame.K_k or event.key == pygame.K_k and gamepad_mode:
                n_pressed["b_press"] = "none"
                n_held["b_press"] = "none"
            if event.key == pygame.K_l or event.key == pygame.K_l and gamepad_mode:
                n_pressed["o_press"] = "none"
                n_held["o_press"] = "none"
        elif event.type == pygame.KEYDOWN:
            pos_def = (width/2 - background.get_width()/2,height - background.get_height())
            if event.key == pygame.K_SPACE:
                space_pressed = True
            if event.key == pygame.K_KP0:
                note = Note_Class(notes["G"],0,bpm,"g","nn")
                drawable_notes.insert(0,note)
            elif event.key == pygame.K_KP1:
                note = Note_Class(notes["R"],1,bpm,"r","nn")
                drawable_notes.insert(0,note)
            elif event.key == pygame.K_KP2:
                note = Note_Class(notes["Y"],2,bpm,"y","nn")
                drawable_notes.insert(0,note)
            elif event.key == pygame.K_KP3:
                note = Note_Class(notes["B"],3,bpm,"b","nn")
                drawable_notes.insert(0,note)
            elif event.key == pygame.K_KP4:
                note = Note_Class(notes["O"],4,bpm,"o","nn")
                drawable_notes.insert(0,note)
            elif event.key == pygame.K_KP5:
                note = Note_Class(Lnotes["G"],0,bpm,"g","nl")
                drawable_notes.insert(0,note)
            elif event.key == pygame.K_KP6:
                note = Note_Class(Lnotes["R"],1,bpm,"r","nl")
                drawable_notes.insert(0,note)
            elif event.key == pygame.K_KP7:
                note = Note_Class(Lnotes["Y"],2,bpm,"y","nl")
                drawable_notes.insert(0,note)
            elif event.key == pygame.K_KP8:
                note = Note_Class(Lnotes["B"],3,bpm,"b","nl")
                drawable_notes.insert(0,note)
            elif event.key == pygame.K_KP9:
                note = Note_Class(Lnotes["O"],4,bpm,"o","nl")
                drawable_notes.insert(0,note)
            if event.key == pygame.K_a and space_pressed or event.key == pygame.K_a and gamepad_mode:
                n_pressed["g_press"] = "normal"
                n_held["g_press"] = "normal"
            elif event.key == pygame.K_a:
                n_pressed["g_press"] = "light"
            if event.key == pygame.K_s and space_pressed or event.key == pygame.K_s and gamepad_mode:
                n_pressed["r_press"] = "normal"
                n_held["r_press"] = "normal"
            elif event.key == pygame.K_s:
                n_pressed["r_press"] = "light"
            if event.key == pygame.K_j and space_pressed or event.key == pygame.K_j and gamepad_mode:
                n_pressed["y_press"] = "normal"
                n_held["y_press"] = "light"
            elif event.key == pygame.K_j:
                n_pressed["y_press"] = "normal"
            if event.key == pygame.K_k and space_pressed or event.key == pygame.K_k and gamepad_mode:
                n_pressed["b_press"] = "normal"
                n_held["b_press"] = "normal"
            elif event.key == pygame.K_k:
                n_pressed["b_press"] = "light"
            if event.key == pygame.K_l and space_pressed or event.key == pygame.K_l and gamepad_mode:
                n_pressed["o_press"] = "normal"
                n_held["o_press"] = "normal"
            elif event.key == pygame.K_l:
                n_pressed["o_press"] = "light"
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