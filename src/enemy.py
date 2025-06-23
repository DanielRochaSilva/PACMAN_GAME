# Os Vilões: Lógica dos Fantasmas.

import pygame
from settings import *


class Enemy:
    def __init__(self, game, pos, image):
        self.game = game
        self.grid_pos = pygame.Vector2(pos[0], pos[1])
        self.pixel_pos = pygame.Vector2(
            self.grid_pos.x * GRID_SIZE + GRID_SIZE // 2,
            self.grid_pos.y * GRID_SIZE + GRID_SIZE // 2
        )

        # Agora guardamos a imagem e o rect >>>>
        self.image = image
        self.rect = self.image.get_rect()

    def update(self):
        # A lógica de movimento e IA virá aqui no futuro
        pass

    def draw(self, screen):
        #Usamos blit para desenhar a imagem >>>>
        # Centralizamos o retângulo da imagem na nossa posição em pixels
        self.rect.center = self.pixel_pos
        # Desenhamos a imagem na tela
        screen.blit(self.image, self.rect)