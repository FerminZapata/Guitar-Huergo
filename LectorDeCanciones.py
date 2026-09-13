import os, time

os.system("cls")
def rutaCarpetaRaiz():
    return os.path.dirname(__file__)

def createRuta(archivo):
    try:
        path = rutaCarpetaRaiz()
        file_path = os.path.join(path, archivo)
        open(file_path, "r")
        return file_path
    except FileNotFoundError:
        print("Archivo no encontrado, se creara uno nuevo")
        time.sleep(2)
        open(file_path, "w")

def main():
    rutaArchivo = createRuta("notes.chart")
    print(rutaArchivo)
    return rutaArchivo

chart_path = main()

def leerChart(chart):
    try:
        with open(chart, "r", encoding="utf-8") as archivo:
            rdblFile = {'Song': [], 'SyncTrack': [], 'Events': [], 'HardSingle': []}
            contador = 0
            for linea in archivo:
                if "[Song]" in linea or "[SyncTrack]" in linea or "[Events]" in linea or "[HardSingle]" in linea:
                    contador += 1
                else:
                    if contador == 1:
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
                            rdblFile["HardSingle"].append(linea.strip().split(" = "))
                            rdblFile["HardSingle"].append(linea.strip().split(" = "))
        for bpms in rdblFile["SyncTrack"]:
            bpms[1] = bpms[1].split(" ")
        for notes in rdblFile["HardSingle"]:
            notes[1] = notes[1].split(" ")
        print(rdblFile)
    except FileNotFoundError:
        print("No se encontro el archivo.")
        time.sleep(2)
        return

def tick2ms(target_tick, time_map, resolution):
    ActBpm = time_map[0]
    for event in time_map:
        if event["tick"] <= target_tick:
            ActBpm = event
        else:
            break
    ticks_since_lastBpmChng = target_tick - ActBpm["tick"]
    ms_since_lastBpmChng = (ticks_since_lastBpmChng * 60000) / (ActBpm["bpm"] * resolution)
    return ActBpm["MS"] + ms_since_lastBpmChng

def parse_BPM(rdblChart):
    Resolution = rdblChart["Song"][6][1]
    ts = rdblChart["SyncTrack"][1][1]
    time_map = []
    rawBpmEvents = []
    for x in rdblChart["SyncTrack"]:
        if x[1][0] == "TS":
            continue
        else:
            rawBpmEvents.append({'tick': int(x[0]), 'bpm': float(x[1][1]/1000)})

    totMS = 0.0
    for i in range(len(rawBpmEvents)):
        currEvent = rawBpmEvents[i]
        currTick = currEvent["tick"]
        currBPM = currEvent["bpm"]
    # Formula: (ticks * 60000) / (BPM * Resolution)
        if currTick == 0:
            totMS = 0.0
            prevEvent = currEvent
        else:
            Ticks = currTick - prevEvent["tick"]
            ms = (Ticks * 60000) / (prevEvent["bpm"] * Resolution)
            totMS += ms
            time_map.append({"tick": currTick,
                             "bpm": currBPM,
                             "MS": totMS})
            prevEvent = currEvent

def parseNote():
    parsed_notes = []


leerChart(chart_path)