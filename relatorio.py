import pygame
import sys
import json
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from game_objects import Botao

class Relatorio:
    def __init__(self):
        pygame.init()
        
        # Definir o tamanho da tela (ajuste conforme necessário)
        self.tela = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Inicializa a tela

        # Carregar e ajustar o layout do relatório
        self.layout_relatorio_professor = pygame.image.load("assets/layouts/12.png") 
        self.layout_relatorio_professor = pygame.transform.smoothscale(self.layout_relatorio_professor, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Desenhar o layout na tela
        self.tela.blit(self.layout_relatorio_professor, (0, 0))
        
        # Atualizar a tela após desenhar
        pygame.display.update()
        
        # Configurar o relógio para controle de FPS
        self.clock = pygame.time.Clock()
        
        # Criar uma nova superfície para os componentes da tela
        self.superficie_relatorio = pygame.Surface((800, 600))  # Novo nome para a superfície

        # Configurar a fonte para renderizar textos
        self.font = pygame.font.SysFont("Arial", 20)
        
        # Definir número de resultados por página e o deslocamento inicial
        self.resultados_por_pagina = 3
        self.offset_jogadores = 0
        self.cor_preta = (0,0,0)


    def ler_log(self, caminho):
        try:
            with open(caminho, "r", encoding="utf-8") as arquivo:
                linhas = arquivo.readlines()

            jogadores = []
            jogador_atual = []
            coletando = False

            for linha in linhas:
                linha = linha.strip()
                if linha.startswith("-") and all(c == "-" for c in linha):
                    continue

                if linha.strip().lower().startswith("jogador: "):  # Ignorar maiúsculas/minúsculas
                    if jogador_atual:
                        jogadores.append(jogador_atual)
                    jogador_atual = [linha.strip()]
                    coletando = True
                elif coletando:
                    if linha.startswith("Pontuacao Professor: "):  # Verificar apenas o início da linha
                        linha = self.formatar_pontuacao_professor(linha)  # Formatar a pontuação
                    jogador_atual.append(linha)
                elif linha.strip().lower().startswith("Pontuacao Professor:") and coletando:
                    jogador_atual.append(linha.strip())
                    jogadores.append(jogador_atual)
                    jogador_atual = []
                    coletando = False
                

            # Caso o último jogador não tenha sido adicionado
            if jogador_atual:
                jogadores.append(jogador_atual)

            return jogadores
        except FileNotFoundError:
            print("Arquivo resultados.txt não encontrado.")
            return []
        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")
            return []

    

    import json

    def formatar_pontuacao_professor(self, linha):
        
        try:
            # Extrai o trecho do dicionário da linha
            inicio = linha.index("{")
            dados_json = linha[inicio:].replace("'", '"')  # Substitui aspas simples por duplas (formato JSON)

            # Converte a string do dicionário para um objeto Python
            dados = json.loads(dados_json)

            partes = []
            for dificuldade, valores in dados.items():
                primarias = ", ".join(valores[0].get('primarias', [])) or "sem dificuldade"
                secundarias = ", ".join(valores[0].get('secundarias', [])) or "sem dificuldade"

                # Remover colchetes e aspas desnecessárias
                primarias = primarias.replace("[", "").replace("]", "").replace("'", "")
                secundarias = secundarias.replace("[", "").replace("]", "").replace("'", "")

                partes_dificuldade = [
                    f"primarias: {primarias}",
                    f"secundarias: {secundarias}"
                ]

                partes.append(f"{dificuldade.capitalize()}: {', '.join(partes_dificuldade)}")

            return "Pontuação Professor:\n" + "\n".join(partes)
        except Exception as e:
            print(f"Erro ao formatar pontuação: {e}")
            return linha





    def quebrar_texto(self, texto, largura_maxima, font):
        palavras = texto.split(" ")
        linhas = []
        linha_atual = ""

        for palavra in palavras:
            if font.size(linha_atual + " " + palavra)[0] <= largura_maxima:
                linha_atual += " " + palavra
            else:
                if linha_atual:
                    linhas.append(linha_atual)
                linha_atual = palavra

        if linha_atual:
            linhas.append(linha_atual)

        return linhas

    def desenhar_jogadores(self, jogadores):
        largura_tela = self.tela.get_width()
        altura_tela = self.tela.get_height()

        largura_quadrado = largura_tela // 4.3
        altura_quadrado = altura_tela - 270  # Reservar espaço para botões

        for i, jogador in enumerate(jogadores):
            x = (i + 1) * (largura_tela // (len(jogadores) + 0.9)) - largura_quadrado // 3 - 80
            y = 165

            # Desenhar o retângulo
            pygame.draw.rect(self.tela, (255, 228, 225), (x, y, largura_quadrado, altura_quadrado))

            # Desenhar o texto do jogador com quebra de linha
            for j, linha in enumerate(jogador):
                linhas_quebradas = self.quebrar_texto(linha.strip(), largura_quadrado - 20, self.font)
                for l, linha_quebrada in enumerate(linhas_quebradas):
                    texto = self.font.render(linha_quebrada, True, (0, 0, 0))
                    self.tela.blit(texto, (x + 10, y + 10 + (j + l) * 30))

    def acao_professor(self):
        caminho_log = "resultados.txt"
        logs = self.ler_log(caminho_log)

        if not logs:
            print("Nenhum jogador encontrado no arquivo de resultados.")

        running = True
        while running:
            self.tela.blit(self.layout_relatorio_professor, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT and self.offset_jogadores + self.resultados_por_pagina < len(logs):
                        self.offset_jogadores += self.resultados_por_pagina
                    elif event.key == pygame.K_LEFT and self.offset_jogadores > 0:
                        self.offset_jogadores -= self.resultados_por_pagina
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    largura_tela = self.tela.get_width()
                    altura_tela = self.tela.get_height()

                    pos = pygame.mouse.get_pos()
                    if bot.foi_clicado(pos):
                        bot.acao()

                    botao_anterior = pygame.Rect(50, altura_tela - 500, 100, 60)
                    botao_proximo = pygame.Rect(largura_tela - 150, altura_tela - 500, 100, 60)

                    if botao_proximo.collidepoint(mouse_x, mouse_y) and self.offset_jogadores + self.resultados_por_pagina < len(logs):
                        self.offset_jogadores += self.resultados_por_pagina
                    elif botao_anterior.collidepoint(mouse_x, mouse_y) and self.offset_jogadores > 0:
                        self.offset_jogadores -= self.resultados_por_pagina

            jogadores_exibidos = logs[self.offset_jogadores:self.offset_jogadores + self.resultados_por_pagina]
            self.desenhar_jogadores(jogadores_exibidos)

            # Desenhar botões de navegação
            largura_tela = self.tela.get_width()
            altura_tela = self.tela.get_height()
            botao_anterior = pygame.Rect(50, altura_tela - 500, 100, 60)
            botao_proximo = pygame.Rect(largura_tela - 150, altura_tela - 500, 100, 60)
            bot = Botao(SCREEN_WIDTH * 0.88, SCREEN_HEIGHT * 0.83, SCREEN_WIDTH * 0.11, SCREEN_HEIGHT * 0.16, "Sair", (255, 255, 0), acao=lambda:quit())
            bot.desenhar(self.tela)
           # Desenhar o contorno primeiro (ligeiramente maior)
            pygame.draw.rect(self.tela, self.cor_preta, botao_anterior.inflate(10, 10))  
            pygame.draw.rect(self.tela, self.cor_preta, botao_proximo.inflate(10, 10))  # Reduzi o tamanho para 10,10

            # Desenhar o botão por cima do contorno
            pygame.draw.rect(self.tela, (255, 255, 203), botao_anterior)  
            pygame.draw.rect(self.tela, (255, 255, 203), botao_proximo)  

            # Renderizar o texto por cima dos botões
            texto_anterior = self.font.render("Anterior", True, (0, 0, 0))
            texto_proximo = self.font.render("Próximo", True, (0, 0, 0))

            self.tela.blit(texto_anterior, (botao_anterior.x + 15, botao_anterior.y + 15))
            self.tela.blit(texto_proximo, (botao_proximo.x + 15, botao_proximo.y + 15))

            

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    relatorio = Relatorio()
    relatorio.acao_professor()
