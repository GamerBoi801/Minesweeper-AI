import pygame
from config import MAX_LOG_MESSAGES, LIGHT_GRAY, BLACK

class LogPanel:
    def __init__(self, screen, panel_rect, font):
        self.screen = screen
        self.panel_rect = panel_rect
        self.font = font
        self.messages = []

    def add_message(self, msg):
        if len(self.messages)>=MAX_LOG_MESSAGES:
            self.messages.pop(0)
        self.messages.append(msg)

    def draw(self):
        pygame.draw.rect(self.screen, LIGHT_GRAY, self.panel_rect, border_radius=8)
        title = self.font.render("AI Reasoning", True, BLACK)
        self.screen.blit(title, (self.panel_rect.x+10, self.panel_rect.y+10))
        for idx, msg in enumerate(self.messages):
            line = self.font.render(msg, True, BLACK)
            self.screen.blit(line, (self.panel_rect.x+15, self.panel_rect.y+50 + idx*25))
