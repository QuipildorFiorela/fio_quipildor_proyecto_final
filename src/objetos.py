from settings import *
import pygame
from random import randint
#OBJETOS EN EL JUEGO: MONEDAS(PUNTOS), HEAVY MACHINE GUN(ATAQUE ESPECIAL+POTENCIA)

def create_block(x, y, width, height, image_path, speed, object_type):
    image = pygame.image.load(image_path).convert_alpha()
    image = pygame.transform.scale(image, (width, height))
    rect = pygame.Rect(x, y, width, height)
    return {'image': image, 'rect': rect, 'speed': speed, 'type': object_type}

def create_object(object_type, image_path):
    object_width, object_height, speed = 0, 0, 0
    
    if object_type == "coin":
        object_width, object_height, speed = 30, 30, randint(2, 4)
    elif object_type == "special_gun":
        object_width, object_height, speed = 35, 35, 3
    else:
        raise ValueError("Tipo de objeto no reconocido")
    
    return create_block(randint(0, WIDTH - object_width), 0, object_width, object_height, image_path, speed, object_type)
                        
def load_object_list(object_list, object_type, cantidad, image_path):
    for _ in range(cantidad): 
        object_list.append(create_object(object_type, image_path))

def draw_objects(pantalla, object_list):
    for obj in object_list:
        pantalla.blit(obj["image"], obj["rect"])

def move_objects(object_list, screen_height):
    for obj in object_list:
        obj["rect"].y += obj["speed"]
        if obj["rect"].y > screen_height:
            object_list.remove(obj)
