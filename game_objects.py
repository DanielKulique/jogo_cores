import pygame, os
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

class Jogador:
    def __init__(self, nome, pontuacao_professor, pontuacao_estudante, data):
        self.nome = nome
        self.pontuacao_professor = pontuacao_professor
        self.pontuacao_estudante = pontuacao_estudante
        self.tentativas_fase1_nivel_1 = 0
        self.tentativas_fase1_nivel_2 = 0
        self.tentativas_fase2_nivel_1 = 0
        self.tentativas_fase2_nivel_2 = 0
        self.fase_1 = False
        self.fase_2 = False
        self.data = data

    def completar_fase(self, fase):
        if fase == 1:
            self.fase_1 = True
        elif fase == 2:
            self.fase_2 = True
        else:
            raise ValueError("Fase inválida. Use 1 ou 2.")

    def registrar_tentativa(self, fase, nivel):
        if fase == 1:
            if nivel == "primaria":
                self.tentativas_fase1_nivel_1 += 1
            elif nivel == "secundaria":
                self.tentativas_fase1_nivel_2 += 1
        elif fase == 2:
            if nivel == "primaria":
                self.tentativas_fase2_nivel_1 += 1
            elif nivel == "secundaria":
                self.tentativas_fase2_nivel_2 += 1
        else:
            raise ValueError("Fase ou nível inválidos.")

    def calcular_pontuacao(self):
        pontuacao = self.pontuacao_estudante
        if self.fase_1:
            pontuacao += (100 - self.tentativas_fase1_nivel_1 - self.tentativas_fase1_nivel_2)
        if self.fase_2:
            pontuacao += (100 - self.tentativas_fase2_nivel_1 - self.tentativas_fase2_nivel_2)
        #return max(0, pontuacao)

    def __str__(self):
        return (f"Jogador: {self.nome}\n"
                f"Pontuação Estudante: {self.pontuacao_estudante}\n"
                f"Pontuação Professor: {self.pontuacao_professor}\n"
                f"Fase 1 Concluída: {self.fase_1}\n"
                f"Fase 2 Concluída: {self.fase_2}\n"
                f"Tentativas Fase 1 Nível 1: {self.tentativas_fase1_nivel_1}\n"
                f"Tentativas Fase 1 Nível 2: {self.tentativas_fase1_nivel_2}\n"
                f"Tentativas Fase 2 Nível 1: {self.tentativas_fase2_nivel_1}\n"
                f"Tentativas Fase 2 Nível 2: {self.tentativas_fase2_nivel_2}\n"
                f"Pontuação Final: \n" #self.calcular_pontuacao()
                f"Data: {self.data}")

    def salvar_log(self, caminho_arquivo="resultados.txt"):
        """
        Salva a representação do jogador em um arquivo de log.
        """
        with open(caminho_arquivo, "a", encoding="utf-8") as arquivo:
            arquivo.write(self.__str__() + "\n" + "-" * 50 + "\n")

    @staticmethod
    def verificar_ultimo_jogador(caminho_arquivo="resultados.txt"):
        """
        Verifica se há um jogador registrado no arquivo de log e retorna o último jogador registrado.
        Caso não exista nenhum registro, retorna None.
        """
        if not os.path.exists(caminho_arquivo):
            print("Arquivo de log não encontrado.")
            return None

        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read().strip()
        
        if not conteudo:
            print("Arquivo de log está vazio.")
            return None

        # Dividimos os registros de jogadores pelo separador usado no método salvar_log()
        registros = conteudo.split("-" * 50)
        registros = [registro.strip() for registro in registros if registro.strip()]
        
        if not registros:
            print("Nenhum registro de jogador encontrado.")
            return None

        # Pega o último registro válido
        ultimo_registro = registros[-1]
        linhas = ultimo_registro.split("\n")
        
        if len(linhas) >= 9:  # Ajustar para o número correto de linhas esperadas
            try:
                nome = linhas[0].split(": ")[1] if len(linhas) > 0 else "Desconhecido"
                pontuacao_estudante = int(linhas[1].split(": ")[1]) if len(linhas) > 1 and linhas[1].split(": ")[1] else 0
                pontuacao_professor = int(linhas[2].split(": ")[1]) if len(linhas) > 2 and linhas[2].split(": ")[1] else 0
                data = linhas[-1].split(": ")[1] if len(linhas) > 8 else "Data desconhecida"  # A data está na última linha
                
                # Se o nome estiver vazio, considere isso como um erro
                if not nome.strip():
                    nome = "Desconhecido"
                
                return Jogador(nome, pontuacao_professor, pontuacao_estudante, data)
            except ValueError as ve:
                print(f"Erro ao converter pontuações para inteiro: {ve}")
                return None
        else:
            print("Dados do jogador estão incompletos!")
            return 



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
        self.ultimo_clique = 0

    def desenhar(self, tela):
        """
        Desenha o botão na tela.
        """
        if self.mostrar:
            pygame.draw.rect(tela, self.cor, self.rect, 2)
            texto_surface = self.fonte.render(self.texto, True, self.cor_texto)
            texto_rect = texto_surface.get_rect(center=self.rect.center)
            tela.blit(texto_surface, texto_rect)

    def foi_clicado(self, pos):
        return self.rect.collidepoint(pos)


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



