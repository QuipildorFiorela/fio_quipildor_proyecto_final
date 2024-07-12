import pygame
from settings import *
from enemies import *
from files import musica

def punto_en_rectangulo(punto, rect):
    x, y = punto
    return x >= rect.left and x <= rect.right and y >= rect.top and y <= rect.bottom

def detectar_colision(rect_1, rect_2):
    return punto_en_rectangulo(rect_1.topleft, rect_2) or \
       punto_en_rectangulo(rect_1.topright, rect_2) or\
       punto_en_rectangulo(rect_1.bottomleft, rect_2) or\
       punto_en_rectangulo(rect_1.bottomright, rect_2) or\
       punto_en_rectangulo(rect_2.topleft, rect_1) or \
       punto_en_rectangulo(rect_2.topright, rect_1) or\
       punto_en_rectangulo(rect_2.bottomleft, rect_1) or\
       punto_en_rectangulo(rect_2.bottomright, rect_1)

def distancia_entre_puntos(pto_1:tuple[int, int], pto_2:tuple[int, int]) -> float:
    base = pto_1[0] - pto_2[0] #0:x 1:y
    altura = pto_1[1] - pto_2[1] 
    return (base ** 2 + altura ** 2) ** 0.5

def manejar_colision(personaje, character_rect, object_list, collision_sound_path=None, special=False): #character rect es la hitbox con la cual comparo
    collision_sound_temp = pygame.mixer.Sound(collision_sound_path)
    for obj in object_list[:]:  # Guardar una copia de la lista para iterar
        if character_rect.colliderect(obj["rect"]):  # la función colliderect() de Pygame, específicamente diseñada para detectar colisiones entre rectángulos.
            if obj['type'] == 'medusa':  # caso colisión con enemigo
                if special:
                    obj['vida'] -= 2
                    print("piumm special")
                    if obj['vida'] <= 0:
                        object_list.remove(obj)
                        collision_sound_temp.play()
                else:
                    obj['vida'] -= 1
                    print("pium -1 bala normal")
                    if obj['vida'] <= 0:
                        object_list.remove(obj)
                        collision_sound_temp.play()
            elif obj['type'] == 'bala':
                object_list['balas'].remove(obj)
            else:
                object_list.remove(obj)
                collision_sound_temp.play()
            return True
    return False

def manejar_colision_con_personaje(personaje, medusas_list, collision_sound_path=None):
    collision_sound_temp = pygame.mixer.Sound(collision_sound_path)
    for medusa in medusas_list[:]:  # Guardar una copia de la lista para iterar
        if personaje['rect'].colliderect(medusa['rect']):
            print("fio golpeada!!!!!!!")
            medusas_list.remove(medusa)
            collision_sound_temp.play()
            personaje['vidas'] -= 1
            print("fio pierde vida!!!!!!!")
            
            return True
    return False

#special ------------------------------
def manejar_special_attack_collision(personaje, nueva_imagen_path, nueva_bala_imagen_path, screen_height):
    personaje['imagen'] = pygame.image.load(nueva_imagen_path).convert_alpha()
    personaje['imagen'] = pygame.transform.scale(personaje['imagen'], FIO_SIZE)
    personaje['bala_imagen_path'] = nueva_bala_imagen_path
    personaje['rect'].size = personaje['imagen'].get_size()  # Asegúrate de actualizar el rectángulo del personaje
    personaje['rect'].bottom = screen_height  # Ajustar la posición del rectángulo del personaje
    personaje['balas_disponibles'] += SPECIAL_BULLETS_QTY
