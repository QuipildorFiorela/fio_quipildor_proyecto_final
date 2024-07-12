import pygame
import sys
from settings import *
from character import *
from enemies import *
from objetos import *
from colisiones import manejar_colision, manejar_special_attack_collision, manejar_colision_con_personaje
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


#FLAGS ------------------------------------------------------------------------------------------------
mostrar_inicio_flag = True
mostrar_tutorial_flag = False
mostrar_juego_flag = False
mostrar_game_over_flag = False
mostrar_view_scores_flag = False
mostrando_animacion_muerte = False
pedir_nombre = True

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
    current_time = pygame.time.get_ticks() 
    # Pantalla inicial
    if mostrar_inicio_flag:
        personaje = crear_personaje(HALF_WIDTH, HEIGHT -115, PLAYER_SPEED, DEFAULT_IMAGE_PATH_PLAYER, DEFAULT_PATH_BALA , WIDTH, HEIGHT)

        medusas_list = []
        load_object_list(medusas_list, 'medusa', 0, 'enemies_sprites\\enemy_medusa.png')
        last_medusa_spawn_time = 0
        medusa_spawn_interval = 1500

        coins_list = []
        load_object_list(coins_list, 'coin', 0, 'items_sprites\\coins.png')
        last_coin_spawn_time = 0
        coin_spawn_interval = 2000 

        special_gun_list = []
        load_object_list(special_gun_list, 'special_gun', 0, 'items_sprites\\heavy_machine_gun.png')
        last_shoot_spawn_time = 0
        shoot_spawn_interval = 10000

        score = 0
        mostrar_pantalla_inicio(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BOTON_PLAY.collidepoint(event.pos): 
                    pygame.mixer.Sound(musica["fio_start_game_sound"]).play()
                    pygame.mixer.music.stop() #paro la musica del menu
                    playing_music_flag = False
                    mostrar_inicio_flag = False

                    pygame.time.wait(2000)
                    mostrar_mission_start(SCREEN)
                    mostrar_juego_flag = True
                    start_time = pygame.time.get_ticks()

                    pygame.mixer.music.load(musica["game_music"])
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.music.play()
                    playing_music_flag = True

                if BOTON_EXIT.collidepoint(event.pos):
                    running = False
                if BOTON_TUTORIAL.collidepoint(event.pos):
                    pygame.mixer.Sound(musica["press_button_sound"]).play()
                    mostrar_inicio_flag = False
                    mostrar_tutorial_flag = True
                if BOTON_VIEW_SCORE.collidepoint(event.pos):
                    pygame.mixer.Sound(musica["press_button_sound"]).play()
                    mostrar_inicio_flag = False
                    mostrar_view_scores_flag = True

    elif mostrar_tutorial_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.Sound(musica["press_button_sound"]).play()
                    current_image_index += 1
                    if current_image_index >= len(tutorial_path_list):
                        current_image_index = 0
                if event.key == pygame.K_BACKSPACE:  # Volver a la pantalla de inicio con Backspace
                    pygame.mixer.Sound(musica["press_button_sound"]).play()
                    mostrar_tutorial_flag = False
                    mostrar_inicio_flag = True
        mostrar_tutorial(SCREEN, tutorial_path_list, current_image_index)

    elif mostrar_view_scores_flag:
        mostrar_scores(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:  
                        pygame.mixer.Sound(musica["press_button_sound"]).play()
                        mostrar_view_scores_flag = False
                        mostrar_inicio_flag = True
        pygame.display.flip()

    elif mostrar_juego_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                        disparar_bala(personaje)
                        pygame.mixer.Sound(musica["basic_shoot_gun_sound"]).play()
                if event.key == pygame.K_p: 
                    pause_on(SCREEN)
                    pause_duration = wait_user(pygame.K_p, playing_music_flag, start_time)
                    start_time += pause_duration
                if event.key == pygame.K_m:
                    playing_music_flag = not playing_music_flag #cuando se toca m,not invierte un booleano
        if playing_music_flag: 
            pygame.mixer.music.unpause()
        else:
            mute_on(SCREEN)
            pygame.mixer.music.pause()
            pygame.display.flip()
        # Manejo del estado de las teclas para movimiento fluido con get pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            mover_personaje(personaje, 'izquierda')
        if keys[pygame.K_RIGHT]:
            mover_personaje(personaje, 'derecha')

        # Crear nuevas monedas, el ataque especial y las medusas--------------
        if (current_time - start_time) - last_coin_spawn_time >= coin_spawn_interval:
            coins_list.append(create_object('coin', 'items_sprites\\coins.png'))
            last_coin_spawn_time = (current_time - start_time)

        if (current_time - start_time) - last_shoot_spawn_time >= shoot_spawn_interval:
            special_gun_list.append(create_object('special_gun', 'items_sprites\\heavy_machine_gun.png'))
            last_shoot_spawn_time = (current_time - start_time)

        if (current_time - start_time) - last_medusa_spawn_time >= medusa_spawn_interval:
            for _ in range(2):
                medusas_list.append(create_enemy('medusa', 'enemies_sprites\\enemy_medusa.png'))
                last_medusa_spawn_time = (current_time - start_time)

        # Movimiento de las monedas, balas y enemigos---------------
        move_objects(coins_list, HEIGHT)
        move_objects(special_gun_list, HEIGHT)
        move_objects(medusas_list, HEIGHT)
        mover_balas(personaje, HEIGHT)

        # colisiones--------------------------------------
        if manejar_colision(personaje, personaje['rect'], coins_list, musica["coin_sound"]):
            print("coins!!")
            score = actualizar_puntos(score, COIN_POINT)

        if manejar_colision(personaje, personaje['rect'], special_gun_list, musica["heavy_machine_gun_sound"]):
            print("heavy machine gun!!!!")
            manejar_special_attack_collision(personaje, 'fio_sprites\\HM_gun.png', 'fio_sprites\\heavy_machine_shoot.png', HEIGHT)
            personaje['balas_disponibles'] = 10  # Establezco la cantidad de balas que tiene el powerup

        if personaje['balas_disponibles'] == float('inf'):
            for bala in personaje['balas']:
                if manejar_colision(personaje, bala['rect'], medusas_list, musica["medusa_explosion_sound"]):# Colisión de balas normales con medusas
                    personaje['balas'].remove(bala)
                    score = actualizar_puntos(score, ENEMY_POINT)
        else:
            for special_bala in personaje['balas']:
                if manejar_colision(personaje, special_bala['rect'], medusas_list, musica["medusa_explosion_sound"], special=True):# Colisión de balas especiales con medusas
                    personaje['balas'].remove(special_bala)
                    score = actualizar_puntos(score, ENEMY_POINT)

# Control de colisiones del personaje con medusas
        if manejar_colision_con_personaje(personaje, medusas_list, musica["electric_medusa_sound"]):
            if personaje['vidas'] <= 0:
                pygame.mixer.Sound(musica['electric_medusa_killing_sound']).play()
                pygame.mixer.Sound(musica['fio_death_sound']).play()
                pygame.mixer_music.stop()
                mostrando_animacion_muerte = True
                mostrar_juego_flag = False
                mostrar_game_over_flag = True
                print("GAME OVEEEEEEEEEEEEEEER")
                playing_music_flag = False
                game_over_sonido = pygame.mixer.Sound(musica['game_over_sound']).play()
                game_over_sonido.set_volume(0.2)
        mostrar_juego(SCREEN, current_time, start_time, personaje, coins_list, special_gun_list, medusas_list, score, mostrando_animacion_muerte)
        mostrando_animacion_muerte = False  # Desactivar la bandera después de mostrar la animación

    elif mostrar_game_over_flag:
        mostrar_game_over(SCREEN, score)
        if pedir_nombre:
            print("GAME OVER - Puntaje obtenido:", score)
            # Pedir nombre por consola para guardar en el CSV
            name = input("Ingrese su nombre para guardar en el ranking: ").strip()
            while name == "":  # Validar que el nombre no esté vacío
                print("El nombre no puede estar vacío.")
                name = input("Ingrese su nombre para guardar en el ranking: ").strip()    
            guardado_exito = save_csv(score, name)
        pedir_nombre = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False   
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BOTON_BACK_TO_MENU.collidepoint(event.pos):
                        pygame.mixer.Sound(musica["press_button_sound"]).play()
                        mostrar_game_over_flag = False
                        mostrar_inicio_flag = True #pido por consola un nickname
                if BOTON_EXIT_GAME_OVER.collidepoint(event.pos):
                    running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
