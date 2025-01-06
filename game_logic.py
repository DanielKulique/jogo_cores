# game_logic.py

from game_objects import Bolinha
import random
import pygame

class Jogo:
    def __init__(self, cores_primarias):
        self.cores_primarias = cores_primarias
        self.bolinhas = []
        self.mensagem = ""
        self.iniciar_fase()

    def iniciar_fase(self):
        """
        Inicializa uma nova fase com bolinhas em posições aleatórias.
        """
        posicoes = [(200, 300), (400, 300), (600, 300)]
        random.shuffle(posicoes)

        # Cria as bolinhas para a fase atual
        self.bolinhas = [
            Bolinha(x, y, cor) for (x, y), cor in zip(posicoes, self.cores_primarias.values())
        ]
        self.mensagem = "Clique na cor correta!"

    def verificar_clique(self, posicao_mouse):
        """
        Verifica se o jogador clicou em uma bolinha válida.
        """
        for bolinha in self.bolinhas:
            if bolinha.foi_clicada(posicao_mouse):
                if bolinha.cor in self.cores_primarias.values():
                    self.mensagem = "Acertou! Próxima fase!"
                    self.iniciar_fase()
                else:
                    self.mensagem = "Errou! Tente novamente."
                return

    def desenhar(self, tela):
        """
        Desenha as bolinhas e a mensagem de feedback na tela.
        """
        for bolinha in self.bolinhas:
            bolinha.desenhar(tela)

        # Exibir mensagem
        fonte = pygame.font.Font(None, 36)
        texto = fonte.render(self.mensagem, True, (0, 0, 0))
        tela.blit(texto, (400 - texto.get_width() // 2, 50))
