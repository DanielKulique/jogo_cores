from game_objects import Botao
import random

class Jogo:
	def __init__(self, cores_primarias, cores_erradas):
		self.cores_primarias = cores_primarias
		self.cores_erradas = cores_erradas
		self.cores = []
		self.feedback = ""
		self.iniciar_fase()

	def iniciar_fase(self):
		cores_primarias = random.sample(list(self.cores_primarias.items()), 3)
		cor_errada = random.choice(list(self.cores_erradas.items()))
		opcoes = cores_primarias + [cor_errada]
		random.shuffle(opcoes)

		self.cores = [
            Botao(100 + i * 200, 200, cor, imagem) for i, (cor, imagem) in enumerate(opcoes)
        ]
        self.feedback = ""

    def verificar_cor(self, cor):
    	if cor in self.cores_primarias:
    		self.feedback = "Acertou! Clique para continuar!"
    		self.iniciar_fase()
    	else:
    		self.feedback = "Errou! Tente novamente."

    def desenhar(self, tela):
    	for botao in self.cores:
    		botao.desenhar(tela)

    	if self.feedback:
    		fonte = pygame.font.Font(None, 36)
    		texto = fonte.render(self.feedback, True, (0, 0, 0))
    		tela.blit(texto, (400 - texto.get_width() // 2, 50))
    		
