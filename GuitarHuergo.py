import pygame, os

width = 1920
height = 1080

pygame.init()
window = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

assets = os.path.join(os.path.dirname(__file__), "Assets")

# Background assets
# SE CARGAN LOS ASSETS CON ANTELACION PARA NO GASTAR MUCHOS RECURSOS DURANTE EL JUEGO (aclaracion)
bgnd_assets = os.path.join(assets, "Background")  # acceso a la ruta con los assets

traste = pygame.image.load(os.path.join(bgnd_assets,"Back.png")).convert_alpha()  # carga y guarda la imagen

# pygame.image.load() SIRVE PARA CARGAR IMAGENES.
# PARA UTILIZARLO HAY QUE ESCRIBIR LA DIRECCION DE LA IMAGEN Y PYGAME LO VA A CARGAR.
# .convert_alpha() ES UTILIZADO PARA QUE EL PROGRAMA NO TENGA QUE PROCESAR TODOS LOS
# PIXELES DE LA IMAGEN

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

# EL DICCIONARIO ES UTIL PARA YA TENER LOS FOTOGRAMAS DE LA ANIMACION CARGADAS

# KEYS
key_assets = os.path.join(assets, "Keys") # acceso a la ruta con los assets

# Teclas del juego
normal_keys = os.path.join(key_assets,"Normal")

G_K = pygame.image.load(os.path.join(normal_keys,"Green.png")).convert_alpha()
R_K = pygame.image.load(os.path.join(normal_keys,"Red.png")).convert_alpha()
Y_K = pygame.image.load(os.path.join(normal_keys,"Yellow.png")).convert_alpha()
B_K = pygame.image.load(os.path.join(normal_keys,"Blue.png")).convert_alpha()
O_K = pygame.image.load(os.path.join(normal_keys,"Orange.png")).convert_alpha()

# Teclas cuando son presionadas
hit_keysN = os.path.join(key_assets,"HitNormal")

G_KHN = pygame.image.load(os.path.join(hit_keysN,"Green.png")).convert_alpha()
R_KHN = pygame.image.load(os.path.join(hit_keysN,"Red.png")).convert_alpha()
Y_KHN = pygame.image.load(os.path.join(hit_keysN,"Yellow.png")).convert_alpha()
B_KHN = pygame.image.load(os.path.join(hit_keysN,"Blue.png")).convert_alpha()
O_KHN = pygame.image.load(os.path.join(hit_keysN,"Orange.png")).convert_alpha()

# Teclas cuando son presionadas con la strum bar
hit_keysB = os.path.join(key_assets,"HitBar")

G_KHB = pygame.image.load(os.path.join(hit_keysB,"Green.png")).convert_alpha()
R_KHB = pygame.image.load(os.path.join(hit_keysB,"Red.png")).convert_alpha()
Y_KHB = pygame.image.load(os.path.join(hit_keysB,"Yellow.png")).convert_alpha()
B_KHB = pygame.image.load(os.path.join(hit_keysB,"Blue.png")).convert_alpha()
O_KHB = pygame.image.load(os.path.join(hit_keysB,"Orange.png")).convert_alpha()

def draw_background(fps):
    window.fill("black") # CONVIERTE EL FONDO EN NEGRO
    window.blit(cuerda_anim[str(int(fps))])
    window.blit(traste,(0,0))

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_a] and teclas[pygame.K_SPACE]:
        window.blit(G_KHB, (0,0))
    elif teclas[pygame.K_a]:
        window.blit(G_KHN, (0,0))
    else:
        window.blit(G_K, (0,0))
    if teclas[pygame.K_s] and teclas[pygame.K_SPACE]:
        window.blit(R_KHB, (0,0))
    elif teclas[pygame.K_s]:
        window.blit(R_KHN, (0,0))
    else:
        window.blit(R_K, (0,0))
    if teclas[pygame.K_j] and teclas[pygame.K_SPACE]:
        window.blit(Y_KHB, (0,0))
    elif teclas[pygame.K_j]:
        window.blit(Y_KHN, (0,0))
    else:
        window.blit(Y_K, (0,0))
    if teclas[pygame.K_k] and teclas[pygame.K_SPACE]:
        window.blit(B_KHB, (0,0))
    elif teclas[pygame.K_k]:
        window.blit(B_KHN, (0,0))
    else:
        window.blit(B_K, (0,0))
    if teclas[pygame.K_l] and teclas[pygame.K_SPACE]:
        window.blit(O_KHB, (0,0))
    elif teclas[pygame.K_l]:
        window.blit(O_KHN, (0,0))
    else:
        window.blit(O_K, (0,0))

bgr_fps = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    draw_background(bgr_fps)

    bgr_fps += 0.5

    if bgr_fps > 47:
        bgr_fps = 0
    pygame.display.update()
    clock.tick(60)