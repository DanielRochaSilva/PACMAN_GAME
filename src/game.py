#Gerencia os estados e o loop principal.

# src/game.py

import pygame
import sys
import os  # <<<<---- 1. IMPORTAMOS A BIBLIOTECA 'os' PARA JUNTAR OS CAMINHOS
from settings import *
from level import Level
from player import Player

class Game:
    def __init__(self):
        """
        Construtor da classe Game. Inicializa o Pygame e a tela.
        """
        pygame.init()


        self.score = 0
        self.lives = PLAYER_START_LIVES
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITULO)
        self.clock = pygame.time.Clock()
        self.running = True


        # Construcao do caminho para o arquivo
        caminho_do_mapa = os.path.join(MAPS_FOLDER, 'level_2.txt')
        #  instância do Level
        self.level = Level(caminho_do_mapa)

        # <<<< ADICIONADO: Bloco que cria o jogador
        # Usa o metodo find_symbol do TAD Mapa para achar a posição inicial
        start_pos_list = self.level.find_symbol('P')
        if start_pos_list:
            # Pega a primeira posição encontrada (formato: (linha, coluna))
            # e converte para (coluna, linha) para o nosso Player
            start_pos = (start_pos_list[0][1], start_pos_list[0][0])
            self.player = Player(self, start_pos)
        else:
            # Posição padrão caso 'P' não seja encontrado no mapa
            self.player = Player(self, (1, 1))



    def run(self):
        """
        Inicia e mantém o loop principal do jogo.
        """
        while self.running:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def events(self):
        """
        Processa todos os eventos do jogo (teclado, mouse, fechar janela).
        """
        for event in pygame.event.get():
            # Verificação #1: O jogador quer fechar o jogo?
            if event.type == pygame.QUIT:
                self.running = False

            # Verificação #2: O jogador apertou uma tecla?
            # Este 'if' está no mesmo nível do 'if' anterior, fora dele.
            if event.type == pygame.KEYDOWN:

                # Agora, verificamos qual tecla foi para mover o jogador
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.player.move(pygame.Vector2(-1, 0))
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.player.move(pygame.Vector2(1, 0))
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.player.move(pygame.Vector2(0, -1))
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.player.move(pygame.Vector2(0, 1))

    def update(self):
        """
        Atualiza a lógica do jogo.
        """
        self.player.update()

    def draw(self):
        """
        Desenha todos os elementos na tela.
        """
        self.screen.fill(BLACK)
        self.level.draw(self.screen)
        # <<<< ADICIONADO: Chama o metodo de desenho do jogador
        self.player.draw(self.screen)
        pygame.display.flip()


