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
                            rdblFile["SyncTrack"].append(str(linea.strip().split(" = ")))
                    elif contador == 3:
                        if "{" in linea or "}" in linea: 
                            continue
                        else:
                            rdblFile["Events"].append(str(linea.strip().split(" = ")))
                    elif contador == 4:
                        if "{" in linea or "}" in linea: 
                            continue
                        else:
                            rdblFile["HardSingle"].append(str(linea.strip().split(" = ")))
        print(rdblFile)
    except FileNotFoundError:
        print("No se encontro el archivo.")
        time.sleep(2)
        return

filepath = main()

leerChart(filepath)