import pygame
import sys

# Inicializar o Pygame
pygame.init()

# Configurações da tela
LARGURA_TELA = 800
ALTURA_TELA = 600
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Log do Jogo")
clock = pygame.time.Clock()

# Configurações de fontes e cores
fonte = pygame.font.SysFont("Arial", 24)
cor_texto = (0, 0, 0)
cor_fundo = (255, 255, 255)
cor_barra = (200, 200, 200)
cor_bola_barra = (100, 100, 100)

# Função para ler o log do arquivo
def ler_log(caminho_arquivo):
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
        return conteudo.split("--------------------------------------------------")
    except FileNotFoundError:
        print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
        return []

# Ler os logs do arquivo
caminho_log = "resultados.txt"
logs = ler_log(caminho_log)

# Scroll horizontal
offset_x = 0
velocidade_scroll = 0.5

# Configurações da barra de rolagem
altura_barra = 20
largura_total_conteudo = len(logs) * (LARGURA_TELA // 2)
tamanho_bola = max(LARGURA_TELA * (LARGURA_TELA / largura_total_conteudo), 40)  # Tamanho mínimo da bola
pos_bola = 0  # Posição inicial da bola na barra

# Controle do arraste
arrastando = False
mouse_x_inicial = 0
offset_x_inicial = 0

# Função para calcular a posição da bola na barra
def atualizar_pos_bola():
    if largura_total_conteudo > LARGURA_TELA:
        return -offset_x * (LARGURA_TELA - tamanho_bola) / (largura_total_conteudo - LARGURA_TELA)
    return 0

# Loop principal
running = True
while running:
    tela.fill(cor_fundo)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clique esquerdo
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if ALTURA_TELA - altura_barra <= mouse_y <= ALTURA_TELA:  # Clique na barra
                    if pos_bola <= mouse_x <= pos_bola + tamanho_bola:  # Dentro da bola
                        arrastando = True
                        mouse_x_inicial = mouse_x
                        offset_x_inicial = offset_x
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Soltar clique
                arrastando = False
        elif event.type == pygame.MOUSEMOTION and arrastando:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            deslocamento = mouse_x - mouse_x_inicial
            if largura_total_conteudo > LARGURA_TELA:
                offset_x = offset_x_inicial - deslocamento  * (largura_total_conteudo - LARGURA_TELA) / (LARGURA_TELA - tamanho_bola) 

    # Limitar o scroll horizontal
    offset_x = min(0, offset_x)
    offset_x = max(offset_x, LARGURA_TELA - largura_total_conteudo)

    # Atualizar a posição da bola
    pos_bola = atualizar_pos_bola()

    # Renderizar os logs lado a lado
    for i, log in enumerate(logs):
        linhas = log.strip().split("\n")
        for j, linha in enumerate(linhas):
            texto = fonte.render(linha, True, cor_texto)
            tela.blit(texto, (i * (LARGURA_TELA // 2) + offset_x, j * 30))

    # Desenhar a barra de rolagem
    pygame.draw.rect(tela, cor_barra, (0, ALTURA_TELA - altura_barra, LARGURA_TELA, altura_barra))
    pygame.draw.rect(
        tela,
        cor_bola_barra,
        (pos_bola, ALTURA_TELA - altura_barra, tamanho_bola, altura_barra),
    )

    pygame.display.flip()
    clock.tick(60)