class BotaoEspecial:
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
    def criar_botao_voltar(acao=None):
        """
        Cria um botão 'Voltar ao jogo →' com estilo configurado.
        """
        largura = 200
        altura = 60
        fonte = pygame.font.SysFont("Baskerville", 36, bold=True)
        return Botao(
            x=300,
            y=500,  # Ajuste conforme a altura da sua tela
            largura=largura,
            altura=altura,
            texto="Voltar ao jogo →",
            fonte=fonte,
            cor_normal=(255, 220, 140),  # Cor normal (#FFA12B)
            cor_hover=(255, 220, 100),  # Cor hover (#F78900)
            cor_sombra=(204, 153, 100),  # Cor da sombra (#915100)
            cor_texto=(0, 0, 0),  # Cor do texto (branco)
            acao=acao,
        )





class Bolinha:
    def __init__(self, x, y, cor, raio=67):
        self.x = x
        self.y = y
        self.cor = cor
        self.raio = raio
        self.hover = False  # Novo atributo para hover

    def foi_clicada(self, pos):
        """Verifica se o clique foi dentro da bolinha."""
        mx, my = pos
        distancia = ((self.x - mx) ** 2 + (self.y - my) ** 2) ** 0.5
        return distancia <= self.raio

    def verificar_hover(self, pos):
        """Verifica se o mouse está sobre a bolinha."""
        mx, my = pos
        distancia = ((self.x - mx) ** 2 + (self.y - my) ** 2) ** 0.5
        self.hover = distancia <= self.raio

    def desenhar(self, tela):
        """Desenha a bolinha com um efeito hover que inclui borda preta e brilho amarelo."""
        if self.hover:
            # Desenhar o efeito hover preto em torno da bolinha
            pygame.draw.circle(tela, (0, 0, 0), (self.x, self.y), self.raio + 5)
            raio1 = self.raio + 2
            brilho = 30
            for i in range (5):
                # Desenhar o brilho amarelo translúcido fora dos limites do hover preto
                raio1 += 3
                brilho += 5
                brilho_raio = raio1  # Ajuste para manter o brilho além da borda preta
                brilho_cor = (255, 255, 0, brilho)  # Amarelo translúcido
                surface = pygame.Surface((brilho_raio * 2, brilho_raio * 2), pygame.SRCALPHA)
                pygame.draw.circle(surface, brilho_cor, (brilho_raio, brilho_raio), brilho_raio)
                pygame.draw.circle(surface, (0, 0, 0, 0), (brilho_raio, brilho_raio), self.raio + 5)  # Recorte central
                tela.blit(surface, (self.x - brilho_raio, self.y - brilho_raio))
                    
        # Desenhar a bolinha principal
        pygame.draw.circle(tela, self.cor, (self.x, self.y), self.raio)


class Quadrado:
    def __init__(self, x, y, caminho_imagem, lado):
        self.x = x
        self.y = y
        self.lado = lado
        self.hover = False  # Novo atributo para hover
        self.imagem = pygame.image.load(caminho_imagem)  # Carrega a imagem
        self.imagem = pygame.transform.scale(self.imagem, (lado + 30, lado))  # Ajusta o tamanho da imagem

    def foi_clicada(self, pos):
        """Verifica se o clique foi dentro do quadrado."""
        mx, my = pos
        return self.x <= mx <= self.x + self.lado and self.y <= my <= self.y + self.lado

    def verificar_hover(self, pos):
        """Verifica se o mouse está sobre o quadrado."""
        mx, my = pos
        self.hover = self.x <= mx <= self.x + self.lado and self.y <= my <= self.y + self.lado

    def desenhar(self, tela):
        """Desenha o quadrado com a imagem e um efeito hover."""
        if self.hover:
            # Desenhar o efeito hover preto em torno do quadrado
            pygame.draw.rect(tela, (255, 255, 100), (self.x - 5, self.y - 5, self.lado + 35, self.lado + 20))

            # Criar brilho amarelo translúcido fora dos limites do hover preto
            brilho = 30
            for i in range(5):
                brilho += 5
                largura = self.lado + 35 + (i + 1) * 6
                altura = self.lado + 20 + (i + 1) * 6
                brilho_x = self.x - 5 - (i + 1) * 3
                brilho_y = self.y - 5 - (i + 1) * 3

                surface = pygame.Surface((largura, altura), pygame.SRCALPHA)
                brilho_cor = (255, 255, 0, brilho)  # Amarelo translúcido
                pygame.draw.rect(surface, brilho_cor, (0, 0, largura, altura))
                pygame.draw.rect(surface, (0, 0, 0, 0), (3, 3, largura - 6, altura - 6))  # Recorte central
                tela.blit(surface, (brilho_x, brilho_y))

        # Desenhar o quadrado com a imagem
        tela.blit(self.imagem, (self.x, self.y))







