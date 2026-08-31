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
    rutaArchivo = createRuta("gastos.csv")
    print(rutaArchivo)
    return rutaArchivo

def leerChart(chart):
    