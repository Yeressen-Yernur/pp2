import pygame

WIDTH = 800
HEIGHT = 600

def run_game():

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Ball")

    clock = pygame.time.Clock()

    x = WIDTH // 2
    y = HEIGHT // 2

    radius = 25
    speed = 20

    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT and x - speed - radius >= 0:
                    x -= speed

                if event.key == pygame.K_RIGHT and x + speed + radius <= WIDTH:
                    x += speed

                if event.key == pygame.K_UP and y - speed - radius >= 0:
                    y -= speed

                if event.key == pygame.K_DOWN and y + speed + radius <= HEIGHT:
                    y += speed

        screen.fill((255,255,255))

        pygame.draw.circle(screen, (255,0,0), (x,y), radius)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()