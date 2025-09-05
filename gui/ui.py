import pygame
from config import BLACK

def draw_button(screen, rect, text, base_color, hover_color, font):
    mouse_pos = pygame.mouse.get_pos()
    color = hover_color if rect.collidepoint(mouse_pos) else base_color
    pygame.draw.rect(screen, color, rect, border_radius=10)
    text_surf = font.render(text, True, BLACK)
    screen.blit(text_surf, text_surf.get_rect(center=rect.center))
