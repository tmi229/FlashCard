import os
import pygame
from UI import BButton
from UI.Theme import Theme
from .Base_Screen import base


class MenuScreen(base):
    def __init__(self,audio):
        # Load fonts with Vietnamese support
        try:
            self.title_font = pygame.font.SysFont(Theme.FONT, 38, bold=True)
            self.subtitle_font = pygame.font.SysFont(Theme.FONT, 18)
            self.card_title_font = pygame.font.SysFont(Theme.FONT, 22, bold=True)
            self.card_desc_font = pygame.font.SysFont(Theme.FONT, 16)
            self.badge_font = pygame.font.SysFont(Theme.FONT, 13, bold=True)
        except Exception:
            current_dir = os.path.dirname(__file__)
            font_path = os.path.join(current_dir, "arial.ttf")
            if os.path.exists(font_path):
                self.title_font = pygame.font.Font(font_path, 38)
                self.subtitle_font = pygame.font.Font(font_path, 18)
                self.card_title_font = pygame.font.Font(font_path, 22)
                self.card_desc_font = pygame.font.Font(font_path, 16)
                self.badge_font = pygame.font.Font(font_path, 13)
            else:
                self.title_font = pygame.font.SysFont("Arial", 38, bold=True)
                self.subtitle_font = pygame.font.SysFont("Arial", 18)
                self.card_title_font = pygame.font.SysFont("Arial", 22, bold=True)
                self.card_desc_font = pygame.font.SysFont("Arial", 16)
                self.badge_font = pygame.font.SysFont("Arial", 13, bold=True)
        self.audio_manager = audio
        self.Menu_Button = []

        # Feature Card 1: Học & Quản lý từ vựng
        self.card1_rect = pygame.Rect(230, 200, 440, 360)
        btn_learn = BButton.Button(
            x=260, y=475, width=380, height=54,
            text="Vào Học & Quản Lý", id="learn",
            color=Theme.PRIMARY, color_line=Theme.PRIMARY, color_text=Theme.TEXT,
            hover_color=Theme.PRIMARY_HOVER, color_active=Theme.PRIMARY,
            left=True, right=False, size=18
        )
        self.Menu_Button.append(btn_learn)

        # Feature Card 2: Luyện tập & Quiz
        self.card2_rect = pygame.Rect(730, 200, 440, 360)
        btn_quiz = BButton.Button(
            x=760, y=475, width=380, height=54,
            text="Vào Luyện Tập (Quiz)", id="quiz",
            color=(16, 185, 129), color_line=(16, 185, 129), color_text=Theme.TEXT,
            hover_color=(34, 197, 94), color_active=(16, 185, 129),
            left=True, right=False, size=18
        )
        self.Menu_Button.append(btn_quiz)

        # Quick exit button
        btn_exit = BButton.Button(
            x=620, y=605, width=160, height=44,
            text="Thoát", id="exit",
            color=Theme.BUTTON, color_line=Theme.BORDER, color_text=Theme.TEXT_SECOND,
            hover_color=Theme.BUTTON_HOVER, color_active=Theme.BUTTON_ACTIVE,
            left=True, right=False, size=16
        )
        self.Menu_Button.append(btn_exit)

        # Card hover states
        self.card1_hover = False
        self.card2_hover = False

    def handle_event(self, event):
        for nut in self.Menu_Button:
            result = nut.handle_event(event)
            if result is not None and result != "out_box":
                self.audio_manager.play("click")
                return result
        return None

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        self.card1_hover = self.card1_rect.collidepoint(mouse_pos)
        self.card2_hover = self.card2_rect.collidepoint(mouse_pos)

        for nut in self.Menu_Button:
            nut.update()

    def draw(self, screen):
        screen.fill(Theme.BG)

        # Header Badge
        badge_text = self.badge_font.render("FLASHCARD MASTER • SMART LEARNING", True, Theme.PRIMARY_HOVER)
        badge_w = badge_text.get_width() + 24
        badge_rect = pygame.Rect(700 - badge_w // 2, 45, badge_w, 26)
        pygame.draw.rect(screen, Theme.PANEL, badge_rect, border_radius=13)
        pygame.draw.rect(screen, Theme.PRIMARY_LIGHT, badge_rect, width=1, border_radius=13)
        screen.blit(badge_text, badge_text.get_rect(center=badge_rect.center))

        # Main Title
        title_surf = self.title_font.render("HỌC TỪ VỰNG THÔNG MINH", True, Theme.TEXT)
        title_rect = title_surf.get_rect(center=(700, 105))
        screen.blit(title_surf, title_rect)

        # Subtitle
        sub_surf = self.subtitle_font.render("Ghi nhớ lâu hơn với phương pháp lặp lại ngắt quãng & luyện tập tương tác", True, Theme.TEXT_SECOND)
        sub_rect = sub_surf.get_rect(center=(700, 148))
        screen.blit(sub_surf, sub_rect)

        # Draw Feature Card 1 (Learn & Manage)
        c1_bg = Theme.PANEL_LIGHT if self.card1_hover else Theme.PANEL
        c1_border = Theme.PRIMARY if self.card1_hover else Theme.BORDER
        shadow1 = self.card1_rect.move(0, 4)
        pygame.draw.rect(screen, Theme.SHADOW, shadow1, border_radius=Theme.CARD_RADIUS)
        pygame.draw.rect(screen, c1_bg, self.card1_rect, border_radius=Theme.CARD_RADIUS)
        pygame.draw.rect(screen, c1_border, self.card1_rect, width=1 if not self.card1_hover else 2, border_radius=Theme.CARD_RADIUS)

        # Card 1 Badge / Tag
        tag1 = self.badge_font.render("QUẢN LÝ DỮ LIỆU", True, Theme.PRIMARY_HOVER)
        screen.blit(tag1, (260, 230))

        # Card 1 Title
        c1_title = self.card_title_font.render("Kho Từ Vựng & Bộ Thẻ", True, Theme.TEXT)
        screen.blit(c1_title, (260, 255))

        # Card 1 Descriptions
        desc1_items = [
            "• Quản lý và tạo mới nhiều bộ từ vựng theo chủ đề",
            "• Thêm từ, phiên âm, giải nghĩa và câu ví dụ",
            "• Tìm kiếm nhanh chóng, lọc từ và sắp xếp A-Z",
            "• Chỉnh sửa hoặc xóa từ vựng linh hoạt"
        ]
        y_pos = 300
        for item in desc1_items:
            t = self.card_desc_font.render(item, True, Theme.TEXT_SECOND)
            screen.blit(t, (260, y_pos))
            y_pos += 34

        # Draw Feature Card 2 (Quiz & Practice)
        c2_bg = Theme.PANEL_LIGHT if self.card2_hover else Theme.PANEL
        c2_border = (16, 185, 129) if self.card2_hover else Theme.BORDER
        shadow2 = self.card2_rect.move(0, 4)
        pygame.draw.rect(screen, Theme.SHADOW, shadow2, border_radius=Theme.CARD_RADIUS)
        pygame.draw.rect(screen, c2_bg, self.card2_rect, border_radius=Theme.CARD_RADIUS)
        pygame.draw.rect(screen, c2_border, self.card2_rect, width=1 if not self.card2_hover else 2, border_radius=Theme.CARD_RADIUS)

        # Card 2 Badge / Tag
        tag2 = self.badge_font.render("LUYỆN TẬP PHẢN XẠ", True, (34, 197, 94))
        screen.blit(tag2, (760, 230))

        # Card 2 Title
        c2_title = self.card_title_font.render("4 Chế Độ Kiểm Tra Trí Nhớ", True, Theme.TEXT)
        screen.blit(c2_title, (760, 255))

        # Card 2 Descriptions
        desc2_items = [
            "• Thẻ ghi nhớ Flashcard lật 3D trực quan",
            "• Trắc nghiệm 4 đáp án chọn nhanh tính điểm",
            "• Match Game kéo thả ghép từ - nghĩa linh hoạt",
            "• Tự luận gõ đáp án để ghi nhớ chính xác mặt chữ"
        ]
        y_pos = 300
        for item in desc2_items:
            t = self.card_desc_font.render(item, True, Theme.TEXT_SECOND)
            screen.blit(t, (760, y_pos))
            y_pos += 34

        # Draw Buttons
        for nut in self.Menu_Button:
            nut.draw(screen)
            nut.active = False