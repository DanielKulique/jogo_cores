import pygame
import sys
from game_objects import Botao
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Menu Inicial")
        self.clock = pygame.time.Clock()
        self.running = True

        # Instanciando os botões
        self.botoes = {
            "professor": Botao(50, SCREEN_HEIGHT - 185, 260, 140, "Professor", (255, 0, 0), acao=self.acao_professor),
            "config": Botao(18, 18, 75, 75, "Configuração", (0, 255, 0), acao=self.acao_configuracao),
            "nome": Botao((SCREEN_WIDTH - 750) // 2, (SCREEN_HEIGHT - 120) // 2 + 65, 750, 120, "Nome", (0, 0, 255), acao=self.acao_nome_jogador),
            "ajuda": Botao(SCREEN_WIDTH - 80, 20, 60, 80, "Ajuda", (255, 255, 0), acao=self.acao_ajuda),
            "som": Botao(SCREEN_WIDTH - 180, 20, 95, 80, "Som", (255, 165, 0), acao=self.acao_som),
        }
        self.botoes_config = {
            "ajuda": Botao(SCREEN_WIDTH - 80, 20, 60, 80, "Ajuda", (255, 255, 0), acao=self.acao_ajuda),
            "som": Botao(SCREEN_WIDTH - 180, 20, 95, 80, "Som", (255, 165, 0), acao=self.acao_som),
            "config": Botao(18, 18, 75, 75, "Configuração", (0, 255, 0), acao=self.menu_nome),
        }

        # Carregando o layout de fundo do menu inicial
        self.layout_menu = pygame.image.load("assets/layouts/start.png")
        self.layout_menu = pygame.transform.smoothscale(self.layout_menu, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.layout_config = pygame.image.load("assets/layouts/configuração1.png")
        self.layout_config = pygame.transform.smoothscale(self.layout_config, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def desenhar_menu(self):
        """Desenha o layout do menu inicial com os botões."""
        # Desenhar o fundo
        self.tela.blit(self.layout_menu, (0, 0))
        
        # Desenhar os botões
        for botao in self.botoes.values():
            botao.desenhar(self.tela)

    def desenhar_configuracao(self):
        """Desenha o layout do menu inicial com os botões."""
        # Desenhar o fundo
        self.tela.blit(self.layout_config, (0, 0))

        # desenha os botoes da config
        for botao in self.botoes_config.values():
            botao.desenhar(self.tela)

    def verificar_clique(self, pos):
        """Verifica qual botão foi clicado."""
        for botao in self.botoes.values():
            if botao.foi_clicado(pos):
                if botao.acao:
                    botao.acao()
                return

    def menu_nome(self):
        """Loop para o menu inicial."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.verificar_clique(pos)

            self.desenhar_menu()
            pygame.display.flip()
            self.clock.tick(60)

    # Métodos de ação para os botões
    def acao_professor(self):
        print("Ação: Professor")
        # Adicione aqui a lógica para mudar para a tela do professor

    def acao_configuracao(self):
        print("Ação: Configuração")
        # Adicione aqui a lógica para mudar para a tela de configuração
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for botao in self.botoes_config.values():
                        if botao.foi_clicado(pos):
                            if botao.acao == self.acao_configuracao:
                                botao.acao()
                                return
                            return #retorna ao menu anterior

            self.desenhar_configuracao()
            pygame.display.flip()
            self.clock.tick(60)

    def acao_nome_jogador(self):
        print("Ação: Nome")
        # Adicione aqui a lógica para tratar o nome do jogador

    def acao_ajuda(self):
        print("Ação: Ajuda")
        # Adicione aqui a lógica para exibir a tela de ajuda

    def acao_som(self):
        print("Ação: Som")
        # Adicione aqui a lógica para ajustar as configurações de som


# Inicializando o jogo
if __name__ == "__main__":
    jogo = Jogo()
    jogo.menu_nome()
