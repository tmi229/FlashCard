import os
import random
import math
import pygame

from UI import BButton, TextBox
from UI.Theme import Theme
from .Base_Screen import base


class QuizScreen(base):

    def __init__(self, list_card_manager,audio):
        super().__init__()

        # ==================================================
        # FONTS (Robust Vietnamese font fallback)
        # ==================================================
        try:
            self.card_font = pygame.font.SysFont(Theme.FONT, 46, bold=True)
            self.title_font = pygame.font.SysFont(Theme.FONT, 28, bold=True)
            self.section_font = pygame.font.SysFont(Theme.FONT, 20, bold=True)
            self.font = pygame.font.SysFont(Theme.FONT, 18)
            self.font_bold = pygame.font.SysFont(Theme.FONT, 18, bold=True)
            self.small_font = pygame.font.SysFont(Theme.FONT, 15)
            self.small1_font = pygame.font.SysFont(Theme.FONT, 16)
            self.hint_font = pygame.font.SysFont(Theme.FONT, 14)
            self.phonetic_font = pygame.font.SysFont(Theme.FONT, 22)
            
        except Exception:
            current_dir = os.path.dirname(__file__)
            font_path = os.path.join(current_dir, "arial.ttf")
            if os.path.exists(font_path):
                self.card_font = pygame.font.Font(font_path, 46)
                self.title_font = pygame.font.Font(font_path, 28)
                self.section_font = pygame.font.Font(font_path, 20)
                self.font = pygame.font.Font(font_path, 18)
                self.font_bold = pygame.font.Font(font_path, 18)
                self.small_font = pygame.font.Font(font_path, 15)
                self.small1_font = pygame.font.Font(font_path, 16)
                self.hint_font = pygame.font.Font(font_path, 14)
                self.phonetic_font = pygame.font.Font(font_path, 22)
            else:
                self.card_font = pygame.font.SysFont("Arial", 46, bold=True)
                self.title_font = pygame.font.SysFont("Arial", 28, bold=True)
                self.section_font = pygame.font.SysFont("Arial", 20, bold=True)
                self.font = pygame.font.SysFont("Arial", 18)
                self.font_bold = pygame.font.SysFont("Arial", 18, bold=True)
                self.small_font = pygame.font.SysFont("Arial", 15)
                self.small1_font = pygame.font.SysFont("Arial", 16)
                self.hint_font = pygame.font.SysFont("Arial", 14)
                self.phonetic_font = pygame.font.SysFont("Arial", 22)

        # ==================================================
        # DATA MANAGERS
        # ==================================================
        self.audio_manager = audio
        self.list_manager = list_card_manager
        self.card_manager = list_card_manager.List_Managers[0]
        self.nut_list_card = []
        self.nut_in_quiz_scr = []

        # 0 = Flash Card, 1 = Trắc Nghiệm, 2 = Match, 3 = Tự Luận
        self.current_mode = 0

        # ==================================================
        # MAIN LAYOUT
        # ==================================================
        self.sidebar_rect = pygame.Rect(20, 20, 360, 680)
        self.content_rect = pygame.Rect(400, 20, 980, 680)

        # ==================================================
        # SIDEBAR BUTTONS
        # ==================================================
        self.back_button = BButton.Button(
            x=45, y=35, width=90, height=42,
            text="← BACK", id="menu",
            color=Theme.BUTTON, color_line=Theme.BORDER, color_text=Theme.TEXT,
            hover_color=Theme.BUTTON_HOVER, color_active=Theme.BUTTON_ACTIVE,
            left=True, right=False, size=15
        )
        self.nut_in_quiz_scr.append(self.back_button)

        mode_buttons_info = [
            ("Flash Card", "FC", 150),
            ("Trắc Nghiệm", "TN", 212),
            ("Ghép Thẻ (Match)", "match", 274),
            ("Tự Luận", "TL", 336)
        ]
        self.flash_card = BButton.Button(
            x=45, y=150, width=310, height=50,
            text="  Flash Card", id="FC",
            color=Theme.BUTTON, color_line=Theme.BORDER, color_text=Theme.TEXT,
            hover_color=Theme.BUTTON_HOVER, color_active=Theme.PRIMARY,
            left=True, right=False, size=17
        )
        self.nut_in_quiz_scr.append(self.flash_card)

        self.trac_nghiem = BButton.Button(
            x=45, y=212, width=310, height=50,
            text="  Trắc Nghiệm", id="TN",
            color=Theme.BUTTON, color_line=Theme.BORDER, color_text=Theme.TEXT,
            hover_color=Theme.BUTTON_HOVER, color_active=Theme.PRIMARY,
            left=True, right=False, size=17
        )
        self.nut_in_quiz_scr.append(self.trac_nghiem)

        self.Match = BButton.Button(
            x=45, y=274, width=310, height=50,
            text="  Ghép Thẻ (Match)", id="match",
            color=Theme.BUTTON, color_line=Theme.BORDER, color_text=Theme.TEXT,
            hover_color=Theme.BUTTON_HOVER, color_active=Theme.PRIMARY,
            left=True, right=False, size=17
        )
        self.nut_in_quiz_scr.append(self.Match)

        self.tu_luan = BButton.Button(
            x=45, y=336, width=310, height=50,
            text="  Tự Luận", id="TL",
            color=Theme.BUTTON, color_line=Theme.BORDER, color_text=Theme.TEXT,
            hover_color=Theme.BUTTON_HOVER, color_active=Theme.PRIMARY,
            left=True, right=False, size=17
        )
        self.nut_in_quiz_scr.append(self.tu_luan)

        # Deck scrollable area in sidebar
        self.scroll_list = pygame.Rect(45, 465, 310, 215)
        self.y_scroll_list = 0
        self.update_list()

        # ==================================================
        # FLASHCARD STATE (MODE 0)
        # ==================================================
        self.card_rect = pygame.Rect(560, 180, 660, 430)
        self.cards = []
        self.card = None
        self.card_index = 0
        self.flipping = False
        self.progress = 0.0
        self.side = 0  # 0: Front (Word + Phonetic), 1: Back (Meaning + Example)

        self.previous_button = BButton.Button(
            x=480, y=365, width=60, height=60,
            text="<", id="previous",
            color=Theme.BUTTON, color_line=Theme.BORDER, color_text=Theme.TEXT,
            hover_color=Theme.BUTTON_HOVER, color_active=Theme.BUTTON_ACTIVE,
            left=True, right=False, size=24
        )
        self.next_button = BButton.Button(
            x=1240, y=365, width=60, height=60,
            text=">", id="next",
            color=Theme.BUTTON, color_line=Theme.BORDER, color_text=Theme.TEXT,
            hover_color=Theme.BUTTON_HOVER, color_active=Theme.BUTTON_ACTIVE,
            left=True, right=False, size=24
        )
        self.nut_chuyen_card = [self.previous_button, self.next_button]

        # ==================================================
        # TRẮC NGHIỆM STATE (MODE 1)
        # ==================================================
        self.quiz_question_rect = pygame.Rect(460, 160, 860, 170)
        self.nut_dap_an_ABCD = []
        answer_positions = [
            (460, 360, 410, 75),
            (910, 360, 410, 75),
            (460, 460, 410, 75),
            (910, 460, 410, 75)
        ]
        for i, (ax, ay, aw, ah) in enumerate(answer_positions):
            nut = BButton.Button(
                x=ax, y=ay, width=aw, height=ah,
                text="", id=f"answer_{i}",
                color=Theme.PANEL_LIGHT, color_line=Theme.BORDER, color_text=Theme.TEXT,
                hover_color=Theme.PANEL_HOVER, color_active=Theme.PRIMARY,
                left=True, right=False, size=18
            )
            self.nut_dap_an_ABCD.append(nut)

        self.quiz_cards = []
        self.quiz_index = 0
        self.correct_count = 0
        self.wrong_count = 0
        self.quiz_question = None
        self.quiz_answers = []
        self.quiz_answer_cards = []
        self.quiz_correct_answer = None
        self.quiz_type = 0
        self.index_choice = -1
        self.round_finished = False
        self.show_result = False

        self.result_button = BButton.Button(
            x=1110, y=560, width=210, height=50,
            text="Xem Kết Quả →", id="show_result",
            color=Theme.PRIMARY, color_line=Theme.PRIMARY, color_text=Theme.TEXT,
            hover_color=Theme.PRIMARY_HOVER, color_active=Theme.PRIMARY,
            left=True, right=False, size=18
        )
        self.retry_button = BButton.Button(
            x=720, y=595, width=160, height=50,
            text="Luyện Lại", id="retry",
            color=Theme.BUTTON, color_line=Theme.BORDER, color_text=Theme.TEXT,
            hover_color=Theme.BUTTON_HOVER, color_active=Theme.BUTTON_ACTIVE,
            left=True, right=False, size=17
        )
        self.next_button_result = BButton.Button(
            x=900, y=595, width=160, height=50,
            text="Tiếp Tục", id="next",
            color=Theme.PRIMARY, color_line=Theme.PRIMARY, color_text=Theme.TEXT,
            hover_color=Theme.PRIMARY_HOVER, color_active=Theme.PRIMARY,
            left=True, right=False, size=17
        )

        # ==================================================
        # MATCH GAME STATE (MODE 2)
        # ==================================================
        self.match_pairs = []
        self.match_assignments = {}  # {word_index: slot_row}
        self.match_dragging = None   # Index of word currently being dragged
        self.match_drag_pos = None
        self.match_drag_offset = (0, 0)
        self.match_drag_origin = None
        self.match_checked = False
        self.match_message = ""
        self.match_retry_pairs = []
        self.match_used_ids = set()

        self.match_word_rects = []
        self.match_slot_rects = []
        self.match_meaning_rects = []
        self.match_meaning_order = []

        self.match_check_rect = pygame.Rect(730, 605, 140, 48)
        self.match_retry_rect = pygame.Rect(890, 605, 140, 48)
        self.match_next_rect = pygame.Rect(1050, 605, 140, 48)

        # ==================================================
        # TỰ LUẬN STATE (MODE 3)
        # ==================================================
        self.written_cards = []
        self.written_index = 0
        self.written_checked = False
        self.written_is_correct = False
        self.written_box = TextBox.Textbox(
            x=560, y=360, width=540, height=54,
            color=Theme.INPUT, color_text=Theme.TEXT, color_line=Theme.BORDER,
            hover_color=Theme.INPUT_HOVER, max_length=40, size=20,
            placeholder="Gõ câu trả lời vào đây..."
        )
        self.written_box.enter = True

        self.written_check_btn = BButton.Button(
            x=1120, y=360, width=140, height=54,
            text="Kiểm tra", id="written_check",
            color=Theme.PRIMARY, color_line=Theme.PRIMARY, color_text=Theme.TEXT,
            hover_color=Theme.PRIMARY_HOVER, color_active=Theme.PRIMARY,
            left=True, right=False, size=17
        )
        self.written_next_btn = BButton.Button(
            x=1120, y=360, width=140, height=54,
            text="Câu tiếp →", id="written_next",
            color=Theme.PRIMARY, color_line=Theme.PRIMARY, color_text=Theme.TEXT,
            hover_color=Theme.PRIMARY_HOVER, color_active=Theme.PRIMARY,
            left=True, right=False, size=17
        )

        # Initialize rounds
        self.shuffle_cards()
        self.start_match_round()

    # ======================================================
    # UPDATE
    # ======================================================
    def update(self, dt):
        for nut in self.nut_in_quiz_scr:
            nut.update()

        for nut in self.nut_list_card:
            nut.update(self.y_scroll_list)

        if self.current_mode == 0:
            for nut in self.nut_chuyen_card:
                nut.update()

            if self.flipping:
                self.progress += dt / 0.45
                if self.progress >= 1.0:
                    self.progress = 1.0
                    self.flipping = False
                    self.side = 1 - self.side

        elif self.current_mode == 1:
            if not self.show_result:
                for nut in self.nut_dap_an_ABCD:
                    nut.update()
                if self.round_finished:
                    self.result_button.update()
            else:
                self.retry_button.update()
                self.next_button_result.update()

        elif self.current_mode == 3:
            self.written_box.update(dt)
            if not self.written_checked:
                self.written_check_btn.update()
            else:
                self.written_next_btn.update()

    def update_list(self):
        y = 475
        self.nut_list_card.clear()
        for i, lm in enumerate(self.list_manager.List_Managers):
            nut = BButton.Button(
                x=55, y=y, width=290, height=44,
                text=lm.name, id=lm.id,
                color=Theme.BUTTON, color_line=Theme.BORDER, color_text=Theme.TEXT,
                hover_color=Theme.BUTTON_HOVER, color_active=Theme.PRIMARY,
                left=True, right=True, size=15
            )
            self.nut_list_card.append(nut)
            y += 50

    def shuffle_cards(self):
        if self.list_manager and self.card_manager.Cards:
            self.cards = self.card_manager.Cards.copy()
            random.shuffle(self.cards)
            self.card_index = 0
            self.card = self.cards[self.card_index]

            self.quiz_cards = self.card_manager.Cards.copy()
            random.shuffle(self.quiz_cards)
            self.quiz_index = 0
            self.correct_count = 0
            self.wrong_count = 0
            self.round_finished = False
            self.show_result = False
            self.index_choice = -1

            self.written_cards = self.card_manager.Cards.copy()
            random.shuffle(self.written_cards)
            self.written_index = 0
            self.written_checked = False
            self.written_box.clear()
            self.written_box.active = True

            if len(self.card_manager.Cards) >= 4:
                self.create_quiz_question()
        else:
            self.cards = []
            self.card_index = 0
            self.card = None
            self.quiz_cards = []
            self.quiz_question = None
            self.written_cards = []

    # ======================================================
    # FLASHCARD LOGIC
    # ======================================================
    def start_flip(self):
        if not self.flipping and self.card is not None:
            self.audio_manager.play("flip")
            self.flipping = True
            self.progress = 0.0

    def next_card(self):
        if not self.cards:
            return
        if self.card_index == len(self.cards) - 1:
            self.card_index = 0
        else:
            self.card_index += 1

        self.card = self.cards[self.card_index]
        self.side = 0
        self.progress = 0.0
        self.flipping = False

    def previous_card(self):
        if not self.cards:
            return
        if self.card_index == 0:
            self.card_index = len(self.cards) - 1
        else:
            self.card_index -= 1

        self.card = self.cards[self.card_index]
        self.side = 0
        self.progress = 0.0
        self.flipping = False

    def ease(self, t):
        return 0.5 - 0.5 * math.cos(math.pi * t)

    def draw_card(self, surface):
        if not self.card:
            empty_img = self.font.render("Bộ từ vựng này đang trống. Hãy thêm từ vựng để bắt đầu!", True, Theme.TEXT_SECOND)
            surface.blit(empty_img, empty_img.get_rect(center=self.card_rect.center))
            return

        if not self.flipping:
            scale = 1.0
            side_now = self.side
            show_text = True
        else:
            p = self.progress
            if p < 0.40:
                z = p / 0.40
                scale = 1.0 - self.ease(z) * 0.85
                side_now = self.side
                show_text = p < 0.20
            elif p < 0.60:
                t = (p - 0.40) / 0.20
                scale = 0.15 + 0.02 * math.sin(math.pi * t)
                side_now = self.side
                show_text = False
            else:
                z = (p - 0.60) / 0.40
                scale = 0.15 + self.ease(z) * 0.85
                side_now = 1 - self.side
                show_text = p > 0.80

        width = max(6, int(self.card_rect.width * scale))
        x = self.card_rect.centerx - width // 2
        rect = pygame.Rect(x, self.card_rect.y, width, self.card_rect.height)

        # Card shadow
        shadow_rect = rect.move(0, 8)
        pygame.draw.rect(surface, Theme.SHADOW, shadow_rect, border_radius=Theme.CARD_RADIUS)

        color = Theme.CARD if side_now == 0 else Theme.CARD_BACK
        pygame.draw.rect(surface, color, rect, border_radius=Theme.CARD_RADIUS)
        pygame.draw.rect(surface, Theme.BORDER_LIGHT if side_now == 0 else Theme.PRIMARY, rect, width=2, border_radius=Theme.CARD_RADIUS)

        # Draw Card Contents
        if show_text and width > 120:
            # Side Badge
            badge_str = "MẶT TRƯỚC: TỪ VỰNG" if side_now == 0 else "MẶT SAU: Ý NGHĨA"
            badge_col = Theme.PRIMARY_HOVER if side_now == 0 else Theme.SUCCESS
            badge_surf = self.hint_font.render(badge_str, True, badge_col)
            surface.blit(badge_surf, badge_surf.get_rect(center=(rect.centerx, rect.top + 35)))

            if side_now == 0:
                # Word
                w_surf = self.card_font.render(self.card.word, True, Theme.TEXT)
                surface.blit(w_surf, w_surf.get_rect(center=(rect.centerx, rect.centery - 25)))

                # Phonetic
                if getattr(self.card, "phonetic", None):
                    p_surf = self.phonetic_font.render(f"/{self.card.phonetic}/", True, Theme.ACCENT)
                    surface.blit(p_surf, p_surf.get_rect(center=(rect.centerx, rect.centery + 35)))

                # Flip hint
                h_surf = self.hint_font.render("💡 Bấm chuột vào thẻ hoặc gõ SPACE để lật mặt", True, Theme.TEXT_MUTED)
                surface.blit(h_surf, h_surf.get_rect(center=(rect.centerx, rect.bottom - 35)))
            else:
                # Meaning
                m_surf = self.card_font.render(self.card.meaning, True, Theme.TEXT)
                surface.blit(m_surf, m_surf.get_rect(center=(rect.centerx, rect.centery - 30)))

                # Example
                if getattr(self.card, "example", None):
                    ex_surf = self.font.render(f'"{self.card.example}"', True, Theme.TEXT_SECOND)
                    surface.blit(ex_surf, ex_surf.get_rect(center=(rect.centerx, rect.centery + 35)))

                # Flip hint
                h_surf = self.hint_font.render("💡 Bấm chuột hoặc gõ SPACE để quay lại", True, Theme.TEXT_MUTED)
                surface.blit(h_surf, h_surf.get_rect(center=(rect.centerx, rect.bottom - 35)))

    # ======================================================
    # TRẮC NGHIỆM LOGIC (MODE 1)
    # ======================================================
    def create_quiz_question(self):
        # Kiểm tra số lượng từ vựng
        if len(self.card_manager.Cards) < 4 or not self.quiz_cards:
            self.quiz_question = None
            self.quiz_answers = []
            self.quiz_answer_cards = []
            self.quiz_correct_answer = None
            return

        # Kiểm tra chỉ số câu hỏi
        if not 0 <= self.quiz_index < len(self.quiz_cards):
            self.quiz_question = None
            self.quiz_answers = []
            self.quiz_answer_cards = []
            return

        self.index_choice = -1
        self.quiz_type = random.randint(0, 1)

        # Lấy câu hỏi theo chỉ số hiện tại, không tăng chỉ số ở đây
        correct_card = self.quiz_cards[self.quiz_index]

        # Lấy 3 đáp án sai
        wrong_pool = [
            card for card in self.card_manager.Cards
            if card != correct_card
        ]

        wrong_cards = random.sample(wrong_pool, 3)

        # Trộn 1 đáp án đúng và 3 đáp án sai
        answer_cards = wrong_cards + [correct_card]
        random.shuffle(answer_cards)

        self.quiz_correct_answer = correct_card
        self.quiz_answer_cards = answer_cards

        # Tạo nội dung câu hỏi và đáp án
        if self.quiz_type == 0:
            # Cho từ tiếng Anh, chọn nghĩa
            self.quiz_question = correct_card.word
            self.quiz_answers = [
                card.meaning for card in answer_cards
            ]
        else:
            # Cho nghĩa, chọn từ tiếng Anh
            self.quiz_question = correct_card.meaning
            self.quiz_answers = [
                card.word for card in answer_cards
            ]

        # Cập nhật lại 4 nút đáp án
        prefix = ["A", "B", "C", "D"]

        for i, nut in enumerate(self.nut_dap_an_ABCD):
            nut.text = f"{prefix[i]}.  {self.quiz_answers[i]}"
            nut.color = Theme.PANEL_LIGHT
            nut.hover_color = Theme.PANEL_HOVER
            nut.color_text = Theme.TEXT
            nut.color_active = Theme.PRIMARY
            nut.color_line = Theme.BORDER
            nut.disabled = False
            nut.active = False
            
    def start_quiz_round(self):
        self.quiz_cards = self.card_manager.Cards.copy()
        random.shuffle(self.quiz_cards)

        self.quiz_index = 0
        self.correct_count = 0
        self.wrong_count = 0

        self.round_finished = False
        self.show_result = False
        self.index_choice = -1

        if len(self.quiz_cards) >= 4:
            self.create_quiz_question()
        else:
            self.quiz_question = None
            self.quiz_answers = []
            self.quiz_answer_cards = []
            self.quiz_correct_answer = None

    def Retry_quiz(self):
        self.start_quiz_round()

    def Next_quiz(self):
        self.current_mode = 0
        self.show_result = False
        self.round_finished = False
        self.quiz_index = 0

    # ======================================================
    # MATCH GAME LOGIC (MODE 2)
    # ======================================================
    def start_match_round(self, cards=None):
        if cards is None:
            available = [c for c in self.card_manager.Cards
                         if getattr(c, "id", id(c)) not in self.match_used_ids]
            if len(available) < 4:
                self.match_used_ids.clear()
                available = list(self.card_manager.Cards)
            cards = available[:4]

        self.match_pairs = list(cards)
        random.shuffle(self.match_pairs)
        self.match_assignments = {}
        self.match_dragging = None
        self.match_drag_pos = None
        self.match_drag_offset = (0, 0)
        self.match_drag_origin = None
        self.match_checked = False
        self.match_message = ""
        self.match_retry_pairs = []

        # 3 Columns with precise modern geometry
        # Col 1: Word cards (left: 445, width: 235)
        # Col 2: Drop slot cards (center: 725, width: 235)
        # Col 3: Meaning fixed cards (right: 1005, width: 335)
        y0, step, h = 180, 92, 62
        n = len(self.match_pairs)
        self.match_word_rects = [pygame.Rect(445, y0 + i * step, 235, h) for i in range(n)]
        self.match_slot_rects = [pygame.Rect(725, y0 + i * step, 235, h) for i in range(n)]
        self.match_meaning_rects = [pygame.Rect(1005, y0 + i * step, 335, h) for i in range(n)]

        self.match_meaning_order = list(range(n))
        random.shuffle(self.match_meaning_order)

        self.match_check_rect = pygame.Rect(730, 605, 140, 48)
        self.match_retry_rect = pygame.Rect(890, 605, 140, 48)
        self.match_next_rect = pygame.Rect(1050, 605, 140, 48)

    def handle_match_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not self.match_checked:
                self.audio_manager.play("click")
                # 1. Grab from Column 1 (unassigned word cards)
                for i, rect in enumerate(self.match_word_rects):
                    if i not in self.match_assignments and rect.collidepoint(event.pos):
                        self.match_dragging = i
                        self.match_drag_pos = event.pos
                        self.match_drag_offset = (event.pos[0] - rect.x, event.pos[1] - rect.y)
                        self.match_drag_origin = ("left", None)
                        self.match_message = ""
                        return

                # 2. Grab from Column 2 (already assigned cards in slot to rearrange)
                assigned_to = {slot: w for w, slot in self.match_assignments.items()}
                for row, rect in enumerate(self.match_slot_rects):
                    if row in assigned_to and rect.collidepoint(event.pos):
                        word_i = assigned_to[row]
                        self.match_dragging = word_i
                        self.match_drag_pos = event.pos
                        self.match_drag_offset = (event.pos[0] - rect.x, event.pos[1] - rect.y)
                        self.match_drag_origin = ("slot", row)
                        self.match_message = ""
                        return

            # Check Button
            if self.match_check_rect.collidepoint(event.pos) and not self.match_checked:
                self.audio_manager.play("click")
                if len(self.match_assignments) != len(self.match_pairs):
                    self.match_message = "Vui lòng ghép đủ các cặp trước khi kiểm tra!"
                else:
                    self.match_checked = True
                    self.match_retry_pairs = []
                    for word_i, slot_row in self.match_assignments.items():
                        meaning_card_i = self.match_meaning_order[slot_row]
                        if self.match_pairs[word_i] != self.match_pairs[meaning_card_i]:
                            self.match_retry_pairs.append(self.match_pairs[word_i])
                    correct = len(self.match_pairs) - len(self.match_retry_pairs)
                    if correct == len(self.match_pairs):
                        self.match_message = " Xuất sắc! Tất cả các cặp từ đều chính xác!"
                    else:
                        self.match_message = f"Hoàn thành! Bạn đã ghép đúng {correct}/{len(self.match_pairs)} cặp."
                return

            # Retry Button
            if self.match_checked and self.match_retry_rect.collidepoint(event.pos):
                self.audio_manager.play("click")
                if self.match_retry_pairs:
                    self.start_match_round(self.match_retry_pairs)
                else:
                    self.match_message = "Tất cả các cặp đều đúng! Hãy bấm Tiếp Theo."
                return

            # Next Button
            if self.match_checked and self.match_next_rect.collidepoint(event.pos):
                self.audio_manager.play("click")
                for card in self.match_pairs:
                    self.match_used_ids.add(getattr(card, "id", id(card)))
                self.start_match_round()
                return

        elif event.type == pygame.MOUSEMOTION and self.match_dragging is not None:
            self.match_drag_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.match_dragging is not None:
                word_i = self.match_dragging
                target_slot = next((row for row, rect in enumerate(self.match_slot_rects)
                                    if rect.collidepoint(event.pos)), None)
                dropped_in_left = any(rect.collidepoint(event.pos) for rect in self.match_word_rects)

                if target_slot is not None:
                    # Dropped into Column 2 (Drop slot)
                    old_word = next((w for w, slot in self.match_assignments.items()
                                     if slot == target_slot and w != word_i), None)
                    prev_slot = self.match_assignments.get(word_i)

                    if old_word is not None:
                        # Swap or replace
                        if prev_slot is not None:
                            self.match_assignments[old_word] = prev_slot
                        else:
                            self.match_assignments.pop(old_word, None)
                    self.match_assignments[word_i] = target_slot
                    self.match_message = ""

                elif dropped_in_left:
                    # Dropped back into Column 1 -> unassign
                    self.match_assignments.pop(word_i, None)
                    self.match_message = ""

                # Reset drag state
                self.match_dragging = None
                self.match_drag_pos = None
                self.match_drag_origin = None

    def draw_match(self, screen):
        # Header for Match
        title = self.title_font.render("Ghép Thẻ Từ Vựng (Match)", True, Theme.TEXT)
        screen.blit(title, (445, 65))
        sub = self.hint_font.render("Kéo thẻ từ Cột 1 hoặc Ô ghép thả sang ô tương ứng để nối với nghĩa.", True, Theme.TEXT_SECOND)
        screen.blit(sub, (445, 105))

        if len(self.card_manager.Cards) < 4 and not self.match_pairs:
            msg = self.font.render("Cần ít nhất 4 từ vựng trong bộ thẻ để chơi Ghép Thẻ.", True, Theme.TEXT_SECOND)
            screen.blit(msg, msg.get_rect(center=self.content_rect.center))
            return
        if not self.match_pairs:
            msg = self.font.render("Bộ từ vựng này đang trống.", True, Theme.TEXT_SECOND)
            screen.blit(msg, msg.get_rect(center=self.content_rect.center))
            return

        assigned_to = {slot: word_i for word_i, slot in self.match_assignments.items()}
        mouse_pos = pygame.mouse.get_pos()

        # ------------------------------------------------------
        # CỘT 1: THẺ TỪ CÓ THỂ KÉO (Chỉ hiện khi chưa ghép và không đang kéo)
        # ------------------------------------------------------
        for i, card in enumerate(self.match_pairs):
            rect = self.match_word_rects[i]
            # THẺ LÀ ĐỐI TƯỢNG DUY NHẤT: Nếu đã ghép hoặc đang kéo thì ẩn ở cột 1
            if i in self.match_assignments or i == self.match_dragging:
                # Vẽ placeholder rỗng mờ
                pygame.draw.rect(screen, Theme.PANEL, rect, border_radius=Theme.BUTTON_RADIUS)
                pygame.draw.rect(screen, Theme.BORDER, rect, width=1, border_radius=Theme.BUTTON_RADIUS)
                continue

            hover = rect.collidepoint(mouse_pos) and self.match_dragging is None and not self.match_checked
            bg_color = Theme.CARD_HOVER if hover else Theme.CARD
            border_col = Theme.PRIMARY if hover else Theme.BORDER

            shadow = rect.move(0, 3)
            pygame.draw.rect(screen, Theme.SHADOW, shadow, border_radius=Theme.BUTTON_RADIUS)
            pygame.draw.rect(screen, bg_color, rect, border_radius=Theme.BUTTON_RADIUS)
            pygame.draw.rect(screen, border_col, rect, width=1, border_radius=Theme.BUTTON_RADIUS)

            txt = self.font_bold.render(card.word, True, Theme.TEXT)
            screen.blit(txt, txt.get_rect(center=rect.center))

        # ------------------------------------------------------
        # CỘT 2: VÙNG GHÉP (SLOT)
        # ------------------------------------------------------
        for row, rect in enumerate(self.match_slot_rects):
            word_i = assigned_to.get(row)
            is_hover_drop = (
                self.match_dragging is not None and
                rect.collidepoint(mouse_pos) and
                not self.match_checked
            )

            # Phân biệt kết quả sau khi Check
            if self.match_checked:
                meaning_card_i = self.match_meaning_order[row]
                is_correct = (word_i is not None and self.match_pairs[word_i] == self.match_pairs[meaning_card_i])
                bg_col = Theme.ANSWER_CORRECT if is_correct else Theme.ANSWER_WRONG
                border_col = Theme.ANSWER_CORRECT if is_correct else Theme.ANSWER_WRONG
            elif is_hover_drop:
                bg_col = Theme.PANEL_HOVER
                border_col = Theme.PRIMARY
            elif word_i is not None:
                bg_col = Theme.CARD
                border_col = Theme.PRIMARY
            else:
                bg_col = Theme.PANEL_LIGHT
                border_col = Theme.BORDER

            # Draw Slot Rect
            pygame.draw.rect(screen, bg_col, rect, border_radius=Theme.BUTTON_RADIUS)
            border_w = 2 if (is_hover_drop or word_i is not None or self.match_checked) else 1
            pygame.draw.rect(screen, border_col, rect, width=border_w, border_radius=Theme.BUTTON_RADIUS)

            # Draw arrow pointing from Slot to Meaning
            arrow_surf = self.hint_font.render("→", True, Theme.TEXT_MUTED)
            screen.blit(arrow_surf, (rect.right + 18, rect.centery - 7))

            # Draw word inside slot (if assigned and not dragging)
            if word_i is not None and word_i != self.match_dragging:
                txt = self.font_bold.render(self.match_pairs[word_i].word, True, Theme.TEXT)
                screen.blit(txt, txt.get_rect(center=rect.center))

        # ------------------------------------------------------
        # CỘT 3: NGHĨA CỐ ĐỊNH
        # ------------------------------------------------------
        for row, meaning_i in enumerate(self.match_meaning_order):
            rect = self.match_meaning_rects[row]
            if self.match_checked:
                word_i = assigned_to.get(row)
                is_correct = (word_i is not None and self.match_pairs[word_i] == self.match_pairs[meaning_i])
                bg_col = Theme.ANSWER_CORRECT if is_correct else Theme.ANSWER_WRONG
                border_col = Theme.ANSWER_CORRECT if is_correct else Theme.ANSWER_WRONG
            else:
                bg_col = Theme.CARD
                border_col = Theme.BORDER

            shadow = rect.move(0, 3)
            pygame.draw.rect(screen, Theme.SHADOW, shadow, border_radius=Theme.BUTTON_RADIUS)
            pygame.draw.rect(screen, bg_col, rect, border_radius=Theme.BUTTON_RADIUS)
            pygame.draw.rect(screen, border_col, rect, width=1, border_radius=Theme.BUTTON_RADIUS)

            meaning = self.match_pairs[meaning_i].meaning
            m_surf = self.small1_font.render(meaning, True, Theme.TEXT)
            # Clip if too long
            if m_surf.get_width() > rect.width - 24:
                short_m = meaning
                while short_m and self.small1_font.size(short_m + "…")[0] > rect.width - 24:
                    short_m = short_m[:-1]
                m_surf = self.small1_font.render(short_m + "…", True, Theme.TEXT)
            screen.blit(m_surf, m_surf.get_rect(center=rect.center))

        # ------------------------------------------------------
        # THẺ ĐANG KÉO (Đi theo con trỏ chuột mượt mà)
        # ------------------------------------------------------
        if self.match_dragging is not None and self.match_drag_pos is not None:
            card = self.match_pairs[self.match_dragging]
            orig_rect = self.match_word_rects[self.match_dragging]
            drag_x = self.match_drag_pos[0] - self.match_drag_offset[0]
            drag_y = self.match_drag_pos[1] - self.match_drag_offset[1]
            drag_rect = pygame.Rect(drag_x, drag_y, orig_rect.width, orig_rect.height)

            # Soft drop shadow
            shadow = drag_rect.move(5, 7)
            shadow_surf = pygame.Surface(shadow.size, pygame.SRCALPHA)
            pygame.draw.rect(shadow_surf, (0, 0, 0, 110), shadow_surf.get_rect(), border_radius=Theme.BUTTON_RADIUS)
            screen.blit(shadow_surf, shadow.topleft)

            # Elevated card body
            pygame.draw.rect(screen, Theme.BUTTON_HOVER, drag_rect, border_radius=Theme.BUTTON_RADIUS)
            pygame.draw.rect(screen, Theme.PRIMARY, drag_rect, width=2, border_radius=Theme.BUTTON_RADIUS)
            txt = self.font_bold.render(card.word, True, Theme.TEXT)
            screen.blit(txt, txt.get_rect(center=drag_rect.center))

        # ------------------------------------------------------
        # ACTION BUTTONS & FEEDBACK MESSAGE
        # ------------------------------------------------------
        if not self.match_checked:
            all_filled = len(self.match_assignments) == len(self.match_pairs)
            self.draw_custom_button(screen, self.match_check_rect, "Kiểm Tra", Theme.PRIMARY if all_filled else Theme.BUTTON)
        else:
            if self.match_retry_pairs:
                self.draw_custom_button(screen, self.match_retry_rect, "Luyện Lại", Theme.BUTTON)
            self.draw_custom_button(screen, self.match_next_rect, "Tiếp Theo", Theme.PRIMARY)

        if self.match_message:
            msg_color = Theme.SUCCESS if "🎉" in self.match_message else Theme.TEXT_SECOND
            msg = self.font_bold.render(self.match_message, True, msg_color)
            screen.blit(msg, msg.get_rect(center=(890, 560)))

    def draw_custom_button(self, screen, rect, text, bg_color):
        mouse_pos = pygame.mouse.get_pos()
        hover = rect.collidepoint(mouse_pos)
        color = Theme.PRIMARY_HOVER if (hover and bg_color == Theme.PRIMARY) else (Theme.BUTTON_HOVER if hover else bg_color)
        shadow = rect.move(0, 3)
        pygame.draw.rect(screen, Theme.SHADOW, shadow, border_radius=Theme.BUTTON_RADIUS)
        pygame.draw.rect(screen, color, rect, border_radius=Theme.BUTTON_RADIUS)
        pygame.draw.rect(screen, Theme.PRIMARY if hover else Theme.BORDER, rect, width=1, border_radius=Theme.BUTTON_RADIUS)
        txt = self.font_bold.render(text, True, Theme.TEXT)
        screen.blit(txt, txt.get_rect(center=rect.center))

    # ======================================================
    # TỰ LUẬN LOGIC (MODE 3)
    # ======================================================
    def check_written_answer(self):
        if not self.written_cards or self.written_checked:
            return
        current_card = self.written_cards[self.written_index]
        user_ans = self.written_box.user_text.strip().lower()
        # Cho phép đúng nếu khớp với meaning hoặc word (bỏ khoảng trắng thừa)
        correct_meaning = current_card.meaning.strip().lower()
        correct_word = current_card.word.strip().lower()

        if user_ans == correct_meaning or user_ans == correct_word:
            self.written_is_correct = True
            self.correct_count += 1
        else:
            self.written_is_correct = False
            self.wrong_count += 1

        self.written_checked = True

    def next_written_question(self):
        self.written_index += 1
        self.written_checked = False
        self.written_box.clear()
        self.written_box.active = True
        if self.written_index >= len(self.written_cards):
            self.round_finished = True
            self.show_result = False

    def draw_written(self, screen):
        title = self.title_font.render("Luyện Tập Tự Luận", True, Theme.TEXT)
        screen.blit(title, (445, 65))
        sub = self.hint_font.render("Nhìn từ vựng và tự gõ nghĩa tiếng Việt (hoặc ngược lại) để nhớ mặt chữ.", True, Theme.TEXT_SECOND)
        screen.blit(sub, (445, 105))

        if not self.written_cards:
            msg = self.font.render("Bộ từ vựng này đang trống.", True, Theme.TEXT_SECOND)
            screen.blit(msg, msg.get_rect(center=self.content_rect.center))
            return

        current_card = self.written_cards[self.written_index]

        # Progress bar
        total = len(self.written_cards)
        prog_str = f"Câu {self.written_index + 1} / {total}"
        prog_surf = self.font_bold.render(prog_str, True, Theme.PRIMARY_HOVER)
        screen.blit(prog_surf, (460, 150))

        bar_rect = pygame.Rect(460, 180, 860, 6)
        pygame.draw.rect(screen, Theme.PANEL_LIGHT, bar_rect, border_radius=3)
        fill_w = int(860 * ((self.written_index + 1) / total))
        if fill_w > 0:
            fill_rect = pygame.Rect(460, 180, fill_w, 6)
            pygame.draw.rect(screen, Theme.PRIMARY, fill_rect, border_radius=3)

        # Question Card Box
        q_box = pygame.Rect(460, 210, 860, 120)
        pygame.draw.rect(screen, Theme.CARD, q_box, border_radius=Theme.CARD_RADIUS)
        pygame.draw.rect(screen, Theme.BORDER_LIGHT, q_box, width=1, border_radius=Theme.CARD_RADIUS)

        w_surf = self.card_font.render(current_card.word, True, Theme.TEXT)
        screen.blit(w_surf, w_surf.get_rect(center=q_box.center))

        # Textbox and Action button
        self.written_box.draw(screen)
        if not self.written_checked:
            self.written_check_btn.draw(screen)
        else:
            self.written_next_btn.draw(screen)

        # Feedback area
        if self.written_checked:
            fb_rect = pygame.Rect(460, 440, 860, 100)
            fb_color = Theme.ANSWER_CORRECT if self.written_is_correct else Theme.ANSWER_WRONG
            pygame.draw.rect(screen, Theme.PANEL, fb_rect, border_radius=12)
            pygame.draw.rect(screen, fb_color, fb_rect, width=2, border_radius=12)

            if self.written_is_correct:
                res_txt = self.title_font.render("✓ CHÍNH XÁC! Bạn đã trả lời đúng.", True, Theme.SUCCESS)
                screen.blit(res_txt, (490, 470))
            else:
                res_txt = self.title_font.render("✗ CHƯA ĐÚNG! Đáp án chính xác là:", True, Theme.ERROR)
                screen.blit(res_txt, (490, 458))
                ans_txt = self.font_bold.render(f"Nghĩa: {current_card.meaning}", True, Theme.TEXT)
                screen.blit(ans_txt, (490, 495))

    # ======================================================
    # HANDLE EVENT
    # ======================================================
    def handle_event(self, event):
        # 1. Result dialog interactions
        if self.show_result:
            if self.retry_button.handle_event(event) == "retry":
                self.audio_manager.play("click")
                self.Retry_quiz()
            if self.next_button_result.handle_event(event) == "next":
                self.audio_manager.play("click")
                self.Next_quiz()
            return None

        # 2. Round finished button
        if self.round_finished:
            if self.result_button.handle_event(event) == "show_result":
                self.audio_manager.play("click")
                self.show_result = True
            return None

        # 3. Sidebar buttons (Mode switching & Back)
        for nut in self.nut_in_quiz_scr:
            result = nut.handle_event(event)
            if result == "menu":
                self.audio_manager.play("click")
                return result
            elif result == "FC":
                self.audio_manager.play("click")
                self.current_mode = 0
            elif result == "TN":
                self.audio_manager.play("click")

                if self.current_mode != 1:
                    self.current_mode = 1
                    self.start_quiz_round()
            elif result == "match":
                self.audio_manager.play("click")
                self.current_mode = 2
            elif result == "TL":
                self.audio_manager.play("click")
                self.current_mode = 3

        # 4. Deck list click
        if event.type == pygame.MOUSEWHEEL:
            mouse_pos = pygame.mouse.get_pos()
            if self.scroll_list.collidepoint(mouse_pos):
                self.y_scroll_list -= event.y * 22
                max_scroll = max(0, len(self.list_manager.List_Managers) * 50 - 200)
                self.y_scroll_list = max(0, min(self.y_scroll_list, max_scroll))

        for nut in self.nut_list_card:
            result = nut.handle_event(event, self.y_scroll_list)
            if result is not None and result != "out_box":
                self.audio_manager.play("click")
                if event.button == 1 or event.button == 3:
                    for lm in self.list_manager.List_Managers:
                        if lm.id == result:
                            self.card_manager = lm
                            self.shuffle_cards()
                            self.side = 0
                            self.progress = 0.0
                            self.flipping = False
                            self.update_list()
                            self.match_used_ids.clear()
                            self.start_match_round()
                            break

        # 5. Handle current mode events
        if self.current_mode == 0:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.card_rect.collidepoint(event.pos):
                    self.start_flip()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.start_flip()

            for nut in self.nut_chuyen_card:
                res = nut.handle_event(event)
                if res == "previous":
                    self.audio_manager.play("click")
                    self.previous_card()
                elif res == "next":
                    self.audio_manager.play("click")
                    self.next_card()

        elif self.current_mode == 1:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.index_choice != -1 and not self.round_finished:
                    self.quiz_index += 1

                    if self.quiz_index < len(self.quiz_cards):
                        self.create_quiz_question()
                    else:
                        self.round_finished = True
                        self.show_result = False

            for i, nut in enumerate(self.nut_dap_an_ABCD):
                result = nut.handle_event(event)
                if result == f"answer_{i}" and self.index_choice == -1:
                    
                    selected_card = self.quiz_answer_cards[i]
                    if selected_card == self.quiz_correct_answer:
                        self.audio_manager.play("correct")
                        self.correct_count += 1

                        nut.color = Theme.ANSWER_CORRECT
                        nut.hover_color = Theme.ANSWER_CORRECT_HOVER
                        nut.color_active = Theme.ANSWER_CORRECT
                        nut.color_line = Theme.ANSWER_CORRECT

                    else:
                        self.audio_manager.play("wrong")
                        self.wrong_count += 1

                        nut.color = Theme.ANSWER_WRONG
                        nut.hover_color = Theme.ANSWER_WRONG_HOVER
                        nut.color_active = Theme.ANSWER_WRONG
                        nut.color_line = Theme.ANSWER_WRONG

                        # Tô xanh lá cho đáp án đúng
                        for j, c in enumerate(self.quiz_answer_cards):
                            if c == self.quiz_correct_answer:
                                correct_btn = self.nut_dap_an_ABCD[j]

                                correct_btn.color = Theme.ANSWER_CORRECT
                                correct_btn.hover_color = Theme.ANSWER_CORRECT_HOVER
                                correct_btn.color_active = Theme.ANSWER_CORRECT
                                correct_btn.color_line = Theme.ANSWER_CORRECT

                    self.index_choice = i
                    if self.quiz_index == len(self.quiz_cards) - 1:
                        self.round_finished = True
                        self.show_result = False

                    break

            if self.index_choice != -1:
                for i, nut in enumerate(self.nut_dap_an_ABCD):
                    if i != self.index_choice and self.quiz_answer_cards[i] != self.quiz_correct_answer:
                        nut.disabled = True
                        nut.color = Theme.DISABLED
                        nut.line = Theme.DISABLED_BORDER
                        nut.color_text = Theme.DISABLED_TEXT

        elif self.current_mode == 2:
            self.handle_match_event(event)

        elif self.current_mode == 3:
            box_res = self.written_box.handle_event(event)
            if box_res is not None:
                self.audio_manager.play("click")
                self.check_written_answer()

            if not self.written_checked:
                if self.written_check_btn.handle_event(event) == "written_check":
                    self.audio_manager.play("click")
                    self.check_written_answer()
            else:
                if self.written_next_btn.handle_event(event) == "written_next":
                    self.audio_manager.play("click")
                    self.next_written_question()

        return None

    # ======================================================
    # DRAW
    # ======================================================
    def draw(self, screen):
        screen.fill(Theme.BG)

        # --------------------------------------------------
        # SIDEBAR
        # --------------------------------------------------
        shadow_sb = self.sidebar_rect.move(0, 4)
        pygame.draw.rect(screen, Theme.SHADOW, shadow_sb, border_radius=Theme.CARD_RADIUS)
        pygame.draw.rect(screen, Theme.PANEL, self.sidebar_rect, border_radius=Theme.CARD_RADIUS)
        pygame.draw.rect(screen, Theme.BORDER, self.sidebar_rect, width=1, border_radius=Theme.CARD_RADIUS)

        title = self.title_font.render("Luyện Tập", True, Theme.TEXT)
        screen.blit(title, (50, 95))

        

        # Mode buttons active state
        self.flash_card.active = (self.current_mode == 0)
        self.trac_nghiem.active = (self.current_mode == 1)
        self.Match.active = (self.current_mode == 2)
        self.tu_luan.active = (self.current_mode == 3)
        self.back_button.active = False

        for nut in self.nut_in_quiz_scr:
            nut.draw(screen)

        # Deck List in sidebar
        deck_title = self.section_font.render("BỘ TỪ VỰNG", True, Theme.TEXT)
        screen.blit(deck_title, (50, 430))

        list_panel = self.scroll_list.inflate(8, 8)
        pygame.draw.rect(screen, Theme.PANEL_LIGHT, list_panel, border_radius=12)
        pygame.draw.rect(screen, Theme.BORDER, list_panel, width=1, border_radius=12)

        screen.set_clip(self.scroll_list)
        for nut in self.nut_list_card:
            nut.active = (nut.id == self.card_manager.id)
            tmp = nut.rect.y
            nut.rect.y = nut.rect.y - self.y_scroll_list
            nut.draw(screen)
            nut.rect.y = tmp
        screen.set_clip(None)

        # --------------------------------------------------
        # MAIN CONTENT PANEL
        # --------------------------------------------------
        shadow_c = self.content_rect.move(0, 4)
        pygame.draw.rect(screen, Theme.SHADOW, shadow_c, border_radius=Theme.CARD_RADIUS)
        pygame.draw.rect(screen, Theme.PANEL, self.content_rect, border_radius=Theme.CARD_RADIUS)
        pygame.draw.rect(screen, Theme.BORDER, self.content_rect, width=1, border_radius=Theme.CARD_RADIUS)

        # Render Active Mode
        if not self.show_result:
            if self.current_mode == 0:
                # Mode 0: Flashcard
                h_title = self.title_font.render("Flash Card", True, Theme.TEXT)
                screen.blit(h_title, (445, 65))
                h_sub = self.hint_font.render("Học từ vựng bằng phương pháp thẻ ghi nhớ 3D lặp lại ngắt quãng.", True, Theme.TEXT_SECOND)
                screen.blit(h_sub, (445, 105))

                # Counter badge
                if self.cards:
                    c_badge = self.font_bold.render(f"Thẻ {self.card_index + 1} / {len(self.cards)}", True, Theme.PRIMARY_HOVER)
                    screen.blit(c_badge, c_badge.get_rect(midright=(1340, 80)))

                self.draw_card(screen)

                for nut in self.nut_chuyen_card:
                    nut.draw(screen)
                    nut.active = False

            elif self.current_mode == 1:
                # Mode 1: Trắc nghiệm
                h_title = self.title_font.render("Trắc Nghiệm 4 Đáp Án", True, Theme.TEXT)
                screen.blit(h_title, (445, 65))
                h_sub = self.hint_font.render("Chọn câu trả lời chính xác nhất để kiểm tra khả năng phản xạ từ vựng.", True, Theme.TEXT_SECOND)
                screen.blit(h_sub, (445, 105))

                if len(self.card_manager.Cards) < 4:
                    empty_msg = self.font.render("Cần ít nhất 4 từ vựng trong bộ thẻ để làm bài trắc nghiệm.", True, Theme.TEXT_SECOND)
                    screen.blit(empty_msg, empty_msg.get_rect(center=self.content_rect.center))
                else:
                    # Progress counter
                    total = len(self.quiz_cards)
                    q_str = f"Câu hỏi {self.quiz_index + 1} / {total}"
                    q_badge = self.font_bold.render(q_str, True, Theme.PRIMARY_HOVER)
                    screen.blit(q_badge, (460, 140))

                    # Question Card
                    pygame.draw.rect(screen, Theme.CARD, self.quiz_question_rect, border_radius=Theme.CARD_RADIUS)
                    pygame.draw.rect(screen, Theme.BORDER_LIGHT, self.quiz_question_rect, width=1, border_radius=Theme.CARD_RADIUS)

                    q_txt = self.card_font.render(self.quiz_question if self.quiz_question else "", True, Theme.TEXT)
                    screen.blit(q_txt, q_txt.get_rect(center=self.quiz_question_rect.center))

                    # 4 Option buttons
                    for nut in self.nut_dap_an_ABCD:
                        nut.draw(screen)

                    # Next question hint / button
                    if self.index_choice != -1 and not self.round_finished:
                        hint = self.hint_font.render(" Gõ SPACE để chuyển sang câu tiếp theo", True, Theme.PRIMARY_HOVER)
                        screen.blit(hint, hint.get_rect(center=(890, 560)))

                    if self.round_finished:
                        self.result_button.draw(screen)

            elif self.current_mode == 2:
                # Mode 2: Match Game
                self.draw_match(screen)

            elif self.current_mode == 3:
                # Mode 3: Tự luận
                self.draw_written(screen)

        else:
            # --------------------------------------------------
            # KẾT QUẢ LUYỆN TẬP (SUMMARY CARD)
            # --------------------------------------------------
            box_w, box_h = 600, 480
            res_box = pygame.Rect(self.content_rect.centerx - box_w // 2, 80, box_w, box_h)
            pygame.draw.rect(screen, Theme.PANEL_LIGHT, res_box, border_radius=Theme.CARD_RADIUS)
            pygame.draw.rect(screen, Theme.BORDER_LIGHT, res_box, width=1, border_radius=Theme.CARD_RADIUS)

            r_title = self.title_font.render("KẾT QUẢ LUYỆN TẬP", True, Theme.TEXT)
            screen.blit(r_title, r_title.get_rect(center=(res_box.centerx, res_box.top + 45)))

            r_deck = self.font.render(f"Bộ thẻ: {self.card_manager.name}", True, Theme.TEXT_SECOND)
            screen.blit(r_deck, r_deck.get_rect(center=(res_box.centerx, res_box.top + 80)))

            total = len(self.quiz_cards) if self.current_mode == 1 else len(self.written_cards)
            accuracy = (self.correct_count / total * 100) if total > 0 else 0.0

            stats = [
                ("Tổng số câu đã làm", total, Theme.TEXT),
                ("Số câu trả lời đúng", self.correct_count, Theme.SUCCESS),
                ("Số câu trả lời sai", self.wrong_count, Theme.ERROR),
                ("Độ chính xác đạt được", f"{accuracy:.1f}%", Theme.PRIMARY_HOVER)
            ]

            y_stat = res_box.top + 130
            for label, val, val_col in stats:
                l_surf = self.font.render(label, True, Theme.TEXT_SECOND)
                v_surf = self.title_font.render(str(val), True, val_col)
                screen.blit(l_surf, (res_box.left + 50, y_stat))
                screen.blit(v_surf, v_surf.get_rect(midright=(res_box.right - 50, y_stat + 10)))

                # Divider
                pygame.draw.line(screen, Theme.BORDER, (res_box.left + 50, y_stat + 42), (res_box.right - 50, y_stat + 42), 1)
                y_stat += 62

            self.retry_button.rect.centerx = res_box.centerx - 90
            self.retry_button.rect.y = res_box.bottom - 70
            self.next_button_result.rect.centerx = res_box.centerx + 90
            self.next_button_result.rect.y = res_box.bottom - 70

            self.retry_button.draw(screen)
            self.next_button_result.draw(screen)