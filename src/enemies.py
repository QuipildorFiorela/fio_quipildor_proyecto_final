import pygame
from random import randint
from objetos import create_block, load_object_list
from settings import *

def create_enemy(enemy_type, image_path):
    dimension = randint(1000, 2000)/1000 

    if enemy_type == "medusa":
        enemy_width, enemy_height, speed = round(dimension*50), round(dimension*52), randint(3, 6)#round para descartar los decimales
        vida = 2  
    else:
        raise ValueError("Tipo de enemigo no reconocido")

    obj = create_block(randint(0, WIDTH - enemy_width), 0, enemy_width, enemy_height, image_path, speed, enemy_type)
    if enemy_type == 'medusa':
        obj['vida'] = vida

    return obj
