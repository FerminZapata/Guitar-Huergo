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

# Background assets
bgnd_assets = os.path.join(assets, "Background")  # acceso a la ruta con los assets

traste = pygame.image.load(os.path.join(bgnd_assets,"Back.png")).convert_alpha()  # carga y guarda la imagen

# pygame.image.load() sirve para cargar imagenes.
# Para cargar una imagen hay que escribir la ruta de esta adentro de los parentesis
# .convert_alpha() es utilizado para procesar todos los pixeles de la imagen más rapido

cuerda_anim = {"0":pygame.image.load(os.path.join(bgnd_assets,"Lines0.png")).convert_alpha(),
             "1":pygame.image.load(os.path.join(bgnd_assets,"Lines1.png")).convert_alpha(),
             "2":pygame.image.load(os.path.join(bgnd_assets,"Lines2.png")).convert_alpha(),
             "3":pygame.image.load(os.path.join(bgnd_assets,"Lines3.png")).convert_alpha(),
             "4":pygame.image.load(os.path.join(bgnd_assets,"Lines4.png")).convert_alpha(),
             "5":pygame.image.load(os.path.join(bgnd_assets,"Lines5.png")).convert_alpha(),
             "6":pygame.image.load(os.path.join(bgnd_assets,"Lines6.png")).convert_alpha(),
             "7":pygame.image.load(os.path.join(bgnd_assets,"Lines7.png")).convert_alpha(),
             "8":pygame.image.load(os.path.join(bgnd_assets,"Lines8.png")).convert_alpha(),
             "9":pygame.image.load(os.path.join(bgnd_assets,"Lines9.png")).convert_alpha(),
             "10":pygame.image.load(os.path.join(bgnd_assets,"Lines10.png")).convert_alpha(),
             "11":pygame.image.load(os.path.join(bgnd_assets,"Lines11.png")).convert_alpha(),
             "12":pygame.image.load(os.path.join(bgnd_assets,"Lines12.png")).convert_alpha(),
             "13":pygame.image.load(os.path.join(bgnd_assets,"Lines13.png")).convert_alpha(),
             "14":pygame.image.load(os.path.join(bgnd_assets,"Lines14.png")).convert_alpha(),
             "15":pygame.image.load(os.path.join(bgnd_assets,"Lines15.png")).convert_alpha(),
             "16":pygame.image.load(os.path.join(bgnd_assets,"Lines16.png")).convert_alpha(),
             "17":pygame.image.load(os.path.join(bgnd_assets,"Lines17.png")).convert_alpha(),
             "18":pygame.image.load(os.path.join(bgnd_assets,"Lines18.png")).convert_alpha(),
             "19":pygame.image.load(os.path.join(bgnd_assets,"Lines19.png")).convert_alpha(),
             "20":pygame.image.load(os.path.join(bgnd_assets,"Lines20.png")).convert_alpha(),
             "21":pygame.image.load(os.path.join(bgnd_assets,"Lines21.png")).convert_alpha(),
             "22":pygame.image.load(os.path.join(bgnd_assets,"Lines22.png")).convert_alpha(),
             "23":pygame.image.load(os.path.join(bgnd_assets,"Lines23.png")).convert_alpha(),
             "24":pygame.image.load(os.path.join(bgnd_assets,"Lines24.png")).convert_alpha(),
             "25":pygame.image.load(os.path.join(bgnd_assets,"Lines25.png")).convert_alpha(),
             "26":pygame.image.load(os.path.join(bgnd_assets,"Lines26.png")).convert_alpha(),
             "27":pygame.image.load(os.path.join(bgnd_assets,"Lines27.png")).convert_alpha(),
             "28":pygame.image.load(os.path.join(bgnd_assets,"Lines28.png")).convert_alpha(),
             "29":pygame.image.load(os.path.join(bgnd_assets,"Lines29.png")).convert_alpha(),
             "30":pygame.image.load(os.path.join(bgnd_assets,"Lines30.png")).convert_alpha(),
             "31":pygame.image.load(os.path.join(bgnd_assets,"Lines31.png")).convert_alpha(),
             "32":pygame.image.load(os.path.join(bgnd_assets,"Lines32.png")).convert_alpha(),
             "33":pygame.image.load(os.path.join(bgnd_assets,"Lines33.png")).convert_alpha(),
             "34":pygame.image.load(os.path.join(bgnd_assets,"Lines34.png")).convert_alpha(),
             "35":pygame.image.load(os.path.join(bgnd_assets,"Lines35.png")).convert_alpha(),
             "36":pygame.image.load(os.path.join(bgnd_assets,"Lines36.png")).convert_alpha(),
             "37":pygame.image.load(os.path.join(bgnd_assets,"Lines37.png")).convert_alpha(),
             "38":pygame.image.load(os.path.join(bgnd_assets,"Lines38.png")).convert_alpha(),
             "39":pygame.image.load(os.path.join(bgnd_assets,"Lines39.png")).convert_alpha(),
             "40":pygame.image.load(os.path.join(bgnd_assets,"Lines40.png")).convert_alpha(),
             "41":pygame.image.load(os.path.join(bgnd_assets,"Lines41.png")).convert_alpha(),
             "42":pygame.image.load(os.path.join(bgnd_assets,"Lines42.png")).convert_alpha(),
             "43":pygame.image.load(os.path.join(bgnd_assets,"Lines43.png")).convert_alpha(),
             "44":pygame.image.load(os.path.join(bgnd_assets,"Lines44.png")).convert_alpha(),
             "45":pygame.image.load(os.path.join(bgnd_assets,"Lines45.png")).convert_alpha(),
             "46":pygame.image.load(os.path.join(bgnd_assets,"Lines46.png")).convert_alpha(),
             "47":pygame.image.load(os.path.join(bgnd_assets,"Lines47.png")).convert_alpha(),}

