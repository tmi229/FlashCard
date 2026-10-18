# import pygame
# import os

# class Label :
#     def __init__(self,x,y,font_size,text,color):
#         current_dir = os.path.dirname(__file__)
#         font_path = os.path.join(current_dir, "arial.ttf")
#         self.font = pygame.font.Font(font_path, font_size)
#         self.x = x
#         self.y = y
#         self.text = text
#         self.color = color
#         self.text_surface = self.font.render(self.text,True,self.color)

#     def set_text(self,new_text):
#         self.text = new_text
#         self.text_surface = self.font.render(self.text, True,self.color )

#     def draw(self, screen):
#         screen.blit(self.text_surface,(self.x,self.y))

import os
import pygame
from .Theme import Theme


class Label:
    def __init__(self, x, y, font_size, text, color=None):
        try:
            self.font = pygame.font.SysFont(Theme.FONT, font_size)
        except Exception:
            current_dir = os.path.dirname(__file__)
            font_path = os.path.join(current_dir, "arial.ttf")
            if os.path.exists(font_path):
                self.font = pygame.font.Font(font_path, font_size)
            else:
                self.font = pygame.font.SysFont("Arial", font_size)

        self.x = x
        self.y = y
        self.text = text
        self.color = Theme.TEXT if color is None else color

        self.text_surface = self.font.render(
            self.text,
            True,
            self.color
        )

    def set_text(self, new_text, color=None):
        self.text = str(new_text)
        if color is not None:
            self.color = color
        self.text_surface = self.font.render(
            self.text,
            True,
            self.color
        )

    def draw(self, screen):
        screen.blit(self.text_surface, (self.x, self.y))
