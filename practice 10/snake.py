import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

snake = [[100, 100], [80, 100], [60, 100]]
direction = "RIGHT"

def generate_food():
    while True:
        pos = [random.randrange(0, WIDTH, 20),
               random.randrange(0, HEIGHT, 20)]
        if pos not in snake:
            return pos

food = generate_food()

score = 0
level = 1
speed = 10
font = pygame.font.SysFont("Arial", 24)

def check_wall(head):
    return head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT

running = True
while running:
    clock.tick(speed)
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        direction = "LEFT"
    if keys[pygame.K_RIGHT]:
        direction = "RIGHT"
    if keys[pygame.K_UP]:
        direction = "UP"
    if keys[pygame.K_DOWN]:
        direction = "DOWN"

    head = snake[0].copy()

    if direction == "RIGHT":
        head[0] += 20
    if direction == "LEFT":
        head[0] -= 20
    if direction == "UP":
        head[1] -= 20
    if direction == "DOWN":
        head[1] += 20

    if check_wall(head) or head in snake:
        running = False

    snake.insert(0, head)

    if head == food:
        score += 1
        food = generate_food()
        level = score // 3 + 1
        speed = 10 + (level - 1) * 2
    else:
        snake.pop()

    pygame.draw.rect(screen, (255, 0, 0), (*food, 20, 20))

    for block in snake:
        pygame.draw.rect(screen, (0, 255, 0), (*block, 20, 20))

    screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (10, 10))
    screen.blit(font.render(f"Level: {level}", True, (255, 255, 255)), (10, 35))

    pygame.display.update()

pygame.quit()