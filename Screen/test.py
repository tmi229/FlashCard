 ######################################################    
import pygame
import math

pygame.init()

screen = pygame.display.set_mode((1400, 720))
pygame.display.set_caption("FlashCard - 3D Flip Demo")
clock = pygame.time.Clock()

BG = (12, 20, 38)
CARD = (24, 40, 68)
CARD_BACK = (31, 48, 82)
BORDER = (64, 87, 124)
TEXT = (238, 243, 255)
TEXT_SECOND = (155, 171, 199)

font = pygame.font.SysFont("segoeui", 42, bold=True)
small_font = pygame.font.SysFont("segoeui", 20)

card_rect = pygame.Rect(500, 160, 700, 390)
flipping = False
flip_progress = 0.0
card_side = 0


def start_flip():
    global flipping, flip_progress
    if not flipping:
        flipping = True
        flip_progress = 0.0


def ease(t):
    # Smooth acceleration/deceleration.
    return 0.5 - 0.5 * math.cos(math.pi * t)


def draw_card(surface):
    global flipping, flip_progress, card_side

    if not flipping:
        scale = 1.0
        side = card_side
        show_text = True
    else:
        p = flip_progress

        # 0.00 -> 0.40 : chữ biến mất trước khi thẻ tới cạnh
        # 0.40 -> 0.60 : thẻ đi qua trạng thái cạnh
        # 0.60 -> 1.00 : thẻ mở ra, sau đó chữ mới xuất hiện
        if p < 0.40:
            scale = 1.0 - ease(p / 0.40) * 0.75
            side = card_side
            show_text = p < 0.22
        elif p < 0.60:
            # Gần như cạnh thẻ: không cho chữ xuất hiện.
            t = (p - 0.40) / 0.20
            scale = 0.25 + 0.02 * math.sin(math.pi * t)
            side = card_side
            show_text = False
        else:
            scale = 0.25 + ease((p - 0.60) / 0.40) * 0.75
            side = 1 - card_side
            # Chỉ hiện nghĩa sau khi thẻ đã mở đủ rộng.
            show_text = p > 0.82

    width = max(2, int(card_rect.width * scale))

    # Card luôn co/mở quanh tâm.
    x = card_rect.centerx - width // 2
    rect = pygame.Rect(x, card_rect.y, width, card_rect.height)

    color = CARD if side == 0 else CARD_BACK
    pygame.draw.rect(surface, color, rect, border_radius=18)
    pygame.draw.rect(surface, BORDER, rect, width=2, border_radius=18)

    # Chữ không xuất hiện trong lúc thẻ đang "đi qua" cạnh.
    if show_text and width > 90:
        if side == 0:
            title = "ETHANOL"
            body = "What is the molecular formula?"
        else:
            title = "CH₃CH₂OH"
            body = "Ethyl alcohol / ethanol"

        title_img = font.render(title, True, TEXT)
        body_img = small_font.render(body, True, TEXT_SECOND)

        surface.blit(
            title_img,
            title_img.get_rect(center=(rect.centerx, rect.centery - 35))
        )
        surface.blit(
            body_img,
            body_img.get_rect(center=(rect.centerx, rect.centery + 30))
        )


running = True
while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if card_rect.collidepoint(event.pos):
                start_flip()

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            start_flip()

    if flipping:
        # Around 0.6 seconds for a complete flip.
        flip_progress += dt / 0.72

        if flip_progress >= 1.0:
            flip_progress = 1.0
            flipping = False
            card_side = 1 - card_side

    screen.fill(BG)

    draw_card(screen)

    hint = small_font.render(
        "Click the card or press SPACE to flip",
        True,
        TEXT_SECOND
    )
    screen.blit(hint, hint.get_rect(center=(850, 620)))

    pygame.display.flip()

pygame.quit()
