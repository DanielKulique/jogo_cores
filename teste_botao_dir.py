import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configurações da tela
LARGURA_TELA = 800
ALTURA_TELA = 600
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Lista de Jogadores")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 128, 255)
VERMELHO = (255, 0, 0)

# Fonte
fonte = pygame.font.Font(None, 36)

# Ler jogadores do arquivo
def ler_jogadores(arquivo):
    jogadores = []
    try:
        with open(arquivo, "r") as file:
            jogador_atual = {}
            for linha in file:
                linha = linha.strip()
                
                if not linha:  # Ignora linhas vazias
                    continue
                
                # Verifica se a linha contém ": " para garantir que seja formatada corretamente
                if ": " not in linha:
                    print(f"Formato inválido na linha: {linha}")
                    continue
                
                # Processa cada campo de acordo com o prefixo
                if linha.startswith("Jogador:"):
                    jogador_atual["nome"] = linha.split(": ")[1]
                elif linha.startswith("Pontuação Estudante:"):
                    jogador_atual["pontuacao_estudante"] = linha.split(": ")[1] if ": " in linha else ""
                elif linha.startswith("Pontuação Professor:"):
                    jogador_atual["pontuacao_professor"] = linha.split(": ")[1] if ": " in linha else ""
                elif linha.startswith("Fase 1 Concluída:"):
                    jogador_atual["fase_1_concluida"] = linha.split(": ")[1] == "True"
                elif linha.startswith("Fase 2 Concluída:"):
                    jogador_atual["fase_2_concluida"] = linha.split(": ")[1] == "True"
                elif linha.startswith("Tentativas Fase 1 Nível 1:"):
                    jogador_atual["tentativas_fase_1_nivel_1"] = int(linha.split(": ")[1])
                elif linha.startswith("Tentativas Fase 1 Nível 2:"):
                    jogador_atual["tentativas_fase_1_nivel_2"] = int(linha.split(": ")[1])
                elif linha.startswith("Tentativas Fase 2 Nível 1:"):
                    jogador_atual["tentativas_fase_2_nivel_1"] = int(linha.split(": ")[1])
                elif linha.startswith("Tentativas Fase 2 Nível 2:"):
                    jogador_atual["tentativas_fase_2_nivel_2"] = int(linha.split(": ")[1])
                elif linha.startswith("Pontuação Final:"):
                    jogador_atual["pontuacao_final"] = linha.split(": ")[1] if ": " in linha else ""
                elif linha.startswith("Data:"):
                    jogador_atual["data"] = linha.split(": ")[1]
                elif linha.startswith("--------------------------------------------------"):
                    if jogador_atual:  # Adiciona o jogador somente se tiver dados
                        jogadores.append(jogador_atual)
                        jogador_atual = {}
            
            # Adiciona o último jogador (caso não termine com uma linha de separação)
            if jogador_atual:
                jogadores.append(jogador_atual)

    except FileNotFoundError:
        print("Arquivo não encontrado!")
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")

    return jogadores

def desenhar_jogadores(tela, jogadores, pagina_atual):
    # Exibe 3 jogadores por vez
    jogadores_a_exibir = jogadores[pagina_atual * 3:(pagina_atual + 1) * 3]

    for idx, jogador in enumerate(jogadores_a_exibir):
        y_offset = 50 + idx * 100  # Posição Y para exibir cada jogador
        nome = jogador.get("nome", "Desconhecido")
        pontuacao_professor = jogador.get("pontuacao_professor", "Não disponível")
        data = jogador.get("data", "Data não disponível")
        
        texto = f"Nome: {nome}, Pontuação: {pontuacao_professor}, Data: {data}"
        # Aqui você desenha o texto na tela (assumindo que pygame está sendo usado)
        font = pygame.font.Font(None, 36)
        texto_surface = font.render(texto, True, (255, 255, 255))
        tela.blit(texto_surface, (50, y_offset))

# Exemplo de uso
jogadores = ler_jogadores("resultados.txt")
pagina_atual = 0

# Função para verificar cliques nos botões
def verificar_clique(pos, pagina_atual, total_jogadores, por_pagina=3):
    # Botão "Anterior"
    if 50 <= pos[0] <= 150 and ALTURA_TELA - 100 <= pos[1] <= ALTURA_TELA - 50:
        if pagina_atual > 0:
            pagina_atual -= 1

    # Botão "Próximo"
    if LARGURA_TELA - 150 <= pos[0] <= LARGURA_TELA - 50 and ALTURA_TELA - 100 <= pos[1] <= ALTURA_TELA - 50:
        if (pagina_atual + 1) * por_pagina < total_jogadores:
            pagina_atual += 1

    return pagina_atual

# Loop principal
rodando = True
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            pagina_atual = verificar_clique(pos, pagina_atual, len(jogadores))

    # Desenhar jogadores
    desenhar_jogadores(tela, jogadores, pagina_atual)

    # Atualizar tela
    pygame.display.flip()

pygame.quit()
sys.exit()
