import pygame

# Inicializa o Pygame
pygame.init()

# Configurações da tela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Exemplo de Texto no Pygame")

# Definição de fonte e cor
fonte = pygame.font.Font(None, 50)  # Usa a fonte padrão com tamanho 50
cor_texto = (255, 255, 255)  # Branco

# Loop principal
rodando = True
while rodando:
    tela.fill((0, 0, 0))  # Preenche a tela com preto

    # Renderiza o texto
    texto = fonte.render("muito bom!!", True, cor_texto)
    posicao_texto = texto.get_rect(center=(largura // 1.5, altura // 1.5))

    # Desenha o texto na tela
    tela.blit(texto, posicao_texto)

    # Atualiza a tela
    pygame.display.flip()

    # Captura eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

# Encerra o Pygame
pygame.quit()
