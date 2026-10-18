class Theme:

    # =========================
    # BACKGROUND & SURFACES
    # =========================
    BG = (15, 18, 26)              # Deep navy dark canvas

    PANEL = (22, 27, 39)           # Primary panels and sidebars
    PANEL_LIGHT = (30, 37, 53)     # Elevated panels
    PANEL_HOVER = (38, 47, 66)     # Hover on panels

    LIST_PANEL = (18, 22, 32)      # Container for list items
    CARD_PANEL = (20, 25, 36)      # Container for cards

    # =========================
    # BUTTON
    # =========================
    BUTTON = (32, 39, 56)          # Neutral modern button
    BUTTON_HOVER = (46, 56, 78)    # Hover state
    BUTTON_ACTIVE = (59, 130, 246) # Selected / Active button (Vibrant blue)

    # =========================
    # QUIZ ANSWER
    # =========================
    ANSWER_CORRECT = (16, 185, 129)       # Emerald green
    ANSWER_WRONG = (239, 68, 68)          # Coral red

    ANSWER_CORRECT_HOVER = (34, 197, 94)
    ANSWER_WRONG_HOVER = (248, 113, 113)

    # =========================
    # DISABLED
    # =========================
    DISABLED = (40, 48, 66)
    DISABLED_HOVER = (40, 48, 66)
    DISABLED_TEXT = (100, 116, 139)
    DISABLED_BORDER = (55, 65, 88)

    # =========================
    # PRIMARY / ACCENTS
    # =========================
    PRIMARY = (59, 130, 246)       # Modern Indigo / Blue
    PRIMARY_HOVER = (96, 165, 250) # Light blue hover
    PRIMARY_LIGHT = (30, 58, 138)  # Subtle background tint
    ACCENT = (245, 158, 11)        # Warm amber for phonetics/highlights

    # =========================
    # TEXT
    # =========================
    TEXT = (248, 250, 252)         # Slate 50 - Crisp white
    TEXT_SECOND = (148, 163, 184)  # Slate 400 - Secondary text
    TEXT_MUTED = (100, 116, 139)   # Slate 500 - Subdued hints
    TEXT_DISABLED = (100, 116, 139)

    # =========================
    # INPUT
    # =========================
    INPUT = (18, 23, 34)
    INPUT_HOVER = (26, 32, 47)
    INPUT_ACTIVE = (22, 28, 41)

    INPUT_BORDER = (51, 65, 85)
    INPUT_BORDER_ACTIVE = (59, 130, 246)

    # =========================
    # CARD
    # =========================
    CARD = (26, 32, 47)            # Main flashcard background
    CARD_HOVER = (35, 43, 62)
    CARD_BACK = (22, 28, 42)

    # =========================
    # BORDER & DIVIDERS
    # =========================
    BORDER = (45, 55, 78)          # Subtle border
    BORDER_LIGHT = (65, 78, 108)   # Highlight border

    # =========================
    # STATUS
    # =========================
    SUCCESS = (16, 185, 129)
    ERROR = (239, 68, 68)
    WARNING = (245, 158, 11)

    # =========================
    # FONT
    # =========================
    FONT = "Segoe UI"
    FONT_BOLD = "Segoe UI"

    # =========================
    # RADIUS
    # =========================
    BUTTON_RADIUS = 10
    INPUT_RADIUS = 10
    CARD_RADIUS = 16
    PANEL_RADIUS = 16

    BORDER_RADIUS = BUTTON_RADIUS

    # =========================
    # SHADOW & GLOW
    # =========================
    SHADOW = (10, 12, 18)

    @staticmethod
    def lerp_color(c1, c2, t):
        """Linearly interpolate between color c1 and c2 by factor t (0.0 to 1.0)."""
        t = max(0.0, min(1.0, t))
        return (
            int(c1[0] + (c2[0] - c1[0]) * t),
            int(c1[1] + (c2[1] - c1[1]) * t),
            int(c1[2] + (c2[2] - c1[2]) * t),
        )