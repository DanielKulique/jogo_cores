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
    def __init__(self, x, y, largura, altura, texto, cor, acao=None, cor_texto=(0, 0, 0), fonte=None, mostrar = True):
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
            if self.acao:
                self.acao()
            return True
        return False

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

class Botao_Especial:
    def __init__(self, x, y, largura, altura, texto, fonte, cor_normal, cor_hover, cor_sombra, cor_texto, acao=None):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.texto = texto
        self.fonte = fonte
        self.cor_normal = cor_normal
        self.cor_hover = cor_hover
        self.cor_sombra = cor_sombra
        self.cor_texto = cor_texto
        self.acao = acao
        self.rect = pygame.Rect(x, y, largura, altura)

    def desenhar(self, tela, ativo=False):
        """
        Desenha o botão na tela.
        """
        sombra_offset = 15 if not ativo else 10
        cor_botao = self.cor_hover if ativo else self.cor_normal

        # Sombra do botão
        pygame.draw.rect(
            tela,
            (43, 24, 0),  # Sombra do fundo (#2B1800)
            (self.x - 4, self.y + sombra_offset, self.largura + 8, self.altura + 4),
            border_radius=5,
        )

        # Corpo do botão
        pygame.draw.rect(
            tela,
            cor_botao,
            (self.x, self.y, self.largura, self.altura),
            border_radius=5,
        )

        # Sombras internas
        pygame.draw.rect(
            tela,
            self.cor_sombra,
            (self.x, self.y + self.altura - 10, self.largura, 10),
            border_radius=5,
        )
        pygame.draw.rect(
            tela,
            (255, 229, 196),  # Parte superior (#FFE5C4)
            (self.x, self.y, self.largura, 10),
            border_radius=5,
        )

        # Texto do botão
        texto_surface = self.fonte.render(self.texto, True, self.cor_texto)
        texto_rect = texto_surface.get_rect(center=(self.x + self.largura // 2, self.y + self.altura // 2))
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

    @staticmethod
    def criar_botao_voltar():
        """
        Cria um botão 'Voltar ao jogo →' com estilo configurado.
        """
        largura = 200
        altura = 60
        fonte = pygame.font.SysFont("Helvetica", 36, bold=True)
        return Botao(
            x=300,
            y=500,  # Ajuste conforme a altura da sua tela
            largura=largura,
            altura=altura,
            texto="Voltar ao jogo →",
            fonte=fonte,
            cor_normal=(255, 161, 43),  # Cor normal (#FFA12B)
            cor_hover=(247, 137, 0),  # Cor hover (#F78900)
            cor_sombra=(145, 81, 0),  # Cor da sombra (#915100)
            cor_texto=(255, 255, 255),  # Cor do texto (branco)
            
        )


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



