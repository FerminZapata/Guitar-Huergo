import os, sys, time, mido
from bisect import bisect_right

# ---------------------------------------------------------------------------
# Lector de canciones para el Guitar Hero (pygame)
# Lee notes.chart y notes.mid. En ambos casos SOLO lee la guitarra principal:
#   .chart -> secciones [EasySingle] [MediumSingle] [HardSingle] [ExpertSingle]
#   .mid   -> pista "PART GUITAR"
# Todo lo demas (bajo, bateria, teclado, voces, etc.) se ignora.
#
# Los dos formatos terminan en el MISMO resultado:
#   {"ExpertSingle": [{'start_ms', 'duration_ms', 'lane', 'type', ...}, ...]}
# ---------------------------------------------------------------------------

# --- constantes para el .mid -----------------------------------------------
NOTA_BASE_MIDI = {"easy": 60, "medium": 72, "hard": 84, "expert": 96}   # nota del verde en cada dificultad
ID_DIF_SYSEX   = {"easy": 0, "medium": 1, "hard": 2, "expert": 3}
NOTA_STAR_POWER = 116       # overdrive / star power
NOTA_TAP        = 104       # seccion de tap (todas las dificultades)
NOMBRES_PISTA_GUITARRA = ("PART GUITAR", "T1 GEMS")   # nombres validos de la pista de guitarra
NOMBRE_CARPETA_CANCIONES = "Canciones"                # carpeta (al lado de este archivo) con una subcarpeta por cancion


def rutaCarpetaRaiz():              #extrae la ruta de la carpeta
    return os.path.dirname(os.path.abspath(__file__))

def rutaCarpetaCanciones():         #ruta de la carpeta "Canciones" (esta al lado de este archivo)
    return os.path.join(rutaCarpetaRaiz(), NOMBRE_CARPETA_CANCIONES)

def buscarArchivoNotas(carpetaCancion):     #dentro de la carpeta de UNA cancion busca notes.chart o notes.mid
    try:
        archivos = os.listdir(carpetaCancion)
    except OSError:
        return None
    for nombreBuscado in ("notes.chart", "notes.mid"):      #si estan los dos, usa el .chart
        for archivo in archivos:
            if archivo.lower() == nombreBuscado:            #.lower() para que no importen las mayusculas
                return os.path.join(carpetaCancion, archivo)
    return None

def listarCanciones(carpetaCanciones=None):     #entra a Canciones, recorre cada carpeta y devuelve la lista de canciones que tienen .chart o .mid
    if carpetaCanciones is None:
        carpetaCanciones = rutaCarpetaCanciones()
    if not os.path.isdir(carpetaCanciones):
        print("No se encontro la carpeta:", carpetaCanciones)
        return []
    canciones = []
    for nombre in sorted(os.listdir(carpetaCanciones)):
        carpeta = os.path.join(carpetaCanciones, nombre)
        if not os.path.isdir(carpeta):                      #ignora archivos sueltos
            continue
        rutaNotas = buscarArchivoNotas(carpeta)
        if rutaNotas is None:
            print("Se omite (no tiene notes.chart ni notes.mid):", nombre)
            continue
        canciones.append({'nombre': nombre,                 #nombre de la carpeta, ej: "Metallica - One (Neversoft)"
                          'carpeta': carpeta,               #ruta de la carpeta (aca estan tambien song.opus, guitar.opus, album.jpg...)
                          'notas': rutaNotas,               #ruta del notes.chart / notes.mid
                          'formato': os.path.splitext(rutaNotas)[1][1:].lower()})   # 'chart' o 'mid'
    return canciones


