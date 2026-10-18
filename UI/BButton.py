# import pygame
# class Button:
#     def __init__(self,x, y, width, height, text, id , color, color_line, color_text, hover_color,left,right):
#         self.rect =  pygame.Rect(x, y, width, height)
#         self.x = x
#         self.y = y
#         self.text = text
#         self.id = id
#         self.color = color
#         self.color_text = color_text
#         self.hover_color = hover_color
#         self.color_line = color_line
#         self.hover = False
#         self.active = False
#         self.left = left
#         self.right = right
#         self.font = pygame.font.SysFont('Arial',20)
#         self.text_box = False

#     def update (self):
#         mouse = pygame.mouse.get_pos()
#         self.hover = self.rect.collidepoint(mouse)
        
#     # def TextBox(self):
#     #     x,y,width,height = self.rect
#     #     tb = TextBox.Textbox(x,y,width,height, color = self.color, color_text = self.color_text color_line = color_line , hover_color = hover_color, max_length = 18)

#     def draw(self,screen):
#         now_color = (0,0,0)
#         if self.hover:
#             now_color = self.hover_color
#         else :
#             now_color = self.color
#         pygame.draw.rect(screen,now_color,self.rect)
#         pygame.draw.rect(screen,self.color_line,self.rect,2)
#         surface = self.font.render(self.text,True,self.color_text)
#         text_rect = surface.get_rect()
#         text_rect.center = self.rect.center
#         screen.blit(surface,text_rect)

#     def handle_event (self, event):
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             if event.button == 1:
#                 if self.rect.collidepoint(event.pos) and self.left :
#                     self.active = True
#                     return self.id
#                 else :
#                     return "out_box"
#             elif event.button == 3 : 
#                 if self.rect.collidepoint(event.pos) and self.right :
#                     self.active = True
#                     return self.id
#                 else :
#                     return "out_box"
#         return None


import os
import pygame
from .Theme import Theme


class Button:
    def __init__(
        self,
        x, y, width, height,
        text, id,
        color, color_line, color_text, hover_color, color_active,
        left, right, size
    ):
        self.rect = pygame.Rect(x, y, width, height)

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._text = str(text)
        self.size = size
        self.id = id

        self.color = color
        self.color_text = color_text
        self.hover_color = hover_color
        self.color_active = color_active
        self.color_line = color_line

        self.hover = False
        self.active = False
        self.disabled = False
        self.pressed = False

        self.left = left
        self.right = right

        # Animation states
        self.hover_progress = 0.0

        # Load font with fallback
        try:
            self.font = pygame.font.SysFont(Theme.FONT, size)
        except Exception:
            current_dir = os.path.dirname(__file__)
            font_path = os.path.join(current_dir, "arial.ttf")
            if os.path.exists(font_path):
                self.font = pygame.font.Font(font_path, size)
            else:
                self.font = pygame.font.SysFont("Arial", size)

        self.text_box = False
        self._cached_surface = None
        self._cached_text = None
        self._cached_color = None

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, val):
        val_str = str(val)
        if self._text != val_str:
            self._text = val_str
            self._cached_surface = None

    def update(self, offset_y=0):
        if self.disabled:
            self.hover = False
            self.hover_progress = max(0.0, self.hover_progress - 0.2)
            return

        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_y += offset_y
        mouse = (mouse_x, mouse_y)
        self.hover = self.rect.collidepoint(mouse)

        target = 1.0 if self.hover else 0.0
        self.hover_progress += (target - self.hover_progress) * 0.25

    def draw(self, screen):

        if self.active:
            now_color = self.color_active
            border_color = Theme.PRIMARY_HOVER
            text_color = Theme.TEXT
        else:
            now_color = Theme.lerp_color(self.color, self.hover_color, self.hover_progress)
            border_color = Theme.lerp_color(self.color_line, Theme.PRIMARY, self.hover_progress)
            text_color = self.color_text

        # Soft shadow under button
        if not self.disabled:
            shadow_rect = self.rect.move(0, 3)
            pygame.draw.rect(
                screen,
                Theme.SHADOW,
                shadow_rect,
                border_radius=Theme.BUTTON_RADIUS
            )

        # Button background
        draw_rect = self.rect.move(0, -1 if (self.hover and not self.disabled and not self.active) else 0)
        pygame.draw.rect(
            screen,
            now_color,
            draw_rect,
            border_radius=Theme.BUTTON_RADIUS
        )

        # Subtle border
        pygame.draw.rect(
            screen,
            border_color,
            draw_rect,
            width=1,
            border_radius=Theme.BUTTON_RADIUS
        )

        # Render text with caching
        if self._cached_surface is None or self._cached_color != text_color:
            self._cached_surface = self.font.render(self._text, True, text_color)
            self._cached_color = text_color

        text_rect = self._cached_surface.get_rect(center=draw_rect.center)
        screen.blit(self._cached_surface, text_rect)

    def handle_event(self, event, offset_y=0):
        if self.disabled:
            return None

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            mouse_y += offset_y
            event_pos = (mouse_x, mouse_y)

            if event.button == 1:
                if self.rect.collidepoint(event_pos) and self.left:
                    self.active = True
                    return self.id
                else:
                    return "out_box"

            elif event.button == 3:
                if self.rect.collidepoint(event_pos) and self.right:
                    self.active = True
                    return self.id
                else:
                    return "out_box"

        return None
