import pygame
from pygame import *



class Button:
    """
    simple button, base for everything
    """

    def __init__(self, title: str, size: [int, int], color=Color(155, 230, 250)):
        self.title = title
        self.size = size
        self.color = color
        self.rect = Rect((0, 0), size)
        self.on_click = []
        self.show = True
        self.disabled = False
        self.arial_font = font.SysFont('Arial', 15, bold=True)

    def add_click_listener(self, func):
        self.on_click.append(func)

    def render(self, surface: Surface, pos):
        if(not self.show):
            return
        self.rect.topleft = pos

        title_srf = self.arial_font.render(self.title, True, Color(70, 50, 111))
        title_rect = title_srf.get_rect(center=self.rect.center)
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, Color(50, 50, 50), self.rect, width=5)
        surface.blit(title_srf, title_rect)

    def check(self):
        if self.on_click != [] and not self.disabled:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                clicked, _, _ = pygame.mouse.get_pressed()
                if clicked:
                    for f in self.on_click:
                        f()
