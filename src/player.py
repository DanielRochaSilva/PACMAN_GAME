#O Herói: Lógica do Pacman.

# src/player.py

# src/player.py

import pygame
import os
from settings import *


class Player:
    def __init__(self, game, pos):
        """
        Construtor da entidade Player (Pac-Man).
        """
        self.game = game
        self.grid_pos = pygame.Vector2(pos[0], pos[1])
        self.pixel_pos = pygame.Vector2(
            self.grid_pos.x * GRID_SIZE + GRID_SIZE // 2,
            self.grid_pos.y * GRID_SIZE + GRID_SIZE // 2
        )
        self.direction = pygame.Vector2(0, 0)  # Começa virado para a direita
        self.stored_direction = None
        self.speed = PLAYER_SPEED

        # --- LÓGICA DE ANIMAÇÃO ---
        self.animations = {}  # Dicionário para guardar as listas de sprites
        self.load_animations()

        self.current_frame_index = 0
        self.image = self.animations['right'][self.current_frame_index]  # Imagem atual a ser desenhada
        self.rect = self.image.get_rect()  # Retângulo da imagem, para posicionamento

        self.animation_timer = 0
        self.animation_speed_ms = 80  # Tempo em milissegundos para cada frame da animação

    def load_animations(self):
        """
        Carrega todas as imagens de animação do Pac-Man a partir das pastas.
        """
        # Mapeia a direção para a pasta correspondente e a lista de sprites
        directions = {
            'right': (PACMAN_RIGHT_FOLDER, []),
            'left': (PACMAN_LEFT_FOLDER, []),
            'up': (PACMAN_UP_FOLDER, []),
            'down': (PACMAN_DOWN_FOLDER, [])
        }

        for direction, (folder_path, image_list) in directions.items():
            # Pega todos os arquivos da pasta, ignorando subdiretórios
            filenames = sorted([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])

            for filename in filenames:
                # Carrega a imagem
                img = pygame.image.load(os.path.join(folder_path, filename)).convert_alpha()
                # Redimensiona a imagem para o tamanho do nosso grid
                scaled_img = pygame.transform.scale(img, (GRID_SIZE, GRID_SIZE))
                image_list.append(scaled_img)

        self.animations = {direction: data[1] for direction, data in directions.items()}


    def update(self):
        """
        Atualiza a posição e a animação do jogador a cada frame.
        """


        # --- LÓGICA DE MOVIMENTO ---
        # Primeiro, tentamos mudar para a direção que o jogador apertou
        if self.stored_direction and self.is_on_grid_center():
            next_pos_grid = self.grid_pos + self.stored_direction
            if not self.game.level.is_wall(int(next_pos_grid.y), int(next_pos_grid.x)):
                self.direction = self.stored_direction
                self.stored_direction = None

        # Agora, verificamos se podemos continuar nos movendo na direção ATUAL
        if self.is_on_grid_center():
            next_pos_grid = self.grid_pos + self.direction
            if self.game.level.is_wall(int(next_pos_grid.y), int(next_pos_grid.x)):
                # Se houver uma parede na frente, paramos
                self.direction = pygame.Vector2(0, 0)

        # Move o jogador com base na direção final
        self.pixel_pos += self.direction * self.speed

        # Atualiza a posição no grid (para lógica de colisões futuras)
        if self.direction.x != 0 or self.direction.y != 0:
            self.grid_pos.x = (self.pixel_pos.x - GRID_SIZE / 2) / GRID_SIZE
            self.grid_pos.y = (self.pixel_pos.y - GRID_SIZE / 2) / GRID_SIZE

        # --- LÓGICA DE ATUALIZAÇÃO DA ANIMAÇÃO ---
        # Atualiza a animação
        if self.direction.x != 0 or self.direction.y != 0:

           self.animate()

    def animate(self):
        """ Controla a troca de frames da animação. """
        self.animation_timer += self.game.clock.get_time()  # Adiciona o tempo passado

        if self.animation_timer > self.animation_speed_ms:
            self.animation_timer = 0  # Reseta o timer
            # Avança para o próximo frame, voltando ao início se chegar ao fim
            self.current_frame_index = (self.current_frame_index + 1) % len(
                self.animations[self.get_current_direction_key()])

        # Atualiza a imagem atual com base no frame e na direção
        self.image = self.animations[self.get_current_direction_key()][self.current_frame_index]

    def draw(self, screen):
        """
        Desenha o sprite atual do Pac-Man na tela.
        """
        # Atualiza a posição do retângulo da imagem para o centro da posição em pixels
        self.rect.center = self.pixel_pos
        # Desenha a imagem na tela
        screen.blit(self.image, self.rect)

    def move(self, direction):
        """
        Armazena a próxima direção que o jogador deseja se mover.
        """
        self.stored_direction = direction

    def is_on_grid_center(self):
        """ Verifica se o jogador está próximo o suficiente do centro de uma célula. """
        return (abs(self.pixel_pos.x % GRID_SIZE - GRID_SIZE // 2) < self.speed and
                abs(self.pixel_pos.y % GRID_SIZE - GRID_SIZE // 2) < self.speed)

    def get_current_direction_key(self):
        """ Retorna a chave de string ('up', 'down', etc.) para a direção atual. """
        if self.direction.x == 1: return 'right'
        if self.direction.x == -1: return 'left'
        if self.direction.y == -1: return 'up'
        if self.direction.y == 1: return 'down'

        # Se estiver parado (direction é 0,0), usa a última direção armazenada
        # para que a imagem não mude para 'right' toda vez que ele para.
        if self.stored_direction:
            if self.stored_direction.x == 1: return 'right'
            if self.stored_direction.x == -1: return 'left'
            if self.stored_direction.y == -1: return 'up'
            if self.stored_direction.y == 1: return 'down'

        return 'right'  # Retorna 'right' como um padrão seguro no início do jogo


