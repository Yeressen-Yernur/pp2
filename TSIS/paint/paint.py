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

BG_COLOR = (30, 30, 38)
TOOLBAR_COLOR = (22, 22, 30)
PANEL_BORDER = (55, 55, 70)
ACCENT = (100, 149, 237)
TEXT_COLOR = (220, 220, 230)
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

def draw_rounded_rect(surf, color, rect, radius=8, border=0, border_color=None):
    pygame.draw.rect(surf, color, rect, border_radius=radius)
    if border and border_color:
        pygame.draw.rect(surf, border_color, rect, border, border_radius=radius)

def label(surf, font, text, pos, color=TEXT_COLOR, center=False):
    s = font.render(text, True, color)
    r = s.get_rect()
    if center:
        r.centerx = pos[0]
        r.y = pos[1]
    else:
        r.topleft = pos
    surf.blit(s, r)

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
    status_msg = "Ready"
    status_timer = 0

    def set_status(msg, ms=2500):
        nonlocal status_msg, status_timer
        status_msg = msg
        status_timer = pygame.time.get_ticks() + ms

    def current_size():
        return BRUSH_SIZES[brush_size_key]

    def current_tool():
        return TOOLS[active_tool_idx][2]

    def canvas_pos(p):
        return (p[0]-CANVAS_X, p[1])

    def in_canvas(p):
        return p[0] >= CANVAS_X

    PAD = 10
    tool_buttons = []
    for i in range(len(TOOLS)):
        row, col = divmod(i, 2)
        tool_buttons.append(pygame.Rect(PAD + col*(TOOLBAR_W//2-PAD),
                                        50 + row*42,
                                        TOOLBAR_W//2-PAD-4, 34))

    size_buttons = []
    for i in range(3):
        size_buttons.append(pygame.Rect(PAD + i*((TOOLBAR_W-PAD*2)//3),
                                        50 + ((len(TOOLS)+1)//2)*42 + 30,
                                        (TOOLBAR_W-PAD*2)//3 - 4, 30))

    palette_top = size_buttons[-1].bottom + 20
    swatches = []
    for i, c in enumerate(PALETTE):
        row, col = divmod(i, 6)
        swatches.append((pygame.Rect(PAD+col*25, palette_top+20+row*25, 22, 22), c))

    running = True
    while running:
        now = pygame.time.get_ticks()
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                tool = current_tool()
                if isinstance(tool, TextTool) and tool.active:
                    tool.handle_key(event, canvas, active_color, current_size())
                    continue

                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    if event.key == pygame.K_s:
                        fname = datetime.now().strftime("canvas_%Y%m%d_%H%M%S.png")
                        pygame.image.save(canvas, fname)
                        set_status(fname)
                    continue

                ch = event.unicode.upper() if event.unicode else ""
                for i, (_, k, _) in enumerate(TOOLS):
                    if ch == k:
                        active_tool_idx = i

                if event.key == pygame.K_1: brush_size_key = 1
                if event.key == pygame.K_2: brush_size_key = 2
                if event.key == pygame.K_3: brush_size_key = 3

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                used = False

                for i, r in enumerate(tool_buttons):
                    if r.collidepoint(pos):
                        active_tool_idx = i
                        used = True

                for i, r in enumerate(size_buttons):
                    if r.collidepoint(pos):
                        brush_size_key = i+1
                        used = True

                for r, c in swatches:
                    if r.collidepoint(pos):
                        active_color = c
                        used = True

                if not used and in_canvas(pos):
                    drawing = True
                    current_tool().on_mouse_down(canvas, canvas_pos(pos), active_color, current_size())

            elif event.type == pygame.MOUSEMOTION:
                if drawing and in_canvas(event.pos):
                    current_tool().on_mouse_move(canvas, canvas_pos(event.pos), active_color, current_size())

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if drawing:
                    current_tool().on_mouse_up(canvas, canvas_pos(event.pos), active_color, current_size())
                    drawing = False

        screen.fill(BG_COLOR)
        pygame.draw.rect(screen, TOOLBAR_COLOR, (0,0,TOOLBAR_W,WINDOW_H))
        pygame.draw.line(screen, PANEL_BORDER, (TOOLBAR_W,0),(TOOLBAR_W,WINDOW_H),2)

        label(screen, font_big, "Paint", (PAD,10), ACCENT)

        for i, (name, shortcut, _) in enumerate(TOOLS):
            r = tool_buttons[i]
            active = i == active_tool_idx
            draw_rounded_rect(screen, ACCENT if active else (45,45,58), r, 6, 1,
                              ACCENT if active else PANEL_BORDER)
            txt = font_sm.render(f"{shortcut} {name}", True,
                                 (255,255,255) if active else TEXT_COLOR)
            screen.blit(txt, txt.get_rect(center=r.center))

        for i, r in enumerate(size_buttons):
            active = brush_size_key == i+1
            draw_rounded_rect(screen, ACCENT if active else (45,45,58), r, 6, 1,
                              ACCENT if active else PANEL_BORDER)
            txt = font_sm.render(["S","M","L"][i], True,
                                 (255,255,255) if active else TEXT_COLOR)
            screen.blit(txt, txt.get_rect(center=r.center))

        for r, c in swatches:
            pygame.draw.rect(screen, c, r)
            if c == active_color:
                pygame.draw.rect(screen, (255,255,255), r, 2)

        screen.blit(canvas, (CANVAS_X,0))

        if drawing or (isinstance(current_tool(), TextTool) and current_tool().active):
            preview = canvas.copy()
            current_tool().draw_preview(preview, canvas_pos(mouse), active_color, current_size())
            screen.blit(preview, (CANVAS_X,0))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()