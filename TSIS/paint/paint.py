import pygame
import sys
from datetime import datetime
from tools import (
    PencilTool, LineTool, RectTool, SquareTool, CircleTool,
    RightTriangleTool, EquilateralTriangleTool, RhombusTool,
    EraserTool, FillTool, TextTool, BRUSH_SIZES,
)

# ─────────────────────────────────────────────
# WINDOW
# ─────────────────────────────────────────────
WINDOW_W, WINDOW_H = 1200, 750
TOOLBAR_W = 190
CANVAS_X = TOOLBAR_W
CANVAS_W = WINDOW_W - TOOLBAR_W
CANVAS_H = WINDOW_H

# ─────────────────────────────────────────────
# 🎨 MODERN VISUAL STYLE ONLY
# ─────────────────────────────────────────────
BG = (12, 12, 18)
PANEL = (22, 22, 30)
PANEL_2 = (30, 30, 42)

ACCENT = (90, 160, 255)
ACCENT_HOVER = (120, 190, 255)

TEXT = (235, 235, 245)
MUTED = (150, 150, 170)

CANVAS_BG = (245, 245, 250)


PALETTE = [
    (0,0,0),(255,255,255),(220,60,60),(240,140,50),(240,220,60),
    (60,200,90),(60,150,240),(140,80,220),(240,80,170),
    (160,120,80),(120,180,180),(180,180,180),
    (70,70,70),(255,160,160),(160,255,160),(160,200,255),
]

TOOLS = [
    ("Pencil","P",PencilTool()),
    ("Line","L",LineTool()),
    ("Rectangle","R",RectTool()),
    ("Square","Q",SquareTool()),
    ("Circle","C",CircleTool()),
    ("Rt.Triangle","T",RightTriangleTool()),
    ("Eq.Triangle","E",EquilateralTriangleTool()),
    ("Rhombus","D",RhombusTool()),
    ("Eraser","X",EraserTool()),
    ("Fill","F",FillTool()),
    ("Text","A",TextTool()),
]

# ─────────────────────────────────────────────
# UI HELPERS (UNCHANGED LOGIC)
# ─────────────────────────────────────────────
def draw_round(surf, color, rect, r=12, border=0, bcol=None):
    pygame.draw.rect(surf, color, rect, border_radius=r)
    if border:
        pygame.draw.rect(surf, bcol or (255,255,255), rect, border, border_radius=r)

def hover(rect, mouse):
    return rect.collidepoint(mouse)

def label(surf, font, text, pos, col=TEXT):
    surf.blit(font.render(text, True, col), pos)


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
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

    def pos_fix(p):
        return (p[0]-CANVAS_X, p[1])

    def in_canvas(p):
        return p[0] >= CANVAS_X

    PAD = 10

    tool_buttons = [
        pygame.Rect(PAD + (i%2)*(TOOLBAR_W//2-PAD),
                    60 + (i//2)*42,
                    TOOLBAR_W//2-PAD-6, 34)
        for i in range(len(TOOLS))
    ]

    size_buttons = [
        pygame.Rect(PAD + i*((TOOLBAR_W-PAD*2)//3),
                    60 + ((len(TOOLS)+1)//2)*42 + 40,
                    (TOOLBAR_W-PAD*2)//3 - 6, 30)
        for i in range(3)
    ]

    palette_y = size_buttons[-1].bottom + 25

    swatches = []
    for i,c in enumerate(PALETTE):
        r,cx = divmod(i,6)
        swatches.append((pygame.Rect(PAD+cx*25, palette_y+20+r*25,22,22), c))

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

                for r,c in swatches:
                    if r.collidepoint(p):
                        active_color = c

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

        # ───────────────── UI DRAW ─────────────────
        screen.fill(BG)

        # sidebar
        pygame.draw.rect(screen, PANEL, (0,0,TOOLBAR_W,WINDOW_H))
        pygame.draw.line(screen, PANEL_2, (TOOLBAR_W,0),(TOOLBAR_W,WINDOW_H),2)

        label(screen, font_big, "PAINT", (15,15), ACCENT)

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

            draw_round(screen, color, r, 10, 1, (60,60,80))

            col = (255,255,255) if active else TEXT
            txt = font.render(name, True, col)
            screen.blit(txt, txt.get_rect(center=r.center))

        # sizes
        for i,r in enumerate(size_buttons):
            active = size_key == i+1
            h = hover(r, mouse)

            color = PANEL_2
            if active:
                color = ACCENT
            elif h:
                color = (60,60,80)

            draw_round(screen, color, r, 8, 1, (70,70,90))

            txt = font.render(["S","M","L"][i], True, TEXT if not active else (255,255,255))
            screen.blit(txt, txt.get_rect(center=r.center))

        # palette
        for r,c in swatches:
            pygame.draw.rect(screen, c, r, border_radius=6)

            if c == active_color:
                pygame.draw.rect(screen, ACCENT, r, 2, border_radius=6)
            elif hover(r, mouse):
                pygame.draw.rect(screen, (255,255,255), r, 1, border_radius=6)

        # canvas frame
        pygame.draw.rect(screen, (25,25,35),
                        (CANVAS_X-6,-6,CANVAS_W+12,CANVAS_H+12),
                        border_radius=14)

        screen.blit(canvas,(CANVAS_X,0))

        # preview
        if drawing:
            tmp = canvas.copy()
            tool().draw_preview(tmp, pos_fix(mouse), active_color, size())
            screen.blit(tmp,(CANVAS_X,0))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()