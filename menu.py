import pygame, os, re, math

width = 1500
height = 900

ejecucion = True

pygame.init()

# PANTALLA: el juego siempre se dibuja en 1500x900 y pygame (flag SCALED) lo escala al monitor
# manteniendo la proporcion (con barras negras si hace falta). El mouse tambien se ajusta solo.
# Si el monitor es mas chico que 1500x900 no entraria en ventana, asi que arranca en pantalla completa.
try:
    escritorio = pygame.display.get_desktop_sizes()[0]
except (AttributeError, IndexError, pygame.error):
    escritorio = (width, height)
arranca_fullscreen = escritorio[0] < width or escritorio[1] < height
screen = pygame.display.set_mode((width, height),
                                 pygame.SCALED | (pygame.FULLSCREEN if arranca_fullscreen else 0))
clock = pygame.time.Clock()

# Si mantenes apretada una flecha, la lista sigue bajando/subiendo
pygame.key.set_repeat(400, 70)

# IMPLEMENTACION DEL ICONO EN LA VENTANA
icon_path = os.path.join(os.path.dirname(__file__), "LOGO3.ico")
icono = pygame.image.load(icon_path)
pygame.display.set_icon(icono)

# MENU ACTUAL
state = "main"

# CANCION QUE ELIGIO EL JUGADOR (None si todavia no eligio ninguna)
cancion_elegida = None
modo_juego = None   # "quickplay" o "campaign" (para saber si hay que registrar progreso)
enter_bloqueado = False   # ignora Enter/Espacio repetidos al cambiar de pantalla (ver loop principal)

# ---------------------------------------------------------------------------
# OPCIONES: todo se guarda en este diccionario, el juego puede leerlo desde aca
#   "volumen": 0.0 a 1.0     "gamepad": True / False     "fullscreen": True / False
# ---------------------------------------------------------------------------
opciones = {"volumen": 0.5, "gamepad": False, "fullscreen": arranca_fullscreen}

def aplicar_volumen():
    # aplica el volumen a la musica que este sonando (si el mixer esta activo)
    if pygame.mixer.get_init():
        pygame.mixer.music.set_volume(opciones["volumen"])

aplicar_volumen()

pantalla_completa = arranca_fullscreen   # como esta la ventana ahora mismo

def aplicar_pantalla_completa():
    # pasa a pantalla completa / ventana segun opciones["fullscreen"] (tambien con la tecla F11)
    global pantalla_completa
    if pantalla_completa != opciones["fullscreen"]:
        pygame.display.toggle_fullscreen()
        pantalla_completa = opciones["fullscreen"]

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


