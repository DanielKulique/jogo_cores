import pygame, random, sys, time, os
from game_objects import Botao, BotaoEspecial, Bolinha, Jogador, Quadrado
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from datetime import datetime
from relatorio import Relatorio


class Jogo:
    def __init__(self):
        pygame.init()
        #tela
        self.tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.modo_tela_cheia = True  # Estado inicial
        self.menu_atual = None

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
            "turquesa": (64, 224, 208),
            "magenta": (255, 0, 255),
            "rosa": (255, 192, 203),
            "marrom": (139, 69, 19),
            "bege": (200, 200, 160),
            "cinza": (128, 128, 128),
            "prata": (128, 128, 128),
            "ciano_claro": (100, 180, 180),
            "verde_agua": (32, 178, 170),
            "salmao": (250, 128, 114),
            "vinho": (128, 0, 32),
            "lilas": (200, 162, 200),
            "oliva": (107, 142, 35),
            "ambar": (255, 191, 0),
            "ferrugem": (183, 65, 14),
            "coral": (255, 127, 80),
        }
        
        self.bolinhas = []
        self.iniciar_bolinhas()

        self.jogador = Jogador(
            nome = "",
            pontuacao_professor = 0,
            pontuacao_estudante = "",
            data=datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
            )

        self.fase_1 = "Desbloqueada"
        self.fase_2 = "Bloqueada"
            
        # Instanciando os botões
        self.botoes = {
            "professor": Botao(50, SCREEN_HEIGHT - 185, 260, 140, "Professor", (255, 0, 0), acao=self.acao_professor),
            "config": Botao(18, 18, 75, 75, "Configuração", (0, 255, 0), acao=self.acao_configuracao),
            "nome": Botao((SCREEN_WIDTH - 750) // 2, (SCREEN_HEIGHT - 120) // 2 + 65, 750, 120, "Nome", (0, 0, 255), acao=self.acao_nome_jogador),
            "ajuda": Botao(SCREEN_WIDTH - 80, 20, 60, 80, "Ajuda", (255, 255, 0), acao=self.acao_ajuda_jogo),
            "som": Botao(SCREEN_WIDTH - 180, 20, 95, 80, "Som", (255, 165, 0), acao=self.acao_som),
        }
        self.botoes_config = {
            "ajuda": Botao(SCREEN_WIDTH - 80, 20, 60, 80, "Ajuda", (255, 255, 0), acao=self.acao_ajuda_jogo),
            "som": Botao(SCREEN_WIDTH - 180, 20, 95, 80, "Som", (255, 165, 0), acao=self.acao_som),
            #"menu": Botao((SCREEN_WIDTH - 750) // 2 + 260, (SCREEN_HEIGHT - 120) // 2 - 70, 210, 95, "Menu", (100, 255, 100), acao=self.menu_nome),
            #"config": Botao(18, 18, 75, 75, "Configuração", (0, 255, 0), acao=self.menu_nome),
            "sair": Botao(SCREEN_WIDTH - 137, SCREEN_HEIGHT - 120, 120, 120, "Sair", (255, 255, 0), acao=self.acao_sair)
        }
        self.botoes_menu_fases = {
            "fase_1": Botao(500, SCREEN_HEIGHT - 371, 275, 50, "Fase 1", (150, 150, 255), acao=self.primeira_fase), 
            #"menu": Botao((SCREEN_WIDTH - 750) // 2 + 260, (SCREEN_HEIGHT - 120) // 2 - 70, 210, 95, "Menu", (100, 255, 100), acao=self.menu_nome),
            "config": Botao(18, 18, 75, 75, "Configuração", (0, 255, 0), acao=self.acao_configuracao),
            "ajuda": Botao(SCREEN_WIDTH - 80, 20, 60, 80, "Ajuda", (255, 255, 0), acao=self.acao_ajuda_fase1),
            #"som": Botao(SCREEN_WIDTH - 180, 20, 95, 80, "Som", (255, 165, 0), acao=self.acao_som),
        }
        self.botoes_fase_1 = {
            #"menu": Botao((SCREEN_WIDTH - 750) // 2 + 260, (SCREEN_HEIGHT - 120) // 2 - 70, 210, 95, "Menu", (100, 255, 100), acao=self.menu_nome),
            "config": Botao(18, 18, 75, 75, "Configuração", (0, 255, 0), acao=self.acao_configuracao),
            "ajuda": Botao(SCREEN_WIDTH - 80, 20, 60, 80, "Ajuda", (255, 255, 0), acao=None),
            "som": Botao(SCREEN_WIDTH - 180, 20, 95, 80, "Som", (255, 165, 0), acao=None),
        }
        self.botoes_fase_2 = {
            #"menu": Botao((SCREEN_WIDTH - 750) // 2 + 260, (SCREEN_HEIGHT - 120) // 2 - 70, 210, 95, "Menu", (100, 255, 100), acao=self.menu_nome),
            "config": Botao(18, 18, 75, 75, "Configuração", (0, 255, 0), acao=self.acao_configuracao),
            "ajuda": Botao(SCREEN_WIDTH - 80, 20, 60, 80, "Ajuda", (255, 255, 0), acao=None),
            "som": Botao(SCREEN_WIDTH - 180, 20, 95, 80, "Som", (255, 165, 0), acao=None),
        }

        self.botao_especial_menu = {
            "menu_especial": BotaoEspecial(
                x=(SCREEN_WIDTH - 750)//2 +260,
                y=(SCREEN_HEIGHT - 120) // 2 - 70,
                largura=210,
                altura=90,
                texto=f"MENU",
                cor_normal=(255, 220, 140),
                cor_hover=(255, 220, 100),
                cor_sombra=(204, 153, 100),
                cor_texto=(0, 0, 0),
                fonte=pygame.font.SysFont("Baskerville", 40),
                acao=self.menu_nome,  # Define a ação ao clicar no botão
            )
        }
        '''self.quadrados_primarios = {
            "bola_azul": Quadrado(840, 150, "assets/objetos_primarios/bola_azul.png"),
            "osso_amarelo": Quadrado(1080, 170, "assets/objetos_primarios/osso_amarelo.png"),
            "osso_preto": Quadrado(840, 310, "assets/objetos_primarios/osso_preto.png"),
            "osso_vermelho": Quadrado(1080, 370, "assets/objetos_primarios/osso_vermelho.png"),
            "urso_marrom": Quadrado(890, 440, "assets/objetos_primarios/urso_marrom.png"),
        }'''
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

        self.layout_relatorio_professor = pygame.image.load("assets/layouts/12.png") 
        self.layout_relatorio_professor = pygame.transform.smoothscale(self.layout_relatorio_professor, (SCREEN_WIDTH, SCREEN_HEIGHT))


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
        else:
            for quadrado in self.quadrados_secundarios.values():
                quadrado.desenhar(self.tela)        
    

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
            (1080, 170),
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
            (900, 170),
            (1140, 190),
            (900, 330),
            (1140, 400),
            (950, 470),
        ]
        coordenadas_disponiveis_fase2 = [
            (870, 170),
            (1110, 190),
            (860, 330),
            (1100, 400),
            (910, 470),
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
                self.quadrados_caixa["bola_azul"] = Quadrado(510, 430, f"assets/objetos_primarios/bola_azul.png", 120)
                self.remover_quadrado("bola_azul")
            elif objeto == "osso_amarelo":
                self.quadrados_caixa["osso_amarelo"] = Quadrado(460, 450, f"assets/objetos_primarios/osso_amarelo.png", 120)
                self.remover_quadrado("osso_amarelo")
            elif objeto == "osso_vermelho":
                self.quadrados_caixa["osso_vermelho"] = Quadrado(583, 470, f"assets/objetos_primarios/osso_vermelho.png", 120)
                self.remover_quadrado("osso_vermelho") 
        else:
            if objeto == "bola_verde":
                self.quadrados_caixa["bola_verde"] = Quadrado(510, 430, f"assets/objetos_secundarios/bola_verde.png", 150)
                self.remover_quadrado("bola_verde")
            elif objeto == "laco_laranja":
                self.quadrados_caixa["laco_laranja"] = Quadrado(460, 450, f"assets/objetos_secundarios/laco_laranja.png", 150)
                self.remover_quadrado("laco_laranja")
            elif objeto == "estrela_roxa":
                self.quadrados_caixa["estrela_roxa"] = Quadrado(500, 470, f"assets/objetos_secundarios/estrela_roxa.png", 150)
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
            self.botoes_menu_fases["fase_2"] = Botao(500, SCREEN_HEIGHT - 295, 275, 50, "Fase 2", (255, 150, 150), acao=self.segunda_fase)
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
            (870, 236),  # Primeira bolinha
            (1162, 236),  # Segunda bolinha
            (870, 484),  # Terceira bolinha
            (1162, 484),  # Quarta bolinha
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
                if self.nivel_fase_1 == "primaria":
                    nivel = self.cores_primarias.values()  # nivel_1 cores primárias
                elif self.nivel_fase_1 == "secundaria":
                    nivel = self.cores_secundarias.values()  # nivel_2 cores secundárias
                
                if bolinha.cor in nivel:
                    print(f"AQUI--------> {bolinha.cor}")
                    self.bolinhas.remove(bolinha)
                    return True  # Bolinha correta foi clicada

        # Se nenhuma bolinha válida foi clicada
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

        # Desenho das bolinhas na tela
        for bolinha in self.bolinhas:
            bolinha.desenhar(self.tela)
        
        
        for bolinha in self.bolinhas:
            if self.erro and bolinha.cor in self.cores_erradas.values():
                bolinha.desenhar_x(self.tela)
                    

    def desenhar_segunda_fase(self):
        if self.nivel_fase_2 == "primaria":
            self.tela.blit(self.layout_nivel_12, (0, 0))
        else:
            self.tela.blit(self.layout_nivel_22, (0, 0)) #fazer layout nivel 2

        #desenhar botoes
        for botao in self.botoes_fase_2.values():
            botao.desenhar(self.tela)

        for quadrado in self.quadrados_caixa.values():
            quadrado.desenhar(self.tela)

        #desenha os quadrados na tela
        self.desenhar_quadrados()

    def primeira_fase(self):
        self.menu_atual = "primeira_fase"
        

        print("Iniciando Fase 1")
        while self.running:
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
                    #PAREI AQUI, ESPERO LEMBRAR AMANHA! ------------------------------------------------<>FUCK YOU,BOLINHAS
                    # Verificar o hover sobre as bolinhas
                    for bolinha in self.bolinhas:
                        bolinha.verificar_hover(pos)

                    escolhida = self.verificar_clique_bolinha(pos)
                    if escolhida and self.nivel_fase_1 == "primaria": #SE ACERTAR O PRIMEIRO NIVEL DA PRIMEIRA FASE
                        print("acertou a cor primaria")
                        #remover a bolinha do self bolinhas
                        #nao concluir o caralho da fase
                        #fazer um contador cont = 3, quando bater chama fase das cores secundarias
                        #chamar o contador de erros da class jogador
                        self.jogador.tentativas_fase1_nivel_1 += 1

                        if self.acertou3_primaria == 3:
                            self.nivel_fase_1 = "secundaria"
                            self.erro = False

                            self.tela.blit(self.layout_acertou_nivel_1, (0, 0))
                            pygame.display.flip()
                            #delay
                            
                            tempo_inicio = pygame.time.get_ticks()
                            self.delay(tempo_inicio, 3000)
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
                            pygame.display.flip()
                            #delay
                            tempo_inicio = pygame.time.get_ticks()
                            self.delay(tempo_inicio, 3000)

                            self.desenhar_primeira_fase()
                            pygame.display.flip()
                            self.iniciar_bolinhas()
                            self.fase_2 = "Desbloqueada"
                            self.jogador.fase_1 = True
                            self.botoes_menu_fases["fase_2"] = Botao(500, SCREEN_HEIGHT - 295, 275, 50, "Fase 2", (255, 150, 150), acao=self.segunda_fase)
                            self.menu_fases()
                        self.acertou3_secundaria += 1
                        #repetir a logica da fase primaria
                        print("acertou cor secundaria! parabens")

                    elif not escolhida and self.nivel_fase_1 == "primaria":
                        print("errou cor primaria! tente novamente")
                        self.jogador.tentativas_fase1_nivel_1 += 1  

                        self.erro = True    
                        
                        for bolinha in self.bolinhas:
                            nome_cor = self.obter_nome_cor(bolinha.cor)  # Obtem o nome da cor baseado no RGB
                            self.adicionar_dificuldade("cores_primarias", nome_cor)
                            print(f"\nFalta primaria: {nome_cor}")

                        print("Dificuldade até agora:", self.dificuldade_identificar)

                        #contabilizar erro e dificuldades em relacao as cores restantes na tela do jogador
                        

                    elif not escolhida and self.nivel_fase_1 == "secundaria":
                        self.jogador.tentativas_fase1_nivel_2 += 1
                        self.erro = True
                        print("errou cor secundaria! tente novamente")
                        for bolinha in self.bolinhas:
                            nome_cor = self.obter_nome_cor(bolinha.cor)  # Obtem o nome da cor baseado no RGB
                            self.adicionar_dificuldade("cores_secundarias", nome_cor)
                            print(f"\nFalta secundária: {nome_cor}")

                        print("Dificuldade até agora:", self.dificuldade_identificar)

            self.desenhar_primeira_fase()
            pygame.display.flip()
            self.clock.tick(60)


    def segunda_fase(self):
        self.menu_atual = "segunda_fase"
        self.nivel_fase_2 = "primaria"  # Garante que a fase inicie no nível primário
        self.acertos_nivel1 = 0
        self.acertos_nivel2 = 0
        self.quadrados_caixa.clear()  # Limpa quaisquer quadrados residuais
        self.iniciar_quadrados()  # Inicializa os quadrados da fase

        print("Iniciando Fase 2")

        # Loop principal
        running = True
        while running:
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
                    print(f"Posição do clique: {pos}")

                    if self.nivel_fase_2 == 'primaria':
                        quadrados_para_remover = []
                        for nome, quadrado in self.quadrados_primarios.items():
                            if quadrado.foi_clicada(pos):
                                print(f"Quadrado {nome} clicado!")
                                if nome in ["osso_preto", "urso_marrom"]:
                                    print("ERROU!")
                                    for restante in self.quadrados_primarios.keys():
                                        print(f"falta {restante}")
                                        self.adicionar_dificuldade_2("cores_primarias", restante)

                                else:  # Acerto
                                    quadrados_para_remover.append(nome)
                                    self.acertos_nivel1 += 1
                                    
                        
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
                                    for restante in self.quadrados_secundarios.keys():
                                        print(f"falta {restante}")
                                        self.adicionar_dificuldade_2("cores_secundarias", restante)
                                else:  # Acerto
                                    quadrados_para_remover.append(nome)
                                    self.acertos_nivel2 += 1
                        
                        for nome in quadrados_para_remover:
                            self.remover_quadrado(nome)
                            self.inicia_caixa(nome)

            # Desenha o layout da fase com base no nível atual
            self.desenhar_segunda_fase()
            pygame.display.flip()
            self.clock.tick(60)

            # Verifica condições de vitória no nível primário
            if self.nivel_fase_2 == 'primaria' and self.acertos_nivel1 == 3:
                print("Você completou o nível primário! Avançando para cores secundárias.")
                print(f"{self.dificuldade_identificar_2.values()}")
                tempo_inicio = pygame.time.get_ticks()
                self.delay(tempo_inicio, 3000)
                self.nivel_fase_2 = "secundaria"
                self.acertos_nivel1 = 0  # Reseta o contador para evitar interferências
                self.quadrados_caixa.clear()
                self.iniciar_quadrados()  # Inicializa os quadrados do nível secundário

            # Verifica condições de vitória no nível secundário
            elif self.nivel_fase_2 == 'secundaria' and self.acertos_nivel2 == 3:
                print("Você completou a Fase 2! Parabéns!")
                print(f"{self.dificuldade_identificar_2.values()}")
                self.verificar_dificuldade()
                tempo_inicio = pygame.time.get_ticks()
                self.delay(tempo_inicio, 3000)
                self.jogador.fase_2 = True
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
    
        # Verifica se há um jogador registrado no log
        ultimo_jogador = Jogador.verificar_ultimo_jogador("resultados.txt")
        
        if ultimo_jogador:
            # Se um jogador foi encontrado, carrega-o no jogo
            self.jogador = ultimo_jogador
            self.dificuldade = self.jogador.pontuacao_professor
            print(f"Jogador carregado: {self.jogador.nome}")
            self.verifica_fases_jogador()
            print(f"DIFICULDADES: {self.jogador.pontuacao_professor.values()}")
        else:
            # Caso contrário, permite a criação de um novo jogador
            print("Nenhum jogador encontrado, criando novo jogador.")
            self.jogador = Jogador(nome="Novo Jogador", pontuacao_professor=0, pontuacao_estudante=0, data=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        print(f"fase 1 {self.jogador.fase_1}")
        print(f"fase 2 {self.jogador.fase_2}")
        # Criar o botão 'Voltar ao jogo →' apenas se o nome do jogador foi inserido
        botao_voltar = None
        if self.jogador:
            botao_voltar = BotaoEspecial(
                x=600,
                y=SCREEN_HEIGHT - 200,
                largura=500,
                altura=60,
                texto=f"{((self.jogador.nome))}",
                cor_normal=(255, 220, 140),  # Cor normal (#FFA12B)
                cor_hover=(255, 220, 100),  # Cor hover (#F78900)
                cor_sombra=(204, 153, 100),  # Cor da sombra (#915100)
                cor_texto=(0, 0, 0), 
                fonte=pygame.font.SysFont("Baskerville", 40),
                acao=self.menu_fases,  # Define a ação ao clicar no botão
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


            pygame.display.flip()
            self.clock.tick(60)

    
    def acao_configuracao(self):
        
        print("Ação: Configuração")
        if self.menu_atual == "menu_principal":
            acao_especial = self.menu_nome
        elif self.menu_atual == "menu_fases":
            acao_especial = self.menu_fases
        elif self.menu_atual == "primeira_fase":
            acao_especial = self.primeira_fase
        elif self.menu_atual == "segunda_fase":
            acao_especial = self.segunda_fase

        # Criar o botão com novas coordenadas
        botao_menu = BotaoEspecial(
            x=(SCREEN_WIDTH - 750) // 2 + 245,  # Exemplo de novo valor para 'x'
            y=(SCREEN_HEIGHT - 120) // 2 - 160,  # Exemplo de novo valor para 'y'
            largura=210,
            altura=90,
            texto="MENU",
            cor_normal=(255, 220, 140),  # Cor normal (#FFA12B)
            cor_hover=(255, 220, 100),  # Cor hover (#F78900)
            cor_sombra=(204, 153, 100),  # Cor da sombra (#915100)
            cor_texto=(0, 0, 0),
            fonte=pygame.font.SysFont("Baskerville", 40), 
            acao=acao_especial,
        )

        self.menu_atual = "menu_config"
        while self.running:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    # Verifica os cliques nos botões de configuração
                    for botao in self.botoes_config.values():
                        self.verificar_clique(pos)

                    #Verifica o clique no botão especial menu
                    if botao_menu.foi_clicado(pos):
                        print("Botão menu foi clicado")
                        botao_menu.acao()  # Chama a ação associada ao botão

            # Desenha o layout da configuração
            self.desenhar_configuracao()

            # Desenha o botão especial (com efeito hover)
            botao_menu.desenhar(self.tela, ativo=botao_menu.rect.collidepoint(mouse_x, mouse_y))

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
        campo_texto_x = (SCREEN_WIDTH - 750) // 2
        campo_texto_y = (SCREEN_HEIGHT - 120) // 2 + 65
        campo_texto_largura = 750
        campo_texto_altura = 120

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
                        #cria novo jogador
                        self.salva_estatisticas()
                        self.jogador = Jogador(
                            nome = input_text,
                            data=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            pontuacao_professor = 0,
                            pontuacao_estudante = "",
                            )
                        print(f"Nome do jogador: {self.jogador.nome}")
                        # Aqui você pode chamar a função menu_fases 
                        self.salva_estatisticas()
                        self.menu_fases()
                        return
                    else:
                        input_text += event.unicode  # Adiciona o caractere digitado

            # Renderize o campo de texto
            pygame.draw.rect(self.tela, BLACK if input_active else GRAY, (campo_texto_x, campo_texto_y, campo_texto_largura, campo_texto_altura), 2)

            text_surface = font.render(input_text, True, BLACK)
            text_rect = text_surface.get_rect()
            text_rect.midleft = (campo_texto_x + 10, campo_texto_y + campo_texto_altura // 2)
            self.tela.blit(text_surface, text_rect)  # Ajuste a posição do texto dentro do campo

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
            print(f"dificuldades:{self.dificuldade.values()}")

            self.jogador.pontuacao_professor = self.dificuldade
            #reseta progressao das fases(nivel) para o jogador pode jogar novamente, caso queira!
            self.salva_estatisticas()
            self.verifica_fases_jogador()
            self.nivel_fase_1 = "primaria" 
            self.acertou3_primaria = 1
            self.acertou3_secundaria = 1
            self.bolinhas = []
            self.iniciar_bolinhas()
            #segunda fase
            self.acertos_nivel1 = 0
            self.acertos_nivel2 = 0

            botao_menu = self.botao_especial_menu["menu_especial"]
            
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
                        
                        # Verifique o clique no botão especial menu
                        if botao_menu.foi_clicado(pos):
                            print("Botao menu foi clicado")
                            botao_menu.acao()
                        
                # Desenha o layout do menu de fases
                self.desenhar_menu_fases()

                # Desenha o botão especial (com efeito hover)
                botao_menu.desenhar(self.tela, ativo=botao_menu.rect.collidepoint(mouse_x, mouse_y))
                
                # Atualiza a tela
                pygame.display.flip()
                self.clock.tick(60)


    def acao_ajuda_jogo(self):
        print("Ação: Ajuda")
        
        # Carregar as imagens para exibir na tela de ajuda
        imagens_ajuda = [
            pygame.image.load("assets/layouts/Ajuda_1.png"),
            pygame.image.load("assets/layouts/Ajuda_2.png"),
            pygame.image.load("assets/layouts/Ajuda_3.png"),
            pygame.image.load("assets/layouts/Ajuda_4.png"),
            pygame.image.load("assets/layouts/Ajuda_5.png"),
        ]
        
        # Redimensionar as imagens conforme necessário (se necessário)
        imagens_ajuda = [pygame.transform.smoothscale(img, (SCREEN_WIDTH, SCREEN_HEIGHT)) for img in imagens_ajuda]

        # Variáveis para controlar o tempo de exibição das imagens
        tempo_espera = 3000  # Tempo de espera entre as imagens (em milissegundos)
        indice_imagem = 0
        tempo_inicio = pygame.time.get_ticks()  # Marca o tempo inicial

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Verificar se o tempo de espera passou
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - tempo_inicio > tempo_espera:
                indice_imagem += 1
                if indice_imagem >= len(imagens_ajuda):
                    break  # Finaliza a função após exibir todas as imagens
                tempo_inicio = tempo_atual  # Atualiza o tempo de início para a próxima imagem

            # Desenhar a imagem atual na tela
            self.tela.fill((0, 0, 0))  # Limpa a tela com fundo preto
            self.tela.blit(imagens_ajuda[indice_imagem], (0, 0))  # Exibe a imagem

            pygame.display.flip()
            self.clock.tick(60)  # Limita o loop a 60 quadros por segundo


    def acao_ajuda_fase1(self):
        print("acao_ajuda_fase1")        
        # Carregar as imagens para exibir na tela de ajuda
        imagens_ajuda = [
            pygame.image.load("assets/layouts/videos_cores_primarias.png"),
            pygame.image.load("assets/layouts/tela_escolha_cor_primaria.png"),
            pygame.image.load("assets/layouts/tutorial_seleciona_cor_primaria.png"),
            pygame.image.load("assets/layouts/tutorial_erra_cor_primaria.png"),
            pygame.image.load("assets/layouts/tutorial_tenta_novamente.png"),
            pygame.image.load("assets/layouts/tutorial_tenta_novamente_2.png"),
            pygame.image.load("assets/layouts/mensagem_acertou.png"),
        ]
        
        # Redimensionar as imagens conforme necessário (se necessário)
        imagens_ajuda = [pygame.transform.smoothscale(img, (SCREEN_WIDTH, SCREEN_HEIGHT)) for img in imagens_ajuda]

        # Variáveis para controlar o tempo de exibição das imagens
        tempo_espera = 3000  # Tempo de espera entre as imagens (em milissegundos)
        indice_imagem = 0
        tempo_inicio = pygame.time.get_ticks()  # Marca o tempo inicial

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Verificar se o tempo de espera passou
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - tempo_inicio > tempo_espera:
                indice_imagem += 1
                if indice_imagem >= len(imagens_ajuda):
                    break  # Finaliza a função após exibir todas as imagens
                tempo_inicio = tempo_atual  # Atualiza o tempo de início para a próxima imagem

            # Desenhar a imagem atual na tela
            self.tela.fill((0, 0, 0))  # Limpa a tela com fundo preto
            self.tela.blit(imagens_ajuda[indice_imagem], (0, 0))  # Exibe a imagem

            pygame.display.flip()
            self.clock.tick(60)  # Limita o loop a 60 quadros por segun

    def acao_ajuda_fase2(self):
        print("acao_ajuda_faseq")
        # Adicione aqui a lógica para exibir a tela de ajuda

    def ler_log(self, caminho_arquivo):
        try:
            with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
                conteudo = arquivo.read()
            return conteudo.split("--------------------------------------------------")
        except FileNotFoundError:
            print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
            return []

    def acao_professor(self):

        rela = Relatorio()  # Instancia a classe Jogo
        rela.acao_professor()  # Executa a função acao_professor

    def acao_som(self):
        print("Ação: Som")
        # Adicione aqui a lógica para ajustar as configurações de som

    def acao_sair(self): #APLICAR SALVAMENTO DE JOGO!!!!!!!!!!!
        print("Ação: Sair")
        self.salva_estatisticas()
        pygame.quit()
        sys.exit()

# Inicializando o jogo
if __name__ == "__main__":
    jogo = Jogo()
    jogo.menu_nome()
