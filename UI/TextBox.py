import os
import pygame
from .Theme import Theme


class Textbox:

    def __init__(
        self,
        x,
        y,
        width,
        height,
        color,
        color_text,
        color_line,
        hover_color,
        max_length,
        size,
        placeholder=""
    ):
        self.rect = pygame.Rect(x, y, width, height)

        self.color = color
        self.color_text = color_text

        self.active = False
        self.enter = False

        self.hover_color = hover_color
        self.color_line = color_line
        self.hover = False

        self.max_length = max_length
        self.size = size
        self.placeholder = placeholder

        self.user_text = ""
        self.id = 0

        # Cursor animation
        self.cursor_visible = True
        self.cursor_timer = 0.0

        try:
            self.font = pygame.font.SysFont(Theme.FONT, self.size)
        except Exception:
            current_dir = os.path.dirname(__file__)
            font_path = os.path.join(current_dir, "arial.ttf")
            if os.path.exists(font_path):
                self.font = pygame.font.Font(font_path, self.size)
            else:
                self.font = pygame.font.SysFont("Arial", self.size)

        self.update_surface()

    def update(self, dt=0.016):
        mouse = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint(mouse)

        if self.active:
            self.cursor_timer += 0.025
            if self.cursor_timer >= 1.0:
                self.cursor_timer = 0.0
            self.cursor_visible = self.cursor_timer < 0.5
        else:
            self.cursor_visible = False

    def draw(self, screen):
        if self.active:
            now_color = Theme.INPUT_ACTIVE
            border_color = Theme.INPUT_BORDER_ACTIVE
        elif self.hover:
            now_color = Theme.INPUT_HOVER
            border_color = Theme.BORDER_LIGHT
        else:
            now_color = Theme.INPUT
            border_color = Theme.INPUT_BORDER

        # Background with soft shadow
        shadow_rect = self.rect.move(0, 2)
        pygame.draw.rect(
            screen,
            Theme.SHADOW,
            shadow_rect,
            border_radius=Theme.INPUT_RADIUS
        )

        pygame.draw.rect(
            screen,
            now_color,
            self.rect,
            border_radius=Theme.INPUT_RADIUS
        )

        # Border
        border_width = 2 if self.active else 1
        pygame.draw.rect(
            screen,
            border_color,
            self.rect,
            width=border_width,
            border_radius=Theme.INPUT_RADIUS
        )

        # Content clipping to avoid overflow
        clip_rect = self.rect.inflate(-16, -4)
        old_clip = screen.get_clip()
        screen.set_clip(clip_rect)

        if not self.user_text and self.placeholder and not self.active:
            ph_surface = self.font.render(self.placeholder, True, Theme.TEXT_MUTED)
            ph_rect = ph_surface.get_rect(midleft=(self.rect.left + 12, self.rect.centery))
            screen.blit(ph_surface, ph_rect)
        else:
            screen.blit(self.surface, self.text_rect)

            # Draw cursor
            if self.active and self.cursor_visible:
                cursor_x = self.text_rect.right + 2 if self.user_text else self.rect.left + 12
                cursor_top = self.rect.centery - self.size // 2
                cursor_bottom = self.rect.centery + self.size // 2
                pygame.draw.line(
                    screen,
                    Theme.PRIMARY,
                    (cursor_x, cursor_top),
                    (cursor_x, cursor_bottom),
                    2
                )

        screen.set_clip(old_clip)

    def update_surface(self):
        self.surface = self.font.render(
            self.user_text,
            True,
            self.color_text
        )

        self.text_rect = self.surface.get_rect()
        self.text_rect.midleft = (
            self.rect.left + 12,
            self.rect.centery
        )

    def clear(self):
        self.user_text = ""
        self.update_surface()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.active = self.rect.collidepoint(event.pos)
                if self.active:
                    self.cursor_timer = 0.0
                    self.cursor_visible = True
            else:
                self.active = False

        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                    self.update_surface()
                elif event.key == pygame.K_RETURN and self.enter:
                    return self.user_text
                elif event.key == pygame.K_ESCAPE:
                    self.active = False

            elif event.type == pygame.TEXTINPUT:
                new_text = self.user_text + event.text
                if len(new_text) <= self.max_length:
                    self.user_text = new_text
                    self.update_surface()

        return None