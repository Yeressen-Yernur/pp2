import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WHITE = (255,255,255)
GRAY = (40,40,40)
YELLOW = (255,215,0)


player_img = pygame.image.load("practice 11/racer/car_red_1.png").convert_alpha()
enemy_img = pygame.image.load("practice 11/racer/car_blue_1.png").convert_alpha()
barrel_img = pygame.image.load("practice 11/racer/barrel_red.png").convert_alpha()

player_img = pygame.transform.scale(player_img, (50, 80))
enemy_img = pygame.transform.scale(enemy_img, (50, 80))
barrel_img = pygame.transform.scale(barrel_img, (40, 40))

font = pygame.font.SysFont("Arial", 30)
big_font = pygame.font.SysFont("Arial", 60)

ROAD_LEFT = 100
ROAD_RIGHT = 500

def create_enemy():
    return pygame.Rect(random.randint(ROAD_LEFT, ROAD_RIGHT), random.randint(-600,-100), 50, 80)

def create_barrel():
    return pygame.Rect(random.randint(ROAD_LEFT, ROAD_RIGHT), random.randint(-800,-100), 40, 40)

def spawn_coin():
    coins.append({
        "rect": pygame.Rect(random.randint(ROAD_LEFT, ROAD_RIGHT), -20, 20, 20),
        "weight": random.choice([1,2,3])
    })

def reset():
    global player, enemies, barrels, coins, score, speed, game_over

    player = pygame.Rect(280,650,50,80)
    enemies = [create_enemy() for _ in range(3)]
    barrels = [create_barrel() for _ in range(4)]
    coins = []
    score = 0
    speed = 5
    game_over = False

reset()

spawn_timer = 0
game_over = False
explosion_pos = None

running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_r:
                reset()

    keys = pygame.key.get_pressed()

    if not game_over:

        if keys[pygame.K_LEFT]:
            player.x -= 10

        if keys[pygame.K_RIGHT]:
            player.x += 10

        if player.x < ROAD_LEFT:
            player.x = ROAD_LEFT

        if player.x > ROAD_RIGHT - player.width:
            player.x = ROAD_RIGHT - player.width

        for enemy in enemies:
            enemy.y += speed
            if enemy.y > HEIGHT:
                enemy.y = random.randint(-600,-100)
                enemy.x = random.randint(ROAD_LEFT, ROAD_RIGHT)

            if player.colliderect(enemy):
                game_over = True
                explosion_pos = player.center

        for barrel in barrels:
            barrel.y += speed

            if barrel.y > HEIGHT:
                barrel.y = random.randint(-800,-100)
                barrel.x = random.randint(ROAD_LEFT, ROAD_RIGHT)

            if player.colliderect(barrel):
                game_over = True
                explosion_pos = player.center

        spawn_timer += 1
        if spawn_timer > 50:
            spawn_coin()
            spawn_timer = 0

        for coin in coins[:]:
            coin["rect"].y += speed

            if coin["rect"].colliderect(player):
                score += coin["weight"]
                coins.remove(coin)

            elif coin["rect"].y > HEIGHT:
                coins.remove(coin)

        if score >= 5:
            speed = 7
        if score >= 10:
            speed = 9

    screen.fill(GRAY)

    pygame.draw.rect(screen, WHITE, (290,0,20,HEIGHT))

    screen.blit(player_img, player)

    for enemy in enemies:
        screen.blit(enemy_img, enemy)

    for barrel in barrels:
        screen.blit(barrel_img, barrel)

    for coin in coins:
        pygame.draw.circle(screen, YELLOW, coin["rect"].center, 10)

    screen.blit(font.render(f"Coins: {score}", True, WHITE), (420, 20))

    if game_over:

        pygame.draw.circle(screen, (255,0,0), explosion_pos, 50)

        text = big_font.render("GAME OVER", True, (255,50,50))
        screen.blit(text, (120, 350))

        restart = font.render("Press R to Restart", True, WHITE)
        screen.blit(restart, (180, 430))

    pygame.display.update()

pygame.quit()