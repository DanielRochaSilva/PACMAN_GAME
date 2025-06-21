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

        self.state = 'menu_principal'  # Define o estado inicial do jogo
        self.pause_options = ['Sair e Salvar', 'Sair sem Salvar', 'Cancelar']
        self.selected_pause_option = 0  # O índice da opção selecionada (começa em 0)



    # --- MÉTODOS DE ESTADO: MENU ---


    def menu_principal_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # Se apertar ENTER, muda o estado para 'jogando'
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.state = 'jogando'

    def menu_principal_draw(self):
        self.screen.fill(BLACK)
        # Lógica para desenhar o título e as opções do menu
        try:
            title_font = pygame.font.Font(MAIN_FONT, 48)
            instructions_font = pygame.font.Font(MAIN_FONT, UI_FONT_SIZE)
        except FileNotFoundError:
            title_font = pygame.font.SysFont('arial', 48)
            instructions_font = pygame.font.SysFont('arial', UI_FONT_SIZE)

        title_text = title_font.render(TITULO, True, YELLOW)
        instructions_text = instructions_font.render("Pressione ENTER para iniciar", True, WHITE)

        # Centraliza o texto na tela
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        instructions_rect = instructions_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

        self.screen.blit(title_text, title_rect)
        self.screen.blit(instructions_text, instructions_rect)

        pygame.display.flip()




    def playing_events(self):
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

                # Verifica se o jogador quer pausar o jogo
                if event.key == pygame.K_p or event.key == pygame.K_q:
                    self.state = 'pausado'

                # Agora, verificamos qual tecla foi para mover o jogador
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.player.move(pygame.Vector2(-1, 0))
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.player.move(pygame.Vector2(1, 0))
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.player.move(pygame.Vector2(0, -1))
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.player.move(pygame.Vector2(0, 1))

    def playing_update(self):
        """
        Atualiza a lógica do jogo.
        """
        self.player.update()

    def playing_draw(self):
        """
        Desenha todos os elementos na tela.
        """
        self.screen.fill(BLACK)
        self.level.draw(self.screen)
        # <<<< ADICIONADO: Chama o metodo de desenho do jogador
        self.player.draw(self.screen)
        self.draw_ui()  # Garante que a UI seja desenhada por cima
        pygame.display.flip()

    def draw_ui(self):
        # Área do painel inferior
        panel_rect = pygame.Rect(UI_PANEL_POS[0], UI_PANEL_POS[1], WIDTH, HEIGHT - (GRID_HEIGHT * GRID_SIZE))
        pygame.draw.rect(self.screen, BLACK, panel_rect)  # Fundo preto para o painel

        # Tenta usar a fonte personalizada, se não encontrar, usa uma padrão
        try:
            font = pygame.font.Font(MAIN_FONT, UI_FONT_SIZE)
        except FileNotFoundError:
            font = pygame.font.SysFont('arial', UI_FONT_SIZE)

        # Desenha o Score
        score_text = font.render(f"SCORE: {self.score}", True, WHITE)
        self.screen.blit(score_text, (20, HEIGHT - 40))

        # Desenha as Vidas
        lives_text = font.render(f"LIVES: ", True, WHITE)
        self.screen.blit(lives_text, (WIDTH - 180, HEIGHT - 40))

        # Desenha os ícones de vida do Pac-Man
        for i in range(self.lives):
            # Usamos o primeiro sprite da animação 'right' como ícone
            life_icon = self.player.animations['right'][0]
            # Ajusta o tamanho do ícone se necessário
            life_icon_small = pygame.transform.scale(life_icon, (GRID_SIZE - 10, GRID_SIZE - 10))
            self.screen.blit(life_icon_small, (WIDTH - 100 + (i * 35), HEIGHT - 45))

    # Dentro da classe Game

    def pausado_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                # Navega para cima nas opções
                if event.key == pygame.K_UP:
                    # O operador % (módulo) faz a seleção "dar a volta"
                    self.selected_pause_option = (self.selected_pause_option - 1) % len(self.pause_options)

                # Navega para baixo nas opções
                if event.key == pygame.K_DOWN:
                    self.selected_pause_option = (self.selected_pause_option + 1) % len(self.pause_options)

                # Seleciona a opção atual com ENTER
                if event.key == pygame.K_RETURN:
                    # Opção 0: Sair e Salvar
                    if self.selected_pause_option == 0:
                        print("FUNCIONALIDADE 'SAIR E SALVAR' AINDA NÃO IMPLEMENTADA.")
                        # Aqui viria a lógica para self.save_game() e self.save_ranking()
                        self.running = False  # Por enquanto, apenas fecha o jogo

                    # Opção 1: Sair sem Salvar
                    elif self.selected_pause_option == 1:
                        self.state = 'menu_principal'  # Volta para o menu principal

                    # Opção 2: Cancelar
                    elif self.selected_pause_option == 2:
                        self.state = 'jogando'  # Volta para o jogo

                # Também permite sair da pausa com 'P' ou 'Q' (atalho para "Cancelar")
                if event.key == pygame.K_p or event.key == pygame.K_q:
                    self.state = 'jogando'

    # Dentro da classe Game

    def pausado_draw(self):

        # Agora, criamos uma camada escura semi-transparente por cima
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # SRCALPHA permite transparência
        overlay.fill((0, 0, 0, 170))  # Preto com 170 de alpha (0-255)
        self.screen.blit(overlay, (0, 0))

        # Define as fontes
        try:
            menu_font = pygame.font.Font(MAIN_FONT, 36)
        except FileNotFoundError:
            menu_font = pygame.font.SysFont('arial', 36)

        # Desenha as opções do menu
        for index, option in enumerate(self.pause_options):
            # Se a opção estiver selecionada, usa a cor amarela. Senão, branca.
            color = YELLOW if index == self.selected_pause_option else WHITE

            option_text = menu_font.render(option, True, color)

            # Calcula a posição de cada opção
            option_rect = option_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40 + index * 60))

            self.screen.blit(option_text, option_rect)

        pygame.display.flip()


    def run(self):
        while self.running:
            if self.state == 'menu_principal':
                self.menu_principal_events()
                self.menu_principal_draw()
            elif self.state == 'jogando':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            elif self.state == 'pausado':
                self.pausado_events()
                self.pausado_draw()

            self.clock.tick(FPS)



