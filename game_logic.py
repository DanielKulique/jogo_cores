import pygame, random, sys, time, os
from game_objects import Botao, BotaoEspecial, Bolinha, Jogador, Quadrado, Audio, BotaoVoltar
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from datetime import datetime
from relatorio import Relatorio
import subprocess
import moviepy.editor as mp
import numpy as np
import threading


class Jogo:
    def __init__(self):
        pygame.init()
        #tela
        pygame.display.set_caption("JOGO DAS CORES")
        self.tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.modo_tela_cheia = True  # Estado inicial
        self.menu_atual = None
        self.data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.fase = 1
        #audio
        self.volume = 0.5
        pygame.mixer.init()
        #pygame.mixer.music.load("")
        #pygame.mixer.music.play(-1)  # Toca em loop infinito
        pygame.mixer.music.set_volume(self.volume)
        self.audio = Audio()


        pygame.display.set_caption("Menu Inicial")
        self.clock = pygame.time.Clock()
        self.running = True

        self.menu_atual = "menu_principal" 
        self.ultimo_clique = pygame.time.get_ticks()
        self.nivel_fase_1 = "primaria"
        self.cor_clicada = ""
        self.nivel_fase_2 = "primaria"
        self.erro = False
        self.dificuldade_identificar = {"cores_primarias": [], "cores_secundarias": []}
        self.dificuldade_identificar_2 = {"cores_primarias": [], "cores_secundarias": []}
        self.dificuldade = {
                            "GRANDE DIFICULDADE": [{"primarias": [], "secundarias": []}], 
                            "LEVE DIFICULDADE": [{"primarias": [], "secundarias": []}]
        }

        self.cores_primarias = {
            "vermelho": (255, 0, 0),
            "amarelo": (255, 255, 0),
            "azul": (0, 0, 255),
        }

        self.cores_secundarias = {
            "laranja": (255, 165, 0),
            "verde": (0, 128, 0),
            "roxo": (128, 0, 128),
        }
        #primeira fase
        self.acertou3_primaria = 1
        self.acertou3_secundaria = 1
        #segunda fase
        self.acertos_nivel1 = 0
        self.acertos_nivel2 = 0

        self.cores_erradas = { 
            "marrom": (139, 69, 19),
            "bege": (200, 200, 160),
            "cinza": (128, 128, 128),
            "ciano_claro": (100, 180, 180),
        }
        
        self.bolinhas = []
        self.iniciar_bolinhas()

        self.jogador = Jogador(
            nome = "",
            pontuacao_professor = None,
            pontuacao_estudante = "",
            data= self.data
            )

        self.fase_1 = "Desbloqueada"
        self.fase_2 = "Bloqueada"
            
        # Instanciando os botões
        self.botoes = {
            "professor": Botao(SCREEN_WIDTH * 0.04, SCREEN_HEIGHT * 0.74, SCREEN_WIDTH * 0.2, SCREEN_HEIGHT * 0.17, "Professor", (255, 0, 0), acao=lambda: self.acao_professor()),
            "config": Botao(SCREEN_WIDTH * 0.013, SCREEN_HEIGHT * 0.027, SCREEN_WIDTH * 0.06, SCREEN_HEIGHT * 0.1, "Configuração", (0, 255, 0), acao=lambda: self.acao_configuracao()),
            "nome": Botao((SCREEN_WIDTH - (SCREEN_WIDTH * 0.5)) // 2, (SCREEN_HEIGHT - (SCREEN_HEIGHT * 0.1)) // 2 + SCREEN_HEIGHT * 0.05, SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.15, "Nome", (0, 0, 255), acao=lambda: self.acao_nome_jogador()),
            "ajuda": Botao(SCREEN_WIDTH * 0.94, SCREEN_HEIGHT * 0.03, SCREEN_WIDTH * 0.05, SCREEN_HEIGHT * 0.1, "Ajuda", (255, 255, 0), acao=lambda: self.acao_ajuda_jogo()),
            "som": Botao(SCREEN_WIDTH * 0.85, SCREEN_HEIGHT * 0.03, SCREEN_WIDTH * 0.09, SCREEN_HEIGHT * 0.1, "Som", (255, 165, 0), acao=lambda: self.acao_som(self.tipo_acao_menu)),
        }
        self.botoes_config = {
            "ajuda": Botao(SCREEN_WIDTH * 0.94, SCREEN_HEIGHT * 0.03, SCREEN_WIDTH * 0.05, SCREEN_HEIGHT * 0.1, "Ajuda", (255, 255, 0), acao=lambda:self.acao_ajuda_jogo()),
            "som": Botao(SCREEN_WIDTH * 0.85, SCREEN_HEIGHT * 0.03, SCREEN_WIDTH * 0.09, SCREEN_HEIGHT * 0.1, "Som", (255, 165, 0), acao=lambda:self.acao_som(self.tipo_acao_menu)),
            "audio": Botao(SCREEN_WIDTH * 0.36, SCREEN_HEIGHT * 0.387, SCREEN_WIDTH * 0.22, SCREEN_HEIGHT * 0.074, "Audio", (150, 150, 255), acao=self.verifica_volume),
            "relatorio": Botao(SCREEN_WIDTH * 0.36, SCREEN_HEIGHT * 0.49, SCREEN_WIDTH * 0.22, SCREEN_HEIGHT * 0.074, "relatorio", (150, 150, 255), acao=lambda:self.relatorio_estudante(self.fase)),
            "sair": Botao(SCREEN_WIDTH * 0.88, SCREEN_HEIGHT * 0.83, SCREEN_WIDTH * 0.11, SCREEN_HEIGHT * 0.16, "Sair", (255, 255, 0), acao=lambda:self.acao_sair())
        }
        self.botoes_menu_fases = {
            "fase_1": Botao(SCREEN_WIDTH * 0.38, SCREEN_HEIGHT * 0.48, SCREEN_WIDTH * 0.23, SCREEN_HEIGHT * 0.07, "Fase 1", (150, 150, 255), acao=lambda: self.primeira_fase()), 
            "som": Botao(SCREEN_WIDTH * 0.85, SCREEN_HEIGHT * 0.03, SCREEN_WIDTH * 0.09, SCREEN_HEIGHT * 0.1, "Som", (255, 165, 0), acao=lambda: self.acao_som(self.tipo_acao_menu)),
            "config": Botao(SCREEN_WIDTH * 0.013, SCREEN_HEIGHT * 0.027, SCREEN_WIDTH * 0.06, SCREEN_HEIGHT * 0.1, "Configuração", (0, 255, 0), acao=lambda: self.acao_configuracao()),
            "ajuda": Botao(SCREEN_WIDTH * 0.94, SCREEN_HEIGHT * 0.03, SCREEN_WIDTH * 0.05, SCREEN_HEIGHT * 0.1, "Ajuda", (255, 255, 0), acao=lambda: self.acao_ajuda_menu_fases()),
            #"sair": Botao(SCREEN_WIDTH * 0.88, SCREEN_HEIGHT * 0.83, SCREEN_WIDTH * 0.11, SCREEN_HEIGHT * 0.16, "Sair", (255, 255, 0), acao=lambda: self.menu_nome())          
        }
        self.tipo_acao_fase1 = ""
        self.tipo_acao_fase2 = ""
        self.botoes_fase_1 = {
            #"menu": Botao((SCREEN_WIDTH - 750) // 2 + 260, (SCREEN_HEIGHT - 120) // 2 - 70, 210, 95, "Menu", (100, 255, 100), acao=self.menu_nome),
            "config": Botao(SCREEN_WIDTH * 0.013, SCREEN_HEIGHT * 0.027, SCREEN_WIDTH * 0.06, SCREEN_HEIGHT * 0.1, "Configuração", (0, 255, 0), acao=lambda:self.acao_configuracao()),
            "ajuda": Botao(SCREEN_WIDTH - 80, 20, 60, 80, "Ajuda", (255, 255, 0), acao=lambda:self.acao_ajuda_fase1()),
            "som": Botao(SCREEN_WIDTH * 0.85, SCREEN_HEIGHT * 0.03, SCREEN_WIDTH * 0.09, SCREEN_HEIGHT * 0.1, "Som", (255, 165, 0), acao= lambda: self.acao_som(self.tipo_acao_fase1)),
        }
        self.botoes_fase_2 = {
            #"menu": Botao((SCREEN_WIDTH - 750) // 2 + 260, (SCREEN_HEIGHT - 120) // 2 - 70, 210, 95, "Menu", (100, 255, 100), acao=self.menu_nome),
            "config": Botao(SCREEN_WIDTH * 0.013, SCREEN_HEIGHT * 0.027, SCREEN_WIDTH * 0.06, SCREEN_HEIGHT * 0.1, "Configuração", (0, 255, 0), acao=lambda:self.acao_configuracao()),
            "ajuda": Botao(SCREEN_WIDTH - 80, 20, 60, 80, "Ajuda", (255, 255, 0), acao=lambda:self.acao_ajuda_fase2()),
            "som": Botao(SCREEN_WIDTH * 0.85, SCREEN_HEIGHT * 0.03, SCREEN_WIDTH * 0.09, SCREEN_HEIGHT * 0.1, "Som", (255, 165, 0), acao= lambda: self.acao_som(self.tipo_acao_fase2)),
        }

        
        
        self.caminho_videos = {
            "tutorial": "assets/videos/Funcionalidades.mp4",
            "como_jogar_1": "assets/videos/Como_jogar_1.mp4",
            "como_jogar_2": "assets/videos/Como_jogar_2.mp4",
            "cor_primaria": "assets/videos/Cor_primária.mp4",
            "cor_secundaria": "assets/videos/Cores_secundárias.mp4",
        }

        self.quadrados_primarios = {}
        self.quadrados_secundarios = {}
        self.quadrados_caixa = {}
        self.iniciar_quadrados()
        #self.inicia_caixa()


        # Carregando o layout de fundo do menu inicial
        self.layout_menu = pygame.image.load("assets/layouts/start.png")
        self.layout_menu = pygame.transform.smoothscale(self.layout_menu, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.layout_config = pygame.image.load("assets/layouts/configuração1.png")
        self.layout_config = pygame.transform.smoothscale(self.layout_config, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.layout_menu_fases = pygame.image.load("assets/layouts/fase_1_desbloqueada.png")
        self.layout_menu_fases = pygame.transform.smoothscale(self.layout_menu_fases, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.layout_menu_fases_2 = pygame.image.load("assets/layouts/fase_1_2_desbloqueada.png")
        self.layout_menu_fases_2 = pygame.transform.smoothscale(self.layout_menu_fases_2, (SCREEN_WIDTH, SCREEN_HEIGHT))


        #fase_1
        self.layout_nivel_1 = pygame.image.load("assets/layouts/51.png")
        self.layout_nivel_1 = pygame.transform.smoothscale(self.layout_nivel_1, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.layout_nivel_2 = pygame.image.load("assets/layouts/52.png")
        self.layout_nivel_2 = pygame.transform.smoothscale(self.layout_nivel_2, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.layout_acertou_nivel_1 = pygame.image.load("assets/layouts/mensagem_acertou.png")
        self.layout_acertou_nivel_1 = pygame.transform.smoothscale(self.layout_acertou_nivel_1, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.layout_acertou_nivel_2 = pygame.image.load("assets/layouts/23.png")
        self.layout_acertou_nivel_2 = pygame.transform.smoothscale(self.layout_acertou_nivel_2, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.layout_errou = pygame.image.load("assets/layouts/53.png")
        self.layout_errou = pygame.transform.smoothscale(self.layout_errou, (SCREEN_WIDTH, SCREEN_HEIGHT))

        #fase_2
        self.layout_nivel_12 = pygame.image.load("assets/segunda_fase/40.png") 
        self.layout_nivel_12 = pygame.transform.smoothscale(self.layout_nivel_12, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.layout_nivel_22 = pygame.image.load("assets/segunda_fase/48.png") 
        self.layout_nivel_22 = pygame.transform.smoothscale(self.layout_nivel_22, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.layout_objeto_errado_secundaria =  pygame.image.load("assets/segunda_fase/45.png")
        self.layout_objeto_errado_secundaria = pygame.transform.smoothscale(self.layout_objeto_errado_secundaria, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.layout_objeto_errado_primario = pygame.image.load("assets/segunda_fase/50.png")
        self.layout_objeto_errado_primario = pygame.transform.smoothscale(self.layout_objeto_errado_primario, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.layout_primaria_organizada =  pygame.image.load("assets/segunda_fase/36.png")
        self.layout_primaria_organizada = pygame.transform.smoothscale(self.layout_primaria_organizada, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.layout_caixa_organizada = pygame.image.load("assets/segunda_fase/49.png")
        self.layout_caixa_organizada = pygame.transform.smoothscale(self.layout_caixa_organizada, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.layout_relatorio = pygame.image.load("assets/layouts/8.png")
        self.layout_relatorio = pygame.transform.smoothscale(self.layout_relatorio, (SCREEN_WIDTH, SCREEN_HEIGHT))


        self.quadrados_errados = {}
        
    #ENCAPSULANDO FUNCOES DA CLASSE JOGADOR!
    def registrar_tentativa(self, fase, nivel, acertou):
        """encapsula o registro de tentativas no jogador"""
        self.jogador.registrar_tentativa(fase, nivel, acertou)


    def completar_fase(self, fase):
        """marca as fases concluidas"""
        self.jogador.completar_fase(fase)
    

    def salva_estatisticas(self):
        """salva progresso jogador"""
        ultimo_jogador = Jogador.verificar_ultimo_jogador("resultados.txt")
        if ultimo_jogador.nome == self.jogador.nome:
            self.apagar_ultimas_linhas("resultados.txt", 12) # apaga o ultimo log para nao repetir os dados do mesmo jogador!
            self.jogador.salvar_log()
        else:
            self.jogador.salvar_log()


    #ENCAPSULAR QUADRADOS
    def desenhar_quadrados(self):
        """Desenha todos os quadrados na tela."""
        if self.nivel_fase_2 == "primaria":
            for quadrado in self.quadrados_primarios.values():
                quadrado.desenhar(self.tela)
            quadrados_atuais = self.quadrados_primarios
        else:
            for quadrado in self.quadrados_secundarios.values():
                quadrado.desenhar(self.tela)
            quadrados_atuais = self.quadrados_secundarios
        
        for nome in self.quadrados_errados:  # Percorre os nomes dos quadrados errados
            if nome in quadrados_atuais:  # Garante que o nome existe no dicionário
                quadrado = quadrados_atuais[nome]  # Obtém o objeto Quadrado correspondente
                quadrado.desenhar_x(self.tela)  # Chama o método corretamente
 
    

    def verificar_clique_quadrado(self, pos):
        """Verifica qual quadrado foi clicado."""
        if self.nivel_fase_2 == "primaria":
            for nome, quadrado in self.quadrados_primarios.items():
                if quadrado.foi_clicada(pos):
                    print(f"Quadrado clicado: {nome}")
                    return nome
        else:
            for nome, quadrado in self.quadrados_secundarios.items():
                if quadrado.foi_clicada(pos):
                    print(f"Quadrado clicado: {nome}")
                    return nome
        return None
    #FIM ENCAPSULAMENTO

    def rodar_video(self, nome_video):
        """Reproduz um vídeo no Pygame com áudio sincronizado."""
        if nome_video not in self.caminho_videos:
            print(f"Vídeo '{nome_video}' não encontrado!")
            return

        caminho = self.caminho_videos[nome_video]
        
        try:
            clip = mp.VideoFileClip(caminho)  # Carrega o vídeo
        except Exception as e:
            print(f"Erro ao carregar o vídeo: {e}")
            return

        # Obtém a resolução original do vídeo
        video_largura, video_altura = clip.size
        screen_largura, screen_altura = SCREEN_WIDTH, SCREEN_HEIGHT

        # Calcula fator de escala para manter proporção
        escala = min(screen_largura / video_largura, screen_altura / video_altura)
        novo_largura = int(video_largura * escala)
        novo_altura = int(video_altura * escala)

        self.tela = pygame.display.set_mode((screen_largura, screen_altura))  # Mantém tela cheia

        clock = pygame.time.Clock()

        # Iniciar áudio em uma thread separada
        if clip.audio:
            threading.Thread(target=clip.audio.preview).start()  # Reproduz áudio em paralelo

        for frame in clip.iter_frames(fps=30, dtype="uint8"):
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    clip.close()
                    return

            surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))  # Converte frame para pygame
            surface = pygame.transform.smoothscale(surface, (novo_largura, novo_altura))  # Redimensiona mantendo proporção

            # Centraliza o vídeo na tela
            x = (screen_largura - novo_largura) // 2
            y = (screen_altura - novo_altura) // 2
            self.tela.fill((0, 0, 0))  # Fundo preto para evitar bordas brancas
            self.tela.blit(surface, (x, y))

            pygame.display.update()
            clock.tick(30)


    def verifica_volume(self):
        print(f"Antes: {self.volume}")  # Depuração

        if self.volume == 0:
            self.volume = 0.5
        else:
            self.volume = 0

        print(f"Depois: {self.volume}")  # Depuração

    def alternar_tela(self):
        """
        Alterna entre o modo tela cheia e o modo janela.
        Redimensiona o layout do menu para se ajustar à nova resolução.
        """
        if self.modo_tela_cheia:
            # Volta para o modo janela
            
            self.tela = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.modo_tela_cheia = False
            print("Modo janela ativado.")
        else:
            # Ativa o modo tela cheia
            self.tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.modo_tela_cheia = True
            print("Modo tela cheia ativado.")

        # Redimensiona o layout para o tamanho atual da tela
        largura_tela, altura_tela = pygame.display.get_surface().get_size()
        self.layout_menu = pygame.image.load("assets/layouts/start.png")
        self.layout_menu = pygame.transform.smoothscale(self.layout_menu, (largura_tela, altura_tela))


    def apagar_ultimas_linhas(self, caminho_arquivo, linhas_para_remover):
        """
        Remove as últimas 'linhas_para_remover' do arquivo especificado.
        
        :param caminho_arquivo: Caminho para o arquivo de texto.
        :param linhas_para_remover: Número de linhas a serem removidas a partir do final.
        """
        try:
            # Verificar se o arquivo existe
            if not os.path.exists(caminho_arquivo):
                print(f"Arquivo '{caminho_arquivo}' não encontrado.")
                return

            # Ler todas as linhas do arquivo
            with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
                linhas = arquivo.readlines()

            # Garantir que há linhas suficientes para remover
            if len(linhas) <= linhas_para_remover:
                print("Não há linhas suficientes para remover.")
                linhas = []  # Remove todo o conteúdo
            else:
                linhas = linhas[:-linhas_para_remover]  # Mantém apenas as linhas necessárias

            # Escrever as linhas restantes de volta ao arquivo
            with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
                arquivo.writelines(linhas)

            print(f"As últimas {linhas_para_remover} linhas foram removidas do arquivo '{caminho_arquivo}'.")
        
        except Exception as e:
            print(f"Ocorreu um erro ao processar o arquivo: {e}")


    def adicionar_dificuldade(self, categoria, cor):
        """Adiciona a cor à lista de dificuldades no dicionário, evitando duplicatas."""
        if categoria in self.dificuldade_identificar:
            if cor not in self.dificuldade_identificar[categoria]:
                if cor == "desconhecida":
                    pass
                else:
                    self.dificuldade_identificar[categoria].append(cor)


    def verificar_dificuldade(self):
        # Contadores para as cores
        contador_cores = {
            "cores_primarias": {},
            "cores_secundarias": {}
        }

        # Função auxiliar para contar ocorrências de cores
        def contar_cores(dicionario):
            for tipo_cor, cores in dicionario.items():
                for cor in cores:
                    if cor in contador_cores[tipo_cor]:
                        contador_cores[tipo_cor][cor] += 1
                    else:
                        contador_cores[tipo_cor][cor] = 1

        # Contar cores de dificuldade_identificar e dificuldade_identificar_2
        contar_cores(self.dificuldade_identificar)
        contar_cores(self.dificuldade_identificar_2)

        # Resetar dificuldade
        self.dificuldade = {
            "GRANDE DIFICULDADE": [{"primarias": [], "secundarias": []}],
            "LEVE DIFICULDADE": [{"primarias": [], "secundarias": []}]
        }

        # Classificar as cores baseadas na contagem
        for tipo_cor, cores in contador_cores.items():
            for cor, count in cores.items():
                if count >= 2:  # Grande dificuldade
                    if tipo_cor == "cores_primarias":
                        self.dificuldade["GRANDE DIFICULDADE"][0]["primarias"].append(cor)
                    elif tipo_cor == "cores_secundarias":
                        self.dificuldade["GRANDE DIFICULDADE"][0]["secundarias"].append(cor)
                elif count == 1:  # Leve dificuldade
                    if tipo_cor == "cores_primarias":
                        self.dificuldade["LEVE DIFICULDADE"][0]["primarias"].append(cor)
                    elif tipo_cor == "cores_secundarias":
                        self.dificuldade["LEVE DIFICULDADE"][0]["secundarias"].append(cor)

        # Exibir resultados para depuração
        print("Dificuldade atualizada:")
        print(self.dificuldade)


    def iniciar_quadrados(self):
        """Inicializa os quadrados em posições aleatórias baseadas nas coordenadas fornecidas."""
        '''
        coordenadas_disponiveis = [
            (840, 150),
            (1080, 170),g
            (840, 310),
            (1080, 370),
            (890, 440),
        ]
        coordenadas_disponiveis_fase2 = [
            (800, 120),
            (1020, 170),
            (800, 280),
            (1040, 370),
            (850, 420),
        ]
        '''
        coordenadas_disponiveis = [
            (SCREEN_WIDTH * 0.66, SCREEN_HEIGHT * 0.2),
            (SCREEN_WIDTH * 0.66, SCREEN_HEIGHT * 0.4),
            (SCREEN_WIDTH * 0.66, SCREEN_HEIGHT * 0.6),
            (SCREEN_WIDTH * 0.83, SCREEN_HEIGHT * 0.29),
            (SCREEN_WIDTH * 0.83, SCREEN_HEIGHT * 0.49),
        ]
        coordenadas_disponiveis_fase2 = [
            (SCREEN_WIDTH * 0.66, SCREEN_HEIGHT * 0.2),
            (SCREEN_WIDTH * 0.66, SCREEN_HEIGHT * 0.4),
            (SCREEN_WIDTH * 0.66, SCREEN_HEIGHT * 0.6),
            (SCREEN_WIDTH * 0.83, SCREEN_HEIGHT * 0.29),
            (SCREEN_WIDTH * 0.83, SCREEN_HEIGHT * 0.49),
        ]

        if self.nivel_fase_2 == "primaria":
            nomes = ["bola_azul", "osso_amarelo", "osso_preto", "osso_vermelho", "urso_marrom"]
            
            random.shuffle(coordenadas_disponiveis)  # Embaralha as coordenadas
            
            for nome, (x, y) in zip(nomes, coordenadas_disponiveis):
                # Associa cada nome de quadrado a uma coordenada embaralhada
                self.quadrados_primarios[nome] = Quadrado(x, y, f"assets/objetos_primarios/{nome}.png", 120)
        else:
            nomes = ["bola_verde", "estrela_roxa", "flor_rosa", "laco_laranja", "osso_azul"]
            
            random.shuffle(coordenadas_disponiveis_fase2)  # Embaralha as coordenadas
            
            for nome, (x, y) in zip(nomes, coordenadas_disponiveis_fase2):
                # Associa cada nome de quadrado a uma coordenada embaralhada
                self.quadrados_secundarios[nome] = Quadrado(x, y, f"assets/objetos_secundarios/{nome}.png", 140)
            

    def remover_quadrado(self, nome):
        """Remove um quadrado pelo nome."""
        if self.nivel_fase_2 == "primaria":
            if nome in self.quadrados_primarios:
                del self.quadrados_primarios[nome]  # Ou: self.quadrados.pop(nome)
                print(f"{nome} foi removido com sucesso!")
            else:
                print(f"Erro: {nome} não encontrado.")
        else:
            if nome in self.quadrados_secundarios:
                del self.quadrados_secundarios[nome]
                print(f"{nome} foi removido com sucesso!")
            else:
                print(f"Erro: {nome} não encontrado.")


    def inicia_caixa(self, objeto): 

        if self.nivel_fase_2 == "primaria":
            if objeto == "bola_azul":
                self.quadrados_caixa["bola_azul"] = Quadrado(SCREEN_WIDTH * 0.44, SCREEN_HEIGHT * 0.6, f"assets/objetos_primarios/bola_azul.png", 120)
                self.remover_quadrado("bola_azul")
            elif objeto == "osso_amarelo":
                self.quadrados_caixa["osso_amarelo"] = Quadrado(SCREEN_WIDTH * 0.43, SCREEN_HEIGHT * 0.6, f"assets/objetos_primarios/osso_amarelo.png", 120)
                self.remover_quadrado("osso_amarelo")
            elif objeto == "osso_vermelho":
                self.quadrados_caixa["osso_vermelho"] = Quadrado(SCREEN_WIDTH * 0.46, SCREEN_HEIGHT * 0.63, f"assets/objetos_primarios/osso_vermelho.png", 120)
                self.remover_quadrado("osso_vermelho") 
        else:
            if objeto == "bola_verde":
                self.quadrados_caixa["bola_verde"] = Quadrado(SCREEN_WIDTH * 0.43, SCREEN_HEIGHT * 0.6, f"assets/objetos_secundarios/bola_verde.png", 150)
                self.remover_quadrado("bola_verde")
            elif objeto == "laco_laranja":
                self.quadrados_caixa["laco_laranja"] = Quadrado(SCREEN_WIDTH * 0.41, SCREEN_HEIGHT * 0.6, f"assets/objetos_secundarios/laco_laranja.png", 150)
                self.remover_quadrado("laco_laranja")
            elif objeto == "estrela_roxa":
                self.quadrados_caixa["estrela_roxa"] = Quadrado(SCREEN_WIDTH * 0.45, SCREEN_HEIGHT * 0.63, f"assets/objetos_secundarios/estrela_roxa.png", 150)
                self.remover_quadrado("estrela_roxa") 


    def desenhar_menu(self):
        """Desenha o layout do menu inicial com os botões."""
        # Desenhar o fundo
        self.tela.blit(self.layout_menu, (0, 0))
        
        # Desenhar os botões
        for botao in self.botoes.values():
            botao.desenhar(self.tela)


    def desenhar_menu_fases(self):
        """desenha o layout do menu de fases"""
        self.verifica_fases_jogador()
        
        if self.fase_2 == "Bloqueada":
            self.tela.blit(self.layout_menu_fases, (0, 0))
        elif self.fase_2 == "Desbloqueada":
            self.tela.blit(self.layout_menu_fases_2, (0, 0))
            self.botoes_menu_fases["fase_2"] = Botao(SCREEN_WIDTH * 0.38, SCREEN_HEIGHT * 0.587, SCREEN_WIDTH * 0.23, SCREEN_HEIGHT * 0.07, "Fase 2", (255, 150, 150), acao=lambda:self.segunda_fase())

        # Desenha os botoes do menu

        for botao in self.botoes_menu_fases.values():
            botao.desenhar(self.tela)


    def desenhar_configuracao(self):
        """Desenha o layout do menu inicial com os botões."""
        # Desenhar o fundo
        self.tela.blit(self.layout_config, (0, 0))

        # desenha os botoes da config
        for botao in self.botoes_config.values():
            botao.desenhar(self.tela)


    def iniciar_bolinhas(self):
     
        # Sorteia uma bolinha neutra aleatoriamente
        indice_neutra = random.randint(0, 3)
        '''
        # Coordenadas fixas para as bolinhas
        coordenadas = [
            (815, 216),  # Primeira bolinha
            (1107, 216),  # Segunda bolinha
            (815, 464),  # Terceira bolinha
            (1107, 464),  # Quarta bolinha
        ]'''

        coordenadas = [
            (SCREEN_WIDTH * 0.66, SCREEN_HEIGHT * 0.33),  # Primeira bolinha
            (SCREEN_WIDTH * 0.83, SCREEN_HEIGHT * 0.33),  # Segunda bolinha
            (SCREEN_WIDTH * 0.66, SCREEN_HEIGHT * 0.64),  # Terceira bolinha
            (SCREEN_WIDTH * 0.83, SCREEN_HEIGHT * 0.64),  # Quarta bolinha
        ]
        
        # Copia as cores disponíveis
        cores_neutras_disponiveis = list(self.cores_erradas.values())
        cores_primarias_disponiveis = list(self.cores_primarias.values())
        cores_secundarias_disponiveis = list(self.cores_secundarias.values())
        
        # Limpa a lista de bolinhas antes de iniciar
        self.bolinhas.clear()
        
        for i, (x, y) in enumerate(coordenadas):
            if i == indice_neutra:  # Esta bolinha recebe uma cor neutra
                cor = random.choice(cores_neutras_disponiveis)
                cores_neutras_disponiveis.remove(cor)  # Remove a cor escolhida
            else:  # As demais recebem cores primárias ou secundárias
                if self.nivel_fase_1 == "primaria":
                    cor = random.choice(cores_primarias_disponiveis)
                    cores_primarias_disponiveis.remove(cor)  # Remove a cor escolhida
                else:
                    cor = random.choice(cores_secundarias_disponiveis)
                    cores_secundarias_disponiveis.remove(cor)  # Remove a cor escolhida
            
            # Adiciona a bolinha à lista
            self.bolinhas.append(Bolinha(x, y, cor))


    def delay(self, tempo_inicio, delay):
        while True:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - tempo_inicio >= delay:
                print("10 segundos se passaram!")
                break

    

    def verificar_clique_bolinha(self, pos):
        """
        Verifica qual bolinha foi clicada e retorna se ela está correta ou não.
        """
        for bolinha in self.bolinhas:
            if bolinha.foi_clicada(pos):

                erradas = self.cores_erradas.values()

                if self.nivel_fase_1 == "primaria":
                    nivel = self.cores_primarias.values()  # nivel_1 cores primárias
                elif self.nivel_fase_1 == "secundaria":
                    nivel = self.cores_secundarias.values()  # nivel_2 cores secundárias
                

                if bolinha.cor in nivel:
                    print(f"AQUI--------> {bolinha.cor}")
                    self.bolinhas.remove(bolinha)
                    return True  # Bolinha correta foi clicada
                
                elif bolinha.cor in erradas:
                    print("bolinha errada clicada")
                    self.erro = True
                    return False


    def obter_nome_cor(self, rgb):
        # Verifica nas cores primárias
        for nome, valor in self.cores_primarias.items():
            if valor == rgb:
                return nome
        # Verifica nas cores secundárias
        for nome, valor in self.cores_secundarias.items():
            if valor == rgb:
                return nome
        # Caso não encontre
        return "desconhecida"


    def desenhar_primeira_fase(self):
        if self.nivel_fase_1 == "primaria":
            self.tela.blit(self.layout_nivel_1, (0, 0))
        else:
            self.tela.blit(self.layout_nivel_2, (0, 0))

        for botao in self.botoes_fase_1.values():
            botao.desenhar(self.tela)

        self.desenha_bolinhas()

    def desenha_bolinhas(self):

        # Desenho das bolinhas na tela
        for bolinha in self.bolinhas:
            bolinha.desenhar(self.tela)
        
        for bolinha in self.bolinhas:
            if self.erro and bolinha.cor in self.cores_erradas.values():
                bolinha.desenhar_x(self.tela)

    def desenhar_segunda_fase(self):
        if self.nivel_fase_2 == "primaria":
            self.tela.blit(self.layout_nivel_12, (0, 0))
        elif self.nivel_fase_2 == "secundaria":
            self.tela.blit(self.layout_nivel_22, (0, 0)) #fazer layout nivel 2

        #desenhar botoes
        for botao in self.botoes_fase_2.values():
            botao.desenhar(self.tela)

        self.desenha_caixa()

    def desenha_caixa(self):
        for quadrado in self.quadrados_caixa.values():
            quadrado.desenhar(self.tela)

        #desenha os quadrados na tela
        self.desenhar_quadrados()

    def verifica_pontuacao_jogador(self, fase, nivel):

        if fase == 1 and nivel == 1:
            if self.jogador.tentativas_fase1_nivel_1 == 3:
                self.jogador.pontuacao_estudante = "INCRÍVEL"
            elif self.jogador.tentativas_fase1_nivel_1 == 4:
                self.jogador.pontuacao_estudante = "ÓTIMO"
            elif self.jogador.tentativas_fase1_nivel_1 == 5:
                self.jogador.pontuacao_estudante = "SHOW"
            else:
                self.jogador.pontuacao_estudante = "BOM"
        elif fase == 1 and nivel == 2:
            if self.jogador.tentativas_fase1_nivel_2 == 3:
                self.jogador.pontuacao_estudante = "INCRÍVEL"
            elif self.jogador.tentativas_fase1_nivel_2 == 4:
                self.jogador.pontuacao_estudante = "ÓTIMO"
            elif self.jogador.tentativas_fase1_nivel_2 == 5:
                self.jogador.pontuacao_estudante = "SHOW"
            else:
                self.jogador.pontuacao_estudante = "BOM"
        elif fase == 2 and nivel == 1:
            if self.jogador.tentativas_fase2_nivel_1 == 3:
                self.jogador.pontuacao_estudante = "INCRÍVEL"
            elif self.jogador.tentativas_fase2_nivel_1 == 4:
                self.jogador.pontuacao_estudante = "ÓTIMO"
            elif self.jogador.tentativas_fase2_nivel_1 == 5:
                self.jogador.pontuacao_estudante = "SHOW"
            else:
                self.jogador.pontuacao_estudante = "BOM"
        elif fase == 2 and nivel == 2:
            if self.jogador.tentativas_fase2_nivel_2 == 3:
                self.jogador.pontuacao_estudante = "INCRÍVEL"
            elif self.jogador.tentativas_fase2_nivel_2 == 4:
                self.jogador.pontuacao_estudante = "ÓTIMO"
            elif self.jogador.tentativas_fase2_nivel_2 == 5:
                self.jogador.pontuacao_estudante = "SHOW"
            else:
                self.jogador.pontuacao_estudante = "BOM"
        else:
            print("Erro: fase/nivel desconhecido")

    def nivel_video_fase_1(self):
        if self.nivel_fase_1 == "primaria":
            return "cor_primaria"
        elif self.nivel_fase_1 == "secundaria":
            return "cor_secundaria"
        else:
            print("erro ao identificar nivel da fase 1")
            return None
    
    def nivel_video_fase_2(self):
        if self.nivel_fase_2 == "primaria":
            return "cor_primaria"
        elif self.nivel_fase_2 == "secundaria":
            return "cor_secundaria"
        else:
            print("erro ao identificar nivel da fase 1")
            return None

    def primeira_fase(self):
        self.menu_atual = "primeira_fase"
        self.acao_som(self.tipo_acao_fase1)
        self.jogador.tentativas_fase1_nivel_1 = 0
        self.jogador.tentativas_fase1_nivel_2 = 0

        botao_menu = BotaoEspecial(
            x=SCREEN_WIDTH * 0.82,  # Exemplo de novo valor para 'x'
            y=SCREEN_HEIGHT * 0.844,  # Exemplo de novo valor para 'y'
            largura=SCREEN_HEIGHT * 0.26,
            altura=SCREEN_HEIGHT * 0.11,
            texto="MENU",
            cor_normal=(255, 220, 140),  # Cor normal (#FFA12B)
            cor_hover=(255, 220, 100),  # Cor hover (#F78900)
            cor_sombra=(204, 153, 100),  # Cor da sombra (#915100)
            cor_texto=(0, 0, 0),
            fonte=pygame.font.SysFont("Baskerville", 40), 
            acao=None,
        )
        botao_video = Botao(SCREEN_WIDTH * 0.75, SCREEN_HEIGHT * 0.005, SCREEN_WIDTH * 0.09, SCREEN_HEIGHT * 0.15, "video", (255, 255, 0), acao=lambda:self.rodar_video(self.nivel_video_fase_1()))

        print("Iniciando Fase 1")
        while self.running:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    # Verificar hover para todas as bolinhas
                    pos = pygame.mouse.get_pos()
                    for bolinha in self.bolinhas or self.cores_erradas:
                        bolinha.verificar_hover(pos)

                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    x, y = event.pos
                    print(f"Posição do clique: x = {x}, y = {y}")
                    self.verificar_clique(pos)
                    
                    if botao_menu.foi_clicado(pos):
                        print("Botão menu foi clicado")
                        self.menu_fases()  # Chama a ação associada ao botão

                    for bolinha in self.bolinhas:
                        bolinha.verificar_hover(pos)
                    
                    if botao_video.foi_clicado(pos):
                        botao_video.acao()
                    

                    escolhida = self.verificar_clique_bolinha(pos)
                    if escolhida and self.nivel_fase_1 == "primaria": #SE ACERTAR O PRIMEIRO NIVEL DA PRIMEIRA FASE
                        print("acertou a cor primaria")
                       
                        self.jogador.tentativas_fase1_nivel_1 += 1

                        if self.acertou3_primaria == 3:
                            self.nivel_fase_1 = "secundaria"
                            self.tipo_acao_fase1 = "cor_secundaria"
                            self.erro = False

                            self.tela.blit(self.layout_acertou_nivel_1, (0, 0))
                            botao_menu.desenhar(self.tela, ativo=botao_menu.rect.collidepoint(mouse_x, mouse_y))
                            self.acao_som("proximo_nivel") 
                            pygame.display.flip()


                            #delay
                            tempo_inicio = pygame.time.get_ticks()
                            self.delay(tempo_inicio, 4000)
                            self.verifica_pontuacao_jogador(1, 1)
                            self.fase = 1
                            self.relatorio_estudante(self.fase)

                            self.acao_som("cor_secundaria")
                            self.acertou3_primaria = 1
                            self.acertou3_secundaria = 1
                            self.desenhar_primeira_fase()
                            pygame.display.flip()
                            self.iniciar_bolinhas()
                        self.acertou3_primaria += 1

                    elif (escolhida and self.nivel_fase_1 == "secundaria"):
                        # chamar fase_cores_secundarias()
                        #print("AQUIIIIIIIIIIIIIIIIIi")
                        self.jogador.tentativas_fase1_nivel_2 += 1

                        if self.acertou3_secundaria == 3:
                            self.erro = False
                            self.verificar_dificuldade() 

                            self.tela.blit(self.layout_acertou_nivel_2, (0, 0))
                            botao_menu.desenhar(self.tela, ativo=botao_menu.rect.collidepoint(mouse_x, mouse_y))
                            pygame.display.flip()
                            #delay
                            self.acao_som("proxima_fase")
                            tempo_inicio = pygame.time.get_ticks()
                            self.delay(tempo_inicio, 4000)
                            self.verifica_pontuacao_jogador(1, 2)
                            self.fase = 1
                            self.relatorio_estudante(self.fase)
                            self.desenhar_primeira_fase()
                            pygame.display.flip()
                            self.iniciar_bolinhas()
                            self.fase_2 = "Desbloqueada"
                            self.jogador.fase_1 = True
                            self.botoes_menu_fases["fase_2"] = Botao(500, SCREEN_HEIGHT - 295, 275, 50, "Fase 2", (255, 150, 150), acao=self.segunda_fase)
                            self.salva_estatisticas()
                            self.menu_fases()
                        self.acertou3_secundaria += 1
                        #repetir a logica da fase primaria
                        print("acertou cor secundaria! parabens")

                    elif  escolhida == False and self.nivel_fase_1 == "primaria":
                        print("errou cor primaria! tente novamente")
                        self.jogador.tentativas_fase1_nivel_1 += 1  

                        self.acao_som("bolinha_errada")
                        print("ESTA AQUI")
                        

                        self.tela.blit(self.layout_errou, (0, 0))
                        self.desenha_bolinhas()
                        botao_menu.desenhar(self.tela, ativo=botao_menu.rect.collidepoint(mouse_x, mouse_y))
                        pygame.display.flip()
                        self.clock.tick(60)
                        tempo_inicio = pygame.time.get_ticks()
                        self.delay(tempo_inicio, 4000)

                        self.rodar_video("cor_primaria")

                        for bolinha in self.bolinhas:
                            nome_cor = self.obter_nome_cor(bolinha.cor)  # Obtem o nome da cor baseado no RGB
                            self.adicionar_dificuldade("cores_primarias", nome_cor)
                            print(f"\nFalta primaria: {nome_cor}")

                        print("Dificuldade até agora:", self.dificuldade_identificar)

                        #contabilizar erro e dificuldades em relacao as cores restantes na tela do jogador
                        

                    elif escolhida == False and self.nivel_fase_1 == "secundaria":
                        self.jogador.tentativas_fase1_nivel_2 += 1
                        self.acao_som("bolinha_errada")
                        print("ESTA AQUI")
                        

                        self.tela.blit(self.layout_errou, (0, 0))
                        self.desenha_bolinhas()
                        botao_menu.desenhar(self.tela, ativo=botao_menu.rect.collidepoint(mouse_x, mouse_y))
                        pygame.display.flip()
                        self.clock.tick(60)
                        tempo_inicio = pygame.time.get_ticks()
                        self.delay(tempo_inicio, 4000)
                        self.rodar_video("cor_secundaria")

                        print("errou cor secundaria! tente novamente")
                        for bolinha in self.bolinhas:
                            nome_cor = self.obter_nome_cor(bolinha.cor)  # Obtem o nome da cor baseado no RGB
                            self.adicionar_dificuldade("cores_secundarias", nome_cor)
                            print(f"\nFalta secundária: {nome_cor}")

                        print("Dificuldade até agora:", self.dificuldade_identificar)

            
            self.desenhar_primeira_fase()
            botao_menu.desenhar(self.tela, ativo=botao_menu.rect.collidepoint(mouse_x, mouse_y))
            botao_video.desenhar(self.tela)
            pygame.display.flip()
            self.clock.tick(60)


    def segunda_fase(self):

        self.menu_atual = "segunda_fase"
        self.acao_som(self.tipo_acao_fase2)
        self.acertos_nivel1 = 0
        self.acertos_nivel2 = 0
        self.quadrados_errados = {}
        self.quadrados_caixa.clear()  # Limpa quaisquer quadrados residuais
        self.iniciar_quadrados()  # Inicializa os quadrados da fase
        self.jogador.tentativas_fase2_nivel_1 = 0
        self.jogador.tentativas_fase2_nivel_2 = 0

        botao_menu = BotaoEspecial(
            x=SCREEN_WIDTH * 0.82,  # Exemplo de novo valor para 'x'
            y=SCREEN_HEIGHT * 0.844,  # Exemplo de novo valor para 'y'
            largura=SCREEN_HEIGHT * 0.26,
            altura=SCREEN_HEIGHT * 0.11,
            texto="MENU",
            cor_normal=(255, 220, 140),  # Cor normal (#FFA12B)
            cor_hover=(255, 220, 100),  # Cor hover (#F78900)
            cor_sombra=(204, 153, 100),  # Cor da sombra (#915100)
            cor_texto=(0, 0, 0),
            fonte=pygame.font.SysFont("Baskerville", 40), 
            acao=None,
        )
        botao_video = Botao(SCREEN_WIDTH * 0.75, SCREEN_HEIGHT * 0.005, SCREEN_WIDTH * 0.09, SCREEN_HEIGHT * 0.15, "video", (255, 255, 0), acao=lambda:self.rodar_video(self.nivel_video_fase_2()))
        print("Iniciando Fase 2")

        # Loop principal
        running = True
        while running:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEMOTION:
                    pos = pygame.mouse.get_pos()
                    # Verifica o hover com base no nível atual
                    if self.nivel_fase_2 == 'primaria':
                        for quadrado in self.quadrados_primarios.values():
                            quadrado.verificar_hover(pos)
                    else:
                        for quadrado in self.quadrados_secundarios.values():
                            quadrado.verificar_hover(pos)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.verificar_clique(pos)
                    print(f"Posição do clique: {pos}")

                    if botao_menu.foi_clicado(pos):
                        print("Botão menu foi clicado")
                        self.menu_fases()  # Chama a ação associada ao botão
                    if botao_video.foi_clicado(pos):
                        botao_video.acao()

                    if self.nivel_fase_2 == 'primaria':
                        quadrados_para_remover = []
                        for nome, quadrado in self.quadrados_primarios.items():
                            if quadrado.foi_clicada(pos):
                                print(f"Quadrado {nome} clicado!")
                                if nome in ["osso_preto", "urso_marrom"]:
                                    self.quadrados_errados[nome] = True 
                                    print("ERROU!")
                                    self.jogador.tentativas_fase2_nivel_1 += 1

                                    self.acao_som("objeto_primario_erro")
                                    self.tela.blit(self.layout_objeto_errado_primario, (0, 0))
                                    botao_menu.desenhar(self.tela, ativo=botao_menu.rect.collidepoint(mouse_x, mouse_y))
                                    #desenha quadrados
                                    self.desenha_caixa()
                                    self.desenhar_quadrados()
                                    pygame.display.flip()
                                    self.clock.tick(60)
                                    tempo_inicio = pygame.time.get_ticks()
                                    self.delay(tempo_inicio, 6000)

                                    self.rodar_video("cor_primaria")

                                    for restante in self.quadrados_primarios.keys():
                                        print(f"falta {restante}")
                                        self.adicionar_dificuldade_2("cores_primarias", restante)

                                else:  # Acerto
                                    quadrados_para_remover.append(nome)
                                    self.acertos_nivel1 += 1
                                    self.jogador.tentativas_fase2_nivel_1 += 1
                                    
                        
                        for nome in quadrados_para_remover:
                            self.remover_quadrado(nome)
                            self.inicia_caixa(nome)

                    elif self.nivel_fase_2 == 'secundaria':
                        quadrados_para_remover = []
                        for nome, quadrado in self.quadrados_secundarios.items():
                            if quadrado.foi_clicada(pos):
                                print(f"Quadrado {nome} clicado!")
                                if nome in ["flor_rosa", "osso_azul"]:
                                    print("ERROU!")
                                    self.quadrados_errados[nome] = True 
                                    self.jogador.tentativas_fase2_nivel_2 += 1

                                    self.acao_som("objeto_errado")
                                    self.tela.blit(self.layout_objeto_errado_secundaria, (0, 0))
                                    botao_menu.desenhar(self.tela, ativo=botao_menu.rect.collidepoint(mouse_x, mouse_y))
                                    #desenha quadrados
                                    self.desenha_caixa()
                                    self.desenhar_quadrados()
                                    pygame.display.flip()
                                    self.clock.tick(60)
                                    tempo_inicio = pygame.time.get_ticks()
                                    self.delay(tempo_inicio, 6000)

                                    self.rodar_video("cor_secundaria")

                                    for restante in self.quadrados_secundarios.keys():
                                        print(f"falta {restante}")
                                        self.adicionar_dificuldade_2("cores_secundarias", restante)
                                else:  # Acerto
                                    quadrados_para_remover.append(nome)
                                    self.acertos_nivel2 += 1
                                    self.jogador.tentativas_fase2_nivel_2 += 1
                        
                        for nome in quadrados_para_remover:
                            self.remover_quadrado(nome)
                            self.inicia_caixa(nome)

            # Desenha o layout da fase com base no nível atual
            self.desenhar_segunda_fase()
            botao_menu.desenhar(self.tela, ativo=botao_menu.rect.collidepoint(mouse_x, mouse_y))
            botao_video.desenhar(self.tela)
            pygame.display.flip()
            self.clock.tick(60)

            # Verifica condições de vitória no nível primário
            if self.nivel_fase_2 == 'primaria' and self.acertos_nivel1 == 3:
                print("Você completou o nível primário! Avançando para cores secundárias.")
                self.quadrados_errados = {}
                print(f"{self.dificuldade_identificar_2.values()}")
                tempo_inicio = pygame.time.get_ticks()

                self.tela.blit(self.layout_primaria_organizada, (0, 0))
                self.desenha_caixa()
                self.desenhar_quadrados()
                botao_menu.desenhar(self.tela, ativo=botao_menu.rect.collidepoint(mouse_x, mouse_y))
                pygame.display.flip()
                self.clock.tick(60)

                self.acao_som("obrigado_caixa_primaria")
                self.delay(tempo_inicio, 5500)

                self.verifica_pontuacao_jogador(2, 1)
                self.fase = 2
                self.relatorio_estudante(self.fase)

                self.tipo_acao_fase2 = "caixa_secundaria"
                self.nivel_fase_2 = "secundaria"
                self.acao_som("caixa_secundaria")
                self.acertos_nivel1 = 0  # Reseta o contador para evitar interferências
                self.quadrados_caixa.clear()
                self.iniciar_quadrados()  # Inicializa os quadrados do nível secundário

            # Verifica condições de vitória no nível secundário
            elif self.nivel_fase_2 == 'secundaria' and self.acertos_nivel2 == 3:
                print("Você completou a Fase 2! Parabéns!")
                print(f"{self.dificuldade_identificar_2.values()}")
                self.jogador.fase_2 = True
                self.verificar_dificuldade()
                self.salva_estatisticas()

                self.tela.blit(self.layout_caixa_organizada, (0, 0))
                self.desenha_caixa()
                self.desenhar_quadrados()
                botao_menu.desenhar(self.tela, ativo=botao_menu.rect.collidepoint(mouse_x, mouse_y))
                pygame.display.flip()
                self.clock.tick(60)
                self.acao_som("caixas_organizadas")

                tempo_inicio = pygame.time.get_ticks()
                self.delay(tempo_inicio, 4500)

                self.verifica_pontuacao_jogador(2, 2)
                self.fase = 2
                self.relatorio_estudante(self.fase)

                self.menu_fases()  # Retorna ao menu de fases
                running = False

    def objeto_cor(self, objeto): #recebe o objeto e retorna sua cor
        if objeto == "osso_amarelo":
            return "amarelo"
        elif objeto == "bola_azul":
            return "azul"
        elif objeto == "osso_vermelho":
            return "vermelho"
        elif objeto == "bola_verde":
            return "verde"
        elif objeto == "laco_laranja":
            return "laranja"
        elif objeto == "estrela_roxa":
            return "roxo"
        else:
            return "desconhecida"

    def adicionar_dificuldade_2(self, categoria, objetos):
        """Adiciona a cor à lista de dificuldades no dicionário, evitando duplicatas."""
 
        if categoria in self.dificuldade_identificar_2:
            cor = self.objeto_cor(objetos)
            if cor not in self.dificuldade_identificar_2[categoria]:
                if cor == "desconhecida":
                    pass
                else:
                    self.dificuldade_identificar_2[categoria].append(cor)    

    def verificar_clique(self, pos):
        

        if self.menu_atual == "menu_principal":
            botoes = self.botoes
        elif self.menu_atual == "menu_config":
            botoes = self.botoes_config
        elif self.menu_atual == "menu_fases":
            botoes = self.botoes_menu_fases
        elif self.menu_atual == "primeira_fase":
            botoes = self.botoes_fase_1
        elif self.menu_atual == "segunda_fase":
            botoes = self.botoes_fase_2
        else:
            return

        for botao in botoes.values():
            if botao.foi_clicado(pos):
                if botao.acao:
                    botao.acao()
                return


    def menu_nome(self):
        """
        Exibe o menu inicial. O botão 'Voltar ao jogo →' será mostrado apenas se o nome do jogador já tiver sido inserido.
        O botão 'Menu' estará sempre visível.
        """
        self.menu_atual = "menu_principal"
        self.tipo_acao_menu = "digite_nome"
        self.rodar_video("tutorial")
        # Verifica se há um jogador registrado no log
        ultimo_jogador = Jogador.verificar_ultimo_jogador("resultados.txt")
        print(ultimo_jogador)

        if ultimo_jogador:
            # Se um jogador foi encontrado, carrega-o no jogo
            self.jogador = ultimo_jogador
            self.dificuldade = self.jogador.pontuacao_professor
            self.jogador.data = self.data
            print(f"Jogador carregado: {self.jogador.nome}")
            self.salva_estatisticas()
            self.verifica_fases_jogador()
            #print(f"DIFICULDADES: {self.jogador.pontuacao_professor.values()}")
        else:
            # Caso contrário, permite a criação de um novo jogador
            print("Nenhum jogador encontrado, criando novo jogador.")
            self.jogador = Jogador(nome="Novo Jogador", pontuacao_professor= None, pontuacao_estudante=0, data=self.data)

        print(f"fase 1 {self.jogador.fase_1}")
        print(f"fase 2 {self.jogador.fase_2}")
        # Criar o botão 'Voltar ao jogo →' apenas se o nome do jogador foi inserido
        botao_voltar = None
        if self.jogador:
            botao_voltar = BotaoEspecial(
                x=SCREEN_HEIGHT * 0.8,
                y=SCREEN_HEIGHT * 0.8,
                largura=SCREEN_WIDTH * 0.3,
                altura=SCREEN_HEIGHT * 0.07,
                texto=f"{((self.jogador.nome))}",
                cor_normal=(255, 220, 140),  # Cor normal (#FFA12B)
                cor_hover=(255, 220, 100),  # Cor hover (#F78900)
                cor_sombra=(204, 153, 100),  # Cor da sombra (#915100)
                cor_texto=(0, 0, 0), 
                fonte=pygame.font.SysFont("Baskerville", 40),
                acao=self.menu_fases,  # Define a ação ao clicar no botão
            )

        botao_menu = BotaoEspecial(
            x=SCREEN_WIDTH * 0.409,  # Exemplo de novo valor para 'x'
            y=SCREEN_HEIGHT * 0.33,  # Exemplo de novo valor para 'y'
            largura=SCREEN_HEIGHT * 0.26,
            altura=SCREEN_HEIGHT * 0.11,
            texto="MENU",
            cor_normal=(255, 220, 140),  # Cor normal (#FFA12B)
            cor_hover=(255, 220, 100),  # Cor hover (#F78900)
            cor_sombra=(204, 153, 100),  # Cor da sombra (#915100)
            cor_texto=(0, 0, 0),
            fonte=pygame.font.SysFont("Baskerville", 40), 
            acao=None,
        )

        while self.running:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            is_hovered = botao_voltar and botao_voltar.rect.collidepoint(mouse_x, mouse_y)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    tempo_atual = pygame.time.get_ticks()
                    if tempo_atual - self.ultimo_clique < 200:  # Delay de 200ms
                        continue  # Ignora se o clique for muito próximo do último
                    self.ultimo_clique = tempo_atual
                    
                    pos = pygame.mouse.get_pos()
                    self.verificar_clique(pos)
                    # Verifica clique no botão 'Voltar ao jogo →'
                    if botao_voltar and botao_voltar.foi_clicado(pos):
                        print(f"Botão 'Continuar Como {self.jogador}' clicado!")
                        self.menu_fases()  # Chama a função que exibe o menu de fases
                        return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                    self.alternar_tela()
                    

            # Desenha o menu
            self.desenhar_menu()

            # Desenha o botão 'Voltar ao jogo →' apenas se o nome do jogador foi inserido
            if botao_voltar:
                botao_voltar.desenhar(self.tela, ativo=is_hovered)

            botao_menu.desenhar(self.tela)
            pygame.display.flip()
            self.clock.tick(60)

    
    def acao_configuracao(self):
        self.tipo_acao_menu = "configuracao"
        linha_x1, linha_x2 = 850, 1150  # Início e fim da linha
        linha_y = SCREEN_HEIGHT // 2.4  # Posição vertical da linha
        raio = 10  # Raio da bolinha
        bola_x = (linha_x1 + linha_x2) // 2  # Começa no meio da linha
        if self.fase_1 == "Desbloqueada":
            self.fase = 1
        if self.fase_2 == "Desbloqueada":
            self.fase = 2

        print("Ação: Configuração")
        if self.menu_atual == "menu_principal":
            acao_especial = lambda:self.menu_nome()
        elif self.menu_atual == "menu_fases":
            acao_especial = lambda:self.menu_fases()
        elif self.menu_atual == "primeira_fase":
            acao_especial = lambda:self.primeira_fase()
        elif self.menu_atual == "segunda_fase":
            acao_especial = lambda:self.segunda_fase()

        # Criar o botão com novas coordenadas

        botao_voltar = BotaoVoltar(SCREEN_WIDTH * 0.05, SCREEN_HEIGHT * 0.9, 50, acao_especial)

        self.menu_atual = "menu_config"
        while self.running:
            
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    
                    self.verificar_clique(pos)                              
                    if botao_voltar.foi_clicado(pos):
                        acao_especial
                    # Verifica se o clique foi no controle de volume
                    if linha_x1 <= pos[0] <= linha_x2 and linha_y - raio <= pos[1] <= linha_y + raio:
                        self.volume = (pos[0] - linha_x1) / (linha_x2 - linha_x1)
                        pygame.mixer.music.set_volume(self.volume)

                elif event.type == pygame.MOUSEMOTION and event.buttons[0]:  # Arrastando
                    # Move a bolinha dentro dos limites da barra
                    if linha_x1 <= mouse_x <= linha_x2:
                        self.volume = (mouse_x - linha_x1) / (linha_x2 - linha_x1)
                        pygame.mixer.music.set_volume(self.volume)

            # Desenha o layout da configuração
            self.desenhar_configuracao()

            # Desenha o botão especial (com efeito hover)

            # Desenha a faixa de fundo clara (a faixa que vai preencher toda a linha)
            pygame.draw.rect(self.tela, (100, 100, 100), (linha_x1, linha_y - 5, linha_x2 - linha_x1, 10))  # Faixa clara

            # Desenha a linha preta (barra de volume, vai representar o nível do volume)
            pygame.draw.line(self.tela, (0, 0, 0), (linha_x1, linha_y), (linha_x1 + (linha_x2 - linha_x1) * self.volume, linha_y), 10)  # Preenchimento de volume

            # Desenha a bolinha do volume
            pygame.draw.circle(self.tela, (255, 0, 0), (linha_x1 + (linha_x2 - linha_x1) * self.volume, linha_y), raio)
            botao_voltar.desenhar(self.tela)
            # Atualiza a tela
            pygame.display.flip()
            self.clock.tick(60)

    def acao_nome_jogador(self):
        print("Ação: Nome")

        # Definições de cores e estado
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        GRAY = (200, 200, 200)

        input_active = True  # A entrada começa ativa
        input_text = ""

        font = pygame.font.Font(None, 50)  # Fonte para o texto

        # Definindo as dimensões e a posição do retângulo do campo de texto
        campo_texto_largura = min(750, SCREEN_WIDTH * 0.8)  # No máximo 750px, mas ajustável
        campo_texto_altura = min(120, SCREEN_HEIGHT * 0.1)  # No máximo 120px, mas ajustável

        campo_texto_x = (SCREEN_WIDTH - campo_texto_largura) // 2
        campo_texto_y = (SCREEN_HEIGHT - campo_texto_altura) // 2 + 89

        botao_menu = BotaoEspecial(
            x=SCREEN_WIDTH * 0.409,  # Exemplo de novo valor para 'x'
            y=SCREEN_HEIGHT * 0.33,  # Exemplo de novo valor para 'y'
            largura=SCREEN_HEIGHT * 0.26,
            altura=SCREEN_HEIGHT * 0.11,
            texto="MENU",
            cor_normal=(255, 220, 140),  # Cor normal (#FFA12B)
            cor_hover=(255, 220, 100),  # Cor hover (#F78900)
            cor_sombra=(204, 153, 100),  # Cor da sombra (#915100)
            cor_texto=(0, 0, 0),
            fonte=pygame.font.SysFont("Baskerville", 40), 
            acao=None,
        )
        while self.running:
            self.desenhar_menu()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Clique do mouse para ativar/desativar o campo de texto
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Verifique se o clique está dentro da área do campo de texto
                    if campo_texto_x < event.pos[0] < campo_texto_x + campo_texto_largura and campo_texto_y < event.pos[1] < campo_texto_y + campo_texto_altura:
                        input_active = True
                    else:
                        input_active = False
                        self.verificar_clique(event.pos)
                        return

                # Entrada de texto
                if event.type == pygame.KEYDOWN and input_active:
                    if event.key == pygame.K_BACKSPACE:
                        # Apaga o último caractere se houver texto
                        input_text = input_text[:-1]
                    elif event.key == pygame.K_RETURN:  # Enter
                        # Salva as estatísticas do jogador atual (se existir)
                        if self.jogador:
                            self.salva_estatisticas()
                        
                        # Cria um novo jogador com todos os atributos resetados
                        self.jogador = Jogador(
                            nome=input_text,
                            data=self.data,
                            pontuacao_professor={
                                "GRANDE DIFICULDADE": [{"primarias": [], "secundarias": []}],
                                "LEVE DIFICULDADE": [{"primarias": [], "secundarias": []}]
                            },
                            pontuacao_estudante=0
                        )
                        # Reseta os demais atributos para valores padrão
                        self.jogador.fase_1 = False
                        self.jogador.fase_2 = False
                        self.jogador.tentativas_fase1_nivel_1 = 0
                        self.jogador.tentativas_fase1_nivel_2 = 0
                        self.jogador.tentativas_fase2_nivel_1 = 0
                        self.jogador.tentativas_fase2_nivel_2 = 0
                        self.fase_1 = "Desbloqueada"
                        self.fase_2 = "Bloqueada"
                        print(f"Nome do jogador: {self.jogador.nome}")

                        # Salva as estatísticas iniciais do novo jogador
                        self.verifica_fases_jogador()
                        self.salva_estatisticas()

                        # Chama o menu de fases
                        self.menu_fases()
                        return
                    else:
                        input_text += event.unicode  # Adiciona o caractere digitado

            # Renderize o campo de texto
            #pygame.draw.rect(self.tela, BLACK if input_active else GRAY, (campo_texto_x, campo_texto_y, campo_texto_largura, campo_texto_altura), 2)

            text_surface = font.render(input_text, True, BLACK)
            text_rect = text_surface.get_rect()
            text_rect.midleft = (campo_texto_x + 10, campo_texto_y + campo_texto_altura // 2)
            self.tela.blit(text_surface, text_rect)  # Ajuste a posição do texto dentro do campo
            botao_menu.desenhar(self.tela)
            # Atualize a tela
            pygame.display.flip()
            self.clock.tick(60)

    def verifica_fases_jogador(self): #verifica se ha jogador e se ja desbloqueou as fases
        if self.jogador:
            if self.jogador.fase_1:
                self.fase_1 = "Desbloqueada"
            if self.jogador.fase_2:
                self.fase_2 = "Desbloqueada"
        

    def menu_fases(self):
            print("Acao_menu_fases")
            #print(f"dificuldades:{self.dificuldade.values()}")

            self.jogador.pontuacao_professor = self.dificuldade
            #reseta progressao das fases(nivel) para o jogador pode jogar novamente, caso queira!
            #self.salva_estatisticas()
            self.verifica_fases_jogador()
            self.nivel_fase_1 = "primaria" 
            self.acertou3_primaria = 1
            self.acertou3_secundaria = 1
            self.bolinhas = []
            self.iniciar_bolinhas()
            self.erro = False
            #reseta primeira fase nivel 1
            self.tipo_acao_fase1 = "cor_primaria"

            #segunda fase
            self.tipo_acao_fase2 = "caixa_primaria"
            self.nivel_fase_2 = "primaria"  # Garante que a fase inicie no nível primário
            self.acertos_nivel1 = 0
            self.acertos_nivel2 = 0

            self.tipo_acao_menu = "fase1"
            if self.fase_2 == "Desbloqueada":
                self.tipo_acao_menu = "fase1e2"

            botao_menu = BotaoEspecial(
                x=SCREEN_WIDTH * 0.409,  # Exemplo de novo valor para 'x'
                y=SCREEN_HEIGHT * 0.33,  # Exemplo de novo valor para 'y'
                largura=SCREEN_HEIGHT * 0.26,
                altura=SCREEN_HEIGHT * 0.11,
                texto="MENU",
                cor_normal=(255, 220, 140),  # Cor normal (#FFA12B)
                cor_hover=(255, 220, 100),  # Cor hover (#F78900)
                cor_sombra=(204, 153, 100),  # Cor da sombra (#915100)
                cor_texto=(0, 0, 0),
                fonte=pygame.font.SysFont("Baskerville", 40), 
                acao=lambda:self.menu_nome(),
            )
            self.acao_ajuda_menu_fases()
            self.menu_atual = "menu_fases"
            while self.running:
                
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        self.verificar_clique(pos)  # Verifica os cliques nos botões principais

                        if botao_menu.foi_clicado(pos):
                            botao_menu.acao()
                        
                        # Verifique o clique no botão especial menu
                        
                        
                # Desenha o layout do menu de fases
                self.desenhar_menu_fases()

                # Desenha o botão especial (com efeito hover)
                
                # Atualiza a tela
                botao_menu.desenhar(self.tela, ativo=botao_menu.rect.collidepoint(mouse_x, mouse_y))
                pygame.display.flip()
                self.clock.tick(60)


    def acao_ajuda_jogo(self):
        self.rodar_video("tutorial")

    def acao_ajuda_menu_fases(self):
        if self.fase_2 == "Bloqueada":
            self.rodar_video("como_jogar_1")
        else:
            self.rodar_video("como_jogar_1")
            self.rodar_video("como_jogar_2")

    def acao_ajuda_fase1(self):
        self.rodar_video("como_jogar_1")

    def acao_ajuda_fase2(self):
        self.rodar_video("como_jogar_2")

    def ler_log(self, caminho_arquivo):
        try:
            with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
                conteudo = arquivo.read()
            return conteudo.split("--------------------------------------------------")
        except FileNotFoundError:
            print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
            return []

    def acao_professor(self):
        subprocess.run(["python", "relatorio.py"])  # Executa e espera `relatorio.py` terminar
        print("De volta ao game_logic.py!")

    def acao_som(self, tipo_audio):
        print("Ação: Som")

        # Mapeamento de tipos de áudio para os sons correspondentes
        mapa_audios = {
            "cor_primaria": "cor_primaria",
            "cor_secundaria": "cor_secundaria",
            "proximo_nivel": "proximo_nivel",
            "proxima_fase": "proxima_fase",
            "caixas_organizadas": "caixas_organizadas",
            "caixa_primaria": "caixa_primaria",
            "caixa_secundaria": "caixa_secundaria",
            "obrigado_caixa_primaria": "obrigado_caixa_primaria",
            "bolinha_errada": "bolinha_errada",
            "aprender_primarias": "aprender_primarias",
            "aprender_secundarias": "aprender_secundarias",
            "objeto_errado": "objeto_errado",
            "objeto_primario_erro": "objeto_primario_erro",
            "digite_nome": "digite_nome",
            "configuracao": "configuracao",
            "fase1": "fase1",
            "fase1e2": "fase1e2",
        }

        # Obtém o som correspondente ao tipo de áudio fornecido
        audio = mapa_audios.get(tipo_audio)

        if audio:
            self.audio.reproduzir_audio(audio, self.volume)
        else:
            print(f"Tipo de áudio '{tipo_audio}' não encontrado.")


    def relatorio_estudante(self, fase):
        cor_texto = (0, 0, 0) #preto
        fonte3 = pygame.font.Font(None, 70)
        

        #self.jogador.pontuacao_estudante
        texto_1 = fonte3.render(f"{fase}", True, cor_texto)
        posicao_texto = texto_1.get_rect(center=(SCREEN_WIDTH // 1.53, SCREEN_HEIGHT // 1.48))
        texto_2 = fonte3.render(f"{self.jogador.pontuacao_estudante}", True, cor_texto)
        posicao_texto_2 = texto_2.get_rect(center=(SCREEN_WIDTH // 3.1, SCREEN_HEIGHT // 1.48))
        texto_3 = fonte3.render(f"{self.jogador.nome}", True, cor_texto)
        posicao_texto_3 = texto_3.get_rect(center=(SCREEN_WIDTH // 2.1, SCREEN_HEIGHT // 3))
    

        self.tela.blit(self.layout_relatorio, (0, 0))
        self.tela.blit(texto_1, posicao_texto)
        self.tela.blit(texto_2, posicao_texto_2)
        self.tela.blit(texto_3, posicao_texto_3)
        pygame.display.flip()
        tempo_inicio = pygame.time.get_ticks()
        self.delay(tempo_inicio, 4000)



    def acao_sair(self): #APLICAR SALVAMENTO DE JOGO!!!!!!!!!!!
        print("Ação: Sair")
        self.salva_estatisticas()
        pygame.quit()
        sys.exit()

# Inicializando o jogo
if __name__ == "__main__":
    jogo = Jogo()
    jogo.menu_nome()
