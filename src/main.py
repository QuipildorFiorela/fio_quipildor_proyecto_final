import pygame
import sys
import random

from settings import *
from character import *
from enemies import *
from objetos import *
from colisiones import manejar_colision, ataque_rayo_colision, manejar_special_attack_collision
from def_archivos import *
from pantallas import *
from files import musica

pygame.init()
pygame.mixer.init()

# Pantalla settings
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("FIO'S SPACE ATTACK")
icono = pygame.image.load("images\\fio_icon.png")
pygame.display.set_icon(icono)

# Creo al personaje -----------------------------------------------------------------------------

personaje = crear_personaje(HALF_WIDTH, HEIGHT -115, PLAYER_SPEED, DEFAULT_IMAGE_PATH_PLAYER, DEFAULT_PATH_BALA , WIDTH, HEIGHT)


# Creo los items----------------------------------------------------------------------------------
coins_list = []
load_object_list(coins_list, 'coin', 0, 'items_sprites\\coins.png')
last_coin_spawn_time = 0 
coin_spawn_interval = 2000  # Intervalo de tiempo en milisegundos para crear una nueva moneda

special_gun_list = []
load_object_list(special_gun_list, 'special_gun', 0, 'items_sprites\\heavy_machine_gun.png')
last_shoot_spawn_time = 0
shoot_spawn_interval = 15000


#CONTADOR PUNTOS----------------------------------------------------------------------------------
score = 0

#ARCHIVO CSV


#FLAGS ------------------------------------------------------------------------------------------------
mostrar_inicio_flag = True
mostrar_tutorial_flag = False
mostrar_juego_flag = False
mostrar_game_over_flag = False


# Variables de control----------------------------------------------------------------------------------
running = True
clock = pygame.time.Clock()

pygame.mixer.music.load(musica["menu_music"])
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)#que se repita la cancion

# Estado de pausa y música----------------------------------------------------------------------------
continuar = False


