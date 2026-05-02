import pygame

# ── palette ──────────────────────────────────────────────────────────────────
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
GRAY   = (120, 120, 120)
DARK   = (20, 20, 30)
ACCENT = (255, 200, 0)
RED    = (220, 50, 50)
GREEN  = (50, 200, 80)
BLUE   = (50, 130, 255)
ORANGE = (255, 140, 0)
PURPLE = (170, 80, 220)
TEAL   = (0, 210, 180)

CAR_COLORS = {
    "red":    (220, 50,  50),
    "blue":   (50,  130, 255),
    "green":  (50,  200, 80),
    "yellow": (255, 220, 0),
    "purple": (170, 80,  220),
}

DIFFICULTY_LABELS = ["easy", "normal", "hard"]


def _font(size):
    return pygame.font.SysFont("consolas", size, bold=True)


def draw_text(surface, text, size, color, cx, cy):
    f = _font(size)
    s = f.render(text, True, color)
    r = s.get_rect(center=(cx, cy))
    surface.blit(s, r)
    return r


def draw_button(surface, text, rect, hover=False):
    color = ACCENT if hover else (60, 60, 80)
    txt_color = BLACK if hover else WHITE
    pygame.draw.rect(surface, color, rect, border_radius=8)
    pygame.draw.rect(surface, WHITE, rect, 2, border_radius=8)
    f = _font(22)
    s = f.render(text, True, txt_color)
    surface.blit(s, s.get_rect(center=rect.center))


# ── screens ───────────────────────────────────────────────────────────────────

