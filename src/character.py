import pygame
from settings import *
# character.py
pygame.init()


def crear_personaje(x, y, velocidad, imagen_path, bala_path, screen_width, screen_height):
    imagen = pygame.image.load(imagen_path).convert_alpha()
    imagen = pygame.transform.scale(imagen, PLAYER_SIZE)  # Cambiar el tamaño de la imagen del personaje
    personaje = {
        'imagen': imagen,
        'imagen_default': imagen_path,  # Imagen del personaje por defecto
        'rect': pygame.Rect(x, y, 0, 0),
        'velocidad': velocidad,
        'screen_width': screen_width,
        'vidas': 3,  # Vidas del personaje
        'balas': [],   # Lista para almacenar las balas disparadas por el personaje
        'special_balas': [],
        'balas_disponibles': float('inf'),  # Balas disponibles (por defecto infinitas),
        'bala_imagen_path': bala_path  # Imagen por defecto de la bala
    }
    personaje['rect'].size = personaje['imagen'].get_size()
    personaje['rect'].bottom = screen_height  # Ajustar el bottom al crear el personaje
    return personaje

def mover_personaje(personaje, direccion):
    if direccion == "izquierda" and personaje['rect'].left > 0: #si se mueve para la izq mientras que sea mayor al 0 del eje x (así no se sale de la pantalla)
        personaje['rect'].x -= personaje['velocidad'] #se mueve 5 pixeles hacia la izq
    if direccion == "derecha" and personaje['rect'].right < personaje['screen_width']: 
        personaje['rect'].x += personaje['velocidad']

def dibujar_personaje(pantalla, personaje):
    pantalla.blit(personaje['imagen'], personaje['rect'].topleft)
    # dibujar_contador_vidas(pantalla, personaje)
    dibujar_balas(pantalla, personaje)
    dibujar_contador_vidas(pantalla, personaje)

#VIDAS------------------------------------------------------------------------------------

def dibujar_contador_vidas(pantalla, personaje):
    vida_3_imagen_path = pygame.image.load('images\\texto\\lifes_3.png').convert_alpha()
    vida_3_imagen_path = pygame.transform.scale(vida_3_imagen_path, (140, 16))

    vida_2_imagen_path = pygame.image.load('images\\texto\\lifes_2.png').convert_alpha()
    vida_2_imagen_path = pygame.transform.scale(vida_2_imagen_path, (140, 16))

    vida_1_imagen_path = pygame.image.load('images\\texto\\lifes_1.png').convert_alpha()
    vida_1_imagen_path = pygame.transform.scale(vida_1_imagen_path, (140, 16))

    vida_x = 10
    vida_y = 8

    if personaje['vidas'] == 3:
        vida_imagen = vida_3_imagen_path
    elif personaje['vidas'] == 2:
        vida_imagen = vida_2_imagen_path
    else:
        vida_imagen = vida_1_imagen_path

    pantalla.blit(vida_imagen, (vida_x, vida_y))

def actualizar_vidas(personaje, cantidad):
    personaje['vidas'] += cantidad
    if personaje['vidas'] > 3:
        personaje['vidas'] = 3
    if personaje['vidas'] < 0:
        personaje['vidas'] = 0

#SCORE COINS-------------------------------------------------------------------------------------------------

def dibujar_contador_puntos(pantalla, puntos):
    fondo_contador = pygame.image.load("images\\texto\\points.png").convert_alpha()
    fondo_contador = pygame.transform.scale(fondo_contador, (80, 14))  # Ajusta el tamaño según sea necesario
    font = pygame.font.Font(None, 22)
    texto_points = font.render(f"{puntos}", True, BLACK)

    # Coordenadas para dibujar el fondo y el texto
    fondo_x = 10
    fondo_y = 30
    texto_x = fondo_x + 80  # Ajusta la posición X del texto
    texto_y = fondo_y   # Ajusta la posición Y del texto

    pantalla.blit(fondo_contador, (fondo_x, fondo_y))
    pantalla.blit(texto_points, (texto_x, texto_y))

def actualizar_puntos(score, cantidad):
    score += cantidad
    return score


#BALAS---------------------------------------------------------------------------------------------------
def disparar_bala(personaje):
    if personaje['balas_disponibles'] > 0:
        bala_imagen = pygame.image.load(personaje['bala_imagen_path']).convert_alpha()
        bala_imagen = pygame.transform.scale(bala_imagen, (10, 20))  # Ajusta el tamaño de la imagen de la bala
        bala_rect = bala_imagen.get_rect(midtop=personaje['rect'].midtop)  # Se disparan del top/2 del personaje
        bala = {
            'imagen': bala_imagen,
            'rect': bala_rect,
            'velocidad': -10  # Velocidad hacia arriba (negativa en Y)
        }
        personaje['balas'].append(bala)  # Agregar la bala a la lista

        if personaje['balas_disponibles'] != float('inf'):  # Evaluar el caso de las balas del ataque especial, las cuales son limitadas
            personaje['balas_disponibles'] -= 1  # Disminuir el contador

        # Restaurar el personaje a su imagen por defecto si se quedan sin balas especiales
        if personaje['balas_disponibles'] == 0:
            personaje['imagen'] = pygame.image.load(personaje['imagen_default']).convert_alpha()
            personaje['imagen'] = pygame.transform.scale(personaje['imagen'], PLAYER_SIZE)
            personaje['bala_imagen_path'] = DEFAULT_PATH_BALA
            print("Se acabaron las balas especiales")
            
    else:
        # Añadir una nueva bala común a la lista de balas
        bala_imagen_comun = pygame.image.load(DEFAULT_PATH_BALA).convert_alpha()
        bala_imagen_comun = pygame.transform.scale(bala_imagen_comun, (10, 20))
        bala_rect_comun = bala_imagen_comun.get_rect(midtop=personaje['rect'].midtop)
        nueva_bala_comun = {
            'imagen': bala_imagen_comun,
            'rect': bala_rect_comun,
            'velocidad': -10
        }
        personaje['balas'].append(nueva_bala_comun)
        personaje['balas_disponibles'] = float('inf')


def dibujar_balas(pantalla, personaje):
    for bala in personaje['balas']:
        pantalla.blit(bala['imagen'], bala['rect'])

def dibujar_contador_balas(pantalla, balas_disponibles):
    fondo_contador = pygame.image.load("images\\texto\\arms.png").convert_alpha()
    fondo_contador = pygame.transform.scale(fondo_contador, (85, 36))  # Ajusta el tamaño según sea necesario

    fuente = pygame.font.Font(None, 20)
    if balas_disponibles == float('inf'):
        texto = "Balas: inf"
    else:
        texto = f"Balas: {balas_disponibles}"
    texto_render = fuente.render(texto, True, BLACK)

    # Coordenadas para dibujar el fondo y el texto
    fondo_x = 8
    fondo_y = 50
    texto_x = fondo_x + 14  # Ajusta la posición X del texto
    texto_y = fondo_y + 22  # Ajusta la posición Y del texto

    pantalla.blit(fondo_contador, (fondo_x, fondo_y))
    pantalla.blit(texto_render, (texto_x, texto_y))

def mover_balas(personaje, screen_height):
    for bala in personaje['balas'][:]:  # Usar una copia para poder eliminar elementos dentro del bucle
        bala['rect'].y += bala['velocidad']
        if bala['rect'].bottom < 0: #si se va de la pantalla elimino la bala de la lista así no se acumula
            personaje['balas'].remove(bala)