def lerp_color(a, b, t):
    # mezcla dos colores: t=0 -> a, t=1 -> b
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# LISTA DE CANCIONES ESTILO GUITAR HERO
# Se maneja con: flechas / W-S / rueda del mouse / click. Enter, espacio o click sobre
# la cancion ya seleccionada = jugar. ESC = volver al menu principal.
class song_menu:
    def __init__(self, title, songs):
        self.title = title
        self.songs = songs          # lista de diccionarios (ver abajo)
        # indice de la cancion seleccionada (se saltean los encabezados de tier)
        self.selected = next(i for i, s in enumerate(songs) if not s.get("header"))
        self.scroll = float(self.selected)  # posicion "visual" de la lista (se acerca suave a selected)
        self.item_h = 90            # separacion vertical entre canciones

        self.panel = pygame.Rect(150, 40, 1200, 640)   # fondo de todo el menu
        self.area = pygame.Rect(150, 110, 1200, 570)   # zona donde se ve la lista

        self.font_title = pygame.font.SysFont(None, 60)
        self.font_song = pygame.font.SysFont(None, 44)
        self.font_info = pygame.font.SysFont(None, 28)

    def item_rect(self, i):
        # la cancion que esta en el centro se ve mas ancha (efecto Guitar Hero)
        t = max(0.0, 1.0 - abs(i - self.scroll))
        w = 900 + 140 * t
        h = self.item_h - 10
        cy = self.area.centery + (i - self.scroll) * self.item_h
        return pygame.Rect(int(self.area.centerx - w / 2 - 20), int(cy - h / 2), int(w), int(h))

    def move(self, delta):
        step = 1 if delta > 0 else -1
        for _ in range(abs(delta)):
            i = self.selected + step
            while 0 <= i < len(self.songs) and self.songs[i].get("header"):
                i += step           # los encabezados de tier no se pueden seleccionar
            if 0 <= i < len(self.songs):
                self.selected = i
            else:
                break

    def choose(self):
        song = self.songs[self.selected]
        if song.get("locked", False):
            return None
        return song

    def handle_event(self, event):
        """Devuelve el diccionario de la cancion si el jugador la eligio, si no None."""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_DOWN, pygame.K_s):
                self.move(1)
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.move(-1)
            elif event.key == pygame.K_PAGEDOWN:
                self.move(5)
            elif event.key == pygame.K_PAGEUP:
                self.move(-5)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return self.choose()
        elif event.type == pygame.MOUSEWHEEL:
            self.move(-event.y)     # rueda hacia abajo -> y negativo -> bajamos en la lista
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.area.collidepoint(event.pos):
                for i in range(len(self.songs)):
                    if self.songs[i].get("header"):
                        continue
                    if self.item_rect(i).collidepoint(event.pos):
                        if i == self.selected:
                            return self.choose()
                        self.selected = i
                        break
        return None

    def update(self):
        # scroll suave hacia la cancion seleccionada
        self.scroll += (self.selected - self.scroll) * 0.2
        if abs(self.selected - self.scroll) < 0.001:
            self.scroll = float(self.selected)

        # fondo y titulo
        pygame.draw.rect(screen, (255, 255, 255), self.panel.inflate(10, 10))
        pygame.draw.rect(screen, (30, 30, 30), self.panel)
        titulo = self.font_title.render(self.title, True, (255, 255, 255))
        screen.blit(titulo, (self.panel.centerx - titulo.get_width() / 2, 60))

        # lista (recortada para que las canciones no se salgan del panel)
        screen.set_clip(self.area)
        for i, song in enumerate(self.songs):
            rect = self.item_rect(i)
            if rect.bottom < self.area.top or rect.top > self.area.bottom:
                continue

            # encabezado de tier (ej: "TIER 2" + progreso)
            if song.get("header"):
                locked = song.get("locked", False)
                color = (110, 110, 110) if locked else (230, 140, 20)
                nombre = self.font_song.render(song["name"], True, color)
                screen.blit(nombre, (rect.x + 25, rect.centery - nombre.get_height() / 2))
                derecha = "BLOQUEADO" if locked else song.get("progress", "")
                info = self.font_info.render(derecha, True, color)
                screen.blit(info, (rect.right - 40 - info.get_width(), rect.centery - info.get_height() / 2))
                pygame.draw.line(screen, color, (rect.x + 25, rect.bottom - 4), (rect.right - 40, rect.bottom - 4), 2)
                continue

            t = max(0.0, 1.0 - abs(i - self.scroll))   # 1 = en el centro, 0 = lejos
            locked = song.get("locked", False)

            if locked:
                bg = lerp_color((40, 40, 40), (90, 90, 90), t)
                txt_color = lerp_color((90, 90, 90), (160, 160, 160), t)
            else:
                bg = lerp_color((50, 50, 50), (200, 110, 0), t)
                txt_color = lerp_color((150, 150, 150), (255, 255, 255), t)
                if song.get("secret"):      # la cancion secreta se ve en dorado
                    txt_color = lerp_color((200, 170, 60), (255, 230, 90), t)

            pygame.draw.rect(screen, bg, rect, border_radius=12)
            if t > 0.5:
                pygame.draw.rect(screen, (255, 255, 255), rect, 3, border_radius=12)

            nombre = self.font_song.render(song["name"], True, txt_color)
            screen.blit(nombre, (rect.x + 25, rect.y + 10))

            if locked:
                info_txt = "BLOQUEADA"
            else:
                partes = [song.get("artist", ""), song.get("duration", "")]
                if song.get("done"):
                    partes.append("COMPLETADA")
                info_txt = "  -  ".join(p for p in partes if p) or " "
            info = self.font_info.render(info_txt, True, txt_color)
            screen.blit(info, (rect.x + 25, rect.y + 48))

            # dificultad: 5 circulitos (rellenos = dificultad)
            if not locked:
                for k in range(5):
                    cx = rect.right - 40 - (4 - k) * 28
                    cy = rect.centery
                    if k < song.get("difficulty", 1):
                        pygame.draw.circle(screen, txt_color, (cx, cy), 9)
                    else:
                        pygame.draw.circle(screen, txt_color, (cx, cy), 9, 2)
        screen.set_clip(None)

        # barra de scroll a la derecha (para que se note que hay mas canciones abajo)
        track = pygame.Rect(self.panel.right - 30, self.area.top + 10, 8, self.area.height - 20)
        pygame.draw.rect(screen, (70, 70, 70), track, border_radius=4)
        if len(self.songs) > 1:
            thumb_h = 50
            prog = max(0.0, min(1.0, self.scroll / (len(self.songs) - 1)))
            thumb_y = track.top + prog * (track.height - thumb_h)
            pygame.draw.rect(screen, (255, 255, 255), (track.x, thumb_y, track.width, thumb_h), border_radius=4)


