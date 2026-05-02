import pygame
import sys
from tools import (
    PencilTool, LineTool, RectTool, SquareTool, CircleTool,
    RightTriangleTool, EquilateralTriangleTool, RhombusTool,
    EraserTool, FillTool, TextTool, BRUSH_SIZES,
)

# ─────────────────────────────
# WINDOW
# ─────────────────────────────
WINDOW_W, WINDOW_H = 1200, 750

TOOLBAR_H = 120
CANVAS_Y = TOOLBAR_H
CANVAS_H = WINDOW_H - TOOLBAR_H

CANVAS_W = WINDOW_W

# ─────────────────────────────
# STYLE
# ─────────────────────────────
BG = (12, 12, 18)
PANEL = (22, 22, 30)
PANEL_2 = (30, 30, 42)

ACCENT = (90, 160, 255)
TEXT = (235, 235, 245)

CANVAS_BG = (245, 245, 250)

PALETTE = [
    (0,0,0),(255,255,255),(220,60,60),(240,140,50),(240,220,60),
    (60,200,90),(60,150,240),(140,80,220),(240,80,170),
    (160,120,80),(120,180,180),(180,180,180),
]

TOOLS = [
    ("Pencil","P",PencilTool()),
    ("Line","L",LineTool()),
    ("Rectangle","R",RectTool()),
    ("Square","Q",SquareTool()),
    ("Circle","C",CircleTool()),
    ("Triangle","T",RightTriangleTool()),
    ("EqTri","E",EquilateralTriangleTool()),
    ("Rhombus","D",RhombusTool()),
    ("Eraser","X",EraserTool()),
    ("Fill","F",FillTool()),
    ("Text","A",TextTool()),
]

# ─────────────────────────────
def draw_round(surf, color, rect, r=10, border=0, bcol=None):
    pygame.draw.rect(surf, color, rect, border_radius=r)
    if border:
        pygame.draw.rect(surf, bcol or (255,255,255), rect, border, border_radius=r)

def hover(rect, mouse):
    return rect.collidepoint(mouse)

def pos_fix(p):
    return (p[0], p[1] - TOOLBAR_H)

def in_canvas(p):
    return p[1] >= TOOLBAR_H


# ─────────────────────────────
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Segoe UI", 14)
    font_big = pygame.font.SysFont("Segoe UI", 18, bold=True)

    canvas = pygame.Surface((CANVAS_W, CANVAS_H))
    canvas.fill(CANVAS_BG)

    active_tool = 0
    active_color = (0,0,0)
    size_key = 1
    drawing = False

    def size():
        return BRUSH_SIZES[size_key]

    def tool():
        return TOOLS[active_tool][2]

    # ───────────────────────── TOOLBAR LAYOUT (TOP)
    PAD = 10

    tool_buttons = [
        pygame.Rect(10 + i*110, 10, 100, 40)
        for i in range(len(TOOLS))
    ]

    size_buttons = [
        pygame.Rect(10 + i*60, 60, 50, 40)
        for i in range(3)
    ]

    palette = [
        pygame.Rect(250 + i*25, 60, 22, 22)
        for i in range(len(PALETTE))
    ]

    running = True

    while running:
        mouse = pygame.mouse.get_pos()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

            elif e.type == pygame.MOUSEBUTTONDOWN:
                p = e.pos

                for i,r in enumerate(tool_buttons):
                    if r.collidepoint(p):
                        active_tool = i

                for i,r in enumerate(size_buttons):
                    if r.collidepoint(p):
                        size_key = i+1

                for i,r in enumerate(palette):
                    if r.collidepoint(p):
                        active_color = PALETTE[i]

                if in_canvas(p):
                    drawing = True
                    tool().on_mouse_down(canvas, pos_fix(p), active_color, size())

            elif e.type == pygame.MOUSEMOTION:
                if drawing and in_canvas(e.pos):
                    tool().on_mouse_move(canvas, pos_fix(e.pos), active_color, size())

            elif e.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    tool().on_mouse_up(canvas, pos_fix(e.pos), active_color, size())
                    drawing = False

        # ───────────────── DRAW ─────────────────
        screen.fill(BG)

        # TOP BAR
        pygame.draw.rect(screen, PANEL, (0,0,WINDOW_W,TOOLBAR_H))

        # tools
        for i,(name,_,_) in enumerate(TOOLS):
            r = tool_buttons[i]
            active = i == active_tool
            h = hover(r, mouse)

            color = PANEL
            if active:
                color = ACCENT
            elif h:
                color = PANEL_2

            draw_round(screen, color, r, 8, 1, (70,70,90))

            txt = font.render(name, True, TEXT if not active else (255,255,255))
            screen.blit(txt, txt.get_rect(center=r.center))

        # sizes
        for i,r in enumerate(size_buttons):
            active = size_key == i+1
            pygame.draw.rect(screen, ACCENT if active else PANEL_2, r, border_radius=6)

            txt = font.render(["S","M","L"][i], True, TEXT)
            screen.blit(txt, txt.get_rect(center=r.center))

        # palette
        for i,r in enumerate(palette):
            pygame.draw.rect(screen, PALETTE[i], r, border_radius=6)
            if PALETTE[i] == active_color:
                pygame.draw.rect(screen, ACCENT, r, 2, border_radius=6)

        # canvas
        pygame.draw.rect(screen, (25,25,35),
                        (0,TOOLBAR_H,WINDOW_W,CANVAS_H))

        screen.blit(canvas, (0,TOOLBAR_H))

        # preview
        if drawing:
            tmp = canvas.copy()
            tool().draw_preview(tmp, pos_fix(mouse), active_color, size())
            screen.blit(tmp,(0,TOOLBAR_H))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()