from settings import *
from files import *


# PANTALLA INICIO--------------------------------------------------------------------------------
fondo_inicio = pygame.image.load("images\\start_screen.jpg")
fondo_game = pygame.image.load("images\\background_space.jpg")

# Botones Inicios-------------------------------------------------------------------------------
boton_play = pygame.Rect(HALF_WIDTH - 250, HALF_HEIGHT - 85, 152, 64) #152:ancho, 64Llargo
boton_exit = pygame.Rect(HALF_WIDTH - 250, HALF_HEIGHT, 112, 64)
boton_view_score = pygame.Rect(HALF_WIDTH - 250, HALF_HEIGHT - 130, 160, 25) 
boton_tutorial = pygame.Rect(HALF_WIDTH - 250, HALF_HEIGHT - 170, 180, 24) 

texto_boton_play = pygame.image.load("images\\texto\\start_button.png")
texto_boton_exit = pygame.image.load("images\\texto\\exit_button.png")
texto_boton_view_score = pygame.image.load("images\\texto\\view_score_button.png")
texto_boton_tutorial = pygame.image.load("images\\texto\\tutorial_button.png")


def mostrar_pantalla_inicio(pantalla):
    pantalla.blit(fondo_inicio, (0, 0))
    pygame.draw.rect(pantalla, VERDE, boton_play)
    pygame.draw.rect(pantalla, BORDO, boton_exit)
    pygame.draw.rect(pantalla, AQUA, boton_view_score)
    pygame.draw.rect(pantalla, ROSA, boton_tutorial)
    
    pantalla.blit(texto_boton_view_score, (boton_view_score.x, boton_view_score.y))
    pantalla.blit(texto_boton_play, (boton_play.x, boton_play.y))
    pantalla.blit(texto_boton_exit, (boton_exit.x, boton_exit.y))
    pantalla.blit(texto_boton_tutorial, (boton_tutorial.x, boton_tutorial.y))
    
    pygame.display.update()

def mostrar_tutorial(pantalla):
    imagen_tutorial = pygame.image.load("images\\tutorial.png").convert_alpha()
    pantalla.blit(imagen_tutorial, (0, 0))
    pygame.display.update()

def mostrar_mission_start(pantalla):
    texto_mission_start = pygame.image.load("images\\texto\\mission_start.png")
    TEXT_SIZE = (HALF_WIDTH - 200, HALF_HEIGHT - 50, 150, 100)  # Ajuste de posición
    pantalla.blit(fondo_game, (0, 0))
    pantalla.blit(texto_mission_start, TEXT_SIZE)
    pygame.mixer.Sound(musica["mission_start_sound"]).play()
    pygame.display.update()
    pygame.time.wait(2000)


def mostrar_juego():
    pass

def mostrar_game_over():
    pass


def mute_on(pantalla):
    mute_on = pygame.image.load("images\\texto\\mute_on.png").convert_alpha()
    mute_on = pygame.transform.scale(mute_on, (150, 23))
    pantalla.blit(mute_on, (450, 10))
    pygame.display.update()

def pause_on(pantalla):
    pause = pygame.image.load("images\\texto\\pause_game.png").convert_alpha()
    # pause = pygame.transform.scale(pause, (100, 15))
    pantalla.blit(pause, (HALF_WIDTH - 120, HALF_HEIGHT - 50))
    pygame.display.update()


def wait_user(tecla, playing_music_flag):
    continuar = True
    was_playing = playing_music_flag #Si se tocaba musica al principio de la funcion
    pygame.mixer.music.pause() #al pausar pauso la musica sin importar si 

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
        


mission_sound_played = False  # variable para controlar la reproducción del sonido

# TEMPORIZADOR ------------------------------------------------------------------------------------
start_timer = 0
# # Función para mostrar el temporizador
def dibujar_temporizador(pantalla, tiempo_transcurrido):
    font = pygame.font.Font(None, 36)
    minutos = tiempo_transcurrido // 60000 #división sin resto: divide el tiempo en milisegundos por un min en miliseg y toma el cociente
    segundos = (tiempo_transcurrido % 60000) // 1000 #divide el tiempo en miliseg por un min en miliseg y toma el resto
    texto = font.render(f"{minutos:02}:{segundos:02}", True, BLACK)
    pantalla.blit(texto, (255, 10))
