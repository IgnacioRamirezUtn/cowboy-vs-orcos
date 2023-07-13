import pygame
import sys
import pygame.font
import json
from constantes import *
from player import Player
from enemy import Enemy
from othersclass import PowerUp
from othersclass import Plataforma
from othersclass import Obstacle 

pygame.font.init()
font = pygame.font.Font(None, 24)

screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

pygame.init()
pygame.display.set_caption("Cowboy vs Ogros")
clock = pygame.time.Clock()

imagen_fondo = pygame.image.load("images/locations/forest/all.png")
imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO_VENTANA, ALTO_VENTANA))

delta_ms = clock.tick(FPS)
LEVEL_DURATION = 2000



def leer_archivo(nombre_archivo: str, nombre_variable_json: str):
    with open(nombre_archivo, "r") as archivo:
        data = json.load(archivo)
        return data[nombre_variable_json]
# Llamar a la función para obtener las plataformas de cada nivel
plataformas_nivel_1 = leer_archivo("C:\\Users\\Administrador\\Desktop\\CLASE_19_inicio_juego\\parametros.json", "plataformas_data")["plataformas_1"]
plataformas_nivel_2 = leer_archivo("C:\\Users\\Administrador\\Desktop\\CLASE_19_inicio_juego\\parametros.json", "plataformas_data")["plataformas_2"]
plataformas_nivel_3 = leer_archivo("C:\\Users\\Administrador\\Desktop\\CLASE_19_inicio_juego\\parametros.json", "plataformas_data")["plataformas_3"]


plataformas1=[]
plataformas2=[]
plataformas3=[]
for plataforma_data in plataformas_nivel_1:
    plataforma = Plataforma(
        plataforma_data["x"],
        plataforma_data["y"],
        plataforma_data["width"],
        plataforma_data["height"],
        plataforma_data["image_path"]
    )
    plataformas1.append(plataforma)

for plataforma_data in plataformas_nivel_2:
    plataforma = Plataforma(
        plataforma_data["x"],
        plataforma_data["y"],
        plataforma_data["width"],
        plataforma_data["height"],
        plataforma_data["image_path"]
    )
    plataformas2.append(plataforma)

for plataforma_data in plataformas_nivel_3:
    plataforma = Plataforma(
        plataforma_data["x"],
        plataforma_data["y"],
        plataforma_data["width"],
        plataforma_data["height"],
        plataforma_data["image_path"]
    )
    plataformas3.append(plataforma)


plataformas=plataformas1

powerup = PowerUp(1200, 80, 30, 30)
player_1 = Player(0, 0, 4, 8, 8, 32)
enemies = [Enemy(800, 500, 3,0,ANCHO_VENTANA)]
obstacle = Obstacle(550, 300, 30, 30)
player_1.reset_position()
               

show_level_text = False
level = 1
level_timer = 0
restart_text = font.render("Volver a Jugar", True, (255, 255, 255))
restart_rect = restart_text.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 100))
pygame.draw.rect(screen, (0, 0, 255), restart_rect)  # Dibujar un rectángulo azul para el botón "Volver a Jugar"
screen.blit(restart_text, restart_rect)  # Dibujar el texto del botón "Volver a Jugar"

def mostrar_nivel(nivel):
    nivel_text = font.render("Nivel " + str(nivel), True, (255, 255, 255))
    nivel_rect = nivel_text.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2))
    screen.blit(nivel_text, nivel_rect)
    pygame.display.flip()
    pygame.time.wait(2000)


current_screen = 1

def show_start_screen():
    font = pygame.font.Font(None, 36)
    text = font.render("Cowboy vs Ogros", True, (255, 255, 255))
    text_rect = text.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2))

    start_button = pygame.Rect(ANCHO_VENTANA // 2 - 75, ALTO_VENTANA // 2 + 50, 150, 50)
    button_text = font.render("Iniciar Juego", True, (255, 255, 255))
    button_text_rect = button_text.get_rect(center=start_button.center)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return

        screen.fill((0, 0, 0))
        screen.blit(text, text_rect)
        pygame.draw.rect(screen, (255, 0, 0), start_button)
        screen.blit(button_text, button_text_rect)
        pygame.display.flip()
        clock.tick(FPS)


def mostrar_nivel(nivel):
    nivel_text = font.render("Nivel " + str(nivel), True, (255, 255, 255))
    nivel_rect = nivel_text.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2))
    screen.blit(nivel_text, nivel_rect)
    pygame.display.flip()
    pygame.time.wait(2000)