# BARRA DE VOLUMEN: se arrastra con el mouse (tambien rueda del mouse y flechas izq/der)
class volume_slider:
    def __init__(self, pos, length, key):
        self.key = key
        self.track = pygame.Rect(pos[0], pos[1] - 6, length, 12)         # la barra
        self.hit = pygame.Rect(pos[0] - 20, pos[1] - 25, length + 40, 50)  # zona clickeable (mas grande)
        self.dragging = False
        self.font = pygame.font.SysFont(None, 44)

    def set_value(self, v):
        opciones[self.key] = max(0.0, min(1.0, round(v, 2)))
        aplicar_volumen()

    def set_from_x(self, x):
        self.set_value((x - self.track.left) / self.track.width)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hit.collidepoint(event.pos):
                self.dragging = True
                self.set_from_x(event.pos[0])
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.set_from_x(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif event.type == pygame.MOUSEWHEEL and self.hit.collidepoint(pygame.mouse.get_pos()):
            self.set_value(opciones[self.key] + 0.05 * event.y)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.set_value(opciones[self.key] - 0.05)
            elif event.key == pygame.K_RIGHT:
                self.set_value(opciones[self.key] + 0.05)

    def update(self):
        v = opciones[self.key]
        activo = self.dragging or self.hit.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(screen, (70, 70, 70), self.track, border_radius=6)
        llena = pygame.Rect(self.track.left, self.track.top, int(self.track.width * v), self.track.height)
        if llena.width > 0:
            pygame.draw.rect(screen, (200, 110, 0), llena, border_radius=6)
        cx = self.track.left + int(self.track.width * v)
        radio = 18 if activo else 15
        pygame.draw.circle(screen, (255, 255, 255), (cx, self.track.centery), radio)
        pygame.draw.circle(screen, (200, 110, 0), (cx, self.track.centery), radio, 3)
        txt = self.font.render(str(round(v * 100)) + "%", True, (255, 255, 255))
        screen.blit(txt, (self.track.right + 30, self.track.centery - txt.get_height() / 2))


# CASILLA CON TICK: el tick (tickactivado.png) aparece solo cuando la opcion esta activada
class tick_box:
    def __init__(self, pos, size, key, tick_img, al_cambiar=None):
        self.key = key
        self.al_cambiar = al_cambiar    # funcion que se llama despues de cambiar el valor (opcional)
        self.rect = pygame.Rect(pos[0], pos[1], size, size)
        self.tick = pygame.transform.smoothscale(tick_img, (size - 20, size - 20))

    def toggle(self):
        opciones[self.key] = not opciones[self.key]
        if self.al_cambiar:
            self.al_cambiar()

    def update(self):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(screen, (30, 30, 30), self.rect, border_radius=10)
        pygame.draw.rect(screen, (255, 215, 60) if hover else (255, 255, 255), self.rect, 5, border_radius=10)
        if opciones[self.key]:
            screen.blit(self.tick, (self.rect.x + 10, self.rect.y + 10))


# ---------------------------------------------------------------------------
# CANCIONES: lee el song.ini de cada carpeta dentro de Canciones/
# ---------------------------------------------------------------------------
canciones_path = os.path.join(os.path.dirname(__file__), "Canciones")

def leer_ini(path):
    # devuelve un diccionario con lo que hay dentro de [song] (claves en minuscula)
    datos = {}
    try:
        with open(path, encoding="utf-8-sig", errors="replace") as f:
            en_song = False
            for linea in f:
                linea = linea.strip()
                if linea.startswith("["):
                    en_song = linea.lower() == "[song]"
                elif en_song and "=" in linea:
                    clave, valor = linea.split("=", 1)
                    datos[clave.strip().lower()] = valor.strip()
    except OSError:
        pass
    return datos

def limpiar_texto(t):
    t = re.sub(r"<[^>]+>", "", t)         # saca etiquetas tipo <color=orange>...</color>
    return t.replace('\\"', '"').strip()   # y las comillas escapadas

def normalizar(nombre):
    return limpiar_texto(nombre).lower()

# canciones_info["enter sandman"] = {"carpeta": ruta, "ini": {...datos del song.ini...}}
canciones_info = {}
if os.path.isdir(canciones_path):
    for nombre_carpeta in sorted(os.listdir(canciones_path)):
        ruta = os.path.join(canciones_path, nombre_carpeta)
        datos = leer_ini(os.path.join(ruta, "song.ini"))
        if "name" in datos:
            canciones_info[normalizar(datos["name"])] = {"carpeta": ruta, "ini": datos}


# ---------------------------------------------------------------------------
# PANTALLA DE INFORMACION DE LA CANCION (estilo Clone Hero)
# Aparece al elegir una cancion en Quickplay o Campaña. Flechas / mouse para moverse,
# Enter o click para elegir, ESC para volver a la lista.
# ---------------------------------------------------------------------------
def crear_fondo(w, h):
    # degradado azul (centro claro, bordes oscuros, toque violeta abajo a la izquierda)
    cw, ch = 100, 60
    chico = pygame.Surface((cw, ch))
    for x in range(cw):
        for y in range(ch):
            fx, fy = x / (cw - 1), y / (ch - 1)
            d = min(1.0, math.hypot((fx - 0.5) * 1.3, (fy - 0.45) * 1.6) / 0.75)
            color = lerp_color((24, 120, 178), (38, 52, 72), d)
            m = max(0.0, 1.0 - fx * 1.6) * max(0.0, (fy - 0.45) / 0.55)
            chico.set_at((x, y), lerp_color(color, (78, 56, 82), m * 0.8))
    return pygame.transform.smoothscale(chico, (w, h))

def recortar(texto, fuente, ancho):
    # corta el texto con "..." si no entra en el ancho dado
    if fuente.size(texto)[0] <= ancho:
        return texto
    while texto and fuente.size(texto + "...")[0] > ancho:
        texto = texto[:-1]
    return texto + "..."

def wrap_text(texto, fuente, ancho, max_lineas):
    # parte un texto largo en lineas que entren en el ancho dado
    lineas, actual = [], ""
    for palabra in texto.split():
        prueba = (actual + " " + palabra).strip()
        if fuente.size(prueba)[0] <= ancho:
            actual = prueba
        else:
            if actual:
                lineas.append(actual)
            actual = palabra
    if actual:
        lineas.append(actual)
    if len(lineas) > max_lineas:
        lineas = lineas[:max_lineas]
        lineas[-1] = recortar(lineas[-1] + "...", fuente, ancho)
    return lineas

# instrumentos que se muestran en la dificultad: (nombre, clave del song.ini)
# el juego solo tiene guitarra; si algun dia suman otro instrumento, agregarlo aca
INSTRUMENTOS = [("Guitarra", "diff_guitar")]

class song_detail:
    # OJO: la fuente por defecto de pygame recorta las MAYUSCULAS con tilde (Á, Ó...); usar minusculas con tilde
    ANCHO = 860

    def __init__(self):
        self.song = None          # diccionario de la cancion elegida (el de la lista)
        self.origen = "main"      # de que lista vino ("quickplay" o "campaign")
        self.info = None          # {"carpeta":..., "ini":...} o None si no hay carpeta
        self.datos = {}           # lo que dice el song.ini
        self.titulo = ""
        self.frase = []
        self.arte = None
        self.cache_arte = {}
        self.sel = 0
        self.opciones = ["Jugar", "Volver"]
        self.acciones = ["jugar", "volver"]

        self.f_titulo = pygame.font.SysFont(None, 92)
        self.f_frase = pygame.font.SysFont(None, 30)
        self.f_artista = pygame.font.SysFont(None, 60)
        self.f_sub = pygame.font.SysFont(None, 30)
        self.f_dato = pygame.font.SysFont(None, 30)
        self.f_instr = pygame.font.SysFont(None, 26)
        self.f_menu = pygame.font.SysFont(None, 50)
        self.f_menu.set_bold(True)

        self.fondo = crear_fondo(width, height)
        x = (width - self.ANCHO) // 2
        self.panel_info = pygame.Rect(x, 235, self.ANCHO, 420)
        self.panel_menu = pygame.Rect(x, 672, self.ANCHO, 112)
        self.filas = [pygame.Rect(x + 8, 680 + i * 48, self.ANCHO - 16, 46) for i in range(len(self.opciones))]

    @property
    def carpeta(self):
        # ruta de la carpeta de la cancion (con el audio y el chart) o None si no se encontro
        return self.info["carpeta"] if self.info else None

    def abrir(self, song, origen):
        self.song = song
        self.origen = origen
        self.sel = 0
        self.info = canciones_info.get(normalizar(song["name"]))
        self.datos = self.info["ini"] if self.info else {}
        self.titulo = limpiar_texto(self.datos.get("name", song["name"]))
        frase = limpiar_texto(self.datos.get("loading_phrase", ""))
        self.frase = wrap_text(frase, self.f_frase, 1360, 3) if frase else []
        self.arte = self.cargar_arte()

    def cargar_arte(self):
        if not self.info:
            return None
        ruta = self.info["carpeta"]
        if ruta in self.cache_arte:
            return self.cache_arte[ruta]
        arte = None
        for nombre in ("album.jpg", "album.png", "album.jpeg"):
            archivo = os.path.join(ruta, nombre)
            if os.path.isfile(archivo):
                try:
                    img = pygame.image.load(archivo).convert()
                    escala = 180 / max(img.get_width(), img.get_height())
                    arte = pygame.transform.smoothscale(
                        img, (int(img.get_width() * escala), int(img.get_height() * escala)))
                except pygame.error:
                    arte = None
                break
        self.cache_arte[ruta] = arte
        return arte

    def handle_event(self, event):
        """Devuelve "jugar", "volver" o None."""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_DOWN, pygame.K_s):
                self.sel = (self.sel + 1) % len(self.opciones)
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.sel = (self.sel - 1) % len(self.opciones)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return self.acciones[self.sel]
            elif event.key == pygame.K_ESCAPE:
                return "volver"
        elif event.type == pygame.MOUSEMOTION:
            for i, fila in enumerate(self.filas):
                if fila.collidepoint(event.pos):
                    self.sel = i
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for i, fila in enumerate(self.filas):
                if fila.collidepoint(event.pos):
                    self.sel = i
                    return self.acciones[i]
        return None

    def texto_centrado(self, texto, fuente, color, cx, y):
        surf = fuente.render(texto, True, color)
        screen.blit(surf, (cx - surf.get_width() / 2, y))

    def filas_info(self):
        d = self.datos
        filas = []
        if d.get("album"):
            filas.append(("Disco", limpiar_texto(d["album"])))
        if d.get("year"):
            anio = re.match(r"\d{4}", d["year"])
            filas.append(("Año", anio.group(0) if anio else d["year"]))
        if d.get("genre"):
            filas.append(("Género", limpiar_texto(d["genre"])))
        if d.get("charter"):
            filas.append(("Charter", limpiar_texto(d["charter"])))
        if d.get("song_length", "").isdigit():
            seg = int(d["song_length"]) // 1000
            filas.append(("Duración", str(seg // 60) + ":" + str(seg % 60).zfill(2)))
        return filas

    def update(self):
        screen.blit(self.fondo, (0, 0))
        cx = width / 2

        # nombre de la cancion + frase del .ini (loading_phrase)
        titulo = self.f_titulo.render(self.titulo, True, (255, 255, 255))
        if titulo.get_width() > width - 80:
            titulo = pygame.transform.smoothscale(
                titulo, (width - 80, int(titulo.get_height() * (width - 80) / titulo.get_width())))
        screen.blit(titulo, (cx - titulo.get_width() / 2, 18))
        y = 100
        for linea in self.frase:
            self.texto_centrado(linea, self.f_frase, (235, 240, 245), cx, y)
            y += 32

        # panel con la informacion de la cancion
        p = self.panel_info
        pygame.draw.rect(screen, (18, 86, 128), p, border_radius=8)
        pygame.draw.rect(screen, (26, 26, 26), (p.x, p.y, p.width, 70),
                         border_top_left_radius=8, border_top_right_radius=8)
        artista = limpiar_texto(self.datos.get("artist", "Artista desconocido"))
        self.texto_centrado(recortar(artista, self.f_artista, p.width - 40), self.f_artista,
                            (255, 255, 255), p.centerx, p.y + 35 - self.f_artista.get_height() / 2)
        pygame.draw.rect(screen, (32, 32, 32), (p.x, p.y + 78, p.width, 40))
        self.texto_centrado("Información de la canción", self.f_sub, (225, 225, 225),
                            p.centerx, p.y + 98 - self.f_sub.get_height() / 2)

        # caratula (album.jpg)
        ax, ay = p.x + 24, p.y + 136
        pygame.draw.rect(screen, (18, 40, 60), (ax, ay, 180, 180))
        if self.arte:
            screen.blit(self.arte, (ax + (180 - self.arte.get_width()) // 2,
                                    ay + (180 - self.arte.get_height()) // 2))
        pygame.draw.rect(screen, (230, 235, 240), (ax, ay, 180, 180), 2)

        # datos del .ini
        dx = ax + 180 + 28
        filas = self.filas_info()
        if not self.info:
            self.texto_centrado("No se encontró la carpeta de la canción en Canciones/",
                                self.f_dato, (255, 190, 120), dx + 250, ay + 70)
        ancho_valor = p.right - 24 - (dx + 120)
        filas = [(n, wrap_text(v, self.f_dato, ancho_valor, 2)) for n, v in filas]  # valores largos: 2 lineas
        paso = 34 if sum(len(lineas) for _, lineas in filas) <= 5 else 29
        fy = ay + 4
        for nombre, lineas in filas:
            screen.blit(self.f_dato.render(nombre, True, (160, 205, 230)), (dx, fy))
            for linea in lineas:
                screen.blit(self.f_dato.render(linea, True, (255, 255, 255)), (dx + 120, fy))
                fy += paso

        # dificultad por instrumento (escala de 0 a 6, como en el song.ini)
        pygame.draw.line(screen, (70, 140, 180), (p.x + 24, p.y + 336), (p.right - 24, p.y + 336), 1)
        instrumentos = []
        for nombre, clave in INSTRUMENTOS:
            valor = self.datos.get(clave, "")
            if valor.lstrip("-").isdigit() and int(valor) >= 0:
                instrumentos.append((nombre, int(valor)))
        if not instrumentos:
            self.texto_centrado("Sin datos de dificultad en el song.ini", self.f_instr,
                                (160, 205, 230), p.centerx, p.y + 372)
        col = 130
        x0 = p.centerx - len(instrumentos) * col / 2
        for i, (nombre, nivel) in enumerate(instrumentos):
            ccx = x0 + i * col + col / 2
            self.texto_centrado(nombre, self.f_instr, (225, 235, 245), ccx, p.y + 348)
            for k in range(6):
                px = int(ccx - 2.5 * 17 + k * 17)
                if k < nivel:
                    pygame.draw.circle(screen, (255, 200, 40), (px, p.y + 384), 6)
                else:
                    pygame.draw.circle(screen, (120, 170, 200), (px, p.y + 384), 6, 2)

        # menu: Jugar / Volver (la fila elegida se resalta como en Clone Hero)
        pygame.draw.rect(screen, (18, 66, 100), self.panel_menu, border_radius=8)
        for i, fila in enumerate(self.filas):
            if i == self.sel:
                pygame.draw.rect(screen, (208, 212, 215), fila, border_radius=6)
                color = (10, 10, 10)
            else:
                color = (255, 255, 255)
            txt = self.f_menu.render(self.opciones[i], True, color)
            screen.blit(txt, (fila.centerx - txt.get_width() / 2, fila.centery - txt.get_height() / 2))


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

fullscreen_path = os.path.join(menuassets_path,"Fullscreen")

normal = None
pressed = None

for img in os.listdir(fullscreen_path):
    if img[-5] == "P":
        normal = pygame.image.load(os.path.join(fullscreen_path,img))
    else:
        pressed = pygame.image.load(os.path.join(fullscreen_path,img))

Fullscreen = button((width/5-normal.get_width()/5, 375), pressed, normal)

# controles de la pantalla de opciones
tick_img = pygame.image.load(os.path.join(menuassets_path, "tickactivado.png")).convert_alpha()
volumen_slider = volume_slider((760, 300), 300, "volumen")           # al lado del boton MUSICA
gamepad_check = tick_box((1060, 500), 100, "gamepad", tick_img)     # al lado del boton MODO GAMEPAD
fullscreen_check = tick_box((1060, 375), 100, "fullscreen", tick_img,
                            aplicar_pantalla_completa)              # al lado del boton FULLSCREEN

# ---------------------------------------------------------------------------
# CAMPAÑA: tiers de canciones, cada uno mas dificil que el anterior
# Cada cancion es (nombre, dificultad de 1 a 5). La dificultad es una propuesta,
# cambienla a gusto. Si quieren mostrar artista o duracion, agreguen "artist" y
# "duration" al diccionario de la cancion (ver mas abajo).
# ---------------------------------------------------------------------------
TIERS = [
    ("TIER 1", [("Back in the U.S.S.R.", 1), ("You Know You're Right", 1),
                ("Paranoid", 1), ("Stairway to Heaven", 2)]),
    ("TIER 2", [("Enter Sandman", 2), ("Angry Again", 2),
                ("Hallowed Be Thy Name", 3), ("Sugar", 3)]),
    ("TIER 3", [("Liar", 3), ("The Conjuring", 3),
                ("Ride The Lightning", 4), ("Raining Blood", 4)]),
    ("TIER 4", [("Take No Prisoners", 4), ("Five Magics", 4),
                ("Devil's Island", 5), ("One", 5)]),
]

# cuantas canciones de un tier hay que completar para abrir el siguiente (4 = todas)
CANCIONES_PARA_DESBLOQUEAR = 3

campaign_completadas = set()   # nombres de las canciones ya completadas

# lista plana: un encabezado por tier seguido de sus canciones
campaign_songs = []
for t, (tier_name, canciones) in enumerate(TIERS):
    campaign_songs.append({"header": True, "name": tier_name, "tier": t, "total": len(canciones)})
    for nombre, dificultad in canciones:
        campaign_songs.append({"name": nombre, "difficulty": dificultad, "tier": t})

def completadas_en_tier(t):
    return sum(1 for s in campaign_songs
               if s["tier"] == t and not s.get("header") and s["name"] in campaign_completadas)

def tier_desbloqueado(t):
    if t == 0:
        return True
    return tier_desbloqueado(t - 1) and completadas_en_tier(t - 1) >= CANCIONES_PARA_DESBLOQUEAR

def refrescar_campaña():
    # recalcula que tiers estan bloqueados y los contadores de progreso
    for s in campaign_songs:
        s["locked"] = not tier_desbloqueado(s["tier"])
        if s.get("header"):
            s["progress"] = str(completadas_en_tier(s["tier"])) + "/" + str(s["total"]) + " completadas"
        else:
            s["done"] = s["name"] in campaign_completadas

def completar_cancion(song):
    # LLAMAR ESTO cuando el jugador termine una cancion de la campaña
    campaign_completadas.add(song["name"])
    refrescar_campaña()

refrescar_campaña()

# QUICKPLAY: todas las canciones de la campaña, sin bloqueos
quick_songs = [{"name": s["name"], "difficulty": s["difficulty"], "artist": TIERS[s["tier"]][0]}
               for s in campaign_songs if not s.get("header")]

# ---------------------------------------------------------------------------
# CANCION SECRETA: no aparece en Quickplay hasta que se ingresa CODIGO_SECRETO
# en el menu principal (teclas una detras de otra). Para cambiar el codigo, editar la lista.
# Ahora es: arriba, arriba, abajo, abajo, izquierda, derecha, izquierda, derecha, B, A
# ---------------------------------------------------------------------------
CODIGO_SECRETO = [pygame.K_UP, pygame.K_UP, pygame.K_DOWN, pygame.K_DOWN,
                  pygame.K_LEFT, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_RIGHT,
                  pygame.K_b, pygame.K_a]
# "name" tiene que coincidir con el name del song.ini de su carpeta en Canciones/
cancion_secreta = {"name": "Mechanix", "difficulty": 5, "artist": "SECRETA", "secret": True}
secreta_desbloqueada = False
entradas_secretas = []          # ultimas teclas apretadas en el menu principal

aviso_texto = ""                # cartelito que se muestra unos segundos abajo de todo
aviso_hasta = 0
f_aviso = pygame.font.SysFont(None, 38)

def desbloquear_cancion_secreta():
    global secreta_desbloqueada, aviso_texto, aviso_hasta
    if secreta_desbloqueada:
        aviso_texto = "La canción secreta ya está desbloqueada en Quickplay"
    else:
        secreta_desbloqueada = True
        quick_songs.append(cancion_secreta)   # quickity usa esta misma lista, asi que aparece sola
        aviso_texto = "¡Canción secreta desbloqueada: " + cancion_secreta["name"] + "!"
    aviso_hasta = pygame.time.get_ticks() + 4000

def dibujar_aviso():
    if pygame.time.get_ticks() >= aviso_hasta:
        return
    txt = f_aviso.render(aviso_texto, True, (255, 220, 80))
    caja = pygame.Rect(width // 2 - (txt.get_width() + 50) // 2, 826, txt.get_width() + 50, txt.get_height() + 24)
    pygame.draw.rect(screen, (30, 30, 30), caja, border_radius=10)
    pygame.draw.rect(screen, (255, 220, 80), caja, 3, border_radius=10)
    screen.blit(txt, (caja.x + 25, caja.y + 12))


for s in quick_songs + [cancion_secreta]:
    if normalizar(s["name"]) not in canciones_info:
        print("AVISO: no hay carpeta con song.ini para", s["name"], "dentro de Canciones/")

quickity = song_menu("QUICKPLAY", quick_songs)
campaignity = song_menu("CAMPAÑA", campaign_songs)

# menus que tienen lista de canciones (para mandarles los eventos)
song_menus = {"quickplay": quickity, "campaign": campaignity}

detalle = song_detail()   # pantalla de informacion de la cancion

# DICCIONARIO QUE ALMACENA TODOS LOS BOTONES (UTILIZAR ESTO POR FAVOR)
menus = {"main":[Logo, Campaign, Quickplay, Option,Exit],
         "quickplay":[quickity,Exit],
         "campaign":[campaignity,Exit],
         "options":[Music, volumen_slider, Fullscreen, fullscreen_check, Gamepad, gamepad_check, Exit],
         "detalle":[detalle],}

def upt_assets(): # FUNCION QUE REFRESCA LAS IMAGENES DE LA VENTANA
    screen.fill("black")
    for obj in menus[state]:
        obj.update()

while ejecucion:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecucion = False
            continue

        # F11: pantalla completa (tambien se puede activar desde Opciones)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            fullscreen_check.toggle()
            continue

        # codigo secreto (solo en el menu principal): desbloquea una cancion en Quickplay
        if state == "main" and event.type == pygame.KEYDOWN:
            entradas_secretas.append(event.key)
            del entradas_secretas[:-len(CODIGO_SECRETO)]    # guarda solo las ultimas teclas
            if entradas_secretas == CODIGO_SECRETO:
                entradas_secretas.clear()
                desbloquear_cancion_secreta()

        # mantener apretado Enter/Espacio repite el KEYDOWN: lo ignoramos hasta que se suelte,
        # asi la pantalla nueva no reacciona sola al mismo Enter con el que se abrio
        if event.type == pygame.KEYUP and event.key in (pygame.K_RETURN, pygame.K_SPACE):
            enter_bloqueado = False
        elif (event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE)
              and enter_bloqueado):
            continue

        # pantalla de informacion de la cancion
        if state == "detalle":
            accion = detalle.handle_event(event)
            if accion is not None:
                enter_bloqueado = event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE)
                if accion == "volver":
                    state = detalle.origen        # vuelve a la lista de donde vino
                elif accion == "jugar":
                    cancion_elegida = detalle.song
                    modo_juego = detalle.origen
                    # TODO: aca arranca el juego con la cancion elegida. La carpeta con el
                    # audio y el chart esta en detalle.carpeta. Cuando el jugador la termine
                    # y modo_juego == "campaign":  completar_cancion(cancion_elegida)
                    print("Jugar:", cancion_elegida["name"], "| modo:", modo_juego, "| carpeta:", detalle.carpeta)
            continue

        if state == "options":
            volumen_slider.handle_event(event)
        if state in song_menus:
            elegida = song_menus[state].handle_event(event)
            if elegida is not None:
                detalle.abrir(elegida, state)    # abre la pantalla con la info del song.ini
                state = "detalle"
                enter_bloqueado = event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE)
                continue
            # DEBUG (borrar despues): F1 marca como completada la cancion seleccionada
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_F1 and state == "campaign"
                  and not campaignity.songs[campaignity.selected].get("locked")):
                completar_cancion(campaignity.songs[campaignity.selected])

        # ESC vuelve al menu principal
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and state != "main":
            state = "main"

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
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
                elif state == "options" and (Gamepad.rect.collidepoint(event.pos)
                                             or gamepad_check.rect.collidepoint(event.pos)):
                    gamepad_check.toggle()   # click en el boton o en la casilla
                elif state == "options" and (Fullscreen.rect.collidepoint(event.pos)
                                             or fullscreen_check.rect.collidepoint(event.pos)):
                    fullscreen_check.toggle()
    upt_assets()
    dibujar_aviso()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()