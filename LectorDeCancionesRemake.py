import os, time

os.system("cls")

def rutaCarpetaRaiz():              #extrae la ruta de la carpeta
    return os.path.dirname(__file__)

def createRuta(archivo):            #crea una ruta con la cual se puede abrir el archivo.
    try:
        path = rutaCarpetaRaiz()
        file_path = os.path.join(path, archivo)
        open(file_path, "r")
        return file_path
    except FileNotFoundError:
        print("No se encontro el archivo")

def main():                         #Termina de crear la ruta para su apertura
    rutaArchivo = createRuta("notes.chart")
    print(rutaArchivo)
    return rutaArchivo

def leerChart(path,diff):#Funcion que devuelve una difficultad del archivo .chart en un diccionario
    try:
        with open(path, "r", encoding="utf-8") as archivo:
            data = archivo.read()
            rdblFile = {'Song': [], 'SyncTrack': [], 'Events': []}
            if diff.lower() == "expert" and "[ExpertSingle]" in data:
                rdblFile["ExpertSingle"] = []
            elif diff.lower() == "hard" and "[HardSingle]" in data:
                rdblFile["HardSingle"] = []
            elif diff.lower() == "medium" and "[MediumSingle]" in data:
                rdblFile["MediumSingle"] = []
            elif diff.lower() == "easy" and "[EasySingle]" in data:
                rdblFile["EasySingle"] = []
            contador = 0
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

def parse_BPM(rdblChart):           #funcion que parsea las bpm
    for prop in rdblChart["Song"]:          #extraela resolucion de la cancion
        if 'Resolution' in prop:
            Resolution = int(prop[1])
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

def parseNote(chart, diff, time_map, resolution):#funcion que parsea las notas
    parsed_notes = {diff+"Single":[]} #lista para las notas parseadas
    raw_note_chart = {diff+"Single":[]} #lista para las notas 'crudas'
    for x in chart[diff+"Single"]:#recorre cada seccion de las notas y agrega sus datos a la lista de datos crudos
        if 'E' not in x[1]:
            raw_note_chart[diff+"Single"].append(({'tick': x[0],
                                                    'type': x[1][0],
                                                    'lane': x[1][1],
                                                    'sustain': x[1][2]}))

    for x in raw_note_chart:
        for y in raw_note_chart[x]: #recorre la lista de datos crudos y hace esto:
            lane = y['lane'] #extrae la columna en la que esta
            type = y['type']
            start_ms = tick2ms(int(y['tick']), time_map, resolution) #calcula los ms en el que comienza la nota usando la funcion anterior
            end_ms = tick2ms((int(y['tick']) + int(y['sustain'])), time_map, resolution) #luego hace lo mismo pero sumando lo que dura la nota para calcular cuanto termina
            duration_ms = end_ms - start_ms #resta el final con el inicio para calcular cuanto dura
            parsed_notes[diff+"Single"].append({'start_ms': start_ms, #finalmente agrega los datos en ms a la lista de notas parseadas
                                'duration_ms': duration_ms,
                                'lane': lane,
                                'type': type
                                })
    return parsed_notes

chart_path = main()

rdblFile = leerChart(chart_path,"expert")

time_map = parse_BPM(rdblFile)

parse = parseNote(rdblFile, "Expert", time_map[0], time_map[1])