import pygame
from constantes import *
pygame.font.init()
font = pygame.font.Font(None, 24)

class Obstacle:
    def __init__(self, x, y, width, height):
        self.image = pygame.image.load("imagenes/gui/hi_overlays/pinches.png")
        self.image = pygame.transform.scale(self.image, (width,height))  # Cambiar el tamaño de la imagen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.damage = 1
        self.cooldown = 2000
        self.last_hit_time = 0
        self.rect.width -= 1 # Reducir el ancho del rectángulo de colisión
        self.rect.height -= 1 # Reducir la altura del rectángulo de colisión
        self.rect.x += 5  # Alinear el rectángulo de colisión con el centro del obstáculo
        self.rect.y += 5  # Alinear el rectángulo de colisión con el centro del obstáculo

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class PowerUp:
    def __init__(self, x, y, width, height):
        self.image = pygame.image.load("imagenes/gui/hi_overlays/hi_overlay_variant_hearts_x1_1_png_1354840444.png")
        self.rect = pygame.Rect(x, y, width, height)
        self.collected = False  # Indicador de si el power-up ha sido recogido
        
    def draw(self, screen):
        if not self.collected:
            screen.blit(self.image, self.rect)


class Plataforma:
    def __init__(self, x, y, width, height, image_path):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path)

    def draw(self, screen):
        screen.blit(self.image, self.rect)