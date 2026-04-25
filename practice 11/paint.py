import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))

tool = "square"
color = (0, 0, 0)

drawing = False
start = (0, 0)

def draw_square(surf, start, end):
    size = min(abs(end[0]-start[0]), abs(end[1]-start[1]))
    rect = pygame.Rect(start[0], start[1], size, size)
    pygame.draw.rect(surf, color, rect, 2)

def draw_right_triangle(surf, start, end):
    pygame.draw.polygon(surf, color, [
        start,
        (end[0], start[1]),
        end
    ], 2)

def draw_equilateral_triangle(surf, start, end):
    side = abs(end[0]-start[0])
    height = side * math.sqrt(3)/2
    p1 = start
    p2 = (start[0] + side, start[1])
    p3 = (start[0] + side/2, start[1] - height)
    pygame.draw.polygon(surf, color, [p1, p2, p3], 2)

def draw_rhombus(surf, start, end):
    cx = (start[0] + end[0]) // 2
    cy = (start[1] + end[1]) // 2
    p1 = (cx, start[1])
    p2 = (end[0], cy)
    p3 = (cx, end[1])
    p4 = (start[0], cy)
    pygame.draw.polygon(surf, color, [p1, p2, p3, p4], 2)

running = True

while running:
    clock.tick(60)
    screen.blit(canvas, (0, 0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_1:
                tool = "square"

            if event.key == pygame.K_2:
                tool = "right_triangle"

            if event.key == pygame.K_3:
                tool = "equilateral_triangle"

            if event.key == pygame.K_4:
                tool = "rhombus"

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False

            if tool == "square":
                draw_square(canvas, start, event.pos)

            elif tool == "right_triangle":
                draw_right_triangle(canvas, start, event.pos)

            elif tool == "equilateral_triangle":
                draw_equilateral_triangle(canvas, start, event.pos)

            elif tool == "rhombus":
                draw_rhombus(canvas, start, event.pos)

    pygame.display.update()

pygame.quit()