show_start_screen()

mostrar_nivel(1)
current_screen = 1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_1.control("WALK_L")
                player_1.last_direction = "LEFT"
            elif event.key == pygame.K_RIGHT:
                player_1.control("WALK_R")
                player_1.last_direction = "RIGHT"
            elif event.key == pygame.K_SPACE:
                player_1.control("JUMP")
            elif event.key == pygame.K_x:
                player_1.control("SHOOT")

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_SPACE or event.key == pygame.K_x:
                player_1.control("STAY")
                if event.key == pygame.K_x:
                    player_1.is_shooting = False

    screen.blit(imagen_fondo, imagen_fondo.get_rect())

    if player_1.game_over:
        # Renderizar el texto de "Game Over"
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 50))

        # Renderizar el botón de reinicio
        restart_text = font.render("Restart", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 50))

        # Dibujar el cartel de "Game Over" y el botón de reinicio en la pantalla
        screen.blit(game_over_text, game_over_rect)
        pygame.draw.rect(screen, (0, 0, 255), restart_rect)  # Dibujar un rectángulo azul para el botón de reinicio
        screen.blit(restart_text, restart_rect)  # Dibujar el texto del botón de reinicio

        # Detectar clics del mouse para reiniciar la partida
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    # Reiniciar la partida
                    # Volver a establecer el estado inicial del juegO
                    
                    player_1 = Player(0, 0, 4, 8, 8, 32)
                    player_1.reset_position()
                    player_1.lives = 3
                    player_1.score = 0
                    player_1.bullets = []
                    current_screen = 1
                    plataformas = plataformas1
                    enemies = [Enemy(800, 500, 3, 0, ANCHO_VENTANA)]
                    obstacle = Obstacle(550, 300, 30, 30)
                    powerup = PowerUp(1200, 80, 30, 30)

    else:
        player_1.update(plataformas, enemies, powerup, obstacle, delta_ms)
        player_1.draw(screen)

        defeated_enemies = []
        for enemy in enemies:
            enemy.update(player_1,delta_ms)
            enemy.draw(screen)
            if enemy.is_defeated:
                defeated_enemies.append(enemy)

        if len(defeated_enemies) >= len(enemies):
            plataforma_inicial = plataformas[6]

            if current_screen == 1:
                player_1.reset_position()
                mostrar_nivel(2)
                current_screen += 1
                enemies = [Enemy(800, 500, 3, 0, ANCHO_VENTANA), Enemy(plataforma_inicial.rect.x, plataforma_inicial.rect.y - enemy.height, 3, 900, 1400)]
                plataformas = plataformas2
                powerup = PowerUp(700, 100, 30, 30)
            elif current_screen == 2:
                player_1.reset_position()
                mostrar_nivel(3)
                current_screen += 1
                enemies = [Enemy(800, 500, 3, 0, ANCHO_VENTANA), Enemy(plataforma_inicial.rect.x, plataforma_inicial.rect.y - enemy.height, 3, 900, 1400), Enemy(0, 70, 3, 0, 350)]
                plataformas = plataformas3
                powerup = PowerUp(700, 100, 30, 30)
                obstacle = Obstacle(650, 300, 30, 30)
            elif current_screen == 3:
                
                # Calcular puntuación obtenida
                puntuacion_text = font.render("Ganaste! Puntuación: " + str(player_1.score), True, (255, 255, 255))
                puntuacion_rect = puntuacion_text.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2))
                screen.blit(puntuacion_text, puntuacion_rect)
                pygame.display.flip()
                pygame.time.wait(3000)

                # Reiniciar la partida
                player_1 = Player(0, 0, 4, 8, 8, 32)
                player_1.lives = 3
                player_1.score = 0
                player_1.bullets = []
                current_screen = 1
                plataformas = plataformas1
                enemies = [Enemy(800, 500, 3, 0, ANCHO_VENTANA)]
                obstacle = Obstacle(550, 100, 30, 30)
                powerup = PowerUp(1200, 80, 30, 30)
                    
        for plataforma in plataformas:
            plataforma.draw(screen)

        powerup.draw(screen)
        obstacle.draw(screen)

    pygame.display.flip()