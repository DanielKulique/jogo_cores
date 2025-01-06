import pygame
import os
from game_logic import Jogo
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, CORES
from game_objects import CampoNomeJogador, CampoProfessor, CampoConfiguracao, CampoSom, CampoAjuda, CampoMenu

# Função para salvar os resultados no log
def salvar_resultado(nome_jogador, resultado):
    if not os.path.exists("logs"):
        os.makedirs("logs")
    with open("logs/resultados.txt", "a") as arquivo:
        arquivo.write(f"{nome_jogador}: {resultado}\n")

# Função para capturar o nome do jogador
def obter_nome_jogador(tela):
    font = pygame.font.SysFont(None, 48)
    nome = ""
    ativo = True

    # Carrega a imagem base
    imagem_base = pygame.image.load("assets/layouts/start.png")
    imagem_base = pygame.transform.scale(imagem_base, (SCREEN_WIDTH, SCREEN_HEIGHT))

    while ativo:
        tela.fill((255, 255, 255))  # Preenche a tela de branco

        # Exibe a imagem de fundo
        tela.blit(imagem_base, (0, 0))

        # Exibe o nome digitado no centro da tela
        texto_nome = font.render(f"{nome}", True, (0, 0, 0))
        tela.blit(texto_nome, (SCREEN_WIDTH // 2 - texto_nome.get_width() // 2, SCREEN_HEIGHT // 2))

        # Atualiza a tela
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ativo = False
                nome = ""
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:  # Se pressionar Enter, finaliza a inserção
                    ativo = False
                elif evento.key == pygame.K_BACKSPACE:  # Se pressionar backspace, apaga a última letra
                    nome = nome[:-1]
                else:
                    nome += evento.unicode  # Adiciona o caractere pressionado ao nome

        pygame.time.Clock().tick(FPS)

    return nome

def main():
    pygame.init()

    # Inicializa a tela em modo janela
    tela = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Instancia o jogo
    jogo = Jogo(CORES)

    # Variável para controlar o modo tela cheia
    fullscreen = False

    # Tela inicial: pedir nome do jogador
    nome_jogador = ""

    # Instancia os campos
    campo_nome_jogador = CampoNomeJogador()
    campo_professor = CampoProfessor()
    campo_config = CampoConfiguracao()
    campo_som = CampoSom()
    campo_ajuda = CampoAjuda()
    campo_menu = CampoMenu()

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                # Alterna entre modo tela cheia e janela com F11
                if evento.key == pygame.K_F11:
                    fullscreen = not fullscreen
                    if fullscreen:
                        tela = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                    else:
                        tela = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                # Verifica se o clique foi dentro do campo clicável
                if campo_nome_jogador.x <= evento.pos[0] <= campo_nome_jogador.x + campo_nome_jogador.largura and campo_nome_jogador.y <= evento.pos[1] <= campo_nome_jogador.y + campo_nome_jogador.altura:
                    nome_jogador = obter_nome_jogador(tela)

        # Preenche a tela com fundo branco
        tela.fill((255, 255, 255))

        # Desenha a imagem base
        imagem_base = pygame.image.load("assets/layouts/start.png")
        imagem_base = pygame.transform.scale(imagem_base, (SCREEN_WIDTH, SCREEN_HEIGHT))
        tela.blit(imagem_base, (0, 0))

        # Desenha os campos
        campo_nome_jogador.desenhar(tela)
        campo_professor.desenhar(tela)
        campo_config.desenhar(tela)
        campo_som.desenhar(tela)
        campo_ajuda.desenhar(tela)
        campo_menu.desenhar(tela)

        pygame.display.flip()
        clock.tick(FPS)

    # Salva o resultado
    if nome_jogador:
        resultado = "Vitoria"  # Substitua com a lógica do seu jogo (ex: 'Vitória', 'Derrota', 'Pontos')
        salvar_resultado(nome_jogador, resultado)
    else:
        print("Nome não inserido. O jogo será encerrado.")

    pygame.quit()

if __name__ == "__main__":
    main()
