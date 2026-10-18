import os
import pygame
from UI import BButton, TextBox, Label
from UI.Theme import Theme
from .Base_Screen import base
from Data import FlashCard, FlashCardManager, CardList


class LearnScreen(base):
    def __init__(self, list_card_manager,audio_manager):
        # Fonts
        try:
            self.title_font = pygame.font.SysFont(Theme.FONT, 20, bold=True)
            self.font = pygame.font.SysFont(Theme.FONT, 18)
            self.bold_font = pygame.font.SysFont(Theme.FONT, 18, bold=True)
            self.small_font = pygame.font.SysFont(Theme.FONT, 15)
            self.hint_font = pygame.font.SysFont(Theme.FONT, 14)
        except Exception:
            current_dir = os.path.dirname(__file__)
            font_path = os.path.join(current_dir, "arial.ttf")
            if os.path.exists(font_path):
                self.title_font = pygame.font.Font(font_path, 20)
                self.font = pygame.font.Font(font_path, 18)
                self.bold_font = pygame.font.Font(font_path, 18)
                self.small_font = pygame.font.Font(font_path, 15)
                self.hint_font = pygame.font.Font(font_path, 14)
            else:
                self.title_font = pygame.font.SysFont("Arial", 20, bold=True)
                self.font = pygame.font.SysFont("Arial", 18)
                self.bold_font = pygame.font.SysFont("Arial", 18, bold=True)
                self.small_font = pygame.font.SysFont("Arial", 15)
                self.hint_font = pygame.font.SysFont("Arial", 14)


        self.audio_manager = audio_manager
        self.list_manager = list_card_manager
        self.card_manager = list_card_manager.List_Managers[0]

        # 3 Main Panels
        self.panel_input = pygame.Rect(20, 20, 410, 680)
        self.panel_list = pygame.Rect(445, 20, 390, 680)
        self.panel_card = pygame.Rect(850, 20, 530, 680)

        # Inner container panels
        self.list_panel = pygame.Rect(460, 85, 360, 600)
        self.card_panel = pygame.Rect(865, 135, 500, 550)

        # Scroll boundaries
        self.scroll_list = pygame.Rect(460, 85, 360, 600)
        self.scroll_card = pygame.Rect(865, 135, 500, 550)

        self.y_scroll_list = 0
        self.y_scroll_card = 0

        # Textboxes for Input
        self.tbox_list = []

        self.word_box = TextBox.Textbox(
            x=120, y=120, width=290, height=46,
            color=Theme.INPUT, color_text=Theme.TEXT, color_line=Theme.BORDER,
            hover_color=Theme.INPUT_HOVER, max_length=24, size=18,
            placeholder="Nhập từ tiếng Anh..."
        )
        self.meaning_box = TextBox.Textbox(
            x=120, y=176, width=290, height=46,
            color=Theme.INPUT, color_text=Theme.TEXT, color_line=Theme.BORDER,
            hover_color=Theme.INPUT_HOVER, max_length=30, size=18,
            placeholder="Nghĩa tiếng Việt..."
        )
        self.phonetic_box = TextBox.Textbox(
            x=120, y=232, width=290, height=46,
            color=Theme.INPUT, color_text=Theme.TEXT, color_line=Theme.BORDER,
            hover_color=Theme.INPUT_HOVER, max_length=24, size=18,
            placeholder="vd: /ˈæp.əl/..."
        )
        self.example_box = TextBox.Textbox(
            x=120, y=288, width=290, height=46,
            color=Theme.INPUT, color_text=Theme.TEXT, color_line=Theme.BORDER,
            hover_color=Theme.INPUT_HOVER, max_length=45, size=17,
            placeholder="Câu ví dụ minh họa..."
        )
        self.search_box = TextBox.Textbox(
            x=865, y=78, width=320, height=44,
            color=Theme.INPUT, color_text=Theme.TEXT, color_line=Theme.BORDER,
            hover_color=Theme.INPUT_HOVER, max_length=25, size=17,
            placeholder="Tìm kiếm từ hoặc nghĩa..."
        )

        self.tbox_list.append(self.word_box)
        self.tbox_list.append(self.meaning_box)
        self.tbox_list.append(self.phonetic_box)
        self.tbox_list.append(self.example_box)
        self.tbox_list.append(self.search_box)

        # Action Buttons in Learn Screen
        self.nut_in_learn_scr = []

        self.back_button = BButton.Button(
            x=35, y=35, width=80, height=40,
            text="BACK", id="menu",
            color=Theme.BUTTON, color_line=Theme.BORDER, color_text=Theme.TEXT,
            hover_color=Theme.BUTTON_HOVER, color_active=Theme.BUTTON_ACTIVE,
            left=True, right=False, size=16
        )
        self.nut_in_learn_scr.append(self.back_button)

        self.add_button = BButton.Button(
            x=120, y=348, width=190, height=46,
            text="+ Thêm Từ", id="add",
            color=Theme.PRIMARY, color_line=Theme.PRIMARY, color_text=Theme.TEXT,
            hover_color=Theme.PRIMARY_HOVER, color_active=Theme.PRIMARY,
            left=True, right=False, size=17
        )
        self.nut_in_learn_scr.append(self.add_button)

        self.add_list_button = BButton.Button(
            x=685, y=32, width=135, height=40,
            text="+ Tạo Bộ Thẻ", id="add2",
            color=Theme.BUTTON, color_line=Theme.BORDER, color_text=Theme.TEXT,
            hover_color=Theme.BUTTON_HOVER, color_active=Theme.BUTTON_ACTIVE,
            left=True, right=False, size=15
        )
        self.nut_in_learn_scr.append(self.add_list_button)

        self.a_z = BButton.Button(
            x=1195, y=78, width=75, height=44,
            text="A → Z", id="A-Z",
            color=Theme.BUTTON, color_line=Theme.BORDER, color_text=Theme.TEXT,
            hover_color=Theme.BUTTON_HOVER, color_active=Theme.BUTTON_ACTIVE,
            left=True, right=False, size=14
        )
        self.nut_in_learn_scr.append(self.a_z)

        self.z_a = BButton.Button(
            x=1278, y=78, width=75, height=44,
            text="Z → A", id="Z-A",
            color=Theme.BUTTON, color_line=Theme.BORDER, color_text=Theme.TEXT,
            hover_color=Theme.BUTTON_HOVER, color_active=Theme.BUTTON_ACTIVE,
            left=True, right=False, size=14
        )
        self.nut_in_learn_scr.append(self.z_a)

        # Cancel Edit button (visible when editing)
        self.cancel_button = BButton.Button(
            x=320, y=348, width=90, height=46,
            text="Hủy", id="cancel_edit",
            color=Theme.BUTTON, color_line=Theme.BORDER, color_text=Theme.TEXT_SECOND,
            hover_color=Theme.BUTTON_HOVER, color_active=Theme.BUTTON_ACTIVE,
            left=True, right=False, size=15
        )

        # Interactive lists & options
        self.nut_list_card = []
        self.nut_option_list = []
        self.nut_card = []
        self.nut_option_card = []

        # Form Labels
        self.labels = []
        self.lb_word = Label.Label(x=35, y=133, font_size=17, text="Word :")
        self.labels.append(self.lb_word)

        self.lb_meaning = Label.Label(x=35, y=189, font_size=17, text="Meaning :")
        self.labels.append(self.lb_meaning)

        self.lb_phonetic = Label.Label(x=35, y=245, font_size=17, text="Phonetic :")
        self.labels.append(self.lb_phonetic)

        self.lb_example = Label.Label(x=35, y=301, font_size=17, text="Example :")
        self.labels.append(self.lb_example)

        # State flags
        self.adding = False
        self.editing = False
        self.rename = False
        self.selected_id = None
        self.sort = None

        # Feedback toast
        self.toast_msg = ""
        self.toast_color = Theme.SUCCESS
        self.toast_timer = 0.0

    def show_toast(self, message, is_error=False):
        self.toast_msg = message
        self.toast_color = Theme.ERROR if is_error else Theme.SUCCESS
        self.toast_timer = 2.5

    def update(self, dt):
        if self.toast_timer > 0:
            self.toast_timer = max(0.0, self.toast_timer - dt)

        for tb in self.tbox_list:
            tb.update(dt)

        for nut in self.nut_in_learn_scr:
            nut.update()

        if self.editing:
            self.cancel_button.update()

        for nut in self.nut_option_card:
            nut.update(self.y_scroll_card)

        for nut in self.nut_list_card:
            nut.update(self.y_scroll_list)

        for nut in self.nut_option_list:
            nut.update(self.y_scroll_list)

        for nut in self.nut_card:
            nut.update(self.y_scroll_card)

    def update_surface(self):
        for tb in self.tbox_list:
            tb.update_surface()

    def add_card(self):
        if self.editing:
            for card in self.card_manager.Cards:
                if card.id == self.selected_id:
                    card.word = self.word_box.user_text.strip()
                    card.meaning = self.meaning_box.user_text.strip()
                    card.phonetic = self.phonetic_box.user_text.strip()
                    card.example = self.example_box.user_text.strip()

                    for tb in self.tbox_list[:4]:
                        tb.clear()

                    self.update_nut_card()
                    self.selected_id = None
                    self.editing = False
                    self.add_button.text = "+ Thêm Từ"
                    self.show_toast("✓ Đã cập nhật từ vựng!")
                    break
        else:
            word = self.word_box.user_text.strip()
            meaning = self.meaning_box.user_text.strip()
            phonetic = self.phonetic_box.user_text.strip()
            example = self.example_box.user_text.strip()

            if not word or not meaning:
                self.show_toast("Vui lòng nhập cả Từ và Nghĩa!", is_error=True)
                return

            card = FlashCard.FlashCard(word, meaning, phonetic, example)
            self.card_manager.add_card(card)

            for tb in self.tbox_list[:4]:
                tb.clear()

            self.update_nut_card()
            self.show_toast(f"✓ Đã thêm từ '{word}' thành công!")

    def add_list(self):
        t = 1
        while True:
            ok = False
            for lm in self.list_manager.List_Managers:
                if f"New List {t}" == lm.name:
                    t += 1
                    ok = True
                    break
            if not ok:
                break

        tmp = FlashCardManager.FlashCardManager(f"New List {t}")
        self.list_manager.add_manager(tmp)
        self.card_manager = tmp
        self.update_list()
        self.update_nut_card()
        self.show_toast(f"✓ Đã tạo bộ thẻ '{tmp.name}'")

    def update_list(self):
        y = 95
        self.nut_list_card.clear()
        for lm in self.list_manager.List_Managers:
            nut = BButton.Button(
                475, y, 325, 50,
                lm.name, lm.id,
                Theme.PANEL_LIGHT, Theme.BORDER, Theme.TEXT,
                Theme.PANEL_HOVER, Theme.PRIMARY,
                left=True, right=True, size=17
            )
            self.nut_list_card.append(nut)
            y += 62

    def update_card(self, screen):
        y = 145
        if self.sort == "A-Z":
            self.card_manager.Cards.sort(key=lambda c: c.word.lower())
            self.update_nut_card()
            self.nut_in_learn_scr[3].active = True
            self.nut_in_learn_scr[4].active = False
        elif self.sort == "Z-A":
            self.card_manager.Cards.sort(key=lambda c: c.word.lower(), reverse=True)
            self.update_nut_card()
            self.nut_in_learn_scr[3].active = False
            self.nut_in_learn_scr[4].active = True

        text_search = self.search_box.user_text.lower().strip()
        filtered = [
            c for c in self.card_manager.Cards
            if not text_search or text_search in c.word.lower() or text_search in c.meaning.lower()
        ]

        if not filtered:
            if not self.card_manager.Cards:
                empty_title = self.bold_font.render("Bộ từ vựng này đang trống", True, Theme.TEXT_SECOND)
                empty_desc = self.hint_font.render("Hãy nhập thông tin ở khung bên trái và bấm 'Thêm Từ'", True, Theme.TEXT_MUTED)
                screen.blit(empty_title, empty_title.get_rect(center=(self.scroll_card.centerx, 260)))
                screen.blit(empty_desc, empty_desc.get_rect(center=(self.scroll_card.centerx, 290)))
            else:
                empty_srch = self.font.render(f"Không tìm thấy từ khớp với '{text_search}'", True, Theme.TEXT_MUTED)
                screen.blit(empty_srch, empty_srch.get_rect(center=(self.scroll_card.centerx, 260)))
            return

        for card in filtered:
            item_y = y - self.y_scroll_card
            # Draw card item background
            item_rect = pygame.Rect(875, item_y, 475, 48)
            pygame.draw.rect(screen, Theme.PANEL_LIGHT, item_rect, border_radius=8)
            pygame.draw.rect(screen, Theme.BORDER, item_rect, width=1, border_radius=8)

            # Word (bold)
            w_surf = self.bold_font.render(card.word, True, Theme.TEXT)
            screen.blit(w_surf, (890, item_y + 8))

            # Phonetic if exists
            offset_x = 890 + w_surf.get_width() + 10
            if getattr(card, "phonetic", None):
                p_surf = self.small_font.render(f"/{card.phonetic}/", True, Theme.ACCENT)
                screen.blit(p_surf, (offset_x, item_y + 10))
                offset_x += p_surf.get_width() + 10

            # Meaning
            m_surf = self.small_font.render(f"—  {card.meaning}", True, Theme.TEXT_SECOND)
            # Clip if too long
            max_m_w = 1260 - offset_x
            if m_surf.get_width() > max_m_w and max_m_w > 30:
                short_m = card.meaning
                while short_m and self.small_font.size(f"—  {short_m}…")[0] > max_m_w:
                    short_m = short_m[:-1]
                m_surf = self.small_font.render(f"—  {short_m}…", True, Theme.TEXT_SECOND)
            screen.blit(m_surf, (offset_x, item_y + 10))

            y += 56

    def update_nut_card(self):
        y = 145
        self.nut_card.clear()
        text_search = self.search_box.user_text.lower().strip()
        for card in self.card_manager.Cards:
            if not text_search or text_search in card.word.lower() or text_search in card.meaning.lower():
                x_nut = 1315
                y_nut = y + 10
                nut = BButton.Button(
                    x_nut, y_nut, 28, 28,
                    "⋮", card.id,
                    Theme.BUTTON, Theme.BORDER, Theme.TEXT,
                    Theme.BUTTON_HOVER, Theme.BUTTON_ACTIVE,
                    left=True, right=False, size=18
                )
                self.nut_card.append(nut)
                y += 56

    def update_nut_card_option(self, y_nut, card):
        self.nut_option_card.clear()
        # Popup menu with Edit and Delete
        edit = BButton.Button(
            1240, y_nut, 70, 30,
            "Sửa", card.id,
            Theme.BUTTON, Theme.BORDER, Theme.TEXT,
            Theme.PRIMARY, Theme.PRIMARY,
            left=True, right=False, size=14
        )
        delete = BButton.Button(
            1240, y_nut + 34, 70, 30,
            "Xóa", card.id,
            Theme.BUTTON, Theme.BORDER, Theme.TEXT,
            Theme.ERROR, Theme.ERROR,
            left=True, right=False, size=14
        )
        self.nut_option_card.append(edit)
        self.nut_option_card.append(delete)

    def update_nut_list_option(self, y_nut, nut):
        self.nut_option_list.clear()
        rename = BButton.Button(
            680, y_nut, 90, 32,
            "Đổi tên", nut.id,
            Theme.BUTTON, Theme.BORDER, Theme.TEXT,
            Theme.PRIMARY, Theme.PRIMARY,
            left=True, right=False, size=14
        )
        delete = BButton.Button(
            680, y_nut + 36, 90, 32,
            "Xóa bộ", nut.id,
            Theme.BUTTON, Theme.BORDER, Theme.TEXT,
            Theme.ERROR, Theme.ERROR,
            left=True, right=False, size=14
        )
        self.nut_option_list.append(rename)
        self.nut_option_list.append(delete)

    def delete(self, id_del):
        for nut in self.nut_card:
            if nut.id == id_del:
                self.nut_card.remove(nut)
                break
        for card in self.card_manager.Cards:
            if card.id == id_del:
                self.card_manager.remove_card(card)
                self.show_toast(f"Đã xóa từ '{card.word}'")
                break

        self.update_nut_card()
        self.nut_option_card.clear()

    def delete_list(self, id_del):
        if len(self.list_manager.List_Managers) <= 1:
            self.show_toast("Không thể xóa bộ thẻ cuối cùng!", is_error=True)
            return

        for nut in self.nut_list_card:
            if nut.id == id_del:
                self.nut_list_card.remove(nut)
                break

        index = 0
        n = len(self.list_manager.List_Managers)
        for lm in self.list_manager.List_Managers:
            if lm.id == id_del:
                index = self.list_manager.List_Managers.index(lm)
                self.list_manager.remove_manager(lm.id)
                self.show_toast(f"Đã xóa bộ thẻ '{lm.name}'")
                break

        if n - 1 > index and n > 1:
            self.card_manager = self.list_manager.List_Managers[index]
        elif n - 1 == index and n > 1:
            self.card_manager = self.list_manager.List_Managers[index - 1]
        else:
            self.card_manager = self.list_manager.List_Managers[0]

        self.update_list()
        self.update_nut_card()

    def edit(self, id_edit):
        self.editing = True
        self.add_button.text = "Lưu Sửa"
        self.selected_id = id_edit
        for card in self.card_manager.Cards:
            if card.id == id_edit:
                self.word_box.user_text = card.word
                self.meaning_box.user_text = card.meaning
                self.phonetic_box.user_text = card.phonetic
                self.example_box.user_text = card.example
                self.update_surface()
                break
        self.update_nut_card()
        self.nut_option_card.clear()

    def cancel_edit(self):
        self.editing = False
        self.selected_id = None
        self.add_button.text = "+ Thêm Từ"
        for tb in self.tbox_list[:4]:
            tb.clear()

    def Rename(self, id):
        # Chỉ giữ một TextBox đổi tên tại một thời điểm.
        self.tbox_list = self.tbox_list[:5]

        for nut in self.nut_list_card:
            if nut.id == id:
                x, y, width, height = nut.rect
                # nut.rect.y là tọa độ gốc; trừ scroll để khớp vị trí đang hiển thị.
                y -= self.y_scroll_list

                tb = TextBox.Textbox(
                    x + 10, y + 4, width - 20, height - 8,
                    color=Theme.INPUT, color_text=Theme.TEXT,
                    color_line=Theme.PRIMARY, hover_color=Theme.INPUT,
                    max_length=18, size=16
                )
                tb.enter = True
                tb.active = True
                tb.id = id
                tb.user_text = nut.text
                tb.update_surface()
                self.tbox_list.append(tb)
                break

    def Rename2(self, id, new_name):
        new_name_clean = new_name.strip()
        if new_name_clean:
            for lm in self.list_manager.List_Managers:
                if lm.id == id:
                    lm.name = new_name_clean
                    self.show_toast(f"Đã đổi tên thành '{new_name_clean}'")
                    break
        self.update_list()
        if len(self.tbox_list) > 5:
            self.tbox_list.pop()

    def handle_event(self, event):
        # Cuộn danh sách và danh sách từ vựng.
        if event.type == pygame.MOUSEWHEEL:
            mouse_pos = pygame.mouse.get_pos()
            if self.scroll_list.collidepoint(mouse_pos):
                self.y_scroll_list -= event.y * 28
                max_scroll = max(0, len(self.list_manager.List_Managers) * 62 - 580)
                self.y_scroll_list = max(0, min(self.y_scroll_list, max_scroll))

            if self.scroll_card.collidepoint(mouse_pos):
                self.y_scroll_card -= event.y * 28
                max_scroll = max(0, len(self.card_manager.Cards) * 56 - 520)
                self.y_scroll_card = max(0, min(self.y_scroll_card, max_scroll))

        # Xử lý TextBox trước. TextBox đổi tên nằm sau 5 TextBox cố định.
        for tb in list(self.tbox_list):
            clicked = (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and tb.rect.collidepoint(event.pos)
            )

            res = tb.handle_event(event)

            if clicked:
                self.audio_manager.play("click")

            if res is not None:
                if tb in self.tbox_list[5:]:
                    self.Rename2(tb.id, res)
                    return None

        ok = event.type == pygame.MOUSEBUTTONDOWN
        ok2 = event.type == pygame.MOUSEBUTTONDOWN

        # QUAN TRỌNG: xử lý popup bộ thẻ TRƯỚC danh sách bộ thẻ.
        # Nếu xử lý danh sách trước, nút bộ thẻ bên dưới sẽ ăn click popup.
        for nut in list(self.nut_option_list):
            result = nut.handle_event(event, self.y_scroll_list)
            if result is not None and result != "out_box":
                self.audio_manager.play("click")
                ok2 = False

                if nut.text in ["delete", "Xóa bộ"]:
                    list_id = nut.id
                    self.nut_option_list.clear()
                    self.delete_list(list_id)
                    return None

                elif nut.text in ["rename", "Đổi tên"]:
                    list_id = nut.id
                    self.nut_option_list.clear()
                    self.Rename(list_id)
                    return None

                # Đã bấm vào popup: không cho cùng click đi xuống nút phía dưới.
                return None

        # Tương tác với danh sách bộ thẻ.
        for nut in self.nut_list_card:
            result = nut.handle_event(event, self.y_scroll_list)
            if result is not None and result != "out_box":
                self.audio_manager.play("click")
                ok2 = False

                if event.button in (1, 3):
                    for lm in self.list_manager.List_Managers:
                        if lm.id == result:
                            self.nut_option_list.clear()
                            self.nut_card.clear()
                            self.card_manager = lm
                            self.update_list()
                            self.update_nut_card()
                            for nut1 in self.nut_list_card:
                                nut1.active = False
                            nut.active = True
                            break

                if event.button == 3:
                    for nut1 in self.nut_list_card:
                        nut1.active = False
                    nut.active = True
                    self.update_nut_list_option(nut.y, nut)
                break

        # Tương tác với các nút tùy chọn của từng thẻ từ vựng.
        for nut in self.nut_card:
            result = nut.handle_event(event, self.y_scroll_card)
            if result is not None and result != "out_box":
                self.audio_manager.play("click")
                ok = False
                for nut1 in self.nut_card:
                    nut1.active = False
                nut.active = True
                self.selected_id = nut.id
                self.update_nut_card_option(nut.y, nut)
                break

        # Popup Sửa/Xóa từ vựng.
        for nut in list(self.nut_option_card):
            result = nut.handle_event(event, self.y_scroll_card)
            if result is not None and result != "out_box":
                self.audio_manager.play("click")
                ok = False
                if nut.text in ["Delete", "Xóa"]:
                    self.delete(nut.id)
                elif nut.text in ["Edit", "Sửa"]:
                    self.edit(nut.id)
                return None

        if ok:
            if not self.editing:
                self.selected_id = None
            self.nut_option_card.clear()
            for nut1 in self.nut_card:
                nut1.active = False

        if ok2:
            self.nut_option_list.clear()
            for nut1 in self.nut_list_card:
                nut1.active = False

        # Nút hủy sửa.
        if self.editing:
            cancel_res = self.cancel_button.handle_event(event)
            if cancel_res == "cancel_edit":
                self.audio_manager.play("click")
                self.cancel_edit()

        # Các nút cố định của màn Learn.
        for nut in self.nut_in_learn_scr:
            result = nut.handle_event(event)
            if result == "menu":
                self.audio_manager.play("click")
                return result
            elif result == "add":
                self.audio_manager.play("click")
                self.add_card()
            elif result in ("Z-A", "A-Z"):
                self.audio_manager.play("click")
                self.sort = result
            elif result == "add2":
                self.audio_manager.play("click")
                self.add_list()

        return None

    def draw(self, screen):
        screen.fill(Theme.BG)

        # --------------------------------------------------
        # PANEL 1: THÊM & SỬA TỪ VỰNG
        # --------------------------------------------------
        shadow1 = self.panel_input.move(0, 4)
        pygame.draw.rect(screen, Theme.SHADOW, shadow1, border_radius=Theme.CARD_RADIUS)
        pygame.draw.rect(screen, Theme.PANEL, self.panel_input, border_radius=Theme.CARD_RADIUS)
        pygame.draw.rect(screen, Theme.BORDER, self.panel_input, width=1, border_radius=Theme.CARD_RADIUS)

        title_text = "CHỈNH SỬA TỪ VỰNG" if self.editing else "THÊM TỪ VỰNG MỚI"
        input_title = self.title_font.render(title_text, True, Theme.PRIMARY_HOVER if self.editing else Theme.TEXT)
        screen.blit(input_title, (135, 42))

        # --------------------------------------------------
        # PANEL 2: DANH SÁCH BỘ THẺ
        # --------------------------------------------------
        shadow2 = self.panel_list.move(0, 4)
        pygame.draw.rect(screen, Theme.SHADOW, shadow2, border_radius=Theme.CARD_RADIUS)
        pygame.draw.rect(screen, Theme.PANEL, self.panel_list, border_radius=Theme.CARD_RADIUS)
        pygame.draw.rect(screen, Theme.BORDER, self.panel_list, width=1, border_radius=Theme.CARD_RADIUS)

        list_title = self.title_font.render("BỘ TỪ VỰNG", True, Theme.TEXT)
        screen.blit(list_title, (475, 42))

        # --------------------------------------------------
        # PANEL 3: DANH SÁCH TỪ VỰNG
        # --------------------------------------------------
        shadow3 = self.panel_card.move(0, 4)
        pygame.draw.rect(screen, Theme.SHADOW, shadow3, border_radius=Theme.CARD_RADIUS)
        pygame.draw.rect(screen, Theme.PANEL, self.panel_card, border_radius=Theme.CARD_RADIUS)
        pygame.draw.rect(screen, Theme.BORDER, self.panel_card, width=1, border_radius=Theme.CARD_RADIUS)

        deck_name = self.card_manager.name
        card_title = self.title_font.render(f"TỪ VỰNG ({len(self.card_manager.Cards)})", True, Theme.TEXT)
        screen.blit(card_title, (865, 42))

        deck_sub = self.hint_font.render(f"Đang chọn: {deck_name}", True, Theme.TEXT_SECOND)
        screen.blit(deck_sub, (1040, 45))

        # Draw List items with clip
        screen.set_clip(self.scroll_list)
        for nut in self.nut_list_card:
            nut.active = (nut.id == self.card_manager.id)
            tmp = nut.rect.y
            nut.rect.y = nut.rect.y - self.y_scroll_list
            nut.draw(screen)

            # Draw card count badge next to list name
            mgr = self.list_manager.find_manager(nut.id)
            if mgr:
                cnt_str = f"{len(mgr.Cards)} từ"
                cnt_surf = self.small_font.render(cnt_str, True, Theme.TEXT_MUTED if not nut.active else Theme.TEXT)
                screen.blit(cnt_surf, cnt_surf.get_rect(midright=(nut.rect.right - 14, nut.rect.centery)))

            nut.rect.y = tmp

        for nut in self.nut_option_list:
            tmp = nut.rect.y
            nut.rect.y = nut.rect.y - self.y_scroll_list
            nut.draw(screen)
            nut.rect.y = tmp

        screen.set_clip(None)

        # Draw Cards with clip
        screen.set_clip(self.scroll_card)
        self.update_card(screen)

        for nut in self.nut_card:
            tmp = nut.rect.y
            nut.rect.y = nut.rect.y - self.y_scroll_card
            nut.draw(screen)
            nut.rect.y = tmp

        for nut in self.nut_option_card:
            tmp = nut.rect.y
            nut.rect.y = nut.rect.y - self.y_scroll_card
            nut.draw(screen)
            nut.rect.y = tmp

        screen.set_clip(None)

        # Draw Tip / Helper Box at bottom of Panel 1
        tip_rect = pygame.Rect(35, 435, 375, 235)
        pygame.draw.rect(screen, Theme.PANEL_LIGHT, tip_rect, border_radius=12)
        pygame.draw.rect(screen, Theme.BORDER, tip_rect, width=1, border_radius=12)

        tip_title = self.bold_font.render("💡 HƯỚNG DẪN & MẸO HỌC", True, Theme.ACCENT)
        screen.blit(tip_title, (50, 452))

        tips = [
            "• Thêm phiên âm giúp bạn phát âm chuẩn xác.",
            "• Đặt câu ví dụ gắn liền với ngữ cảnh thực tế.",
            "• Nhấp chuột phải vào Bộ Thẻ để Đổi Tên / Xóa.",
            "• Bấm nút ⋮ ở mỗi từ để Sửa hoặc Xóa nhanh.",
            "• Sang chế độ 'Quiz' để làm Flashcard và Match!"
        ]
        y_tip = 485
        for t in tips:
            t_surf = self.hint_font.render(t, True, Theme.TEXT_SECOND)
            screen.blit(t_surf, (50, y_tip))
            y_tip += 34

        # Draw Main Panel Controls
        for nut in self.nut_in_learn_scr:
            nut.draw(screen)

        if self.editing:
            self.cancel_button.draw(screen)

        for tb in self.tbox_list:
            tb.draw(screen)

        for label in self.labels:
            label.draw(screen)

        # Draw Toast Notification if active
        if self.toast_timer > 0:
            toast_surf = self.bold_font.render(self.toast_msg, True, Theme.TEXT)
            tw = toast_surf.get_width() + 32
            th = 40
            t_rect = pygame.Rect(700 - tw // 2, 655, tw, th)
            pygame.draw.rect(screen, self.toast_color, t_rect, border_radius=10)
            pygame.draw.rect(screen, Theme.TEXT, t_rect, width=1, border_radius=10)
            screen.blit(toast_surf, toast_surf.get_rect(center=t_rect.center))

        # Reset button active states for regular buttons
        self.back_button.active = False
        self.add_list_button.active = False
        self.add_button.active = False
