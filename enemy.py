import pygame
from auxiliar import Auxiliar
from constantes import *
pygame.font.init()
font = pygame.font.Font(None, 24)


class Enemy:
    def __init__(self, x, y, speed,min_x,max_x,):
        self.walk_r = Auxiliar.getSurfaceFromSeparateFiles("imagenes/caracters/enemies/ork_sword/WALK/WALK_{:03d}.png", 1, 6, flip=False, scale=0.13)
        self.walk_l = Auxiliar.getSurfaceFromSeparateFiles("imagenes/caracters/enemies/ork_sword/WALK/WALK_{:03d}.png", 1, 6, flip=True, scale=0.13)
        self.attack_r = Auxiliar.getSurfaceFromSeparateFiles("imagenes/caracters/enemies/ork_sword/ATTAK/ATTAK_{:03d}.png", 1, 6, flip=False, scale=0.13)
        self.attack_l = Auxiliar.getSurfaceFromSeparateFiles("imagenes/caracters/enemies/ork_sword/ATTAK/ATTAK_{:03d}.png", 1, 6, flip=True, scale=0.13)
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = 1  # Dirección del movimiento (1: derecha, -1: izquierda)
        self.animation = self.walk_r  # Animación actual
        self.frame = 0  # Fotograma actual de la animación
        self.width = self.animation[0].get_width()  # Ancho del enemigo
        self.height = self.animation[0].get_height()  # Alto del enemigo
        self.rect = pygame.Rect(x, y, self.width, self.height)  # Rectángulo de colisión
        self.attack_timer = 0  # Temporizador para la animación de ataque
        self.attack_duration = 1000  # Duración de la animación de ataque en milisegundos (1 segundo)
        self.is_attacking = False  # Indicador de si el enemigo está atacando
        self.lives = 5
        self.is_defeated = False
        self.health_bar_width = 50
        self.health_bar_height = 5
        self.min_x = min_x  #desplazamiento en x
        self.max_x = max_x

    def update(self, player,delta_ms):
        self.check_collision(player)

        
        # Verificar los límites izquierdo y derecho de la pantalla
        if self.x <= self.min_x:
            self.direction = 1  # Invertir la dirección a la derecha
        elif self.x + self.width >= self.max_x:
            self.direction = -1  # Invertir la dirección a la izquierda

        self.x += self.direction * self.speed

        if self.direction == 1:
            self.animation = self.walk_r
        else:
            self.animation = self.walk_l

        self.frame += 1
        if self.frame >= len(self.animation):
            self.frame = 0

        self.rect.x = self.x
        self.rect.y = self.y

        if self.is_attacking:
            attack_frame = int((self.attack_timer / self.attack_duration) * len(self.attack_r))
            if attack_frame >= len(self.attack_r):
                self.is_attacking = False
            else:
                if self.direction == 1:
                    self.animation = self.attack_r
                else:
                    self.animation = self.attack_l
                self.frame = attack_frame

        self.attack_timer += delta_ms

    def check_collision(self, player):
        if self.rect.colliderect(player.rect) and player.collision_timer >= player.collision_cooldown:
            if self.is_defeated:
                return  # Si el enemigo está derrotado, salir de la función sin hacer nada
                
            if player.current_direction == "RIGHT":
                self.animation = self.attack_r
            else:
                self.animation = self.attack_l
            self.frame = 0
            self.is_attacking = True
            self.attack_timer = 0
            player.lives -= 1
            if player.lives <= 0:
                player.rect.y = 1000
            player.collision_timer = 0  # Reiniciar el temporizador de colisión
            

    def draw(self, screen):
        if not self.is_defeated:
            current_frame = self.animation[self.frame]
            screen.blit(current_frame, (self.x, self.y))

            pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y - 20, self.health_bar_width, self.health_bar_height))
            remaining_health = max(0, self.lives) / 10.0 * self.health_bar_width
            pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y - 20, remaining_health, self.health_bar_height))