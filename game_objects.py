import pygame

class Bolinha:
	def __init__(self, x, y, cor, raio=30):
		self.x = x
		self.y = y
		self.cor = cor
		self.raio = raio
		self.rect = pygame.Rect(x - raio, y - raio, raio * 2, raio *2)
	def desenhar(self, tela)
		"""desenha a bolinha na tela"""
		pygame.draw.circle(tela, self.cor, (self.x, self.y), self.raio)
	def foi_clicada(self, posicao_mouse):
		"""verifica se a bolinha foi clicada"""
		return self.rect.collidepoint(posicao_mouse)

class Botao:
	def __init(self, x, y, largura, altura, texto, cor, cor_texto, fonte = None):
		self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.texto = texto
        self.cor = cor
        self.cor_texto = cor_texto
        self.fonte = fonte or pygame.font.Font(None, 36)
        self.rect = pygame.Rect(x, y, largura, altura)

	def desenhar(self, tela):
		pygame.draw.rect(tela, self.cor, self.rect)
        texto_surface = self.fonte.render(self.texto, True, self.cor_texto)
        texto_rect = texto_surface.get_rect(center=self.rect.center)
        tela.blit(texto_surface, texto_rect)
        
	def	foi_clicado(self, posicao_mouse):
		"""verifica se a bolinha foi clicada"""
		return self.rect.collidepoint(posicao_mouse)

