import os, time

os.system("cls")
def rutaCarpetaRaiz():              #extrae la ruta de la carpeta
    return os.path.dirname(__file__)

def createRuta(archivo):            #crea una ruta con la cual se puede abrir el archivo. Si no existe, crea uno nuevo
    try:
        path = rutaCarpetaRaiz()
        file_path = os.path.join(path, archivo)
        open(file_path, "r")
        return file_path
    except FileNotFoundError:
        print("Archivo no encontrado, se creara uno nuevo")
        time.sleep(2)
        open(file_path, "w")

def main():                         #Termina de crear la ruta para su apertura
    rutaArchivo = createRuta("notes.chart")
    print(rutaArchivo)
    return rutaArchivo

chart_path = main()

def leerChart(chart):       #Funcion que convierte el chart en un diccionario legible con listas
    try:
        with open(chart, "r", encoding="utf-8") as archivo:         # se abre el archivo
            rdblFile = {'Song': [], 'SyncTrack': [], 'Events': [], 'ExpertSingle': [], 'HardSingle': [], 'MediumSingle': [], 'EasySingle': []}        #se crea el diccionario
            contador = 0
            for linea in archivo:
                if "[Song]" in linea or "[SyncTrack]" in linea or "[Events]" in linea or "[HardSingle]" in linea or "[ExpertSingle]" in linea or "[EasySingle]" in linea or "[MediumSingle]" in linea:
                    contador += 1
                else:
                    if contador == 1:                   #se agrega cada linea separada basado en si
                        if "{" in linea or "}" in linea:
                            continue
                        else:
                            rdblFile["Song"].append(linea.strip().split(" = "))
                    elif contador == 2:
                        if "{" in linea or "}" in linea:
                            continue
                        else:
                            rdblFile["SyncTrack"].append(linea.strip().split(" = "))
                    elif contador == 3:
                        if "{" in linea or "}" in linea:
                            continue
                        else:
                            rdblFile["Events"].append(linea.strip().split(" = "))
                    elif contador == 4:
                        if "{" in linea or "}" in linea:
                            continue
                        else:
                            rdblFile["ExpertSingle"].append(linea.strip().split(" = "))
                    elif contador == 5:
                        if "{" in linea or "}" in linea:
                            continue
                        else:
                            rdblFile["HardSingle"].append(linea.strip().split(" = "))
                    elif contador == 6:
                        if "{" in linea or "}" in linea:
                            continue
                        else:
                            rdblFile["MediumSingle"].append(linea.strip().split(" = "))
                    elif contador == 7:
                        if "{" in linea or "}" in linea:
                            continue
                        else:
                            rdblFile["EasySingle"].append(linea.strip().split(" = "))
        for bpms in rdblFile["SyncTrack"]:          # termina de separar las lineas
            bpms[1] = bpms[1].split(" ")
        for notes in rdblFile["ExpertSingle"]:
            notes[1] = notes[1].split(" ")
        for notes in rdblFile["HardSingle"]:
            notes[1] = notes[1].split(" ")
        for notes in rdblFile["MediumSingle"]:
            notes[1] = notes[1].split(" ")
        for notes in rdblFile["EasySingle"]:
            notes[1] = notes[1].split(" ")
        print(rdblFile)
        return rdblFile
    except FileNotFoundError:
        print("No se encontro el archivo.")
        time.sleep(2)
        return

def parse_BPM(rdblChart):           #funcion que parsea las bpm
    Resolution = int(rdblChart["Song"][6][1])   #extraela resolucin de la cancion
    time_map = []    #crea el mapa de tiempos
    rawBpmEvents = []     #crea una lista para extraer los cambios de bpm 'crudos' (es decir como estan)
    for x in rdblChart["SyncTrack"]:
        if x[1][0] == "TS":
            continue
        else:
            rawBpmEvents.append({'tick': int(x[0]), 'bpm': float(x[1][1])/1000})    #a menos que la linea diga ts, agrega
    totMS = 0.0                                                                     #un mini diccionario a la lista con el
    for i in range(len(rawBpmEvents)):                                              #tick y la bpm correspondiente par cada cambio
        currEvent = rawBpmEvents[i]
        currTick = currEvent["tick"]
        currBPM = currEvent["bpm"]
    # Formula: (ticks * 60000) / (BPM * Resolution)
        if int(currTick) == 0:          # si es el cambio inicial
            totMS = 0.0                 #miliegundos acumulados totales es igual a 0
            prevEvent = currEvent       #la bpm de ahora se convierte en el cambio anterior
        else:
            Ticks = currTick - prevEvent["tick"]        #calcula cuantos ticks dura la bpm actual
            ms = (Ticks * 60000) / (prevEvent["bpm"] * Resolution)  #transforma los ticks en milisegundos
            totMS += ms                 #agrega esos milisegundos a los milisegundos totales
            time_map.append({"tick": currTick,
                             "bpm": currBPM,        #agrega todo al timemap
                             "MS": totMS})
            prevEvent = currEvent
    return time_map, Resolution