# ===========================================================================
#  LECTURA .CHART
# ===========================================================================
def leerChart(path,diff):#Funcion que devuelve una difficultad del archivo .chart en un diccionario
    try:
        with open(path, "r", encoding="utf-8") as archivo:
            data = archivo.read()
            rdblFile = {'Song': [], 'SyncTrack': [], 'Events': []}
            seccion = diff.capitalize() + "Single"          # ej: "ExpertSingle" (guitarra principal)
            if "[" + seccion + "]" in data:
                rdblFile[seccion] = []
            else:
                print("El .chart no tiene la dificultad", diff)
                return
            for key in rdblFile.keys():
                found = False
                archivo.seek(0)
                for linea in archivo:
                    if found == False:
                        if key in linea:
                            found = True
                            continue
                    elif found:
                        if "{" not in linea and "}" not in linea:
                            rdblFile[key].append(linea.strip().split(" = "))
                        elif "}" in linea:
                            break
                        else:
                            continue
        for key in rdblFile.keys():# termina de separar las lineas
            if key != "Song":
                for bpms in rdblFile[key]:
                    bpms[1] = bpms[1].split(" ")
        return rdblFile
    except FileNotFoundError:
        print("No se encontro el archivo.")
        time.sleep(2)
        return


# ===========================================================================
#  LECTURA .MID
#  Devuelve un diccionario con la MISMA forma que leerChart, asi parse_BPM y
#  parseNote funcionan igual para los dos formatos.
# ===========================================================================
def buscarPistaGuitarra(mid):       #busca la pista de la guitarra principal (nombre exacto, asi no se confunde con PART REAL_GUITAR, etc)
    for nombre in NOMBRES_PISTA_GUITARRA:
        for track in mid.tracks:
            if track.name.strip().upper() == nombre:
                return track
    return None

def cubierto(tick, intervalos):     #dice si un tick cae dentro de alguno de los intervalos (inicio, fin) ya ordenados
    i = bisect_right(intervalos, (tick, float("inf"))) - 1
    return i >= 0 and tick < max(intervalos[i][1], intervalos[i][0] + 1)

def leerMidi(path, diff):
    diff = diff.lower()
    if diff not in NOTA_BASE_MIDI:
        print("Dificultad invalida:", diff)
        return
    try:
        mid = mido.MidiFile(path, clip=True)    # clip=True: algunos .mid traen bytes sysex fuera de rango y sin esto mido tira error
    except FileNotFoundError:
        print("No se encontro el archivo.")
        time.sleep(2)
        return
    resolution = mid.ticks_per_beat
    pista = buscarPistaGuitarra(mid)
    if pista is None:
        print("El .mid no tiene pista de guitarra (PART GUITAR).")
        return

    # --- mapa de tempos (esta en la primera pista) -> mismo formato que el SyncTrack del .chart
    syncTrack = []
    tick = 0
    for msg in mid.tracks[0]:
        tick += msg.time                                    # en mido cada mensaje trae el tiempo desde el anterior (delta)
        if msg.type == "set_tempo":
            bpmX1000 = 60_000_000_000 / msg.tempo           # tempo viene en microsegundos por negra; el .chart usa BPM*1000
            syncTrack.append([str(tick), ["B", str(bpmX1000)]])

    # --- recorre la pista de guitarra juntando notas (inicio, fin, nota) y sysex
    base = NOTA_BASE_MIDI[diff]
    notas = []
    abiertas = {}                   # nota -> tick en el que se apreto
    sysexIntervalos = {1: [], 4: []}    # 1 = notas open, 4 = notas tap (extension de Phase Shift / Clone Hero)
    sysexInicio = {}
    tick = 0
    for msg in pista:
        tick += msg.time
        if msg.type == "note_on" and msg.velocity > 0:
            abiertas[msg.note] = tick
        elif msg.type in ("note_on", "note_off") and msg.note in abiertas:     # note_on con velocity 0 tambien significa "soltar"
            notas.append((abiertas.pop(msg.note), tick, msg.note))
        elif msg.type == "sysex":
            d = tuple(msg.data)         # formato: 'P' 'S' 0 0 <dificultad> <tipo> <on/off>
            if len(d) >= 7 and d[:4] == (0x50, 0x53, 0, 0) and d[4] in (ID_DIF_SYSEX[diff], 127, 255) and d[5] in sysexIntervalos:
                if d[6]:
                    sysexInicio[d[5]] = tick
                elif d[5] in sysexInicio:
                    sysexIntervalos[d[5]].append((sysexInicio.pop(d[5]), tick))

    # --- separa los intervalos de modificadores (forzar hopo / forzar strum / tap / open)
    forzarHopo = sorted((i, f) for i, f, n in notas if n == base + 5)
    forzarStrum = sorted((i, f) for i, f, n in notas if n == base + 6)
    tap = sorted([(i, f) for i, f, n in notas if n == NOTA_TAP] + sysexIntervalos[4])
    openNotes = sorted(sysexIntervalos[1])

    # --- arma las entradas con el formato del .chart: [tick, [tipo, carril, sustain]]
    umbralSustain = resolution // 3     # los .mid de Harmonix le ponen duracion a TODAS las notas; si dura <= 1/3 de negra no es un sustain real
    entradas = []
    vistos = set()
    for inicio, fin, nota in notas:
        if base <= nota <= base + 4:                        # notas verdes..naranja (carriles 0 a 4)
            sustain = fin - inicio
            if sustain <= umbralSustain:
                sustain = 0
            carril = "7" if cubierto(inicio, openNotes) else str(nota - base)
            if carril == "7":                               # la nota open es una sola, aunque haya varias notas en el mismo tick
                if (inicio, "7") in vistos:
                    continue
                vistos.add((inicio, "7"))
            entradas.append((inicio, "N", carril, sustain))
        elif nota == NOTA_STAR_POWER:
            entradas.append((inicio, "S", "2", fin - inicio))
    for t in sorted({e[0] for e in entradas if e[1] == "N"}):       # modificadores: se agregan en el tick de cada nota que cubren
        if cubierto(t, forzarHopo):
            entradas.append((t, "N", "hopo", 0))
        if cubierto(t, forzarStrum):
            entradas.append((t, "N", "strum", 0))
        if cubierto(t, tap):
            entradas.append((t, "N", "6", 0))
    entradas.sort(key=lambda e: e[0])

    seccion = diff.capitalize() + "Single"
    return {"Song": [["Resolution", str(resolution)]],
            "SyncTrack": syncTrack,
            "Events": [],
            seccion: [[str(t), [tipo, carril, str(s)]] for t, tipo, carril, s in entradas]}


