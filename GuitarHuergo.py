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
             "11":pygame.image.load(os.path.join(bgnd_assets,"Lines11.png")).convert_alpha(),}

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
hit_keys = os.path.join(key_assets,"Hit")

G_KH = pygame.image.load(os.path.join(hit_keys,"Green.png")).convert_alpha()
R_KH = pygame.image.load(os.path.join(hit_keys,"Red.png")).convert_alpha()
Y_KH = pygame.image.load(os.path.join(hit_keys,"Yellow.png")).convert_alpha()
B_KH = pygame.image.load(os.path.join(hit_keys,"Blue.png")).convert_alpha()
O_KH = pygame.image.load(os.path.join(hit_keys,"Orange.png")).convert_alpha()

def draw_background(fps):
    window.fill("black") # CONVIERTE EL FONDO EN NEGRO
    window.blit(cuerda_anim[str(int(fps))])
    window.blit(traste,(0,0))
    if teclas[pygame.K_q]:
        window.blit(G_KH, (0,0))
    else:
        window.blit(G_K, (0,0))
    if teclas[pygame.K_w]:
        window.blit(R_KH, (0,0))
    else:
        window.blit(R_K, (0,0))
    if teclas[pygame.K_e]:
        window.blit(Y_KH, (0,0))
    else:
        window.blit(Y_K, (0,0))
    if teclas[pygame.K_r]:
        window.blit(B_KH, (0,0))
    else:
        window.blit(B_K, (0,0))
    if teclas[pygame.K_t]:
        window.blit(O_KH, (0,0))
    else:
        window.blit(O_K, (0,0))

bgr_fps = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    teclas = pygame.key.get_pressed()

    draw_background(bgr_fps)

    bgr_fps += 0.25

    if bgr_fps > 11:
        bgr_fps = 0
    pygame.display.update()
    clock.tick(60)