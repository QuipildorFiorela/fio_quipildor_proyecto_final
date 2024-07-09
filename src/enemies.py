import pygame
import random
from objetos import *
from settings import *
from esenciales import *

def create_enemy(enemy_type, image_path):
    enemy_width, enemy_height, speed = 0, 0, 0

    if enemy_type == "medusa":
        enemy_width, enemy_height, speed = 50, 52, random.randint(2, 3)
        vida = 4  # Vida de la medusa
    else:
        raise ValueError("Tipo de enemigo no reconocido")

    obj = create_block(random.randint(0, WIDTH - enemy_width), 0, enemy_width, enemy_height, image_path, speed, enemy_type)
    if enemy_type == 'medusa':
        obj['vida'] = vida

    return obj

def create_rayo(medusa):
    rayo = {
        'rect': pygame.Rect(medusa['rect'].centerx, medusa['rect'].bottom, 5, 20),  # Tamaño y posición inicial del rayo
        'speed': 7,  # Velocidad del rayo
        'damage': 1  # Daño que hace al personaje
    }
    return rayo

# Creo los enemigos -----------------------------------------------------------------------------
medusas_list = []
load_object_list(medusas_list, 'medusa', 0, 'enemies_sprites\\enemy_medusa.png')
last_medusa_spawn_time = 0
medusa_spawn_interval = 4000

# Listas para rayos disparados por medusas
rayos_list = []
rayo_spawn_interval = 1500  # Intervalo de tiempo en milisegundos para disparar un rayo
last_rayo_spawn_time = 0