# ===========================================================================
#  PARTE COMUN (sirve para .chart y .mid)
# ===========================================================================
def parse_BPM(rdblChart):           #funcion que parsea las bpm
    Resolution = 192                        #192 es el valor por defecto del formato .chart
    for prop in rdblChart["Song"]:          #extraela resolucion de la cancion
        if prop[0] == 'Resolution':
            Resolution = int(prop[1])
    rawBpmEvents = []     #crea una lista para extraer los cambios de bpm 'crudos' (es decir como estan)
    for x in rdblChart["SyncTrack"]:
        if x[1][0] == "B":                  #solo las lineas de BPM (ignora TS, A, etc.)
            rawBpmEvents.append({'tick': int(x[0]), 'bpm': float(x[1][1])/1000})
    rawBpmEvents.sort(key=lambda e: e["tick"])
    if not rawBpmEvents or rawBpmEvents[0]["tick"] != 0:
        rawBpmEvents.insert(0, {'tick': 0, 'bpm': 120.0})       #si no hay BPM en el tick 0 se asume 120
    time_map = []    #crea el mapa de tiempos
    totMS = 0.0
    for i in range(len(rawBpmEvents)):
        currEvent = rawBpmEvents[i]
        if i > 0:
            prevEvent = rawBpmEvents[i - 1]
            Ticks = currEvent["tick"] - prevEvent["tick"]               #calcula cuantos ticks duro la bpm anterior
            # Formula: (ticks * 60000) / (BPM * Resolution)
            totMS += (Ticks * 60000) / (prevEvent["bpm"] * Resolution)  #transforma los ticks en milisegundos y los acumula
        time_map.append({"tick": currEvent["tick"],
                         "bpm": currEvent["bpm"],        #agrega todo al timemap (ahora tambien el cambio inicial del tick 0)
                         "MS": totMS})
    return time_map, Resolution

