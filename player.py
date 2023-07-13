import pygame
from auxiliar import Auxiliar
from constantes import *
pygame.font.init()
font = pygame.font.Font(None, 24)

class Player:
    def __init__(self, x, y, speed_walk, speed_run, gravity, jump):
        self.walk_r = Auxiliar.getSurfaceFromSeparateFiles("imagenes\\caracters\\players\\cowgirl\\Run ({:d}).png", 1, 8, flip=False, scale=0.3)
        self.walk_l = Auxiliar.getSurfaceFromSeparateFiles("imagenes\\caracters\\players\\cowgirl\\Run ({:d}).png", 1, 8, flip=True, scale=0.3)
        self.stay_l = Auxiliar.getSurfaceFromSeparateFiles("imagenes\\caracters\\players\\cowgirl\\Idle ({:d}).png", 1, 10, flip=True, scale=0.3)
        self.stay_r = Auxiliar.getSurfaceFromSeparateFiles("imagenes\\caracters\\players\\cowgirl\\Idle ({:d}).png", 1, 10, flip=False, scale=0.3)
        self.jump_r = Auxiliar.getSurfaceFromSeparateFiles("imagenes\\caracters\\players\\cowgirl\\Jump ({:d}).png", 1, 10, flip=False, scale=0.3)
        self.jump_l = Auxiliar.getSurfaceFromSeparateFiles("imagenes\\caracters\\players\\cowgirl\\Jump ({:d}).png", 1, 10, flip=True, scale=0.3)
        self.shoot_r = Auxiliar.getSurfaceFromSeparateFiles("imagenes\\caracters\\players\\cowgirl\\Shoot ({:d}).png", 1, 3, flip=False, scale=0.3)
        self.shoot_l = Auxiliar.getSurfaceFromSeparateFiles("imagenes\\caracters\\players\\cowgirl\\Shoot ({:d}).png", 1, 3, flip=True, scale=0.3)
        self.frame = 0
        self.lives = 3
        self.score = 0
        self.move_x = x
        self.move_y = y
        self.speed_walk = speed_walk
        self.speed_run = speed_run
        self.gravity = gravity
        self.jump = jump
        self.animation = self.stay_r
        self.current_direction = "RIGHT"
        self.is_moving = False
        self.image = self.animation[self.frame]
        self.rect = self.image.get_rect()
        self.last_direction = "RIGHT"
        self.is_jump = False
        self.rect.width -= 10  # Reducir el ancho del rectángulo de colisión
        self.rect.x += 5  # Alinear el rectángulo de colisión con el centro del personaje
        self.jump_timer = 0  # Temporizador para el salto
        self.jump_cooldown = 1000  # Tiempo de enfriamiento del salto en milisegundos (1 segundo)
        self.shoot_timer = 0  # Temporizador para el disparo
        self.shoot_cooldown = 1000  # Tiempo de enfriamiento del disparo en milisegundos (1 segundo)
        self.bullets = []  # lista de balas
        self.is_shooting = False
        self.collision_timer = 0  # Temporizador para el enfriamiento de la colisión
        self.collision_cooldown = 3000  # Tiempo de enfriamiento en milisegundos (2 segundos)
        self.vida_texto = font.render("Vidas: " + str(self.lives), True, (255, 255, 255))
        self.vida_texto_rect = self.vida_texto.get_rect()
        self.puntos_texto = font.render("Puntos: " + str(self.score), True, (255, 255, 255))
        self.puntos_texto_rect = self.puntos_texto.get_rect()
        self.puntos_texto_rect.midtop = (self.rect.centerx, self.rect.top + 25)
        self.game_over = False  # Variable para controlar el estado de Game Over
        self.start_x = 0 
        self.start_y = 500
        self.bullet_image = pygame.image.load("imagenes/gui/hi_overlays/bala.png").convert_alpha() 
        self.bullet_image = pygame.transform.scale(self.bullet_image, (15,15))  # Ajusta el tamaño de la imagen de la bala

    def reset_position(self):
        self.rect.x = self.start_x 
        self.rect.y = self.start_y  
        
    def control(self, action):
        if action == "WALK_R":
            self.move_x = self.speed_walk
            self.animation = self.walk_r
            self.frame = 0
            self.last_direction = self.current_direction
            self.current_direction = "RIGHT"  # Actualiza la dirección actual
        elif action == "WALK_L":
            self.move_x = -self.speed_walk
            self.animation = self.walk_l
            self.frame = 0
            self.last_direction = self.current_direction
            self.current_direction = "LEFT"  # Actualiza la dirección actual
        elif action == "JUMP":
            if not self.is_jump and self.jump_timer >= self.jump_cooldown:
                self.move_y = -self.jump
                if self.last_direction == "RIGHT":
                    self.move_x = self.speed_walk
                    self.animation = self.jump_r
                elif self.last_direction == "LEFT":
                    self.move_x = -self.speed_walk
                    self.animation = self.jump_l
                self.frame = 0
                self.is_jump = True
                self.jump_timer = 0  # Reinicia el temporizador de salto
        elif action == "STAY":
            if not self.is_moving:
                self.animation = self.stay_l if self.last_direction == "LEFT" else self.stay_r
                self.frame = 0
                self.move_x = 0
                self.move_y = 0
        elif action == "SHOOT":
            if not self.is_shooting and self.shoot_timer >= self.shoot_cooldown:
                self.is_shooting = True
            if self.shoot_timer >= self.shoot_cooldown:
                if self.last_direction == "RIGHT":
                    self.animation = self.shoot_r
                elif self.last_direction == "LEFT":
                    self.animation = self.shoot_l
                self.frame = 0
                self.shoot_timer = 0  # Reinicia el temporizador de disparo

                bullet_x = self.rect.centerx  # Starting position of the bullet
                bullet_y = self.rect.centery

                if self.last_direction == "RIGHT":
                    bullet_speed = 5  # velocidad bala
                elif self.last_direction == "LEFT":
                    bullet_speed = -5

                bullet = pygame.Rect(bullet_x, bullet_y, 10, 10)  # crea la bala
                self.bullets.append((bullet, bullet_speed))

    def update(self, plataformas, enemies, powerup, obstacle, delta_ms):
        if self.frame < len(self.animation) - 1:
            self.frame += 1
        else:
            self.frame = 0
            if self.is_jump:
                self.is_jump = False
                self.move_y = 0

        self.rect.x += self.move_x

        if self.rect.y < 500:
            self.rect.y += self.gravity

        on_ground = False
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.rect):
                if self.move_y >= 0 and self.rect.bottom <= plataforma.rect.centery:
                    self.rect.y = plataforma.rect.y - self.rect.height
                    self.move_y = 0
                    on_ground = True

        if not on_ground:
            self.rect.y += self.move_y
        
        self.jump_timer += delta_ms  # Actualiza el temporizador de salto
        self.shoot_timer += delta_ms

        for bullet, bullet_speed in self.bullets:
            bullet.x += bullet_speed
            
        self.bullets = [(bullet, bullet_speed) for bullet, bullet_speed in self.bullets if
                        not any(plataforma.rect.colliderect(bullet) for plataforma in plataformas)]
        
        self.check_collision(enemies,powerup)
        self.collision_timer += delta_ms  # Incrementar el temporizador de colisión

        # Actualizar la posición del texto de las vidas
        self.vida_texto_rect.midtop = (self.rect.centerx, self.rect.top - 10)
         # Actualizar el texto de las vidas
        self.vida_texto = font.render("Vidas: " + str(self.lives), True, (255, 255, 255))

        if self.rect.colliderect(obstacle.rect):
            current_time = pygame.time.get_ticks()
            if current_time - obstacle.last_hit_time >= obstacle.cooldown:
                self.lives -= obstacle.damage
                obstacle.last_hit_time = current_time

        if self.lives <= 0:
            self.game_over = True
            self.rect.y = 1000      

    def check_collision(self, enemies,powerup):
        defeated_enemies = []
        for bullet, _ in self.bullets:
            for enemy in enemies:
                if bullet.colliderect(enemy.rect):
                    defeated_enemies.append(enemy)
                    self.bullets.remove((bullet, _))
                    break

        for enemy in defeated_enemies:
            enemy.lives -= 1
            if enemy.lives <= 0:
                enemy.is_defeated = True
                enemy.rect.y = 1000
                self.score += 500  # Incrementar la puntuación en 500 puntos


        # Actualizar el texto de los puntos
        self.puntos_texto = font.render("Puntos: " + str(self.score), True, (255, 255, 255))
        
        if not powerup.collected and self.rect.colliderect(powerup.rect):
            powerup.collected = True
            self.lives += 1  # Recuperar 1 vida
            
    def draw(self, screen):
        self.image = self.animation[self.frame]
        screen.blit(self.image, self.rect)

        for bullet, _ in self.bullets:
            screen.blit(self.bullet_image, bullet)

        # Dibujar el texto de las vidas sobre el jugador
        screen.blit(self.vida_texto, self.vida_texto_rect)
        screen.blit(self.puntos_texto, self.puntos_texto_rect)