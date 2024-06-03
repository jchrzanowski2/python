import pygame
from constants import Constants


class Button:
    def __init__(self, text, x, y, function, color=Constants.BROWN, font_size=30):
        self.color = color
        self.function = function
        self.font = pygame.font.Font(None, font_size)
        self.text = text
        self.rect = pygame.Rect(x, y, 165, 50)
        self.text_surf = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surf, self.text_rect)

    def clicked(self, x, y):
        return self.rect.collidepoint(x, y)