# El diccionario es MUY largo, pero guarda todos los fotogramas de la animacion para que estos esten cargados y para que
# se puedan acceder facilmente, teniendo un contador que aumenta por vuelta en el loop principal

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
note = os.path.join(note_assets, "Normal")

notes = {"G":pygame.image.load(os.path.join(note,"Green.png")).convert_alpha(),
         "R":pygame.image.load(os.path.join(note,"Red.png")).convert_alpha(),
         "Y":pygame.image.load(os.path.join(note,"Yellow.png")).convert_alpha(),
         "B":pygame.image.load(os.path.join(note,"Blue.png")).convert_alpha(),
         "O":pygame.image.load(os.path.join(note,"Orange.png")).convert_alpha()}

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

    window.blit(cuerda_anim[str(int(fps))], pos_def)
    # En este caso fps es convertido en int y en string es para que pueda cumplir con los rangos del diccionario, ya que
    # por defecto, este es un numero decimal
    window.blit(traste,pos_def)
    # .blit(sur, pos) sirve para dibujar una superficie en la ventana, window siendo la ventana en este caso
    # sur = superficie que se va a dibujar (puede ser tanto una recta que dibuja el juego o una imagen)
    # pos = posicion de la superficie

    teclas = pygame.key.get_pressed() # se obtiene una lista booleana con todas las teclas almacenadas (True = tecla presionada)

    if teclas[pygame.K_a] and teclas[pygame.K_SPACE]: # se accede al valor booleano mediante la variable y pygame.nombre_de_la_tecla
        window.blit(G_KHB, pos_def) # se dibuja la imagen de la tecla siendo presionada
    elif teclas[pygame.K_a]:
        window.blit(G_KHN, pos_def)
    else:
        window.blit(G_K, pos_def)
    if teclas[pygame.K_s] and teclas[pygame.K_SPACE]:
        window.blit(R_KHB, pos_def)
    elif teclas[pygame.K_s]:
        window.blit(R_KHN, pos_def)
    else:
        window.blit(R_K, pos_def)
    if teclas[pygame.K_j] and teclas[pygame.K_SPACE]:
        window.blit(Y_KHB, pos_def)
    elif teclas[pygame.K_j]:
        window.blit(Y_KHN, pos_def)
    else:
        window.blit(Y_K, pos_def)
    if teclas[pygame.K_k] and teclas[pygame.K_SPACE]:
        window.blit(B_KHB, pos_def)
    elif teclas[pygame.K_k]:
        window.blit(B_KHN, pos_def)
    else:
        window.blit(B_K, pos_def)
    if teclas[pygame.K_l] and teclas[pygame.K_SPACE]:
        window.blit(O_KHB, pos_def)
    elif teclas[pygame.K_l]:
        window.blit(O_KHN, pos_def)
    else:
        window.blit(O_K, pos_def)

bgr_fps = 0 # contador que se encarga de la animacion del traste


while True:
    for event in pygame.event.get():
        # Este for loop se encarga de revisar todos los eventos de pygame gracias a pygame.event.get() que devuelve
        # una lista con los tipos de eventos (REGISTRA UN INPUT UNA UNICA VEZ, EJ: TOCAS UNA FLECHA Y EL PERSONAJE SE MUEVE UNA VEZ)
        if event.type == pygame.QUIT: # En caso de que el evento sea el que detecta un intento de cierre
            pygame.quit() # se cierra el pygame.init()
            exit() # se termina el programa
    
    draw_background(bgr_fps)

    bgr_fps += 0.5 # con esta variable se puede controlar la velocidad de la animacion (bpm?)

    if bgr_fps > 47:
        bgr_fps = 0
    
    pygame.display.update() # se encarga de actualizar la ventana
    clock.tick(60) # son los fps (en pocas palabras)