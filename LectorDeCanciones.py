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
        rdblFile = []
        with open(chart, "r", encoding="utf-8") as archivo:
            for line in archivo:
                if '{' in line or '}' in line:
                    continue
                else:
                    tempVal = line.strip().split(" ")
                    rdblFile.append(tempVal)
        rdblFile.pop(0)
        print(rdblFile)
    except FileNotFoundError:
        print("No se encontro el archivo.")
        time.sleep(2)
        return

filepath = main()

leerChart(filepath)