import pygame
import sys

from racer import Racer
from coin import Coin
from obstacle import Obstacle
from ui import draw_game, draw_menu, draw_game_over
from persistence import load_scores, save_score

pygame.init()

screen = pygame.display.set_mode((500, 700))
pygame.display.set_caption("Racing Game")

clock = pygame.time.Clock()

# ── game state ─────────────────────
player = Racer()

coins = []
obstacles = []

state = "menu"

score = 0
money = 0

spawn_timer = 0

leaderboard = load_scores()


# ── main loop ──────────────────────
while True:

    dt = clock.tick(60) / 1000

    # ── EVENTS ──────────────────────
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # старт игры
        if state == "menu":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                state = "game"
                player = Racer()
                coins = []
                obstacles = []
                score = 0
                money = 0
                spawn_timer = 0

        # возврат в меню
        if state == "game_over":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                state = "menu"

        # управление (ВАЖНО: только KEYDOWN)
        if state == "game":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    player.move_left()

                if event.key == pygame.K_RIGHT:
                    player.move_right()

    # ── GAME LOGIC ──────────────────
    if state == "game":

        player.update()

        spawn_timer += dt

        if spawn_timer > 0.8:
            coins.append(Coin())
            obstacles.append(Obstacle())
            spawn_timer = 0


        # ── coins SAFE ──
        new_coins = []

        for c in coins:

            c.update()

            if c.rect().colliderect(player.rect()):
                money += c.value
                continue

            if c.y < 800:
                new_coins.append(c)

        coins = new_coins


        # ── obstacles SAFE ──
        new_obs = []
        hit = False

        for o in obstacles:

            o.update()

            if o.rect().colliderect(player.rect()):
                hit = True
                continue

            if o.y < 800:
                new_obs.append(o)

        obstacles = new_obs


        # ── GAME OVER ──
        if hit:
            save_score(score)
            leaderboard = load_scores()
            state = "game_over"


        score += 1


    # ── DRAW ────────────────────────
    if state == "menu":
        draw_menu(screen)

    elif state == "game":
        draw_game(screen, player, coins, obstacles, score, money)

    elif state == "game_over":
        draw_game_over(screen, score, leaderboard)

    pygame.display.flip()