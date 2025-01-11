
mouse_x, mouse_y = pygame.mouse.get_pos()
        botao_menu = self.botao_especial_menu["menu_especial"]
        botao_menu.desenhar(self.tela, ativo=(botao_menu.rect.collidepoint(mouse_x, mouse_y)))


# Verifica clique no botão de menu
                    if botao_menu.foi_clicado(pos):
                        print("Botao menu foi clicado")
                        botao_menu.acao()








import pygame
import sys

pygame.init()

# Dimensões da tela
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Botão Estilizado")

# Cores
BACKGROUND_COLOR = (255, 204, 142)  # #ffcc8e
BUTTON_COLOR = (255, 161, 43)  # #FFA12B
BUTTON_HOVER_COLOR = (247, 137, 0)  # #F78900
BUTTON_SHADOW_COLOR = (145, 81, 0)  # #915100
BUTTON_TEXT_COLOR = (255, 255, 255)  # branco
SHADOW_BACKGROUND_COLOR = (43, 24, 0)  # #2B1800

# Configurações do botão
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60
BUTTON_TEXT = "Clique Aqui"
FONT = pygame.font.SysFont("Helvetica", 36, bold=True)

# Função para desenhar o botão
def draw_button(surface, x, y, text, active=False):
    shadow_offset = 15 if not active else 10
    button_color = BUTTON_HOVER_COLOR if active else BUTTON_COLOR
    
    # Sombra do botão
    pygame.draw.rect(
        surface,
        SHADOW_BACKGROUND_COLOR,
        (x - 4, y + shadow_offset, BUTTON_WIDTH + 8, BUTTON_HEIGHT + 4),
        border_radius=5,
    )

    # Corpo do botão
    pygame.draw.rect(
        surface,
        button_color,
        (x, y, BUTTON_WIDTH, BUTTON_HEIGHT),
        border_radius=5,
    )

    # Sombras internas do botão
    pygame.draw.rect(
        surface,
        BUTTON_SHADOW_COLOR,
        (x, y + BUTTON_HEIGHT - 10, BUTTON_WIDTH, 10),
        border_radius=5,
    )
    pygame.draw.rect(
        surface,
        (255, 229, 196),  # #FFE5C4
        (x, y, BUTTON_WIDTH, 10),
        border_radius=5,
    )

    # Texto do botão
    text_surface = FONT.render(text, True, BUTTON_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(x + BUTTON_WIDTH // 2, y + BUTTON_HEIGHT // 2))
    surface.blit(text_surface, text_rect)

# Função principal
def main():
    running = True
    clock = pygame.time.Clock()
    button_x, button_y = (SCREEN_WIDTH - BUTTON_WIDTH) // 2, (SCREEN_HEIGHT - BUTTON_HEIGHT) // 2
    button_pressed = False

    while running:
        screen.fill(BACKGROUND_COLOR)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        button_rect = pygame.Rect(button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
        is_hovered = button_rect.collidepoint(mouse_x, mouse_y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and is_hovered:
                button_pressed = True
            if event.type == pygame.MOUSEBUTTONUP and button_pressed:
                if is_hovered:
                    print("Botão clicado!")
                button_pressed = False

        draw_button(screen, button_x, button_y, BUTTON_TEXT, active=button_pressed or is_hovered)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()

import pygame
import sys

class MeuJogo:
    def __init__(self):
        self.running = True
        self.menu_atual = "menu_principal"
        self.jogador = "Jogador"
        self.ultimo_clique = 0  # Definir a variável ultimo_clique

    def menu_nome(self):
        """
        Exibe o menu inicial. O botão 'Voltar ao jogo →' será mostrado apenas se o nome do jogador já tiver sido inserido.
        O botão 'Menu' estará sempre visível.
        """
        self.menu_atual = "menu_principal"

        # Criar o botão 'Voltar ao jogo →' apenas se o nome do jogador foi inserido
        botao_voltar = None
        if self.jogador:
            botao_voltar = BotaoEspecial(
                x=600,
                y=SCREEN_HEIGHT - 200,
                largura=500,
                altura=60,
                texto=f"{((self.jogador).split()[0]).upper()}",
                cor_normal=(255, 220, 140),
                cor_hover=(30, 130, 220),
                cor_sombra=(204, 153, 0),
                cor_texto=(0, 0, 0),
                fonte=pygame.font.SysFont("Arial", 40),
                acao=self.menu_fases,  # Define a ação ao clicar no botão
            )

        while self.running:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            is_hovered = botao_voltar and botao_voltar.rect.collidepoint(mouse_x, mouse_y)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.verificar_clique(pos)  # Adicionar o método de verificação de clique

                    # Verifica clique no botão 'Voltar ao jogo →'
                    if botao_voltar and botao_voltar.foi_clicado(pos):
                        print(f"Botão 'Continuar Como {self.jogador}' clicado!")
                        self.menu_fases()  # Chama a função que exibe o menu de fases
                        return

            # Desenha o menu
            self.desenhar_menu()

    def verificar_clique(self, pos):
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.ultimo_clique < 200:  # Delay de 200ms
            return  # Ignora se o clique for muito próximo do último
        self.ultimo_clique = tempo_atual

        if self.menu_atual == "menu_principal":
            botoes = self.botoes
        elif self.menu_atual == "menu_config":
            botoes = self.botoes_config
        elif self.menu_atual == "menu_fases":
            botoes = self.botoes_menu_fases
        else:
            return

        botao.foi_clicado(pos):
            
import pygame
import sys

import pygame

class Botao:
    def __init__(self, x, y, largura, altura, texto, cor, acao=None, cor_texto=(0, 0, 0), fonte=None, mostrar=True):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.texto = texto
        self.cor = cor
        self.acao = acao
        self.cor_texto = cor_texto
        self.fonte = fonte or pygame.font.Font(None, 36)
        self.rect = pygame.Rect(x, y, largura, altura)
        self.mostrar = mostrar
        self.ultimo_clique = 0  # Adiciona a variável de controle de tempo de clique

    def desenhar(self, tela):
        """
        Desenha o botão na tela.
        """
        if self.mostrar:
            pygame.draw.rect(tela, self.cor, self.rect, 2)
            texto_surface = self.fonte.render(self.texto, True, self.cor_texto)
            texto_rect = texto_surface.get_rect(center=self.rect.center)
            tela.blit(texto_surface, texto_rect)

    def foi_clicado(self, posicao_mouse):
        """
        Verifica se o botão foi clicado e executa a ação, se existir.
        """
        if self.rect.collidepoint(posicao_mouse):
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.ultimo_clique > 200:  # Delay de 200ms
                self.ultimo_clique = tempo_atual
                if self.acao:
                    self.acao()
                return True
        return False

    @staticmethod
    def criar_botao_voltar(acao_voltar):
        """
        Cria um botão 'Voltar ao jogo →' usando a classe Botao existente.

        :param acao_voltar: Função a ser executada quando o botão for clicado.
        :return: Instância do botão configurado.
        """
        return Botao(
            x=50,
            y=SCREEN_HEIGHT - 100,
            largura=300,
            altura=60,
            texto="Voltar ao jogo →",
            cor=(50, 150, 250),
            cor_texto=(255, 255, 255),
            fonte=pygame.font.Font(None, 40),
            acao=acao_voltar
        )