def tick2ms(target_tick, time_map, resolution):         #funcion para convertir ticks a milisegundos. esta se usa en la funcion para parsear notas que viene despues
    ActBpm = time_map[0]                                #basicamente, primero asigna la bpm actual a la primera
    for event in time_map:
        if int(event["tick"]) <= int(target_tick):      #para calcular bien los ms, va avanzando de bpms hasta que encuentra una mayor o igual al tick que se quiere calcular (lo que permite calcular los ms con el bpm en elque este tick esta)
            ActBpm = event
        else:
            break
    ticks_since_lastBpmChng = int(target_tick) - int(ActBpm["tick"])    #calcula los ticks desde el ultimo cambio de bpm
    ms_since_lastBpmChng = (int(ticks_since_lastBpmChng) * 60000) / (int(ActBpm["bpm"]) * int(resolution)) #con eso, hace esta cuenta para calcular los ms desde el ultimo cambio de bpm
    return int(ActBpm["MS"]) + int(ms_since_lastBpmChng)     #le agrega a los ms calculados anteriormete a los actuales para hacer los ms reales

def parseNote(chart, time_map, resolution):    #funcion que parsea las notas
    parsed_notes = {'ExpertSingle': [], 'HardSingle': [], 'MediumSingle': [], 'EasySingle': []}              #crea una lista para las notas parseadas
    raw_note_chart = {'ExpertSingle': [], 'HardSingle': [], 'MediumSingle': [], 'EasySingle': []}          #y una para las notas 'crudas'
    for x in chart["ExpertSingle"]:   #recorre cada seccion de las notas y agrega sus datos a la lista de dtos crudos
        raw_note_chart["ExpertSingle"].append(({'tick': x[0],
                                                'type': x[1][0],
                                                'lane': x[1][1],
                                                'sustain': x[1][2]}))
    for x in chart["HardSingle"]:   
        raw_note_chart["HardSingle"].append(({'tick': x[0],
                                                'type': x[1][0],
                                                'lane': x[1][1],
                                                'sustain': x[1][2]}))
    for x in chart["MediumSingle"]:   
        raw_note_chart["MediumSingle"].append(({'tick': x[0],
                                                'type': x[1][0],
                                                'lane': x[1][1],
                                                'sustain': x[1][2]}))
    for x in chart["EasySingle"]:
        raw_note_chart["EasySingle"].append(({'tick': x[0],
                                                'type': x[1][0],
                                                'lane': x[1][1],
                                                'sustain': x[1][2]}))
    count = 1
    for x in raw_note_chart:
        for notes in x:   #recorre la lista de datos crudos y hace esto:
            lane = x['lane']    #extrae la columan en la que esta
            start_ms = tick2ms(int(x['tick']), time_map, resolution)    #calcula los ms en el que comienza la nota usando la funcion anterior
            end_ms = tick2ms((int(x['tick']) + int(x['sustain'])), time_map, resolution)   #luego hace lo mismo pero sumando lo que dura la nota para calcular cuanto termina
            duration_ms = end_ms - start_ms   #resta el final con el inicio para calcular cuanto dura
            if count == 1:
                parsed_notes["ExpertSingle"].append({'start_ms': start_ms,          #finalmente agrega los datos en ms a la lista de notas parseadas
                                    'duration_ms': duration_ms,
                                    'lane': lane
                                    })
            if count == 2:
                parsed_notes["HardSingle"].append({'start_ms': start_ms,          #finalmente agrega los datos en ms a la lista de notas parseadas
                                    'duration_ms': duration_ms,
                                    'lane': lane
                                    })
            if count == 3:
                parsed_notes["MediumSingle"].append({'start_ms': start_ms,          #finalmente agrega los datos en ms a la lista de notas parseadas
                                    'duration_ms': duration_ms,
                                    'lane': lane
                                    })
            if count == 4:
                parsed_notes["EasySingle"].append({'start_ms': start_ms,          #finalmente agrega los datos en ms a la lista de notas parseadas
                                    'duration_ms': duration_ms,
                                    'lane': lane
                                    })
            count += 1
    return parsed_notes



rdblFile = leerChart(chart_path)

time_map = parse_BPM(rdblFile)

parseNote(rdblFile, time_map[0], time_map[1])