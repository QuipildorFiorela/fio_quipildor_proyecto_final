from settings import *


def escalar_imagen(image_path:str,escala:tuple):
    """Cambia el tamaño de una imagen

    Args:
        imagen (una ruta de  imagen): imagen a escalar
        escala (int): escala
    """
    imagen  = pygame.image.load(image_path).convert_alpha()
    new_imagen = pygame.transform.scale(imagen, escala)
    return new_imagen