import pygame
from settings import *
#--------------------------------------------------------CSV
def get_path_actual(nombre_archivo):
    import os
    directorio_actual = os.path.dirname(__file__)
    return os.path.join(directorio_actual, nombre_archivo)

#LEE EL ARCHIVO     (name file que te pasen)  "READ", CON ESTO TRABAJO CON LA LISTA DE DICTS
def cargar_archivo_csv(nombre, score):
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
            nombre, score = linea
            scores["nombre"] = nombre
            scores["score"] = int(score)
            
            lista.append(scores)

def save_csv(score, name):
    with open('src/PUNTAJES.csv', 'a') as file:
            file.write(f'{name},{score}\n')


def show_csv(pantalla) -> None: #para mostrar la lista del csv en la pantalla de show_score
    y = 130
    x = 195 
    with open('src\PUNTAJES.csv', 'r') as file:
        file.readline()

        for line in file.readlines():
            # if file.readlines().index(line) > 10: 
            #     break
            line = line.strip('\n').split(',')
            font = pygame.font.Font(None, 25)
            texto_points = font.render(f'{line[0]}   --->   {line[1]}', True, BLACK)
            pantalla.blit(texto_points, (x, y))  
            y += 15 #para q cada score se dibuje 20pixls abajo del otro

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
