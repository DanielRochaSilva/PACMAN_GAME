#O Mundo: Carrega, desenha e gerencia o mapa.
# src/level.py

import pygame
from settings import *


class Level:
    """
    Representa o mapa do jogo, gerenciando tanto os dados (matriz) quanto
    sua representação visual na tela.
    """

    def __init__(self, map_file_path):
        """
        Inicializa o mapa a partir de um arquivo txt.
        """
        self.matrix = []
        self.load(map_file_path)
        self.height = len(self.matrix)
        # Verifica se existe ao menos uma linha na matriz antes de tentar acessa-la
        self.width = len(self.matrix[0]) if self.height > 0 else 0

    # =========================================================================
    # MÉTODOS DE LÓGICA E DADOS
    # =========================================================================

    def load(self, map_file_path):
        """
        Carrega o mapa do arquivo e transforma em uma matriz 2D de caracteres.

        Parametros:
            map_file_path (str): Caminho para o arquivo de texto com o layout do mapa.
        """
        with open(map_file_path, 'r') as map_file:
            for line in map_file:
                # Usar list() para transformar a string em uma lista de caracteres
                self.matrix.append(list(line.strip()))

    def get_tile(self, line, column):
        """
        Retorna o caractere presente em uma posicao especifica do mapa.

        Parmetros:
            line (int): Indice da linha.
            column (int): Indice da coluna.

        Retorna:
            str: Caractere presente na posicao ou '#' se estiver fora do mapa.
        """
        if (0 <= line < self.height) and (0 <= column < self.width):
            return self.matrix[line][column]
        return '#'  # Retorna parede se estiver fora dos limites

    def set_tile(self, line, column, new_tile):
        """
        Atualiza o caractere de uma posicao especifica do mapa.

        Parametros:
            line (int): indice da linha.
            column (int): indice da coluna.
            new (str): Novo caractere a ser colocado na posicao.
        """
        if 0 <= line < self.height and 0 <= column < self.width:
            self.matrix[line][column] = new_tile

    def is_wall(self, line, column):
        """
        Verifica se a posicao especificada e uma parede.

        Parametros:
            line (int): Indice da linha.
            column (int): Indice da coluna.

        Retorna:
            bool: True se for parede ('#'), False caso contrario.
        """
        return self.get_tile(line, column) == '#'

    def is_path(self, line, column):
        """
        Verifica se a posicao e um caminho livre.

        Parametros:
            line (int): Indice da linha.
            column (int): Indice da coluna.

        Retorna:
            bool: True se for uma celula que o jogador possa passar (ex: '.', ' ', 'o').
        """
        return self.get_tile(line, column) in [' ', '.', 'o', 'P', 'G']

    def find_symbol(self, symbol):
        """
        Retorna todas as posicoes em que um determinado simbolo aparece no mapa.

        Parametros:
            symbol (str): Caractere a ser buscado no mapa.

        Retorna:
            list[tuple(int, int)]: Lista de tuplas com coordenadas (linha, coluna).
        """
        positions = []
        for y, line in enumerate(self.matrix):
            for x, tile in enumerate(line):
                if tile == symbol:
                    positions.append((y, x))
        return positions

    # =========================================================================
    # METODO DE RENDERIZAÇÃO
    # =========================================================================

    def draw(self, screen):
        """
        Desenha o mapa na tela, com base nos caracteres da matriz.
        """
        # Ajustamos self.data para self.matrix para usar a variável correta da classe
        for row_index, row in enumerate(self.matrix):
            for col_index, tile in enumerate(row):
                x = col_index * GRID_SIZE
                y = row_index * GRID_SIZE

                if tile == '#':  # Desenha uma parede
                    pygame.draw.rect(screen, BLUE_WALL, (x, y, GRID_SIZE, GRID_SIZE))
                elif tile == '.':  # Desenha um pontinho
                    pygame.draw.circle(screen, YELLOW, (x + GRID_SIZE // 2, y + GRID_SIZE // 2), 4)
                elif tile == 'o':  # Desenha um super ponto (power-up)
                    pygame.draw.circle(screen, WHITE, (x + GRID_SIZE // 2, y + GRID_SIZE // 2), 8)
                # Os símbolos 'P' e 'G' não são desenhados aqui,
                # pois as entidades (Jogador, Fantasma) serão desenhadas por cima.