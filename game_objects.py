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


class Bolinha:
    def __init__(self, x, y, cor, raio=30):
        self.x = x
        self.y = y
        self.cor = cor
        self.raio = raio
        self.rect = pygame.Rect(x - raio, y - raio, raio * 2, raio * 2)  # Área de clique

    def desenhar(self, tela):
        """
        Desenha a bolinha na tela.
        """
        pygame.draw.circle(tela, self.cor, (self.x, self.y), self.raio)

    def foi_clicada(self, posicao_mouse):
        """
        Verifica se a bolinha foi clicada.
        """
        return self.rect.collidepoint(posicao_mouse)



