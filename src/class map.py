class Map:
    """
    Representa o mapa do jogo como uma matriz 2D de caracteres.

    A classe Mapa e responsavel por carregar um arquivo de texto contendo a
    estrutura do mapa do jogo, armazena-lo como uma matriz 2D (lista de listas) 
    e fornecer metodos utilitarios para acessar, modificar e
    analisar o estado do mapa durante o jogo.

    Cada celula do mapa e representada por um caractere que define seu tipo:
    - '#' : parede
    - '.' : ponto
    - 'o' : super ponto
    - ' ' : espaco livre
    """

    def __init__(self, map_file_path):
        """
        Inicializa o mapa a partir de um arquivo txt.

        Parametros:
            map_file_path (str): Caminho para o arquivo de texto com o layout do mapa.
        """
        self.matrix = []
        self.load(map_file_path)
        self.hight = len(self.matrix)
        # Verifica se existe ao menos uma linha na matriz antes de tentar acessa-la
        self.width = len(self.matrix[0]) if self.hight > 0 else 0 

    def load(self, map_file_path):
        """
        Carrega o mapa do arquivo e transforma em uma matriz 2D de caracteres.

        Parametros:
            map_file_path (str): Caminho para o arquivo de texto com o layout do mapa.
        """
        with open(map_file_path, 'r') as map_file:
            for line in map_file:
                clean_line = line.strip("\n")
                if clean_line != "":
                    self.matrix.append(list(clean_line))

    def get_tile(self, line, column):
        """
        Retorna o caractere presente em uma posicao especifica do mapa.

        Parmetros:
            line (int): Indice da linha.
            column (int): Indice da coluna.

        Retorna:
            str: Caractere presente na posicao ou '#' se estiver fora do mapa.
        """
        # Verifica se line e column sao indices validos
        if (0 <= line < self.hight) and (0 <= column < self.width):
            return self.matrix[line][column]
        return '#'

    def set_tile(self, line, column, new):
        """
        Atualiza o caractere de uma posicao especifica do mapa.

        Parametros:
            line (int): indice da linha.
            column (int): indice da coluna.
            new (str): Novo caractere a ser colocado na posicao.
        """
        if 0 <= line < self.hight and 0 <= column < self.width:
            self.matrix[line][column] = new

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
        return self.get_tile(line, column) in [' ', '.', 'o']

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

    # Para debug
    def __str__(self):
        """
        Retorna uma representacao em string do mapa, como no arquivo original.

        Retorna:
            str: Mapa formatado com quebras de linha.
        """
        return '\n'.join(''.join(line) for line in self.matrix)
