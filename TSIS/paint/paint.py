import pygame
import sys
from datetime import datetime
from tools import (
    PencilTool, LineTool, RectTool, SquareTool, CircleTool,
    RightTriangleTool, EquilateralTriangleTool, RhombusTool,
    EraserTool, FillTool, TextTool, BRUSH_SIZES,
)

WINDOW_W, WINDOW_H = 1200, 750
TOOLBAR_W = 180
CANVAS_X = TOOLBAR_W
CANVAS_W = WINDOW_W - TOOLBAR_W
CANVAS_H = WINDOW_H

# 🎨 NEW MODERN STYLE
BG_COLOR = (18, 18, 24)
TOOLBAR_COLOR = (28, 28, 38)
PANEL_BORDER = (60, 60, 80)

ACCENT = (120, 170, 255)
TEXT_COLOR = (235, 235, 245)
MUTED_TEXT = (160, 160, 180)

CANVAS_BG = (255, 255, 255)

PALETTE = [
    (0,0,0),(255,255,255),(200,50,50),(220,120,40),(220,200,40),
    (50,180,80),(40,140,220),(130,60,200),(220,80,160),
    (150,100,60),(100,160,160),(180,180,180),
    (80,80,80),(255,150,150),(150,255,150),(150,200,255),
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

def draw_rounded_rect(surf, color, rect, radius=10, border=0, border_color=None):
    pygame.draw.rect(surf, color, rect, border_radius=radius)
    if border and border_color:
        pygame.draw.rect(surf, border_color, rect, border, border_radius=radius)

def label(surf, font, text, pos, color=TEXT_COLOR):
    s = font.render(text, True, color)
    surf.blit(s, pos)

def is_hover(rect, mouse):
    return rect.collidepoint(mouse)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    clock = pygame.time.Clock()

    font_sm = pygame.font.SysFont("Segoe UI", 13)
    font_big = pygame.font.SysFont("Segoe UI", 16, bold=True)

    canvas = pygame.Surface((CANVAS_W, CANVAS_H))
    canvas.fill(CANVAS_BG)

    active_tool_idx = 0
    active_color = (0,0,0)
    brush_size_key = 1
    drawing = False

    def current_size():
        return BRUSH_SIZES[brush_size_key]

    def current_tool():
        return TOOLS[active_tool_idx][2]

    def canvas_pos(p):
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

    palette_top = size_buttons[-1].bottom + 25

    swatches = []
    for i, c in enumerate(PALETTE):
        row, col = divmod(i, 6)
        swatches.append((pygame.Rect(PAD+col*25, palette_top+20+row*25, 22, 22), c))

    running = True

    while running:
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos

                for i, r in enumerate(tool_buttons):
                    if r.collidepoint(pos):
                        active_tool_idx = i

                for i, r in enumerate(size_buttons):
                    if r.collidepoint(pos):
                        brush_size_key = i+1

                for r, c in swatches:
                    if r.collidepoint(pos):
                        active_color = c

                if in_canvas(pos):
                    drawing = True
                    current_tool().on_mouse_down(canvas, canvas_pos(pos), active_color, current_size())

            elif event.type == pygame.MOUSEMOTION:
                if drawing and in_canvas(event.pos):
                    current_tool().on_mouse_move(canvas, canvas_pos(event.pos), active_color, current_size())

            elif event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    current_tool().on_mouse_up(canvas, canvas_pos(event.pos), active_color, current_size())
                    drawing = False

        # 🧊 background
        screen.fill(BG_COLOR)

        # sidebar
        pygame.draw.rect(screen, TOOLBAR_COLOR, (0,0,TOOLBAR_W,WINDOW_H))
        pygame.draw.line(screen, PANEL_BORDER, (TOOLBAR_W,0),(TOOLBAR_W,WINDOW_H),2)

        label(screen, font_big, "PAINT", (15,15), ACCENT)

        # tools
        for i, (name, shortcut, _) in enumerate(TOOLS):
            r = tool_buttons[i]
            active = i == active_tool_idx
            hover = is_hover(r, mouse)

            color = TOOLBAR_COLOR
            if active:
                color = ACCENT
            elif hover:
                color = (40,40,55)

            draw_rounded_rect(screen, color, r, 10, 1, PANEL_BORDER)

            txt = font_sm.render(f"{shortcut} {name}", True,
                                 (255,255,255) if active else TEXT_COLOR)
            screen.blit(txt, txt.get_rect(center=r.center))

        # sizes
        for i, r in enumerate(size_buttons):
            active = brush_size_key == i+1
            hover = is_hover(r, mouse)

            color = (45,45,58)
            if active:
                color = ACCENT
            elif hover:
                color = (55,55,75)

            draw_rounded_rect(screen, color, r, 8, 1, PANEL_BORDER)

            txt = font_sm.render(["S","M","L"][i], True,
                                 (255,255,255) if active else TEXT_COLOR)
            screen.blit(txt, txt.get_rect(center=r.center))

        # palette
        for r, c in swatches:
            pygame.draw.rect(screen, c, r, border_radius=6)

            if c == active_color:
                pygame.draw.rect(screen, ACCENT, r, 2, border_radius=6)
            elif is_hover(r, mouse):
                pygame.draw.rect(screen, (255,255,255), r, 1, border_radius=6)

        # canvas frame
        draw_rounded_rect(screen, (25,25,35),
                          (CANVAS_X-5, -5, CANVAS_W+10, CANVAS_H+10),
                          12)

        screen.blit(canvas, (CANVAS_X,0))

        # preview
        if drawing:
            preview = canvas.copy()
            current_tool().draw_preview(preview, canvas_pos(mouse), active_color, current_size())
            screen.blit(preview, (CANVAS_X,0))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()