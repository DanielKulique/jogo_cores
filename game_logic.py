import pygame, random, sys, time
from game_objects import Botao, BotaoEspecial, Bolinha, Jogador
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from datetime import datetime

class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Menu Inicial")
        self.clock = pygame.time.Clock()
        self.running = True
        self.fase_1 = "Desbloqueada"
        self.fase_2 = "Bloqueada"
        self.menu_atual = "menu_principal" 
        self.ultimo_clique = pygame.time.get_ticks()
        self.nivel_fase_1 = "primaria"

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

        self.cores_neutras = {
            "turquesa": (64, 224, 208),
            "magenta": (255, 0, 255),
            "rosa": (255, 192, 203),
            "marrom": (139, 69, 19),
            "bege": (245, 245, 220),
            "cinza": (128, 128, 128),
            "dourado": (255, 215, 0),
            "prata": (192, 192, 192),
            "ciano_claro": (224, 255, 255),
            "verde_agua": (32, 178, 170),
            "salmao": (250, 128, 114),
            "vinho": (128, 0, 32),
            "purpura": (128, 0, 128),
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
            "fase_1": Botao(500, SCREEN_HEIGHT - 371, 275, 50, "Fase 1", (150, 150, 255), acao=self.fase_cores_primarias),
            "fase_2": Botao(500, SCREEN_HEIGHT - 295, 275, 50, "Fase 2", (255, 150, 150), acao=None),
            #"menu": Botao((SCREEN_WIDTH - 750) // 2 + 260, (SCREEN_HEIGHT - 120) // 2 - 70, 210, 95, "Menu", (100, 255, 100), acao=self.menu_nome),
            "config": Botao(18, 18, 75, 75, "Configuração", (0, 255, 0), acao=self.acao_configuracao),
            "ajuda": Botao(SCREEN_WIDTH - 80, 20, 60, 80, "Ajuda", (255, 255, 0), acao=self.acao_ajuda_fase1),
            #"som": Botao(SCREEN_WIDTH - 180, 20, 95, 80, "Som", (255, 165, 0), acao=self.acao_som),
        }
        self.botoes_fase_1 = {
            #"menu": Botao((SCREEN_WIDTH - 750) // 2 + 260, (SCREEN_HEIGHT - 120) // 2 - 70, 210, 95, "Menu", (100, 255, 100), acao=self.menu_nome),
            "config": Botao(18, 18, 75, 75, "Configuração", (0, 255, 0), acao=self.acao_configuracao),
            "ajuda": Botao(SCREEN_WIDTH - 80, 20, 60, 80, "Ajuda", (255, 255, 0), acao=self.acao_ajuda_fase1),
            "som": Botao(SCREEN_WIDTH - 180, 20, 95, 80, "Som", (255, 165, 0), acao=self.acao_som),
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
        self.layout_nivel_1 = pygame.image.load("assets/layouts/tela_escolha_cor_primaria.png")
        self.layout_nivel_1 = pygame.transform.smoothscale(self.layout_nivel_1, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.layout_nivel_2 = pygame.image.load("assets/layouts/tutorial_cores_secundarias.png")
        self.layout_nivel_2 = pygame.transform.smoothscale(self.layout_nivel_2, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.layout_acertou_nivel_1 = pygame.image.load("assets/layouts/mensagem_acertou.png")
        self.layout_acertou_nivel_1 = pygame.transform.smoothscale(self.layout_acertou_nivel_1, (SCREEN_WIDTH, SCREEN_HEIGHT))


    #ENCAPSULANDO FUNCOES DA CLASSE JOGADOR!
    def registrar_tentativa(self, fase, nivel, acertou):
        """encapsula o registro de tentativas no jogador"""
        self.jogador.registrar_tentativa(fase, nivel, acertou)

    def completar_fase(self, fase):
        """marca as fases concluidas"""
        self.jogador.completar_fase(fase)
    
    def salva_estatisticas(self):
        """salva progresso jogador"""
        self.jogador.salvar_log()
    #FIM ENCAPSULAMENTO

    def desenhar_menu(self):
        """Desenha o layout do menu inicial com os botões."""
        # Desenhar o fundo
        self.tela.blit(self.layout_menu, (0, 0))
        
        # Desenhar os botões
        for botao in self.botoes.values():
            botao.desenhar(self.tela)

    def desenhar_menu_fases(self):
        """desenha o layout do menu de fases"""
        if self.fase_2 == "Bloqueada":
            self.tela.blit(self.layout_menu_fases, (0, 0))
        elif self.fase_2 == "Desbloqueada":
            self.tela.blit(self.layout_menu_fases_2, (0, 0))
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
        
        coordenadas = [
            (815, 216),  # Primeira bolinha
            (1107, 216),  # Segunda bolinha
            (815, 464),  # Terceira bolinha
            (1107, 464),  # Quarta bolinha
        ]

        # Criação das bolinhas
        for i, (x, y) in enumerate(coordenadas):
            if i == indice_neutra:  # Esta bolinha recebe uma cor neutra
                cor = random.choice(list(self.cores_neutras.values()))
            else:  # As demais recebem cores primárias
                if self.nivel_fase_1 == "primaria":
                    cor = random.choice(list(self.cores_primarias.values()))
                
                else:
                    cor = random.choice(list(self.cores_secundarias.values()))
            self.bolinhas.append(Bolinha(x, y, cor))

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
                    return True  # Bolinha correta foi clicada

        # Se nenhuma bolinha válida foi clicada
        return False



    def desenhar_fase_cores_primarias(self):
        if self.nivel_fase_1 == "primaria":
            self.tela.blit(self.layout_nivel_1, (0, 0))
        else:
            self.tela.blit(self.layout_nivel_2, (0, 0))

        for botao in self.botoes_fase_1.values():
            botao.desenhar(self.tela)

        # Desenho das bolinhas na tela
        for bolinha in self.bolinhas:
            bolinha.desenhar(self.tela)

    def fase_cores_primarias(self):
        self.menu_atual = "fase_cores_primarias"

        print("Iniciando Fase 1")
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    # Verificar hover para todas as bolinhas
                    pos = pygame.mouse.get_pos()
                    for bolinha in self.bolinhas or self.cores_neutras:
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
                        self.nivel_fase_1 = "secundaria"
                        self.tela.blit(self.layout_acertou_nivel_1, (0, 0))
                        pygame.display.flip()
                        #delay
                        tempo_inicio = pygame.time.get_ticks()
                        delay = 3000  # 10 segundos

                        while True:
                            tempo_atual = pygame.time.get_ticks()
                            if tempo_atual - tempo_inicio >= delay:
                                print("10 segundos se passaram!")
                                break

                        self.desenhar_fase_cores_primarias()
                        pygame.display.flip()
                        self.iniciar_bolinhas()
                    elif (escolhida and self.nivel_fase_1 == "secundaria"):
                        # chamar fase_cores_secundarias()
                        print("acertou cor secundaria! parabens")
                        self.fase_2 = "Desbloqueada"
                        return
                    elif not escolhida and self.nivel_fase_1 == "primaria":
                        print("errou cor primaria! tente novamente")

                    elif not escolhida and self.nivel_fase_1 == "secundaria":
                        print("errou cor secundaria! tente novamente")


            self.desenhar_fase_cores_primarias()
            pygame.display.flip()
            self.clock.tick(60)


    def verificar_clique(self, pos):
        

        if self.menu_atual == "menu_principal":
            botoes = self.botoes
        elif self.menu_atual == "menu_config":
            botoes = self.botoes_config
        elif self.menu_atual == "menu_fases":
            botoes = self.botoes_menu_fases
        elif self.menu_atual == "fase_cores_primarias":
            botoes = self.botoes_fase_1
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
                            pontuacao_professor = 0,
                            pontuacao_estudante = "",
                            data=datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
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

    def menu_fases(self):
            print("Acao_menu_fases")
            
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

    def acao_professor(self):
        print("Ação: Professor")
        # Adicione aqui a lógica para mudar para a tela do professor

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
