import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))

tool = "pen"
color = (0, 0, 0)

drawing = False
start_pos = (0, 0)
eraser_size = 20

def draw_rect(surf, start, end):
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    w = abs(start[0] - end[0])
    h = abs(start[1] - end[1])
    pygame.draw.rect(surf, color, (x, y, w, h), 2)

def draw_circle(surf, start, end):
    radius = int(((end[0]-start[0])**2 + (end[1]-start[1])**2) ** 0.5)
    pygame.draw.circle(surf, color, start, radius, 2)

running = True
while running:
    clock.tick(60)
    screen.blit(canvas, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            if tool == "rect":
                draw_rect(canvas, start_pos, event.pos)
            elif tool == "circle":
                draw_circle(canvas, start_pos, event.pos)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                tool = "pen"
            if event.key == pygame.K_r:
                tool = "rect"
            if event.key == pygame.K_c:
                tool = "circle"
            if event.key == pygame.K_e:
                tool = "eraser"
            if event.key == pygame.K_1:
                color = (0, 0, 0)
            if event.key == pygame.K_2:
                color = (255, 0, 0)
            if event.key == pygame.K_3:
                color = (0, 0, 255)

    if drawing:
        pos = pygame.mouse.get_pos()
        if tool == "pen":
            pygame.draw.circle(canvas, color, pos, 3)
        if tool == "eraser":
            pygame.draw.circle(canvas, (255, 255, 255), pos, eraser_size)

    pygame.display.update()

pygame.quit()