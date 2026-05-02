import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
GRID = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28)
small_font = pygame.font.SysFont("Arial", 20)

# ---------------- STATES ----------------
MENU = "menu"
NAME = "name"
GAME = "game"
GAME_OVER = "over"

state = MENU

# ---------------- GAME DATA ----------------
snake = []
direction = (GRID, 0)
food = (0, 0)

score = 0
speed = 10
username = ""

def reset_game():
    global snake, direction, food, score, speed
    snake = [(100,100),(80,100),(60,100)]
    direction = (GRID, 0)
    food = spawn_food()
    score = 0
    speed = 10

def spawn_food():
    return (
        random.randint(0, (WIDTH//GRID)-1)*GRID,
        random.randint(0, (HEIGHT//GRID)-1)*GRID
    )

food = spawn_food()

# ---------------- DRAW ----------------
def draw_text(text, x, y, color=(255,255,255), fnt=font):
    img = fnt.render(text, True, color)
    screen.blit(img, (x, y))

def draw_menu():
    screen.fill((20,20,20))
    draw_text("SNAKE GAME", 300, 200)
    draw_text("Press ENTER to Start", 250, 260, (180,180,180))

def draw_name():
    screen.fill((20,20,20))
    draw_text("Enter Name:", 300, 200)
    draw_text(username, 300, 260, (0,255,0))
    draw_text("Press ENTER", 300, 320, (180,180,180))

def draw_game():
    screen.fill((25,25,25))

    # food
    pygame.draw.rect(screen, (255,0,0), (*food, GRID, GRID))

    # snake
    for i, p in enumerate(snake):
        color = (0,255,0) if i == 0 else (0,180,0)
        pygame.draw.rect(screen, color, (*p, GRID, GRID))

    draw_text(f"{username} Score: {score}", 10, 10, (255,255,255), small_font)

def draw_game_over():
    screen.fill((20,20,20))
    draw_text("GAME OVER", 300, 180, (255,50,50))
    draw_text(f"Score: {score}", 320, 230)
    draw_text("R - Restart", 320, 280, (180,180,180))
    draw_text("Q - Quit", 320, 320, (180,180,180))

# ---------------- GAME LOGIC ----------------
def move():
    global snake

    head = snake[0]
    new = (head[0]+direction[0], head[1]+direction[1])

    # walls
    if new[0]<0 or new[0]>=WIDTH or new[1]<0 or new[1]>=HEIGHT:
        return False

    if new in snake:
        return False

    snake.insert(0,new)
    snake.pop()
    return True

def check_food():
    global food, score, speed

    if snake[0] == food:
        score += 10
        snake.append(snake[-1])  # grow
        speed = min(speed+1, 25)
        food = spawn_food()

# ---------------- LOOP ----------------
reset_game()

running = True

while running:
    clock.tick(speed if state == GAME else 60)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        # -------- MENU --------
        if state == MENU:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                state = NAME

        # -------- NAME INPUT --------
        elif state == NAME:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    reset_game()
                    state = GAME
                elif e.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += e.unicode

        # -------- GAME --------
        elif state == GAME:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP and direction != (0,GRID):
                    direction = (0,-GRID)
                if e.key == pygame.K_DOWN and direction != (0,-GRID):
                    direction = (0,GRID)
                if e.key == pygame.K_LEFT and direction != (GRID,0):
                    direction = (-GRID,0)
                if e.key == pygame.K_RIGHT and direction != (-GRID,0):
                    direction = (GRID,0)

        # -------- GAME OVER --------
        elif state == GAME_OVER:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    reset_game()
                    state = GAME
                if e.key == pygame.K_q:
                    running = False

    # -------- UPDATE --------
    if state == GAME:
        if not move():
            state = GAME_OVER
        check_food()

    # -------- DRAW --------
    if state == MENU:
        draw_menu()
    elif state == NAME:
        draw_name()
    elif state == GAME:
        draw_game()
    elif state == GAME_OVER:
        draw_game_over()

    pygame.display.flip()

pygame.quit()
sys.exit()