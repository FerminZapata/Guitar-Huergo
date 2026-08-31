import pygame, os

width = 1500
height = 900

pygame.init()
window = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

assets = os.path.join(os.path.dirname(__file__), "Assets")

# Para que no se joda la performance del juego, primero se cargan los assets para no tener que cargarlos individualmente despues (aclaracion)
# Esto beneficia los fps del juego ya que si se tienen que cargar muchos assets por cada vuelta en el loop principal
# los fps van a disminuir, ya que el programa esta cargando todos los assets cada milesima de segundo 

class Note_Class:
    def __init__(self, surf, row,spd):
        self.spd = spd
        self.row = row
        self.surf = surf
        self.add = 0
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
            note = pygame.transform.scale(self.surf, ((self.surf.get_width()/10) + self.add, (self.surf.get_height()/10) + self.add))
            if self.row == 0:
                self.pos = (self.pos[0]-4.3*self.spd,self.pos[1]+8*self.spd)
            elif self.row == 1:
                self.pos = (self.pos[0]-2.8*self.spd,self.pos[1]+8*self.spd)
            elif self.row == 2:
                self.pos = (self.pos[0]-0.9*self.spd,self.pos[1]+8*self.spd)
            elif self.row == 3:
                self.pos = (self.pos[0]+1*self.spd,self.pos[1]+8*self.spd)
            elif self.row == 4:
                self.pos = (self.pos[0]+2.6*self.spd,self.pos[1]+8*self.spd)
            self.add += 1.8*self.spd
            self.spd += 0.005
            window.blit(note,self.pos)

class Trast:
    print("hola")

# Background assets
bgnd_assets = os.path.join(assets, "Background")  # acceso a la ruta con los assets

traste = pygame.image.load(os.path.join(bgnd_assets,"Back.png")).convert_alpha()  # carga y guarda la imagen

# pygame.image.load() sirve para cargar imagenes.
# Para cargar una imagen hay que escribir la ruta de esta adentro de los parentesis
# .convert_alpha() es utilizado para procesar todos los pixeles de la imagen más rapido

# Teclas
key_assets = os.path.join(assets, "Keys") # guarda la ruta con los assets

# Teclas sin ser presionadas
normal_keys = os.path.join(key_assets,"Normal") # guarda la ruta de los assets

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

def draw_background(fps):
    window.fill("black") # CONVIERTE EL FONDO EN NEGRO

    # .fill() sirve para pintar toda una ventana de un solo color.
    # Se puede poner tanto un valor RGB como el nombre del color en minusculas.

    pos_def = (width/2 - traste.get_width()/2,height - traste.get_height()) # variable que almacena la posicion de las superficies

    # En este caso fps es convertido en int y en string es para que pueda cumplir con los rangos del diccionario, ya que
    # por defecto, este es un numero decimal
    window.blit(traste,pos_def)
    # .blit(sur, pos) sirve para dibujar una superficie en la ventana, window siendo la ventana en este caso
    # sur = superficie que se va a dibujar (puede ser tanto una recta que dibuja el juego o una imagen)
    # pos = posicion de la superficie

    teclas = pygame.key.get_pressed() # se obtiene una lista booleana con todas las teclas almacenadas (True = tecla presionada)


    if teclas[pygame.K_a] and teclas[pygame.K_SPACE] or teclas[pygame.K_a] and gamepad_mode: # se accede al valor booleano mediante la variable y pygame.nombre_de_la_tecla
        window.blit(G_KHB, pos_def) # se dibuja la imagen de la tecla siendo presionada
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

#notea = notes["G"]
#notea = pygame.transform.scale(notea, (notea.get_width()/10, notea.get_height()/10))
#window.blit(notea, (655,430))
#noteb = notes["G"]
#noteb = pygame.transform.scale(noteb, (noteb.get_width()/4, noteb.get_height()/4))
#window.blit(noteb, (483,750))

def draw_notes(lista):
    if len(lista) != 0:
        for i in lista:
            if i.pos[1] >= 900:
                del i
            else:
                i.update()

bgr_fps = 0 # contador que se encarga de la animacion del traste

drawable_notes = [] # Lista que almacena las notas actuales

gamepad_mode = True

while True:
    for event in pygame.event.get():
        # Este for loop se encarga de revisar todos los eventos de pygame gracias a pygame.event.get() que devuelve
        # una lista con los tipos de eventos (REGISTRA UN INPUT UNA UNICA VEZ, EJ: TOCAS UNA FLECHA Y EL PERSONAJE SE MUEVE UNA VEZ)
        if event.type == pygame.QUIT: # En caso de que el evento sea el que detecta un intento de cierre
            pygame.quit() # se cierra el pygame.init()
            exit() # se termina el programa
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                note = Note_Class(notes["G"],0,0.5)
                drawable_notes.append(note)
            elif event.key == pygame.K_w:
                note = Note_Class(notes["R"],1,0.5)
                drawable_notes.append(note)
            elif event.key == pygame.K_e:
                note = Note_Class(notes["Y"],2,0.5)
                drawable_notes.append(note)
            elif event.key == pygame.K_r:
                note = Note_Class(notes["B"],3,0.5)
                drawable_notes.append(note)
            elif event.key == pygame.K_t:
                note = Note_Class(notes["O"],4,0.5)
                drawable_notes.append(note)

    draw_background(bgr_fps)

    draw_notes(drawable_notes)

    bgr_fps += 0.5 # con esta variable se puede controlar la velocidad de la animacion (bpm?)

    if bgr_fps > 47:
        bgr_fps = 0
    
    pygame.display.update() # se encarga de actualizar la ventana
    clock.tick(60) # son los fps (en pocas palabras)