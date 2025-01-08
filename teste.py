import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT

# Funções para ações dos botões
def acao_menu():
    print("Navegando para o menu...")

def acao_configuracao():
    print("Navegando para a configuração...")

def acao_professor():
    print("Navegando para o professor...")

def acao_som():
    print("Navegando para o som...")

def acao_ajuda():
    print("Navegando para a ajuda...")

def acao_nome_jogador():
    print("Acessando nome do jogador!")

# Classe Botao reaproveitada para todas as interações
class Botao:
    def __init__(self, x, y, largura, altura, texto, cor, acao=None, cor_texto=(0, 0, 0), fonte=None):
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

    def desenhar(self, tela):
        """
        Desenha o botão na tela.
        """
        pygame.draw.rect(tela, self.cor, self.rect)
        texto_surface = self.fonte.render(self.texto, True, self.cor_texto)
        texto_rect = texto_surface.get_rect(center=self.rect.center)
        tela.blit(texto_surface, texto_rect)

    def foi_clicado(self, posicao_mouse):
        """
        Verifica se o botão foi clicado e executa a ação, se existir.
        """
        if self.rect.collidepoint(posicao_mouse):
            if self.acao:
                self.acao()
            return True
        return False

# Instâncias dos botões com dimensões e ações específicas
def criar_botoes():
    botoes = {
        "professor": Botao(50, SCREEN_HEIGHT - 185, 260, 140, "Professor", (255, 0, 0), acao_professor),
        "config": Botao(18, 18, 75, 75, "Config", (0, 255, 0), acao_configuracao),
        "som": Botao(SCREEN_WIDTH - 180, 20, 95, 80, "Som", (0, 0, 255), acao_som),
        "ajuda": Botao(SCREEN_WIDTH - 80, 20, 60, 80, "Ajuda", (255, 255, 0), acao_ajuda),
        #"nome": Botao((SCREEN_WIDTH - 750) // 2, (SCREEN_HEIGHT - 120) // 2 + 65, 750, 120, "Nome", (255, 100, 100), acao_nome_jogador),
        "menu": Botao((SCREEN_WIDTH - 750) // 2 + 260, (SCREEN_HEIGHT - 120) // 2 - 70, 210, 95, "Menu", (100, 255, 100), acao_menu),
        "fase1": Botao(500, SCREEN_HEIGHT - 371, 275, 50, "Fase 1", (150, 150, 255)),
        "fase2": Botao(500, SCREEN_HEIGHT - 295, 275, 50, "Fase 2", (255, 150, 150)),
    }
    return botoes

# Loop principal para interagir com os botões
def main():
    pygame.init()
    tela = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Menu Inicial")
    clock = pygame.time.Clock()
    running = True

    # Carregar layout de fundo
    layout_menu = pygame.image.load("assets/layouts/menu_fase_bloqueadas.png")
    layout_menu = pygame.transform.smoothscale(layout_menu, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Criar os botões
    botoes = criar_botoes()

    while running:
        tela.blit(layout_menu, (0, 0))  # Desenhar fundo

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for botao in botoes.values():
                    botao.foi_clicado(pos)

        # Desenhar todos os botões
        for botao in botoes.values():
            botao.desenhar(tela)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()