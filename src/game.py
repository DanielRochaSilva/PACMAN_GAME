
#Gerencia os estados e o loop principal.

# src/game.py
# src/game.py

import pygame
import sys
import os  # <<<<---- 1. IMPORTAMOS A BIBLIOTECA 'os' PARA JUNTAR OS CAMINHOS
from settings import *
from level import Level

class Game:
    def __init__(self):
        """
        Construtor da classe Game. Inicializa o Pygame e a tela.
        """
        pygame.init()


        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITULO)
        self.clock = pygame.time.Clock()
        self.running = True


        # Construcao do caminho para o arquivo
        caminho_do_mapa = os.path.join(MAPS_FOLDER, 'level_1.txt')
        #  instância do Level
        self.level = Level(caminho_do_mapa)

        # --- BLOCO DE TESTE TEMPORÁRIO ---
        print("--- INICIANDO TESTES DE DEBUG DO MAPA ---")

        # Teste 1: Usar find_symbol para achar a posição inicial do jogador
        posicao_inicial_p = self.level.find_symbol('P')
        print(f"Posição do jogador ('P') encontrada em: {posicao_inicial_p}")

        # Teste 2: Usar is_wall para verificar uma parede e um caminho
        # (Assumindo que a célula (0,0) é uma parede '#' e (1,1) não é)
        print(f"A coordenada (0, 0) é uma parede? Resposta: {self.level.is_wall(0, 0)}")
        print(f"A coordenada (1, 1) é uma parede? Resposta: {self.level.is_wall(1, 1)}")

        # Teste 3: Usar get_tile para ver o que tem em uma célula
        # (Assumindo que a célula (1,2) tem um pontinho '.' no seu mapa)
        print(f"O que há na coordenada (1, 2)? Tile: '{self.level.get_tile(1, 2)}'")

        print("--- FIM DOS TESTES DE DEBUG ---")




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
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        """
        Atualiza a lógica do jogo.
        """
        pass

    def draw(self):
        """
        Desenha todos os elementos na tela.
        """
        self.screen.fill(BLACK)
        self.level.draw(self.screen)
        pygame.display.flip()