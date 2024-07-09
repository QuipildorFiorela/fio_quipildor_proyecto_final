import pygame
#CONSTANTES--------------------
#de pantalla
WIDTH = 600
HEIGHT = 500
HALF_WIDTH = WIDTH / 2
HALF_HEIGHT = HEIGHT / 2

SCREEN_SIZE = (WIDTH, HEIGHT)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
VERDE = (72, 189, 77)
BORDO = (176, 68, 68)
AQUA = (72, 189, 186)
ROSA = (222, 76, 160)

#de tiempo
FPS = 60

#de personaje
PLAYER_SIZE = (47, 145)
PLAYER_SPEED = 8
DEFAULT_IMAGE_PATH_PLAYER = 'fio_sprites\\basic_gun.png'
DEFAULT_PATH_BALA = 'fio_sprites\\gun_shoot.png'

#de items
COIN_POINT = 100
SPECIAL_BULLETS_QTY = 10