import pygame
import os

tracks = [
    "music/track1.wav",
    "music/track2.wav"
]

current = 0


def play_track():
    pygame.mixer.music.load(tracks[current])
    pygame.mixer.music.play()


def run_player():

    global current

    screen = pygame.display.set_mode((600,200))
    pygame.display.set_caption("Music Player")

    font = pygame.font.SysFont(None, 36)

    running = True

    while running:

        screen.fill((30,30,30))

        text = font.render(f"Track: {os.path.basename(tracks[current])}", True, (255,255,255))
        screen.blit(text,(50,80))

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_p:
                    play_track()

                if event.key == pygame.K_s:
                    pygame.mixer.music.stop()

                if event.key == pygame.K_n:
                    current = (current + 1) % len(tracks)
                    play_track()

                if event.key == pygame.K_b:
                    current = (current - 1) % len(tracks)
                    play_track()

                if event.key == pygame.K_q:
                    running = False

    pygame.quit()