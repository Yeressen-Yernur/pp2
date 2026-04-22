import pygame
import random

pygame.init()


WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


WHITE = (255, 255, 255)
GRAY = (50, 50, 50)


car = pygame.Rect(300, 700, 50, 80)
car_speed = 5


coin_img = pygame.Surface((20, 20))
pygame.draw.circle(coin_img, (255, 215, 0), (10, 10), 10)

coins = []
spawn_timer = 0

score = 0
font = pygame.font.SysFont("Arial", 28)


def spawn_coin():
    x = random.randint(200, 450)
    coins.append(pygame.Rect(x, -20, 20, 20))


running = True
while running:
    clock.tick(60)
    screen.fill(GRAY)

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        car.x -= car_speed
    if keys[pygame.K_RIGHT]:
        car.x += car_speed

    
    spawn_timer += 1
    if spawn_timer > 50:
        spawn_coin()
        spawn_timer = 0

    
    for coin in coins[:]:
        coin.y += 5
        if coin.colliderect(car):
            coins.remove(coin)
            score += 1
        elif coin.y > HEIGHT:
            coins.remove(coin)

    
    pygame.draw.rect(screen, WHITE, (290, 0, 20, HEIGHT))

    
    pygame.draw.rect(screen, (0, 0, 255), car)

    
    for coin in coins:
        screen.blit(coin_img, coin)

    
    text = font.render(f"Coins: {score}", True, WHITE)
    screen.blit(text, (430, 20))

    pygame.display.update()

pygame.quit()