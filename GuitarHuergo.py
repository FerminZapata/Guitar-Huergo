import pygame, os, re, sys, bisect, math, random
import LectorDeCancionesMIDI
from HeroPower import Marcador, HeroPower, MINIMO_PARA_ACTIVAR

# ---------------------------------------------------------------------------
# GuitarHuergo ahora es un MODULO: no abre la ventana ni arranca solo al importarlo.
# menu.py lo usa asi:
#
#     import GuitarHuergo
#     resultado = GuitarHuergo.jugar(carpeta_de_la_cancion, "expert", gamepad=False, volumen=0.5)
#
# Tambien se puede probar solo:  python GuitarHuergo.py  [carpeta_de_la_cancion]  [dificultad]
# ---------------------------------------------------------------------------

width = 1500
height = 900
FPS = 60

bpm = 60                    # velocidad VISUAL de las notas: durante la partida se actualiza sola con el BPM de la cancion (valor inicial por defecto)

# --- BPM dinamico -----------------------------------------------------------
FACTOR_BPM = 0.30           # multiplica el BPM de la cancion antes de usarlo como velocidad (0.75 = notas al 75%). Se cambia en Pausa > Opciones
FACTOR_BPM_MIN = 0.1        # limites que permite el menu de opciones de la pausa
FACTOR_BPM_MAX = 1.5
BPM_VISUAL_MIN = 40         # limites de la velocidad visual, para que un BPM muy bajo o muy alto no deje el juego injugable
BPM_VISUAL_MAX = 240
FRET_INTERVALO_BASE_MS = 900    # cada cuantos ms aparece un traste cuando bpm = 60 (con otro bpm se ajusta para que la separacion en pantalla sea la misma)
VENTANA_ESCALA_MAX = 2.0    # la ventana de golpe se agranda con la velocidad (para que no sea mas corta en ms): hasta x2. Poner 1.0 la deja fija como antes

# --- Sonidos de fallo y fondo custom ------------------------------------------
MISS_COOLDOWN_MS = 150      # separacion minima entre dos sonidos de fallo (un acorde fallado, o varios fallos juntos, suenan una sola vez)
NOMBRES_FONDO = ("background", "fondo")     # nombres (sin extension) que se buscan en la carpeta de la cancion para el fondo custom
FONDO_OSCURECER = 110       # 0 a 255: cuanto se oscurece el fondo custom para que se vean bien las notas

# --- Pausa --------------------------------------------------------------------
CUENTA_REGRESIVA_PAUSA = 3  # segundos de cuenta regresiva al volver de la pausa (0 = reanuda de golpe)

# --- sincronizacion -------------------------------------------------------
PRE_ROLL_MS = 3000          # tiempo de espera antes de que arranque la musica
OFFSET_AUDIO_MS = 0         # calibracion (ms): si la musica suena ADELANTADA respecto a las notas ponele un valor positivo, si suena atrasada uno negativo
VENTANA_MIN = 675           # una nota se puede tocar cuando su centro esta entre estas dos alturas
VENTANA_MAX = 800

# --- Star notes / Hero Power ----------------------------------------------
TECLAS_STAR_POWER = (pygame.K_LSHIFT, pygame.K_RSHIFT)     # teclas para activar el Hero Power
STAR_FRAMES = 30            # cuadros de la animacion de rotacion de la nota Star
STAR_ANIM_FPS = 30          # a cuantos cuadros por segundo gira (30 = una vuelta por segundo)
COLOR_POWER = (90, 200, 255)
# Trapecio del camino (aprox.) que se tine de azul cuando el Hero Power esta activo: (arriba-izq, arriba-der, abajo-der, abajo-izq)
HIGHWAY_POLY = [(650, 430), (850, 430), (1110, 900), (390, 900)]
HUD_DERECHA = 1470          # borde derecho de los textos del HUD
HUD_BARRA_X = 1380          # posicion de la barra de Hero Power

keys_dict = {pygame.K_a :"Green",
             pygame.K_s:"Red",
             pygame.K_j:"Yellow",
             pygame.K_k:"Blue",
             pygame.K_l:"Orange",
             pygame.K_SPACE:"Open"}

n_pressed = {"Green":"none",
             "Red":"none",
             "Yellow":"none",
             "Blue":"none",
             "Orange":"none",
             "Open":"none"}

n_held = {"Green":"none",
          "Red":"none",
          "Yellow":"none",
          "Blue":"none",
          "Orange":"none",
          "Open":"none"}

rowList = ["Green","Red","Yellow","Blue","Orange","Open"]
specialList = ["hammer","pull","tap"]      # 0 = nota normal, 1 = HOPO (iluminada), 2 = tap (transparente)
posChangeList = [-4.5,-2.8,-1,1,2.7,-4.2]

startNotePos = {
    "Green":(655,420),
    "Red":(695,420),
    "Yellow":(730,420),
    "Blue":(765,420),
    "Orange":(800,420),
    "Open":(653,435)
}

# --- estado que se llena al cargar los assets (hace falta que la ventana ya exista) ---
window = None
assets_cargados = False
notecol = None
background = None
fret = {}
spkr = {}
spkr_h = {}
spkr_s = {}
open_note = None
HN = {}
PO = {}
TN = {}
LN = {}
notes = {}
STAR_NOTES = {}             # {"Green": [30 cuadros], ...}
longNotePos = {}
overlay_power = None
fuente_puntaje = fuente_mult = fuente_chica = None
fuente_pausa = fuente_pausa_op = None
viaje_cache = {}            # {bpm: ms que tarda una nota en llegar a la ventana}
SONIDOS_FALLO = []          # Assets/SoundEffects/Miss*.mp3
tecla_de = {nombre: codigo for codigo, nombre in keys_dict.items()}     # {"Green": K_a, ...}

# --- estado de la partida ---
drawable_notes = []         # Lista que almacena las notas actuales
frets = []                  # Lista con los trastes que salen en pantalla
gamepad_mode = False
space_pressed = False
current_fret = 2
o_time = 0
marcador = None
hero = None
toast_texto = ""
toast_hasta = 0
pausa_total = 0             # ms acumulados en pausa en esta partida
volumen_actual = 0.5        # volumen de la partida (se cambia en Pausa > Opciones)
tiempo_cancion = 0          # ms de cancion en este frame (lo actualiza jugar)
fondo_cancion = None        # fondo custom de la cancion que se esta jugando (None = fondo negro de siempre)
ultimo_fallo_ms = -10000
ultimo_sonido_fallo = None

