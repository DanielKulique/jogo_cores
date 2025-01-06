import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class Campo:
    def __init__(self, x, y, largura, altura, cor_borda=(0, 0, 0)):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.cor_borda = cor_borda

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor_borda, (self.x, self.y, self.largura, self.altura), 3)

class CampoProfessor(Campo):
    def __init__(self):
        super().__init__(50, SCREEN_HEIGHT - 185, 260, 140)

class CampoConfiguracao(Campo):
    def __init__(self):
        super().__init__(18, 18, 75, 75)

class CampoSom(Campo):
    def __init__(self):
        super().__init__(SCREEN_WIDTH - 180, 20, 95, 80)

class CampoAjuda(Campo):
    def __init__(self):
        super().__init__(SCREEN_WIDTH - 80, 20, 60, 80)

class CampoNomeJogador(Campo):
    def __init__(self):
        super().__init__((SCREEN_WIDTH - 750) // 2, (SCREEN_HEIGHT - 120) // 2 + 65, 750, 120)

class CampoMenu(Campo):
    def __init__(self):
        super().__init__((SCREEN_WIDTH - 750) // 2 + 260, (SCREEN_HEIGHT - 120) // 2 - 70, 210, 95)


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


class Botao:
    def __init__(self, x, y, largura, altura, texto, cor, cor_texto=(0, 0, 0), fonte=None):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.texto = texto
        self.cor = cor
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
        Verifica se o botão foi clicado.
        """
        return self.rect.collidepoint(posicao_mouse)


