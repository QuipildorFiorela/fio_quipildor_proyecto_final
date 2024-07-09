#--------------------------------------------------------CSV
def get_path_actual(nombre_archivo):
    import os
    directorio_actual = os.path.dirname(__file__)
    return os.path.join(directorio_actual, nombre_archivo)

#LEE EL ARCHIVO     (name file que te pasen)  "READ", CON ESTO TRABAJO CON LA LISTA DE DICTS
def cargar_archivo_csv(nombre, score, tiempo):
    """_summary_

    Args:
        nombre_archivo_data (str): Nombre del archivo de donde se obtendra la informacion
    """
    with open(get_path_actual("puntajes.csv"), "r", encoding="utf-8") as archivo:
        encabezado = archivo.readline().strip("\n").split(",")
        lista = []
        for linea in archivo.readlines():
            scores = {}
            linea = linea.strip("\n").split(",")
            nombre, score, tiempo = linea
            scores["nombre"] = nombre
            scores["score"] = int(score)
            scores["tiempo"] = float(tiempo)
            
            lista.append(scores)

#CARGAR DATOS LISTA EN ARCHIVO NUEVO
def crear_archivo_tipo(bike_type:str, lista_tipo:list):
    with open(get_path_actual(bike_type + ".csv"), "w", encoding="utf-8") as archivo :
        encabezado = ",".join(list(lista_tipo[0].keys())) + "\n"
        archivo.write(encabezado)
        for persona in lista_tipo:
            values = list(persona.values())
            l = []
            for value in values:
                if isinstance(value, int): 
                    l.append(str(value))
                elif isinstance(value, float): 
                    l.append(str(value))
                else:
                    l.append(value)
            linea = ",".join(l) + "\n"
            archivo.write(linea)

#--------------------------------------------------------JSON
def get_path_actual(nombre_archivo):    #Obtiene la ruta completa del archivo en el directorio actual.
    #desde donde se ejecute el archivo, consigo el directorio(la carpeta donde estas parado),le concateno al directorio a la carpeta el nombre del archivo
    """
    Devuelve la ruta completa de un archivo en el directorio actual del script.

    Args:
        nombre_archivo (str): El nombre del archivo para el cual se desea obtener la ruta completa.

    Returns:
        str: La ruta completa del archivo en el directorio actual del script.
    """
    import os
    directorio_actual = os.path.dirname(__file__) 
    return os.path.join(directorio_actual, nombre_archivo)

def load_file(file_to_load): #cargar
    import json
    """
    Carga un archivo JSON y devuelve su contenido.

    Args:
        file_to_load (str): El nombre del archivo JSON a cargar.

    Returns:
        dict or list: El contenido del archivo JSON. Puede ser un diccionario o una lista, dependiendo de la estructura del archivo JSON.

    Raises:
        FileNotFoundError: Si el archivo especificado no se encuentra.
        json.JSONDecodeError: Si el archivo no contiene un JSON válido.
    """
    with open(get_path_actual(file_to_load), "r", encoding="utf-8") as archivo:
        loaded_file = json.load(archivo)
    return loaded_file

def save_list_in_file(lista, nombre_archivo):   #guardar
    import json
    """
    Guarda una lista de diccionarios en un archivo JSON.

    Args:
        lista (list): La lista de diccionarios a guardar.
        nombre_archivo (str): El nombre del archivo donde se guardará la lista.
        indentacion (int, optional): La cantidad de espacios para la indentación en el archivo JSON. El valor por defecto es 4.
    """
    with open(get_path_actual(nombre_archivo), "w", encoding= "utf-8") as archivo:
        saved_list = json.dump(lista, archivo, indent=4)
    return saved_list