def ahora_juego():
    # Reloj de la partida: el de pygame menos el tiempo que estuvo en pausa. Todo lo que dependa
    # del tiempo (aparicion de notas, sustains, avisos) usa ESTE reloj, asi la pausa lo congela.
    return pygame.time.get_ticks() - pausa_total


def tecla_sostenida(tipo):
    # True si la tecla de ese carril (Green, Red, ..., Open = espacio) esta apretada AHORA.
    # Se mira la tecla directamente, asi mantener una nota larga funciona igual para notas
    # normales, HOPO, tap, Star y Open, sin importar con que tipo de golpe se acerto la cabeza.
    return bool(pygame.key.get_pressed()[tecla_de[tipo]])

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


# ===========================================================================
#  CARGA DE ASSETS (se hace una sola vez, la primera vez que se llama a jugar)
# ===========================================================================
EXT_IMAGEN = (".png", ".jpg", ".jpeg", ".webp", ".bmp")

def orden_natural(texto):               # para que "10.png" vaya despues de "9.png"
    return [int(p) if p.isdigit() else p for p in re.split(r"(\d+)", texto.lower())]

def color_de_ruta(ruta):                # busca el nombre de un color (Green, Red...) en la ruta de un archivo
    ruta = ruta.lower().replace("\\", "/")
    for color in rowList:
        if color.lower() in ruta:
            return color
    return None

def cargar_star(carpetas):
    # Busca la carpeta "Star" y arma {"Green": [cuadro0, cuadro1, ...], ...}.
    # Acepta una subcarpeta por color (Star/Green/01.png...), archivos con el color en el nombre
    # (Star/Green_01.png...) o una sola secuencia que se usa para todos los colores.
    carpeta = next((c for c in carpetas if os.path.isdir(c)), None)
    if carpeta is None:
        print("AVISO: no se encontro la carpeta Star, las notas Star se van a ver como notas normales. Busque en:", carpetas)
        return {}
    grupos = {}
    for raiz, _, archivos in os.walk(carpeta):
        for archivo in archivos:
            if os.path.splitext(archivo)[1].lower() in EXT_IMAGEN:
                rel = os.path.relpath(os.path.join(raiz, archivo), carpeta)
                grupos.setdefault(color_de_ruta(rel), []).append(rel)
    compartidos = grupos.pop(None, [])
    frames = {}
    for color in rowList:
        rels = sorted(grupos.get(color) or compartidos, key=orden_natural)
        if rels:
            frames[color] = [pygame.image.load(os.path.join(carpeta, r)).convert_alpha() for r in rels]
            if len(rels) != STAR_FRAMES:
                print("AVISO: Star/" + color, "tiene", len(rels), "imagenes (se esperaban", str(STAR_FRAMES) + ")")
        else:
            print("AVISO: no hay imagenes Star para", color, "(usa la nota normal)")
    return frames

def cargar_sonidos_fallo(carpeta):
    # Assets/SoundEffects/Miss1.mp3, Miss2.mp3, ... (suena uno al azar cada vez que se falla una nota)
    if not os.path.isdir(carpeta):
        print("AVISO: no se encontro la carpeta", carpeta, "- no habra sonido al fallar")
        return []
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
    except pygame.error as e:
        print("AVISO: no se pudo iniciar el audio:", e)
        return []
    sonidos = []
    for archivo in sorted(os.listdir(carpeta), key=orden_natural):
        nombre, ext = os.path.splitext(archivo)
        if nombre.lower().startswith("miss") and ext.lower() in EXT_AUDIO:
            try:
                sonidos.append(pygame.mixer.Sound(os.path.join(carpeta, archivo)))
            except pygame.error as e:
                print("AVISO: no se pudo cargar", archivo, "->", e)
    if not sonidos:
        print("AVISO: no hay archivos Miss*.mp3 en", carpeta)
    return sonidos

