import pygame
from random import randint
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
FIO_SIZE = (47, 145)
FIO_DEATH_SPRITES_SIZE = (80, 89)
PLAYER_SPEED = 8
DEFAULT_IMAGE_PATH_PLAYER = 'fio_sprites\\basic_gun.png'
DEFAULT_PATH_BALA = 'fio_sprites\\gun_shoot.png'

#de items
COIN_POINT = 50
SPECIAL_BULLETS_QTY = 10

#enemies
ENEMY_POINT = 100 #puntos por cada disparo
SPECIAL_ENEMY_POINT = 250

#pantallas fotos
FONDO_INICIO = pygame.image.load("images\\start_screen.jpg")
FONDO_GAME = pygame.image.load("images\\background_space.jpg")
FONDO_GAME_OVER = pygame.image.load("images\\game_over.jpg")
FONDO_VIEW_SCORES = pygame.image.load("images\\scores_fondo.jpg")

#tuto imagenes ---------------------------------------------------------------------------
tutorial_path_list = ["images\\tutorial\\tuto_0.png", "images\\tutorial\\tuto_1.png", "images\\tutorial\\tuto_2.png", "images\\tutorial\\tuto_3.png", "images\\tutorial\\tuto_4.png"]
current_image_index = 0

# Botones Inicios-------------------------------------------------------------------------------
BOTON_PLAY = pygame.Rect(HALF_WIDTH - 250, HALF_HEIGHT - 85, 152, 64) #152:ancho, 64Llargo
BOTON_EXIT = pygame.Rect(HALF_WIDTH - 250, HALF_HEIGHT, 112, 64)
BOTON_VIEW_SCORE = pygame.Rect(HALF_WIDTH - 250, HALF_HEIGHT - 130, 160, 25) 
BOTON_TUTORIAL = pygame.Rect(HALF_WIDTH - 250, HALF_HEIGHT - 170, 180, 24) 

IMAGEN_BOTON_PLAY = pygame.image.load("images\\texto\\start_button.png")
IMAGEN_BOTON_EXIT = pygame.image.load("images\\texto\\exit_button.png")
IMAGEN_BOTON_VIEW_SCORE = pygame.image.load("images\\texto\\view_score_button.png")
IMAGEN_BOTON_TUTORIAL = pygame.image.load("images\\texto\\tutorial_button.png")

# Botones game over--------------------------------------------------------------------
BOTON_BACK_TO_MENU = pygame.Rect(20, 450, 300, 20) #a: ancho pantalla, b: largo pantalla, c:ancho rect, d:largo rect
BOTON_EXIT_GAME_OVER = pygame.Rect(500, 450, 90, 20)
CUADRO_SCORE = pygame.Rect(175, 15, 250, 107)

IMAGEN_BACK_TO_MENU = pygame.image.load("images\\texto\\back_to_menu.png")
IMAGEN_EXIT_GAME_OVER = pygame.image.load("images\\texto\\exit_game_over.png")
IMAGEN_SCORE = pygame.image.load("images\\texto\\score.png")


#
