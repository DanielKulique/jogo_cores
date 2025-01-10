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
        self.jogador = ""
        self.fase_1 = "Desbloqueada"
        self.fase_2 = "Bloqueada"
        self.menu_atual = "menu_principal" 

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
            "menu": Botao((SCREEN_WIDTH - 750) // 2 + 260, (SCREEN_HEIGHT - 120) // 2 - 70, 210, 95, "Menu", (100, 255, 100), acao=self.menu_nome),
            "config": Botao(18, 18, 75, 75, "Configuração", (0, 255, 0), acao=self.menu_nome),
            "sair": Botao(SCREEN_WIDTH - 137, SCREEN_HEIGHT - 120, 120, 120, "Sair", (255, 255, 0), acao=self.acao_sair)
        }
        self.botoes_menu_fases = {
            "fase_1": Botao(500, SCREEN_HEIGHT - 371, 275, 50, "Fase 1", (150, 150, 255), acao=None),
            "fase_2": Botao(500, SCREEN_HEIGHT - 295, 275, 50, "Fase 2", (255, 150, 150), acao=None),
            "menu": Botao((SCREEN_WIDTH - 750) // 2 + 260, (SCREEN_HEIGHT - 120) // 2 - 70, 210, 95, "Menu", (100, 255, 100), acao=self.menu_nome),
            "config": Botao(18, 18, 75, 75, "Configuração", (0, 255, 0), acao=self.acao_configuracao),
            "ajuda": Botao(SCREEN_WIDTH - 80, 20, 60, 80, "Ajuda", (255, 255, 0), acao=self.acao_ajuda),
            "som": Botao(SCREEN_WIDTH - 180, 20, 95, 80, "Som", (255, 165, 0), acao=self.acao_som),
        }

        # Carregando o layout de fundo do menu inicial
        self.layout_menu = pygame.image.load("assets/layouts/start.png")
        self.layout_menu = pygame.transform.smoothscale(self.layout_menu, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.layout_config = pygame.image.load("assets/layouts/configuração1.png")
        self.layout_config = pygame.transform.smoothscale(self.layout_config, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.layout_menu_fases = pygame.image.load("assets/layouts/fase_1_desbloqueada.png")
        self.layout_menu_fases = pygame.transform.smoothscale(self.layout_menu_fases, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def desenhar_menu(self):
        """Desenha o layout do menu inicial com os botões."""
        # Desenhar o fundo
        self.tela.blit(self.layout_menu, (0, 0))
        
        # Desenhar os botões
        for botao in self.botoes.values():
            botao.desenhar(self.tela)

    def desenhar_menu_fases(self):
        """desenha o layout do menu de fases"""
        self.tela.blit(self.layout_menu_fases, (0, 0))

        # Desenha os botoes do menu

        for botao in self.botoes_menu_fases.values():
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
        atual = self.menu_atual

        if atual == "menu_principal":
            botoes = self.botoes
        elif atual == "menu_config":
            botoes = self.botoes_config
        elif atual == "menu_fases":
            botoes = self.botoes_menu_fases
        else:
            return


        for botao in botoes.values():
            if botao.foi_clicado(pos):
                if botao.acao:
                    botao.acao()
                return


    def menu_nome(self):
        """
        Exibe o menu inicial. O botão 'Voltar ao jogo →' será mostrado apenas se o nome do jogador já tiver sido inserido.
        """
        self.menu_atual = "menu_principal"
        botao_voltar = None

        if self.jogador:  # Verifica se o nome do jogador já foi inserido
            botao_voltar = Botao(
                x=600,
                y=SCREEN_HEIGHT - 200,
                largura=300,
                altura=60,
                texto=f"Continuar Como {self.jogador}",
                cor=(50, 150, 250),
                cor_texto=(255, 255, 255),
                fonte=pygame.font.SysFont("Arial", 40),
            )

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.verificar_clique(pos)

                    # Verifica clique no botão 'Voltar ao jogo →'
                    if botao_voltar and botao_voltar.foi_clicado(pos):
                        print("Botão 'Voltar ao jogo →' clicado!")
                        self.menu_fases()

                elif event.type == pygame.KEYDOWN:
                    if not self.jogador:    
                        self.acao_nome_jogador()

            self.desenhar_menu()

            # Desenha o botão 'Voltar ao jogo →' se o nome do jogador foi inserido
            if botao_voltar:
                botao_voltar.desenhar(self.tela)

            pygame.display.flip()
            self.clock.tick(60)

    # Métodos de ação para os botões
    def acao_professor(self):
        print("Ação: Professor")
        # Adicione aqui a lógica para mudar para a tela do professor

    def acao_configuracao(self):
        self.menu_atual = "menu_config"
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
                        self.verificar_clique(pos)


            self.desenhar_configuracao()
            pygame.display.flip()
            self.clock.tick(60)

    def acao_nome_jogador(self):
        print("Ação: Nome")

        # Definições de cores e estado
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        GRAY = (200, 200, 200)

        input_active = True  # A entrada começa ativa
        input_text = ""

        font = pygame.font.Font(None, 50)  # Fonte para o texto

        # Definindo as dimensões e a posição do retângulo do campo de texto
        campo_texto_x = (SCREEN_WIDTH - 750) // 2
        campo_texto_y = (SCREEN_HEIGHT - 120) // 2 + 65
        campo_texto_largura = 750
        campo_texto_altura = 120

        while self.running:
            self.desenhar_menu()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Clique do mouse para ativar/desativar o campo de texto
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Verifique se o clique está dentro da área do campo de texto
                    if campo_texto_x < event.pos[0] < campo_texto_x + campo_texto_largura and campo_texto_y < event.pos[1] < campo_texto_y + campo_texto_altura:
                        input_active = True
                    else:
                        input_active = False
                        return

                # Entrada de texto
                if event.type == pygame.KEYDOWN and input_active:
                    if event.key == pygame.K_BACKSPACE:
                        # Apaga o último caractere se houver texto
                        input_text = input_text[:-1]
                    elif event.key == pygame.K_RETURN:  # Enter
                        self.jogador = input_text
                        print(f"Nome do jogador: {self.jogador}")
                        # Aqui você pode chamar a função menu_fases 
                        self.menu_fases()
                        return
                    else:
                        input_text += event.unicode  # Adiciona o caractere digitado

            # Renderize o campo de texto
            pygame.draw.rect(self.tela, BLACK if input_active else GRAY, (campo_texto_x, campo_texto_y, campo_texto_largura, campo_texto_altura), 2)

            text_surface = font.render(input_text, True, BLACK)
            text_rect = text_surface.get_rect()
            text_rect.midleft = (campo_texto_x + 10, campo_texto_y + campo_texto_altura // 2)
            self.tela.blit(text_surface, text_rect)  # Ajuste a posição do texto dentro do campo

            # Atualize a tela
            pygame.display.flip()
            self.clock.tick(60)

    def menu_fases(self):
        print("Acao_menu_fases")
        self.menu_atual = "menu_fases"
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.verificar_clique(pos)

            self.desenhar_menu_fases()
            pygame.display.flip()
            self.clock.tick(60)


    def acao_ajuda(self):
        print("Ação: Ajuda")
        # Adicione aqui a lógica para exibir a tela de ajuda

    def acao_som(self):
        print("Ação: Som")
        # Adicione aqui a lógica para ajustar as configurações de som

    def acao_sair(self): #APLICAR SALVAMENTO DE JOGO!!!!!!!!!!!
        print("Ação: Sair")
        pygame.quit()
        sys.exit()

# Inicializando o jogo
if __name__ == "__main__":
    jogo = Jogo()
    jogo.menu_nome()