def cargar_assets():
    global assets_cargados, notecol, background, fret, spkr, spkr_h, spkr_s, open_note
    global HN, PO, TN, LN, notes, STAR_NOTES, longNotePos, overlay_power, SONIDOS_FALLO
    global fuente_puntaje, fuente_mult, fuente_chica, fuente_pausa, fuente_pausa_op
    if assets_cargados:
        return

    assets = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Assets")

    notecol = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Calculamos la inclinación interpolando los puntos de HIGHWAY_POLY
    y_top = HIGHWAY_POLY[0][1]
    y_bot = HIGHWAY_POLY[2][1]
    
    def get_x(y, x_t, x_b):
        return x_t + (x_b - x_t) * (y - y_top) / (y_bot - y_top)
    
    # Coordenadas X para la altura de VENTANA_MIN (arriba de la zona de golpe)
    x_tl = get_x(VENTANA_MIN, HIGHWAY_POLY[0][0], HIGHWAY_POLY[3][0])
    x_tr = get_x(VENTANA_MIN, HIGHWAY_POLY[1][0], HIGHWAY_POLY[2][0])
    
    # Coordenadas X para la altura de VENTANA_MAX (abajo de la zona de golpe)
    x_bl = get_x(VENTANA_MAX, HIGHWAY_POLY[0][0], HIGHWAY_POLY[3][0])
    x_br = get_x(VENTANA_MAX, HIGHWAY_POLY[1][0], HIGHWAY_POLY[2][0])
    
    poly_notecol = [(x_tl, VENTANA_MIN), (x_tr, VENTANA_MIN), (x_br, VENTANA_MAX), (x_bl, VENTANA_MAX)]
    
    # Dibujamos la figura translúcida en la superficie
    pygame.draw.polygon(notecol, (255, 255, 255, 100), poly_notecol)

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
    spkr = {}
    for img in os.listdir(spkr_path):
        spkr[img[0]] = pygame.image.load(os.path.join(spkr_path,img)).convert_alpha()

    # Creacion de un diccionario con los altavoces cuando los presionas
    spkrh_path = os.path.join(key_assets,"Hit") # guarda la ruta de los assets
    spkr_h = {}
    for img in os.listdir(spkrh_path):
        spkr_h[img[0]] = pygame.image.load(os.path.join(spkrh_path,img)).convert_alpha()

    # Creacion de un diccionario con los altavoces cuando los presionas junto a la strumbar
    spkrs_path = os.path.join(key_assets,"HitStrum") # guarda la ruta de los assets
    spkr_s = {}
    for img in os.listdir(spkrs_path):
        spkr_s[img[0]] = pygame.image.load(os.path.join(spkrs_path,img)).convert_alpha()

    # Ruta de las notas
    note_assets = os.path.join(assets, "Notes")

    # Creacion de la nota open
    open_note = pygame.image.load(os.path.join(note_assets,"Open.png")).convert_alpha()

    # Creacion de un diccionario con los assets de las notas Hammer on
    hamon_path = os.path.join(note_assets, "Hammer-on")
    HN = {} # Este diccionario guarda todas las notas normales
    for img in os.listdir(hamon_path):
        HN[img[:-4]] = pygame.image.load(os.path.join(hamon_path,img)).convert_alpha()

    # Creacion de un diccionario con los assets de las notas Pull off
    pulloff_path = os.path.join(note_assets, "Pull-off")
    PO = {} # Este diccionario guarda las notas iluminadas
    for img in os.listdir(pulloff_path):
        PO[img[:-4]] = pygame.image.load(os.path.join(pulloff_path,img)).convert_alpha()

    # Creacion de un diccionario con los assets de las notas Tap
    tap_path = os.path.join(note_assets, "Tap")
    TN = {} # Este diccionario guarda las notas transparentes
    for img in os.listdir(tap_path):
        TN[img[:-4]] = pygame.image.load(os.path.join(tap_path,img)).convert_alpha()

    long_path = os.path.join(note_assets, "Long")
    LN = {} # Este diccionario guarda las notas largas
    for img in os.listdir(long_path):
        LN[img[:-4]] = pygame.image.load(os.path.join(long_path,img)).convert_alpha()

    notes = {"hammer":HN,
             "pull":PO,
             "tap":TN}

    # Notas Star (animacion de rotacion): Assets/Notes/Star o Assets/Star
    STAR_NOTES = cargar_star([os.path.join(note_assets, "Star"), os.path.join(assets, "Star")])

    SONIDOS_FALLO = cargar_sonidos_fallo(os.path.join(assets, "SoundEffects"))

    longNotePos = {
        "Green":(380,435),
        "Red":(457,435),
        "Yellow":(530,435),
        "Blue":(605,435),
        "Orange":(680,435),
        "Open":(width/2 - background.get_width()/2,height - background.get_height())
    }

    # Capa azul que se dibuja sobre el camino mientras el Hero Power esta activo
    overlay_power = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.polygon(overlay_power, COLOR_POWER + (255,), HIGHWAY_POLY)

    fuente_puntaje = pygame.font.SysFont(None, 72)
    fuente_mult = pygame.font.SysFont(None, 64)
    fuente_chica = pygame.font.SysFont(None, 30)
    fuente_pausa = pygame.font.SysFont(None, 130)
    fuente_pausa_op = pygame.font.SysFont(None, 64)

    assets_cargados = True


# ===========================================================================
#  NOTAS
# ===========================================================================
class long:
    def __init__(self, surf, pos, span, TYPE, row, bpm_nota=None):
        self.spd = (bpm if bpm_nota is None else bpm_nota)/60
        if row != 7:
            self.add = 0.1
        else:
            self.add = 0.005
        self.pos = pos
        self.surf = surf
        self.end = ahora_juego() + span
        self.type = TYPE
        self.lcut = 20
        self.cuty = 0

    def move(self, missed, pressed):
        self.start = ahora_juego()
        
        if self.start <= self.end:
            if self.lcut <= 430:
                self.lcut += 8*self.spd
        elif self.start >= self.end:
            self.cuty += 8*self.spd
            self.pos = (self.pos[0], self.pos[1]+8*self.spd)
            if self.pos[1] + self.lcut <= 800:
                self.lcut += 8*self.add
                
        # 1. Frenar la aceleración si ya acertamos la nota o la dejamos pasar
        if not pressed and not missed:
            self.add += 0.005*self.spd
            self.spd += 0.005

        # 2. Cortar la nota para que no pase la línea de los altavoces
        if pressed and not missed and tecla_sostenida(self.type):
            limite_y = 800  # Altura central de los altavoces
            fondo_nota = self.pos[1] + self.lcut
            if fondo_nota > limite_y:
                self.lcut -= (fondo_nota - limite_y)

        # 3. Dibujarla solo si todavía queda parte visible (evita errores de Pygame)
        if self.lcut > 0:
            cut = pygame.Rect(0, int(self.cuty), self.surf.get_width(), int(self.lcut))
            window.blit(self.surf, self.pos, cut)