#Cada estado (inicio, juego, game over) tiene su propia lógica para procesar eventos (pygame.event.get()) y actualizar la pantalla en consecuencia.
#region Bucle del juego_________________________________________________________________________________________
while running:
    current_time = pygame.time.get_ticks() #tiempo actual en milisegundos desde que comenzó el juego
    
    # Pantalla inicial
    if mostrar_inicio_flag:
        mostrar_pantalla_inicio(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN: #eventon del click del mouse
                if boton_play.collidepoint(event.pos): #si tocan el boton de play 
                    pygame.mixer.Sound(musica["fio_start_game_sound"]).play()
                    pygame.mixer.music.stop() #paro la musica del menu
                    playing_music_flag = False
                    mostrar_inicio_flag = False

                    pygame.time.wait(2000)# Establece el tiempo para mostrar "Mission Start" después de 2 segundos
                    mostrar_mission_start(SCREEN)

                    pygame.mixer.music.load(musica["game_music"])
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.music.play()
                    playing_music_flag = True

                    mostrar_juego_flag = True
                    start_time = pygame.time.get_ticks()
                    
                if boton_exit.collidepoint(event.pos):
                    running = False
                if boton_tutorial.collidepoint(event.pos):
                    pygame.mixer.Sound(musica["press_button_sound"]).play()
                    mostrar_inicio_flag = False
                    mostrar_tutorial_flag = True
                if boton_view_score.collidepoint(event.pos):
                    pygame.mixer.Sound(musica["press_button_sound"]).play()
                    pass

    if mostrar_tutorial_flag:
        mostrar_tutorial(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:  # Volver a la pantalla de inicio con Backspace
                    pygame.mixer.Sound(musica["press_button_sound"]).play()
                    mostrar_tutorial_flag = False
                    mostrar_inicio_flag = True

    if mostrar_juego_flag:
    #Procesamiento de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:  # disparar al presionar la flecha hacia arriba
                    disparar_bala(personaje)
                    pygame.mixer.Sound(musica["basic_shoot_gun_sound"]).play()
                if event.key == pygame.K_p:  # Pausar o reanudar el juego
                    pause_on(SCREEN)
                    wait_user(pygame.K_p, playing_music_flag)
                if event.key == pygame.K_m:
                    if playing_music_flag:
                        mute_on(SCREEN)
                        pygame.mixer.music.pause()
                        playing_music_flag = False
                        
                    else:
                        pygame.mixer.music.unpause()
                        playing_music_flag = True

        # Manejo del estado de las teclas para movimiento fluido con get pressed
        keys = pygame.key.get_pressed()  # quiero que mientras mantenga la tecla presionada se mueva
        if keys[pygame.K_LEFT]:
            mover_personaje(personaje, 'izquierda')
        if keys[pygame.K_RIGHT]:
            mover_personaje(personaje, 'derecha')

        # Crear nuevas monedas 
        if (current_time - start_time) - last_coin_spawn_time >= coin_spawn_interval:
            coins_list.append(create_object('coin', 'items_sprites\\coins.png'))
            last_coin_spawn_time = (current_time - start_time)
        
        # Crear el ataque especial
        if (current_time - start_time) - last_shoot_spawn_time >= shoot_spawn_interval:
            special_gun_list.append(create_object('special_gun', 'items_sprites\\heavy_machine_gun.png'))
            last_shoot_spawn_time = (current_time - start_time)

        # Crear enemigos 
        if (current_time - start_time) - last_medusa_spawn_time >= medusa_spawn_interval:
            medusas_list.append(create_enemy('medusa', 'enemies_sprites\\enemy_medusa.png'))
            last_medusa_spawn_time = (current_time - start_time)

        # movimiento de las balas
        mover_balas(personaje, HEIGHT)

        # Movimiento de las monedas, balas y enemigos
        move_objects(coins_list, HEIGHT)
        move_objects(special_gun_list, HEIGHT)
        move_objects(medusas_list, HEIGHT)

        # colisiones
        if manejar_colision(personaje['rect'], coins_list, musica["coin_sound"]):
            print("coins!!")
            score = actualizar_puntos(score, COIN_POINT)
        
        if manejar_colision(personaje['rect'], special_gun_list, musica["heavy_machine_gun_sound"]):
            print("heavy machine gun!!!!")
            manejar_special_attack_collision(personaje, 'fio_sprites\\HM_gun.png', 'fio_sprites\\heavy_machine_shoot.png', HEIGHT)
            personaje['balas_disponibles'] = 10  # Establezco la cantidad de balas que tiene el powerup

        if personaje['balas_disponibles'] == float('inf'):
            for bala in personaje['balas']:
                if manejar_colision(bala['rect'], medusas_list, musica["medusa_explosion_sound"]):# Colisión de balas normales con medusas
                    personaje['balas'].remove(bala)
        else:
            
            for special_bala in personaje['special_balas']:
                if manejar_colision(special_bala['rect'], medusas_list, musica["medusa_explosion_sound"], special=True):# Colisión de balas especiales con medusas
                    personaje['balas'].remove(bala)
            
        SCREEN.blit(fondo_game, (0, 0))  # Actualizar pantalla de juego antes de dibujar el personaje
    
        dibujar_contador_balas(SCREEN, personaje['balas_disponibles'])
        dibujar_contador_puntos(SCREEN, score)
        draw_objects(SCREEN, coins_list)
        draw_objects(SCREEN, special_gun_list)
        draw_objects(SCREEN, medusas_list)
        dibujar_personaje(SCREEN, personaje) #dibujo al personaje
        dibujar_balas(SCREEN, personaje)
        tiempo_transcurrido = current_time - start_time
        dibujar_temporizador(SCREEN, tiempo_transcurrido)

        if not playing_music_flag:
            mute_on(SCREEN)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