def tick2ms(target_tick, time_map, resolution):         #funcion para convertir ticks a milisegundos. esta se usa en la funcion para parsear notas que viene despues
    ActBpm = time_map[0]                                #basicamente, primero asigna la bpm actual a la primera
    for event in time_map:
        if event["tick"] <= target_tick:                #va avanzando de bpms hasta que encuentra la ultima que empieza antes (o en) el tick que se quiere calcular
            ActBpm = event
        else:
            break
    ticks_since_lastBpmChng = target_tick - ActBpm["tick"]                                  #calcula los ticks desde el ultimo cambio de bpm
    ms_since_lastBpmChng = (ticks_since_lastBpmChng * 60000) / (ActBpm["bpm"] * resolution) #con eso, calcula los ms desde el ultimo cambio de bpm
    return ActBpm["MS"] + ms_since_lastBpmChng          #le suma los ms acumulados hasta ese cambio para obtener los ms reales (sin redondear la bpm, si no se va corriendo)

def parseNote(chart, diff, time_map, resolution):#funcion que parsea las notas
    seccion = diff.capitalize() + "Single"
    parsed_notes = {seccion: []} #lista para las notas parseadas
    raw_note_chart = []          #lista para las notas 'crudas'
    for x in chart[seccion]:#recorre cada seccion de las notas y agrega sus datos a la lista de datos crudos
        if x[1][0] in ("N", "S"):                       #ignora los eventos 'E'
            raw_note_chart.append({'tick': int(x[0]),
                                   'type': x[1][0],
                                   'lane': x[1][1],
                                   'sustain': int(x[1][2])})

    # modificadores que vienen como "notas" falsas: 5 = forzar (.chart, invierte hopo/strum), 6 = tap, 'hopo'/'strum' = forzar (.mid)
    modificadores = {}
    for y in raw_note_chart:
        if y['type'] == 'N' and y['lane'] in ('5', '6', 'hopo', 'strum'):
            m = modificadores.setdefault(y['tick'], {'forced': None, 'tap': False})
            if y['lane'] == '6':
                m['tap'] = True
            elif y['lane'] == '5':
                m['forced'] = 'toggle'
            else:
                m['forced'] = y['lane']

    for y in raw_note_chart: #recorre la lista de datos crudos y hace esto:
        if y['type'] == 'N' and y['lane'] in ('5', '6', 'hopo', 'strum'):
            continue                                    #los modificadores no son notas, ya se guardaron arriba
        start_ms = tick2ms(y['tick'], time_map, resolution) #calcula los ms en el que comienza la nota usando la funcion anterior
        end_ms = tick2ms(y['tick'] + y['sustain'], time_map, resolution) #luego hace lo mismo pero sumando lo que dura la nota para calcular cuanto termina
        nota = {'start_ms': round(start_ms), #finalmente agrega los datos en ms a la lista de notas parseadas
                'duration_ms': round(end_ms - start_ms),   #resta el final con el inicio para calcular cuanto dura
                'lane': y['lane'],
                'type': y['type']}
        if y['type'] == 'N':
            mod = modificadores.get(y['tick'], {'forced': None, 'tap': False})
            nota['forced'] = mod['forced']      # None / 'toggle' (.chart) / 'hopo' o 'strum' (.mid)
            nota['tap'] = mod['tap']
        parsed_notes[seccion].append(nota)
    return parsed_notes

def cargarCancion(path, diff="expert"):     #funcion principal: elige el lector segun la extension y devuelve las notas parseadas
    extension = os.path.splitext(path)[1].lower()
    if extension == ".chart":
        rdblFile = leerChart(path, diff)
    elif extension in (".mid", ".midi"):
        rdblFile = leerMidi(path, diff)
    else:
        print("Formato no soportado:", extension)
        return
    if rdblFile is None:
        return
    time_map, resolution = parse_BPM(rdblFile)
    return parseNote(rdblFile, diff, time_map, resolution)


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    canciones = listarCanciones()
    print(len(canciones), "canciones encontradas:\n")
    for c in canciones:
        parse = cargarCancion(c['notas'], "expert")
        if parse:
            notas = [n for n in parse["ExpertSingle"] if n['type'] == 'N']
            print(f"[{c['formato']:5}] {c['nombre']}  ->  {len(notas)} notas (expert)")