def draw_main_menu(surface, mouse_pos, W, H):
    surface.fill(DARK)
    # road stripes decoration
    for i in range(0, H, 60):
        pygame.draw.rect(surface, (30, 30, 45), (0, i, W, 30))

    draw_text(surface, "🏎  TURBO RACER  🏎", 42, ACCENT, W // 2, H // 5)
    draw_text(surface, "TSIS-3 Edition", 18, GRAY, W // 2, H // 5 + 48)

    buttons = {}
    labels = ["Play", "Leaderboard", "Settings", "Quit"]
    for i, label in enumerate(labels):
        r = pygame.Rect(W // 2 - 120, H // 2 - 20 + i * 64, 240, 48)
        hover = r.collidepoint(mouse_pos)
        draw_button(surface, label, r, hover)
        buttons[label] = r
    return buttons


def draw_settings(surface, mouse_pos, settings, W, H):
    surface.fill(DARK)
    draw_text(surface, "SETTINGS", 36, ACCENT, W // 2, 60)

    # Sound toggle
    sound_r = pygame.Rect(W // 2 - 120, 140, 240, 48)
    label = f"Sound: {'ON' if settings['sound'] else 'OFF'}"
    draw_button(surface, label, sound_r, sound_r.collidepoint(mouse_pos))

    # Car color cycle
    color_r = pygame.Rect(W // 2 - 120, 210, 240, 48)
    draw_button(surface, f"Car: {settings['car_color'].upper()}", color_r,
                color_r.collidepoint(mouse_pos))
    # preview swatch
    swatch = CAR_COLORS[settings["car_color"]]
    pygame.draw.rect(surface, swatch, (W // 2 + 130, 218, 32, 32), border_radius=4)

    # Difficulty cycle
    diff_r = pygame.Rect(W // 2 - 120, 280, 240, 48)
    draw_button(surface, f"Difficulty: {settings['difficulty'].upper()}", diff_r,
                diff_r.collidepoint(mouse_pos))

    back_r = pygame.Rect(W // 2 - 80, 380, 160, 44)
    draw_button(surface, "Back", back_r, back_r.collidepoint(mouse_pos))

    return {"sound": sound_r, "car_color": color_r, "difficulty": diff_r, "back": back_r}


def draw_leaderboard(surface, mouse_pos, lb, W, H):
    surface.fill(DARK)
    draw_text(surface, "🏆  TOP 10  🏆", 34, ACCENT, W // 2, 50)

    headers = ["#", "NAME", "SCORE", "DIST", "COINS"]
    col_x = [40, 90, 230, 340, 430]
    f = _font(16)
    for i, h in enumerate(headers):
        s = f.render(h, True, GRAY)
        surface.blit(s, (col_x[i], 100))
    pygame.draw.line(surface, GRAY, (30, 120), (W - 30, 120), 1)

    for rank, entry in enumerate(lb[:10], 1):
        y = 128 + (rank - 1) * 34
        color = ACCENT if rank == 1 else (WHITE if rank <= 3 else GRAY)
        row = [str(rank), entry["name"][:10], str(entry["score"]),
               f"{entry['distance']}m", str(entry["coins"])]
        for i, val in enumerate(row):
            s = f.render(val, True, color)
            surface.blit(s, (col_x[i], y))

    back_r = pygame.Rect(W // 2 - 80, H - 70, 160, 44)
    draw_button(surface, "Back", back_r, back_r.collidepoint(mouse_pos))
    return {"back": back_r}


def draw_gameover(surface, mouse_pos, score, distance, coins, W, H):
    surface.fill(DARK)
    draw_text(surface, "GAME OVER", 48, RED, W // 2, H // 4)
    draw_text(surface, f"Score:    {score}", 26, WHITE,  W // 2, H // 4 + 70)
    draw_text(surface, f"Distance: {distance} m", 26, WHITE,  W // 2, H // 4 + 106)
    draw_text(surface, f"Coins:    {coins}", 26, ACCENT, W // 2, H // 4 + 142)

    retry_r = pygame.Rect(W // 2 - 140, H // 2 + 100, 120, 48)
    menu_r  = pygame.Rect(W // 2 + 20,  H // 2 + 100, 120, 48)
    draw_button(surface, "Retry",     retry_r, retry_r.collidepoint(mouse_pos))
    draw_button(surface, "Main Menu", menu_r,  menu_r.collidepoint(mouse_pos))
    return {"retry": retry_r, "menu": menu_r}


def draw_username_prompt(surface, mouse_pos, name_buf, W, H):
    surface.fill(DARK)
    draw_text(surface, "Enter Your Name", 34, ACCENT, W // 2, H // 3)
    # input box
    box = pygame.Rect(W // 2 - 140, H // 2 - 24, 280, 48)
    pygame.draw.rect(surface, (50, 50, 70), box, border_radius=8)
    pygame.draw.rect(surface, ACCENT, box, 2, border_radius=8)
    f = _font(26)
    s = f.render(name_buf + "|", True, WHITE)
    surface.blit(s, s.get_rect(center=box.center))

    ok_r = pygame.Rect(W // 2 - 60, H // 2 + 50, 120, 44)
    draw_button(surface, "Start", ok_r, ok_r.collidepoint(mouse_pos))
    return {"ok": ok_r}


def draw_hud(surface, score, distance, goal_dist, coins, active_pu, pu_timer, W):
    f16 = _font(16)
    f20 = _font(20)

    # Score / distance bar
    pygame.draw.rect(surface, (0, 0, 0, 160), (0, 0, W, 36))
    surface.blit(f20.render(f"Score: {score}", True, ACCENT), (10, 8))
    dist_text = f"Dist: {distance}m / {goal_dist}m"
    surface.blit(f16.render(dist_text, True, WHITE), (W // 2 - 80, 10))
    surface.blit(f16.render(f"Coins: {coins}", True, (255, 220, 0)), (W - 130, 10))

    # Power-up indicator
    if active_pu:
        pu_colors = {"nitro": ORANGE, "shield": TEAL, "repair": GREEN}
        col = pu_colors.get(active_pu, WHITE)
        label = f"[{active_pu.upper()}]  {pu_timer:.1f}s" if pu_timer > 0 else f"[{active_pu.upper()}]"
        s = f20.render(label, True, col)
        surface.blit(s, (W // 2 - s.get_width() // 2, 40))