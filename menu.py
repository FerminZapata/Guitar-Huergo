import pygame, os

width = 1500
height = 900

ejecucion = True

pygame.init()
screen = pygame.display.set_mode((width, height))
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

quickity = song_menu("QUICKPLAY", quick_songs)
campaignity = song_menu("CAMPAÑA", campaign_songs)

# menus que tienen lista de canciones (para mandarles los eventos)
song_menus = {"quickplay": quickity, "campaign": campaignity}

# DICCIONARIO QUE ALMACENA TODOS LOS BOTONES (UTILIZAR ESTO POR FAVOR)
menus = {"main":[Logo, Campaign, Quickplay, Option,Exit],
         "quickplay":[quickity,Exit],
         "campaign":[campaignity,Exit],
         "options":[Music, Gamepad, Exit],}

def upt_assets(): # FUNCION QUE REFRESCA LAS IMAGENES DE LA VENTANA
    screen.fill("black")
    for obj in menus[state]:
        obj.update()

while ejecucion:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecucion = False
            continue
        if state in song_menus:
            elegida = song_menus[state].handle_event(event)
            if elegida is not None:
                cancion_elegida = elegida
                modo_juego = state
                print("Cancion elegida:", cancion_elegida["name"], "| modo:", modo_juego)
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
    upt_assets()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()