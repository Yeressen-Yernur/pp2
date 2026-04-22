import pygame
import datetime

WIDTH = 600
HEIGHT = 600

def run_clock():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mickey Clock")

    clock = pygame.time.Clock()

    background = pygame.image.load("images/mickeyclock.jpeg")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    hand = pygame.image.load("images/mickey_hand.png")

    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(background, (0,0))

        now = datetime.datetime.now()

        seconds = now.second
        minutes = now.minute

        sec_angle = -seconds * 6
        min_angle = -minutes * 6

        sec_hand = pygame.transform.rotate(hand, sec_angle)
        min_hand = pygame.transform.rotate(hand, min_angle)

        rect = sec_hand.get_rect(center=(WIDTH//2, HEIGHT//2))

        screen.blit(sec_hand, rect)
        screen.blit(min_hand, rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()