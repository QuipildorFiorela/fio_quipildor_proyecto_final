import pygame
from settings import *
from def_archivos import show_csv
from files import musica
from character import dibujar_contador_balas, dibujar_contador_puntos, mostrar_animacion_muerte, dibujar_balas, dibujar_personaje, cargar_animacion_muerte
from objetos import draw_objects

def mostrar_pantalla_inicio(pantalla):
    pantalla.blit(FONDO_INICIO, (0, 0))
    pygame.draw.rect(pantalla, VERDE, BOTON_PLAY)
    pygame.draw.rect(pantalla, BORDO, BOTON_EXIT)
    pygame.draw.rect(pantalla, AQUA, BOTON_VIEW_SCORE)
    pygame.draw.rect(pantalla, ROSA, BOTON_TUTORIAL)
    
    pantalla.blit(IMAGEN_BOTON_VIEW_SCORE, (BOTON_VIEW_SCORE.x, BOTON_VIEW_SCORE.y))
    pantalla.blit(IMAGEN_BOTON_PLAY, (BOTON_PLAY.x, BOTON_PLAY.y))
    pantalla.blit(IMAGEN_BOTON_EXIT, (BOTON_EXIT.x, BOTON_EXIT.y))
    pantalla.blit(IMAGEN_BOTON_TUTORIAL, (BOTON_TUTORIAL.x, BOTON_TUTORIAL.y))
    
    pygame.display.update()

def mostrar_tutorial(pantalla, lista_imagenes, indice):
    lista = []
    for path in lista_imagenes:
        imagen = pygame.image.load(path).convert_alpha()
        lista.append(imagen)
    pantalla.blit(lista[indice], (0, 0))
    pygame.display.update()

def mostrar_mission_start(pantalla):
    texto_mission_start = pygame.image.load("images\\texto\\mission_start.png")
    TEXT_SIZE = (HALF_WIDTH - 200, HALF_HEIGHT - 50, 150, 100)  # Ajuste de posición

    pantalla.blit(FONDO_GAME, (0, 0))
    pantalla.blit(texto_mission_start, TEXT_SIZE)
    pygame.mixer.Sound(musica["mission_start_sound"]).play()
    pygame.display.update()
    pygame.time.wait(2000)


def mostrar_juego(pantalla, current_time, start_time, personaje, coins_list, special_gun_list, medusas_list, score, mostrando_animacion_muerte):
    death_sprites_path_list = ["fio_death_sprites\\electrical_death\\0.png", "fio_death_sprites\\electrical_death\\1.png", "fio_death_sprites\\electrical_death\\2.png", "fio_death_sprites\\electrical_death\\3.png", "fio_death_sprites\\electrical_death\\4.png", "fio_death_sprites\\electrical_death\\5.png"]
    image_death_sprites = cargar_animacion_muerte(death_sprites_path_list, FIO_DEATH_SPRITES_SIZE)

    pantalla.blit((FONDO_GAME), (0, 0))  # Actualizar pantalla de juego antes de dibujar el personaje

    dibujar_contador_balas(pantalla, personaje['balas_disponibles'])
    dibujar_contador_puntos(pantalla, score)
    draw_objects(pantalla, coins_list)
    draw_objects(pantalla, special_gun_list)
    draw_objects(pantalla, medusas_list)
    if mostrando_animacion_muerte:
        mostrar_animacion_muerte(pantalla, personaje, image_death_sprites)
        pygame.time.wait(1250)
    else:
        dibujar_personaje(pantalla, personaje)  # Dibujar al personaje si no se está mostrando la animación de muerte
        dibujar_balas(pantalla, personaje)
    tiempo_transcurrido = current_time - start_time
    dibujar_temporizador(pantalla, tiempo_transcurrido)

def mostrar_game_over(pantalla, score):
    pantalla.blit(FONDO_GAME_OVER, (0, 0))
    pygame.draw.rect(pantalla, BLACK, BOTON_BACK_TO_MENU)
    pygame.draw.rect(pantalla, BLACK, BOTON_EXIT_GAME_OVER)
    pygame.draw.rect(pantalla, BLACK, CUADRO_SCORE)

    font = pygame.font.Font(None, 60)
    texto_score = font.render(f"{score}", True, BLACK)
    texto_x =  CUADRO_SCORE.x + 70# Ajusta la posición X del texto
    texto_y = 60  # Ajusta la posición Y del texto

    
    pantalla.blit(IMAGEN_BACK_TO_MENU, (BOTON_BACK_TO_MENU.x, BOTON_BACK_TO_MENU.y))
    pantalla.blit(IMAGEN_EXIT_GAME_OVER, (BOTON_EXIT_GAME_OVER.x, BOTON_EXIT_GAME_OVER.y))
    pantalla.blit(IMAGEN_SCORE, (CUADRO_SCORE.x, CUADRO_SCORE.y))
    pantalla.blit(texto_score, (texto_x, texto_y))
    pygame.display.update()
    
def mostrar_scores(pantalla):
    pantalla.blit(FONDO_VIEW_SCORES, (0, 0))
    show_csv(pantalla)
    pygame.display.update()

def mute_on(pantalla):
    mute_on = pygame.image.load("images\\texto\\mute_on.png").convert_alpha()
    mute_on = pygame.transform.scale(mute_on, (150, 23))
    pantalla.blit(mute_on, (440, 10))

def pause_on(pantalla):
    pause = pygame.image.load("images\\texto\\pause_game.png").convert_alpha()
    # pause = pygame.transform.scale(pause, (100, 15))
    pantalla.blit(pause, (HALF_WIDTH - 120, HALF_HEIGHT - 50))
    pygame.display.update()

def wait_user(tecla, playing_music_flag, start_time):
    continuar = True
    was_playing = playing_music_flag  # Si se tocaba música al principio de la función
    pygame.mixer.music.pause()  # Al pausar, pauso la música sin importar si se estaba tocando

    pause_start_time = pygame.time.get_ticks()  # Capturar el tiempo actual cuando se entra en pausa

    while continuar:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuar = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == tecla:
                    continuar = False

    if was_playing:
        pygame.mixer.music.unpause()

    pause_end_time = pygame.time.get_ticks()  # Capturar el tiempo actual cuando se sale de la pausa
    pause_duration = pause_end_time - pause_start_time  # Calcular la duración de la pausa

    return pause_duration  # Devolver la duración de la pausa

mission_sound_played = False  # variable para controlar la reproducción del sonido

# TEMPORIZADOR ------------------------------------------------------------------------------------
# start_timer = 0
# # Función para mostrar el temporizador
def dibujar_temporizador(pantalla, tiempo_transcurrido):
    font = pygame.font.Font(None, 36)
    minutos = tiempo_transcurrido // 60000 #división sin resto: divide el tiempo en milisegundos por un min en miliseg y toma el cociente
    segundos = (tiempo_transcurrido % 60000) // 1000 #divide el tiempo en miliseg por un min en miliseg y toma el resto
    texto = font.render(f"{minutos:02}:{segundos:02}", True, BLACK)
    pantalla.blit(texto, (255, 10))
