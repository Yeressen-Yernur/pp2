import pygame
import sys

import ui
import racer
import persistence

W, H = 480, 700
FPS  = 60


def run():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Turbo Racer – TSIS-3")
    clock  = pygame.time.Clock()

    settings = persistence.load_settings()
    lb_data  = persistence.load_leaderboard()


    STATE   = "menu"   
    game    = None
    username_buf = ""
    gameover_data = {}

    def start_game():
        nonlocal game
        game = racer.RacerGame(W, H, settings, username_buf)

    while True:
        dt         = clock.tick(FPS) / 1000.0
        mouse_pos  = pygame.mouse.get_pos()

        # ── events ────────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # ── MENU ──────────────────────────────────────────────────────────
            if STATE == "menu":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    btns = ui.draw_main_menu(screen, mouse_pos, W, H)
                    if btns["Play"].collidepoint(mouse_pos):
                        STATE = "username"
                        username_buf = ""
                    elif btns["Leaderboard"].collidepoint(mouse_pos):
                        lb_data = persistence.load_leaderboard()
                        STATE = "leaderboard"
                    elif btns["Settings"].collidepoint(mouse_pos):
                        STATE = "settings"
                    elif btns["Quit"].collidepoint(mouse_pos):
                        pygame.quit(); sys.exit()

            # ── SETTINGS ──────────────────────────────────────────────────────
            elif STATE == "settings":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    btns = ui.draw_settings(screen, mouse_pos, settings, W, H)
                    if btns["sound"].collidepoint(mouse_pos):
                        settings["sound"] = not settings["sound"]
                        persistence.save_settings(settings)
                    elif btns["car_color"].collidepoint(mouse_pos):
                        cols = list(ui.CAR_COLORS.keys())
                        idx  = cols.index(settings["car_color"])
                        settings["car_color"] = cols[(idx + 1) % len(cols)]
                        persistence.save_settings(settings)
                    elif btns["difficulty"].collidepoint(mouse_pos):
                        diffs = ui.DIFFICULTY_LABELS
                        idx   = diffs.index(settings["difficulty"])
                        settings["difficulty"] = diffs[(idx + 1) % len(diffs)]
                        persistence.save_settings(settings)
                    elif btns["back"].collidepoint(mouse_pos):
                        STATE = "menu"

            # ── LEADERBOARD ───────────────────────────────────────────────────
            elif STATE == "leaderboard":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    btns = ui.draw_leaderboard(screen, mouse_pos, lb_data, W, H)
                    if btns["back"].collidepoint(mouse_pos):
                        STATE = "menu"

            # ── USERNAME ──────────────────────────────────────────────────────
            elif STATE == "username":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if username_buf.strip():
                            start_game()
                            STATE = "game"
                    elif event.key == pygame.K_BACKSPACE:
                        username_buf = username_buf[:-1]
                    else:
                        if len(username_buf) < 12 and event.unicode.isprintable():
                            username_buf += event.unicode
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    btns = ui.draw_username_prompt(screen, mouse_pos, username_buf, W, H)
                    if btns["ok"].collidepoint(mouse_pos) and username_buf.strip():
                        start_game()
                        STATE = "game"

            # ── GAME ──────────────────────────────────────────────────────────
            elif STATE == "game":
                if game:
                    game.handle_event(event)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    STATE = "menu"

            # ── GAME OVER ─────────────────────────────────────────────────────
            elif STATE == "gameover":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    btns = ui.draw_gameover(screen, mouse_pos,
                                            gameover_data["score"],
                                            gameover_data["distance"],
                                            gameover_data["coins"], W, H)
                    if btns["retry"].collidepoint(mouse_pos):
                        start_game()
                        STATE = "game"
                    elif btns["menu"].collidepoint(mouse_pos):
                        STATE = "menu"

        # ── update & draw ─────────────────────────────────────────────────────
        if STATE == "menu":
            ui.draw_main_menu(screen, mouse_pos, W, H)

        elif STATE == "settings":
            ui.draw_settings(screen, mouse_pos, settings, W, H)

        elif STATE == "leaderboard":
            ui.draw_leaderboard(screen, mouse_pos, lb_data, W, H)

        elif STATE == "username":
            ui.draw_username_prompt(screen, mouse_pos, username_buf, W, H)

        elif STATE == "game":
            if game:
                game.update(dt)
                game.draw(screen)
                ui.draw_hud(screen,
                            game.score,
                            game.distance,
                            game.goal_dist,
                            game.coins_count,
                            game.active_pu,
                            game.pu_time_left,
                            W)

                if not game.alive:
                    # save score
                    lb_data = persistence.save_score(
                        username_buf or "ANON",
                        game.score,
                        game.distance,
                        game.coins_count
                    )
                    gameover_data = {
                        "score":    game.score,
                        "distance": game.distance,
                        "coins":    game.coins_count,
                        "won":      game.won,
                    }
                    STATE = "gameover"

        elif STATE == "gameover":
            screen.fill(ui.DARK)
            if gameover_data.get("won"):
                ui.draw_text(screen, "🏁 YOU FINISHED! 🏁", 32, ui.ACCENT, W // 2, 40)
            ui.draw_gameover(screen, mouse_pos,
                             gameover_data["score"],
                             gameover_data["distance"],
                             gameover_data["coins"], W, H)

        pygame.display.flip()


if __name__ == "__main__":
    run()