import pygame
import sys

pygame.init()

# Dimensões da tela
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Botão Estilizado")

# Cores
BACKGROUND_COLOR = (255, 204, 142)  # #ffcc8e
BUTTON_COLOR = (255, 161, 43)  # #FFA12B
BUTTON_HOVER_COLOR = (247, 137, 0)  # #F78900
BUTTON_SHADOW_COLOR = (145, 81, 0)  # #915100
BUTTON_TEXT_COLOR = (255, 255, 255)  # branco
SHADOW_BACKGROUND_COLOR = (43, 24, 0)  # #2B1800

# Configurações do botão
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60
BUTTON_TEXT = "Clique Aqui"
FONT = pygame.font.SysFont("Helvetica", 36, bold=True)

# Função para desenhar o botão
def draw_button(surface, x, y, text, active=False):
    shadow_offset = 15 if not active else 10
    button_color = BUTTON_HOVER_COLOR if active else BUTTON_COLOR
    
    # Sombra do botão
    pygame.draw.rect(
        surface,
        SHADOW_BACKGROUND_COLOR,
        (x - 4, y + shadow_offset, BUTTON_WIDTH + 8, BUTTON_HEIGHT + 4),
        border_radius=5,
    )

    # Corpo do botão
    pygame.draw.rect(
        surface,
        button_color,
        (x, y, BUTTON_WIDTH, BUTTON_HEIGHT),
        border_radius=5,
    )

    # Sombras internas do botão
    pygame.draw.rect(
        surface,
        BUTTON_SHADOW_COLOR,
        (x, y + BUTTON_HEIGHT - 10, BUTTON_WIDTH, 10),
        border_radius=5,
    )
    pygame.draw.rect(
        surface,
        (255, 229, 196),  # #FFE5C4
        (x, y, BUTTON_WIDTH, 10),
        border_radius=5,
    )

    # Texto do botão
    text_surface = FONT.render(text, True, BUTTON_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(x + BUTTON_WIDTH // 2, y + BUTTON_HEIGHT // 2))
    surface.blit(text_surface, text_rect)

# Função principal
def main():
    running = True
    clock = pygame.time.Clock()
    button_x, button_y = (SCREEN_WIDTH - BUTTON_WIDTH) // 2, (SCREEN_HEIGHT - BUTTON_HEIGHT) // 2
    button_pressed = False

    while running:
        screen.fill(BACKGROUND_COLOR)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        button_rect = pygame.Rect(button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
        is_hovered = button_rect.collidepoint(mouse_x, mouse_y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and is_hovered:
                button_pressed = True
            if event.type == pygame.MOUSEBUTTONUP and button_pressed:
                if is_hovered:
                    print("Botão clicado!")
                button_pressed = False

        draw_button(screen, button_x, button_y, BUTTON_TEXT, active=button_pressed or is_hovered)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