class Note_Class:
    def __init__(self, note, row, span, special, star_id=None, star=False, bpm_nota=None, fin_ms=None):
        if bpm_nota is None:
            bpm_nota = bpm
        self.spd = bpm_nota/60              # velocidad inicial de ESTA nota (depende del BPM de la cancion)
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
        TYPE = notes[specialTemp]
        if row != 7:
            self.surf = TYPE[self.type]
        else:
            self.surf = open_note
        self.middle = self.surf.get_height() / 2
        if span != 0 and self.row != 7:
            self.lsurf = LN[self.type]
            self.long = long(self.lsurf,longNotePos[self.type],span,self.type,self.row,bpm_nota)
        elif span != 0 and self.row == 7:
            self.lsurf = LN[self.type]
            self.long = long(self.lsurf,longNotePos[self.type],span,self.type,self.row,bpm_nota)
        # ventana de golpe de esta nota: si va mas rapida, la ventana (en pixeles) se agranda para durar lo mismo en ms
        escala = min(max(self.spd, 1.0), VENTANA_ESCALA_MAX)
        centro = (VENTANA_MIN + VENTANA_MAX) / 2
        mitad = (VENTANA_MAX - VENTANA_MIN) / 2 * escala
        self.v_min = centro - mitad
        self.v_max = centro + mitad
        self.fin_ms = fin_ms        # ms de cancion en que termina la nota larga (start_ms + duracion)
        self.t_sustain = None       # hasta que ms de cancion ya se puntuo el sustain (None = todavia no se acerto la cabeza)
        self.pressed = False
        self.missed = False         # (visual) la nota ya paso de largo, lo usa la nota larga
        self.fallada = False        # ya se registro como fallo en el puntaje
        # --- Star ---
        self.star_id = star_id      # frase Star a la que pertenece (None si no es de ninguna)
        self.star = star            # True mientras se dibuja como nota Star
        self.frames = STAR_NOTES.get(self.type)
        self.edad = 0               # cuadros desde que aparecio (para la animacion de rotacion)

    def superficie(self):           # la imagen que toca dibujar ahora
        if self.star and self.frames:
            return self.frames[(self.edad * STAR_ANIM_FPS // FPS) % len(self.frames)]
        return self.surf

    def update(self):
        if self.pos[1] != 900:
            base = self.superficie()
            note = pygame.transform.scale(base, (int(base.get_width()*self.add), int(base.get_height()*self.add)))
            self.middle = note.get_height() / 2
            if self.span != 0:
                self.long.move(self.missed, self.pressed)
            if not self.pressed and not self.missed:
                if self.row != 7:
                    self.pos = (self.pos[0]+posChangeList[self.row]*self.spd,self.pos[1]+8*self.spd)
                    self.add += 0.005*self.spd
                    self.spd += 0.005
                elif self.row == 7:
                    self.pos = (self.pos[0]+posChangeList[self.row-2]*self.spd,self.pos[1]+8*self.spd)
                    self.add += 0.022*self.spd
                    self.spd += 0.005
                self.edad += 1
                window.blit(note,self.pos)


# ===========================================================================
#  DIBUJO
# ===========================================================================
def draw_background():
    if fondo_cancion is not None:
        window.blit(fondo_cancion, (0, 0))      # fondo custom de la cancion
    else:
        window.fill("black") # CONVIERTE EL FONDO EN NEGRO

    window.blit(notecol, (0, 0))

    pos_def = (width/2 - background.get_width()/2,height - background.get_height())

    if len(frets) != 0:
        for surf in frets[:]:
            if surf.pos[1] >= 900:
                frets.remove(surf)
            else:
                surf.update()

    window.blit(background,pos_def)

    if hero is not None and hero.activo:       # camino azul pulsante mientras el Hero Power esta activo
        overlay_power.set_alpha(int(70 + 30 * math.sin(pygame.time.get_ticks() / 150)))
        window.blit(overlay_power, (0, 0))

def draw_speakers():
    pos_def = (width/2 - background.get_width()/2,height - background.get_height())

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
    for i in lista:
        if i.pos[1] < 900:
            i.update()

def draw_hud():
    ahora = pygame.time.get_ticks()
    mult = marcador.multiplicador(hero.activo)

    # puntaje (con puntos de mil: 1.234.500), multiplicador y racha
    txt = fuente_puntaje.render(f"{marcador.puntaje:,}".replace(",", "."), True, (255, 255, 255))
    window.blit(txt, (HUD_DERECHA - txt.get_width(), 30))
    if hero.activo:
        color_mult = COLOR_POWER
    elif mult > 1:
        color_mult = (255, 215, 60)
    else:
        color_mult = (255, 255, 255)
    txt = fuente_mult.render("x" + str(mult), True, color_mult)
    window.blit(txt, (HUD_DERECHA - txt.get_width(), 100))
    txt = fuente_chica.render("Racha " + str(marcador.racha), True, (220, 220, 220))
    window.blit(txt, (HUD_DERECHA - txt.get_width(), 160))

    # barra de Hero Power
    barra = pygame.Rect(HUD_BARRA_X, 260, 40, 480)
    pygame.draw.rect(window, (25, 25, 35), barra, border_radius=8)
    alto = int(barra.height * hero.energia)
    if alto > 0:
        if hero.activo:
            color = COLOR_POWER
        elif hero.energia >= MINIMO_PARA_ACTIVAR:
            color = (80, 160, 255)
        else:
            color = (120, 120, 140)
        pygame.draw.rect(window, color, (barra.x, barra.bottom - alto, barra.width, alto), border_radius=8)
    parpadeo = hero.puede_activar() and (ahora // 300) % 2 == 0
    pygame.draw.rect(window, COLOR_POWER if (hero.activo or parpadeo) else (255, 255, 255), barra, 3, border_radius=8)
    pygame.draw.line(window, (255, 255, 255), (barra.x - 8, barra.centery), (barra.right + 8, barra.centery), 2)   # marca del 50%
    txt = fuente_chica.render("HERO POWER", True, COLOR_POWER if hero.activo else (255, 255, 255))
    window.blit(txt, (barra.centerx - txt.get_width() / 2, barra.y - 34))
    if hero.puede_activar():
        txt = fuente_chica.render("[" + pygame.key.name(TECLAS_STAR_POWER[0]).upper() + "]", True, COLOR_POWER if parpadeo else (255, 255, 255))
        window.blit(txt, (barra.centerx - txt.get_width() / 2, barra.bottom + 12))

    if ahora_juego() < toast_hasta:            # aviso cuando se completa una frase Star
        txt = fuente_chica.render(toast_texto, True, (255, 230, 120))
        window.blit(txt, (barra.centerx - txt.get_width() / 2, barra.y - 64))


# ===========================================================================
#  AUDIO (opcional: si la carpeta no tiene audio, se juega en silencio)
# ===========================================================================
EXT_AUDIO = (".opus", ".ogg", ".mp3", ".wav", ".flac")
EXT_VIDEO = (".mp4", ".avi", ".webm", ".mov", ".mkv", ".ogv")

def buscar_fondo(carpeta):
    # Busca background.png/jpg/... (o fondo.*) dentro de la carpeta de la cancion
    try:
        archivos = sorted(os.listdir(carpeta))
    except OSError:
        return None
    for archivo in archivos:
        nombre, ext = os.path.splitext(archivo)
        if nombre.lower() in NOMBRES_FONDO and ext.lower() in EXT_IMAGEN:
            return os.path.join(carpeta, archivo)
    for archivo in archivos:
        nombre, ext = os.path.splitext(archivo)
        if nombre.lower() in NOMBRES_FONDO and ext.lower() in EXT_VIDEO:
            print("AVISO: el fondo de esta cancion es un video (" + archivo + ") y pygame no lo puede mostrar: se usa el fondo normal")
    return None

def preparar_fondo(carpeta):
    # Devuelve el fondo custom ya escalado a la ventana (llenandola, recortando lo que sobre) y oscurecido, o None si la cancion no trae uno
    ruta = buscar_fondo(carpeta)
    if ruta is None:
        return None
    try:
        imagen = pygame.image.load(ruta).convert_alpha()
        ancho, alto = imagen.get_size()
        escala = max(width / ancho, height / alto)
        nuevo = (max(1, int(ancho * escala)), max(1, int(alto * escala)))
        imagen = pygame.transform.smoothscale(imagen, nuevo)
        fondo = pygame.Surface((width, height))
        fondo.blit(imagen, ((width - nuevo[0]) // 2, (height - nuevo[1]) // 2))
        sombra = pygame.Surface((width, height))
        sombra.set_alpha(FONDO_OSCURECER)
        sombra.fill((0, 0, 0))
        fondo.blit(sombra, (0, 0))
        return fondo.convert()
    except pygame.error as e:
        print("AVISO: no se pudo cargar el fondo", ruta, "->", e)
        return None

def buscar_audios(carpeta):        # todos los audios de la carpeta (song, guitar, ...). "song" va primero
    audios = []
    try:
        archivos = os.listdir(carpeta)
    except OSError:
        return audios
    for archivo in archivos:
        nombre, ext = os.path.splitext(archivo)
        if ext.lower() in EXT_AUDIO and nombre.lower() != "preview":
            audios.append((nombre.lower(), os.path.join(carpeta, archivo)))
    audios.sort(key=lambda a: (a[0] != "song", a[0]))
    return audios

def preparar_audio(carpeta, volumen):
    audios = buscar_audios(carpeta)
    if not audios:
        print("AVISO: no hay archivos de audio en", carpeta, "- se juega sin musica")
        return None
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
    except pygame.error as e:
        print("AVISO: no se pudo iniciar el audio:", e)
        return None
    pygame.mixer.set_num_channels(max(8, len(audios) + 2))
    audio = {"musica": False, "sonidos": []}
    for nombre, ruta in audios:
        try:
            if not audio["musica"]:                 # la primera pista va por mixer.music, las demas como Sound
                pygame.mixer.music.load(ruta)
                pygame.mixer.music.set_volume(volumen)
                audio["musica"] = True
            else:
                sonido = pygame.mixer.Sound(ruta)
                sonido.set_volume(volumen)
                audio["sonidos"].append(sonido)
        except pygame.error as e:
            print("AVISO: no se pudo cargar", ruta, "->", e)
    return audio

def reproducir_audio(audio):
    if audio is None:
        return
    if audio["musica"]:
        pygame.mixer.music.play()
    for sonido in audio["sonidos"]:
        sonido.play()

def aplicar_volumen_audio(audio, volumen):
    if audio is None:
        return
    if audio["musica"]:
        pygame.mixer.music.set_volume(volumen)
    for sonido in audio["sonidos"]:
        sonido.set_volume(volumen)

def pausar_audio(audio):
    if audio is None:
        return
    if audio["musica"]:
        pygame.mixer.music.pause()
    pygame.mixer.pause()            # pausa tambien las demas pistas (los Sound)

def reanudar_audio(audio):
    if audio is None:
        return
    if audio["musica"]:
        pygame.mixer.music.unpause()
    pygame.mixer.unpause()

def detener_audio(audio):
    if audio is None:
        return
    if audio["musica"]:
        pygame.mixer.music.stop()
        try:
            pygame.mixer.music.unload()
        except (AttributeError, pygame.error):
            pass
    for sonido in audio["sonidos"]:
        sonido.stop()


# ===========================================================================
#  LOGICA DE LA PARTIDA
# ===========================================================================
def preparar_eventos(parse):
    # Agrupa las notas que tienen el mismo start_ms (acordes) en un solo evento.
    # Cada nota queda como: lane, dur (sustain en ms), tipo (0 normal / 1 HOPO / 2 tap) y star_id.
    grupos = {}
    for n in parse:
        if n['type'] == 'N':
            grupos.setdefault(n['start_ms'], []).append(n)
    eventos = []
    for ms in sorted(grupos):
        lista = []
        for n in grupos[ms]:
            tipo = 2 if n.get('tap') else (1 if n.get('hopo') else 0)
            lista.append({'lane': int(n['lane']), 'dur': int(n['duration_ms']), 'tipo': tipo, 'star_id': n.get('star_id')})
        eventos.append({'ms': ms, 'notas': lista})
    return eventos

def bpm_visual(bpm_cancion):
    # BPM de la cancion -> velocidad visual de las notas
    return max(BPM_VISUAL_MIN, min(BPM_VISUAL_MAX, bpm_cancion * FACTOR_BPM))

def calcular_viaje_ms(bpm_valor, abierta=False):
    # Cuanto tarda una nota, que sale con ese bpm, en ir desde que aparece hasta el centro de la ventana de golpe.
    # Se simula el mismo movimiento que hace Note_Class.update(), asi la musica queda alineada con las notas.
    # La nota Open tiene otra fisica (otro tamano inicial, otra altura de salida y crece mas rapido), por eso va aparte.
    clave = (round(bpm_valor, 3), abierta)
    if clave in viaje_cache:
        return viaje_cache[clave]
    if abierta:
        base, y, add, crecimiento = open_note, startNotePos["Open"][1], 0.48, 0.022
    else:
        base = HN["Green"] if "Green" in HN else next(iter(HN.values()))
        y, add, crecimiento = startNotePos["Green"][1], 0.1, 0.005
    alto = base.get_height()
    spd = bpm_valor / 60
    objetivo = (VENTANA_MIN + VENTANA_MAX) / 2
    frames = 0
    while frames < 600:
        medio = int(alto * add) / 2
        y += 8 * spd
        add += crecimiento * spd
        spd += 0.005
        frames += 1
        if y + medio >= objetivo:
            break
    viaje_cache[clave] = frames * 1000 / FPS
    return viaje_cache[clave]

def aplicar_velocidad(eventos, orden_spawn, desde, t):
    # Se llama despues de cambiar FACTOR_BPM en la pausa. Las notas que ya estan en pantalla siguen como estaban;
    # a las que todavia no salieron se les recalcula la velocidad y el momento en que aparecen.
    # Si con la velocidad nueva ya no llegarian a tiempo (por ejemplo, al bajar la velocidad una nota que sale
    # en un instante), conservan la velocidad anterior para no desincronizarse.
    for i in orden_spawn[desde:]:
        ev = eventos[i]
        nuevo_bpm = bpm_visual(ev['bpm_real'])
        nuevo_spawn = ev['ms'] - calcular_viaje_ms(nuevo_bpm, any(n['lane'] == 7 for n in ev['notas']))
        if nuevo_spawn >= t:
            ev['bpm'] = nuevo_bpm
            ev['spawn_ms'] = nuevo_spawn
    orden_spawn[desde:] = sorted(orden_spawn[desde:], key=lambda i: eventos[i]['spawn_ms'])

def mostrar_toast(texto, ms=1500):
    global toast_texto, toast_hasta
    toast_texto = texto
    toast_hasta = ahora_juego() + ms

def sonar_fallo():
    # Un sonido Miss al azar (distinto al ultimo), con una separacion minima para que no se amontonen
    global ultimo_fallo_ms, ultimo_sonido_fallo
    if not SONIDOS_FALLO:
        return
    ahora = pygame.time.get_ticks()
    if ahora - ultimo_fallo_ms < MISS_COOLDOWN_MS:
        return
    candidatos = [sn for sn in SONIDOS_FALLO if sn is not ultimo_sonido_fallo] or SONIDOS_FALLO
    sonido = random.choice(candidatos)
    sonido.set_volume(volumen_actual)
    sonido.play()
    ultimo_fallo_ms = ahora
    ultimo_sonido_fallo = sonido

def golpear(n):                     # una nota se acerto
    n.pressed = True
    if n.span != 0 and n.fin_ms is not None:        # nota larga: el sustain empieza a puntuar desde su inicio (o desde ahora si se acerto tarde)
        n.t_sustain = max(tiempo_cancion, n.fin_ms - n.span)
    marcador.acierto(hero.activo)
    if n.star_id is not None and hero.nota_acertada(n.star_id):
        mostrar_toast("HERO POWER +25%")

def fallar(n):                      # una nota se paso sin tocarse
    n.fallada = True
    marcador.fallo()
    sonar_fallo()
    if n.star_id is not None and hero.nota_fallada(n.star_id):
        for otra in drawable_notes:                 # al perder la frase, las notas que quedan dejan de ser Star
            if otra.star_id == n.star_id:
                otra.star = False

def puntuar_sustains(t, bpm_cancion):
    # Suma puntos por cada nota larga acertada que se esta manteniendo apretada.
    # Si se suelta, deja de sumar (y el tiempo que estuvo suelta no se recupera); no afecta la racha.
    for n in drawable_notes:
        if n.span == 0 or not n.pressed or n.t_sustain is None:
            continue
        hasta = min(t, n.fin_ms)
        if hasta > n.t_sustain:
            if tecla_sostenida(n.type):
                marcador.sustain((hasta - n.t_sustain) * bpm_cancion / 60000.0, hero.activo)
            n.t_sustain = hasta

def procesar_golpes():
    global space_pressed
    
    # 1. Recolectar todas las notas candidatas a ser golpeadas en este frame
    notas_a_golpear = []
    for press in n_pressed:
        estado = n_pressed[press]
        if estado == "normal":
            for n in drawable_notes:
                if not n.pressed and not n.fallada and n.type == press:
                    if n.v_min <= n.pos[1] + n.middle <= n.v_max:
                        notas_a_golpear.append(n)
        elif estado == "light":
            for n in drawable_notes:
                if not n.pressed and not n.fallada and n.type == press and n.special != 0:
                    if n.v_min <= n.pos[1] + n.middle <= n.v_max:
                        notas_a_golpear.append(n)

    # 2. Si hay notas para golpear, filtrar y golpear solo las del mismo start_ms
    if notas_a_golpear:
        # El start_ms de una nota es exactamente (fin_ms - span)
        primer_start_ms = min(n.fin_ms - n.span for n in notas_a_golpear)
        
        for n in notas_a_golpear:
            if n.fin_ms - n.span == primer_start_ms:
                golpear(n)
                n_pressed["Open"] = "none"
                space_pressed = False

    # 3. Limpiar los inputs
    for press in n_pressed:
        n_pressed[press] = "none"

def actualizar_notas():
    for n in drawable_notes[:]:
        if not n.pressed and not n.fallada and n.pos[1] + n.middle > n.v_max:
            fallar(n)
        if n.span != 0:
            if n.long.pos[1] >= 800:
                drawable_notes.remove(n)
            if n.pos[1] >= 800:
                n.missed = True
        else:
            if n.pressed or n.pos[1] >= 800:
                drawable_notes.remove(n)

def cuenta_regresiva(foto, sombra, clock):
    # Cuenta 3, 2, 1 sobre la imagen congelada antes de reanudar. Devuelve "cerrar" si cierran la ventana.
    inicio = pygame.time.get_ticks()
    total = CUENTA_REGRESIVA_PAUSA * 1000
    while True:
        transcurrido = pygame.time.get_ticks() - inicio
        if transcurrido >= total:
            return None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "cerrar"
        window.blit(foto, (0, 0))
        window.blit(sombra, (0, 0))
        txt = fuente_pausa.render(str(CUENTA_REGRESIVA_PAUSA - transcurrido // 1000), True, (255, 255, 255))
        window.blit(txt, (width / 2 - txt.get_width() / 2, height / 2 - txt.get_height() / 2))
        pygame.display.update()
        clock.tick(30)

def pausar(clock, audio):
    # Pausa la partida: congela la musica y el reloj de la cancion y muestra el menu de pausa
    # (Continuar / Opciones / Salir al menu). En Opciones se ajusta el volumen, la velocidad de las notas
    # y el modo gamepad. Devuelve None si hay que seguir jugando, "salir" (volver al menu) o "cerrar" (cerraron la ventana).
    global pausa_total, FACTOR_BPM, gamepad_mode, volumen_actual
    inicio = pygame.time.get_ticks()
    pausar_audio(audio)
    pygame.key.set_repeat(350, 80)              # en los menus, mantener una flecha repite
    foto = window.copy()                        # la ultima imagen de la partida queda de fondo
    sombra = pygame.Surface((width, height))
    sombra.set_alpha(170)
    sombra.fill((0, 0, 0))

    def filas_de(pantalla):
        if pantalla == "pausa":
            # Añadimos "Reiniciar Canción" como segunda opción
            return "PAUSA", ["Continuar", "Reiniciar Canción", "Opciones", "Salir al menú"]
        return "OPCIONES", ["Volumen: " + str(round(volumen_actual * 100)) + "%",
                            "Velocidad de notas: " + str(round(FACTOR_BPM * 100)) + "%",
                            "Modo gamepad: " + ("Sí" if gamepad_mode else "No"),
                            "Volver"]

    pantalla = "pausa"
    sel = 0
    decision = None
    while decision is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                decision = "cerrar"
            elif event.type == pygame.KEYDOWN:
                tecla = event.key
                cantidad = len(filas_de(pantalla)[1])
                if tecla == pygame.K_ESCAPE:
                    if pantalla == "opciones":                  # ESC en Opciones = volver a la pausa
                        pantalla, sel = "pausa", 1
                    else:                                       # ESC en la pausa = continuar
                        decision = "continuar"
                elif tecla in (pygame.K_UP, pygame.K_w):
                    sel = (sel - 1) % cantidad
                elif tecla in (pygame.K_DOWN, pygame.K_s):
                    sel = (sel + 1) % cantidad
                elif pantalla == "opciones" and tecla in (pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d):
                    paso = -1 if tecla in (pygame.K_LEFT, pygame.K_a) else 1
                    if sel == 0:
                        volumen_actual = max(0.0, min(1.0, round(volumen_actual + 0.05 * paso, 2)))
                        aplicar_volumen_audio(audio, volumen_actual)
                    elif sel == 1:
                        FACTOR_BPM = max(FACTOR_BPM_MIN, min(FACTOR_BPM_MAX, round(FACTOR_BPM + 0.05 * paso, 2)))
                    elif sel == 2:
                        gamepad_mode = not gamepad_mode
                elif tecla in (pygame.K_RETURN, pygame.K_SPACE):
                    if pantalla == "pausa":
                        if sel == 0:
                            decision = "continuar"
                        elif sel == 1:
                            decision = "reiniciar" # <- NUEVA DECISIÓN
                        elif sel == 2:
                            pantalla, sel = "opciones", 0
                        else:
                            decision = "salir"
                    elif sel == 2:
                        gamepad_mode = not gamepad_mode
                    elif sel == 3:
                        pantalla, sel = "pausa", 1
        titulo_txt, filas = filas_de(pantalla)
        window.blit(foto, (0, 0))
        window.blit(sombra, (0, 0))
        titulo = fuente_pausa.render(titulo_txt, True, (255, 255, 255))
        window.blit(titulo, (width / 2 - titulo.get_width() / 2, 200))
        for i, texto in enumerate(filas):
            caja = pygame.Rect(width / 2 - 380, 400 + i * 85, 760, 70)
            if i == sel:
                pygame.draw.rect(window, (200, 110, 0), caja, border_radius=12)
            pygame.draw.rect(window, (255, 255, 255), caja, 3, border_radius=12)
            txt = fuente_pausa_op.render(texto, True, (255, 255, 255))
            window.blit(txt, (caja.centerx - txt.get_width() / 2, caja.centery - txt.get_height() / 2))
        if pantalla == "opciones":
            ayuda = fuente_chica.render("Izquierda / Derecha para cambiar   -   ESC para volver", True, (210, 210, 210))
            window.blit(ayuda, (width / 2 - ayuda.get_width() / 2, 400 + len(filas) * 85 + 10))
        pygame.display.update()
        clock.tick(30)
    pygame.key.set_repeat()                     # en la partida la repeticion de teclas no sirve
    if decision == "continuar" and CUENTA_REGRESIVA_PAUSA > 0:
        if cuenta_regresiva(foto, sombra, clock) == "cerrar":
            decision = "cerrar"
    if decision == "continuar":
        reanudar_audio(audio)
    pausa_total += pygame.time.get_ticks() - inicio     # todo este rato NO cuenta para la cancion
    return None if decision == "continuar" else decision

def pantalla_resultados(resultado, clock):
    # Pantalla final: puntaje, precision y mejor racha. Devuelve "cerrar" si se cerro la ventana.
    f_grande = pygame.font.SysFont(None, 110)
    f_media = pygame.font.SysFont(None, 56)
    f_chica = pygame.font.SysFont(None, 36)
    lineas = [("Puntaje", f"{resultado['puntaje']:,}".replace(",", ".")),
              ("Notas acertadas", f"{resultado['aciertos']} / {resultado['aciertos'] + resultado['fallos']}"),
              ("Precision", f"{resultado['precision']:.1f}%"),
              ("Mejor racha", str(resultado['mejor_racha']))]
    inicio = pygame.time.get_ticks()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "cerrar"
            if event.type == pygame.KEYDOWN and pygame.time.get_ticks() - inicio > 1200:   # espera un poco para no saltarse la pantalla por accidente
                if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                    return None
        window.fill((12, 12, 18))
        titulo = f_grande.render("CANCION COMPLETADA", True, (255, 255, 255))
        window.blit(titulo, (width / 2 - titulo.get_width() / 2, 150))
        y = 340
        for nombre, valor in lineas:
            a = f_media.render(nombre, True, (160, 205, 230))
            b = f_media.render(valor, True, (255, 255, 255))
            window.blit(a, (width / 2 - 330, y))
            window.blit(b, (width / 2 + 330 - b.get_width(), y))
            y += 80
        pie = f_chica.render("Enter para volver", True, (200, 200, 200))
        window.blit(pie, (width / 2 - pie.get_width() / 2, 780))
        pygame.display.update()
        clock.tick(30)


def jugar(carpeta, nivel="expert", gamepad=False, volumen=0.5, con_audio=True):
    global window, gamepad_mode, space_pressed, current_fret, o_time, bpm, pausa_total, volumen_actual
    global tiempo_cancion, fondo_cancion, ultimo_fallo_ms, ultimo_sonido_fallo
    global drawable_notes, frets, marcador, hero, toast_hasta

    window = pygame.display.get_surface()
    if window is None:
        window = pygame.display.set_mode((width, height))
    cargar_assets()

    # --- cargar la cancion ---
    ruta_notas = LectorDeCancionesMIDI.buscarArchivoNotas(carpeta)
    if ruta_notas is None:
        return None
    cargada = LectorDeCancionesMIDI.cargarCancionCompleta(ruta_notas, nivel)
    if cargada is None:
        return None
    parse, time_map, _ = cargada
    eventos = preparar_eventos(parse[list(parse.keys())[0]])
    if not eventos:
        return None

    tiempos_bpm = [e["MS"] for e in time_map]
    def bpm_en(ms):                 
        return time_map[max(0, bisect.bisect_right(tiempos_bpm, ms) - 1)]["bpm"]

    for ev in eventos:
        ev['bpm_real'] = bpm_en(ev['ms'])           
        ev['bpm'] = bpm_visual(ev['bpm_real'])
        ev['spawn_ms'] = ev['ms'] - calcular_viaje_ms(ev['bpm'], any(n['lane'] == 7 for n in ev['notas']))
    orden_spawn = sorted(range(len(eventos)), key=lambda i: eventos[i]['spawn_ms'])

    notas_por_frase = {}
    for ev in eventos:
        for nota in ev['notas']:
            if nota['star_id'] is not None:
                notas_por_frase[nota['star_id']] = notas_por_frase.get(nota['star_id'], 0) + 1

    # ENVOLVEMOS EL JUEGO EN UN LOOP PARA PODER REINICIAR
    while True:
        # --- estado de la partida ---
        marcador = Marcador()
        hero = HeroPower(notas_por_frase)
        drawable_notes = []
        frets = []
        gamepad_mode = gamepad
        space_pressed = False
        current_fret = 2
        toast_hasta = 0
        pausa_total = 0
        volumen_actual = volumen
        tiempo_cancion = 0
        ultimo_fallo_ms = -10000
        ultimo_sonido_fallo = None
        fondo_cancion = preparar_fondo(carpeta)         
        bpm = bpm_visual(bpm_en(0))
        for d in (n_pressed, n_held):
            for k in d:
                d[k] = "none"

        clock = pygame.time.Clock()
        pygame.key.set_repeat()         
        audio = preparar_audio(carpeta, volumen) if con_audio else None

        t0 = pygame.time.get_ticks()
        o_time = t0
        NoteNum = 0
        audio_sonando = False
        fin_hasta = None
        motivo = None                   

        try:
            while motivo is None:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        motivo = "cerrar"
                    elif event.type == pygame.KEYUP:
                        keys = pygame.key.get_pressed()
                        for key in keys_dict:
                            if not keys[key]:
                                n_pressed[keys_dict[key]] = "none"
                                n_held[keys_dict[key]] = "none"
                        if event.key == pygame.K_SPACE:
                            space_pressed = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            factor_antes = FACTOR_BPM
                            motivo = pausar(clock, audio)
                            
                            if motivo == "reiniciar":
                                break # Rompe el for loop
                                
                            if motivo is None:          
                                if FACTOR_BPM != factor_antes:      
                                    aplicar_velocidad(eventos, orden_spawn, NoteNum, ahora_juego() - t0 - PRE_ROLL_MS)
                                keys = pygame.key.get_pressed()
                                for key in keys_dict:
                                    n_pressed[keys_dict[key]] = "none"
                                    if not keys[key]:
                                        n_held[keys_dict[key]] = "none"
                                if not keys[pygame.K_SPACE]:
                                    space_pressed = False
                        elif event.key in TECLAS_STAR_POWER:
                            hero.activar()
                        elif event.key == pygame.K_SPACE:
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
                            keys = pygame.key.get_pressed()
                            
                            # AQUÍ OCURRE LA MAGIA PARA ACORDES (Toma la nueva tecla Y las mantenidas)
                            if space_pressed or gamepad_mode:
                                for code, name in keys_dict.items():
                                    if name != pygame.K_SPACE and keys[code]:
                                        n_pressed[name] = "normal"
                                        n_held[name] = "normal"
                                n_pressed[pressed] = "normal"
                                n_held[pressed] = "normal"
                            else:
                                for code, name in keys_dict.items():
                                    if name != pygame.K_SPACE and keys[code]:
                                        n_pressed[name] = "light"
                                        n_held[name] = "light"
                                n_pressed[pressed] = "light"
                                n_held[pressed] = "light"
                        if event.key == pygame.K_p:
                            gamepad_mode = not gamepad_mode
                if motivo is not None:
                    break

                ahora = ahora_juego()                   # reloj de la partida (no avanza durante la pausa)
                t = ahora - t0 - PRE_ROLL_MS            # ms de cancion (negativo mientras espera que   arranque la musica)
                tiempo_cancion = t
                bpm = bpm_visual(bpm_en(max(t, 0)))     # el bpm sigue al archivo de la cancion (lo usan    los trastes y las notas nuevas)

                if not audio_sonando and t >= OFFSET_AUDIO_MS:
                    audio_sonando = True
                    reproducir_audio(audio)

                if ahora - o_time >= 0:
                    o_time = ahora + FRET_INTERVALO_BASE_MS * 60 / bpm      # a mas bpm los trastes salen   mas seguido (misma separacion en pantalla)
                    if current_fret != 3:
                        current_fret += 1
                    else:
                        current_fret = 0
                    frets.insert(0, Fret(fret[current_fret], bpm))

                # --- aparecen las notas que ya les toca (llegan a la ventana justo en su start_ms) ---
                while NoteNum < len(orden_spawn) and t >= eventos[orden_spawn[NoteNum]]['spawn_ms']:
                    ev = eventos[orden_spawn[NoteNum]]
                    for nota in ev['notas']:
                        es_star = nota['star_id'] is not None and not hero.frase_perdida(nota['star_id'])
                        drawable_notes.append(Note_Class(None, nota['lane'], nota['dur'], nota['tipo'], nota    ['star_id'], es_star, ev['bpm'], ev['ms'] + nota['dur']))
                    NoteNum += 1

                hero.actualizar(clock.get_time(), bpm_en(max(t, 0)))

                draw_background()
                procesar_golpes()
                puntuar_sustains(t, bpm_en(max(t, 0)))
                actualizar_notas()
                draw_notes(drawable_notes)
                draw_speakers()
                draw_hud()

                # --- fin de la cancion: se mostraron todas las notas y ya no queda ninguna en pantalla ---
                if NoteNum >= len(eventos) and not drawable_notes:
                    if fin_hasta is None:
                        fin_hasta = ahora + 1500
                    elif ahora >= fin_hasta:
                        motivo = "fin"

                pygame.display.update()
                clock.tick(FPS)
        finally:
            detener_audio(audio)
            for sonido in SONIDOS_FALLO:
                sonido.stop()
            fondo_cancion = None
            
        # SI DECIDIMOS REINICIAR, VOLVEMOS AL INICIO DEL WHILE TRUE
        if motivo == "reiniciar":
            continue

        resultado = {"terminada": motivo == "fin",
                     "cerrar": motivo == "cerrar",
                     "puntaje": marcador.puntaje,
                     "aciertos": marcador.aciertos,
                     "fallos": marcador.fallos,
                     "precision": marcador.precision(),
                     "mejor_racha": marcador.mejor_racha,
                     "volumen": volumen_actual,         
                     "gamepad": gamepad_mode}
                     
        if motivo == "fin":
            if pantalla_resultados(resultado, clock) == "cerrar":
                resultado["cerrar"] = True
        return resultado        


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((width, height))
    carpeta = sys.argv[1] if len(sys.argv) > 1 else None
    nivel = sys.argv[2] if len(sys.argv) > 2 else "expert"
    if carpeta is None:
        canciones = LectorDeCancionesMIDI.listarCanciones()
        if not canciones:
            print("No hay canciones en la carpeta Canciones")
            sys.exit()
        carpeta = canciones[0]["carpeta"]
    print(jugar(carpeta, nivel))
    pygame.quit()