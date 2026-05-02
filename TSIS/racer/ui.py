import pygame

pygame.font.init()

font = pygame.font.Font(None, 36)
small = pygame.font.Font(None, 26)

def draw_game(screen, player, coins, obstacles, score, money):

    screen.fill((30,120,30))
    pygame.draw.rect(screen,(40,40,40),(125,0,250,700))

    pygame.draw.line(screen,(255,255,255),(125,0),(125,700),4)
    pygame.draw.line(screen,(255,255,255),(375,0),(375,700),4)

    player.draw(screen)

    for c in coins:
        c.draw(screen)

    for o in obstacles:
        o.draw(screen)

    screen.blit(small.render(f"Score: {score}",True,(255,255,255)),(10,10))
    screen.blit(small.render(f"Coins: {money}",True,(255,215,0)),(10,40))


def draw_menu(screen):
    screen.fill((10,10,10))
    screen.blit(font.render("RACING GAME",True,(255,255,255)),(130,250))
    screen.blit(small.render("ENTER to start",True,(200,200,200)),(160,320))


def draw_game_over(screen, score, board):

    screen.fill((10,10,10))

    screen.blit(font.render("GAME OVER",True,(255,50,50)),(140,120))
    screen.blit(small.render(f"Score: {score}",True,(255,255,255)),(160,180))
    screen.blit(small.render("Leaderboard:",True,(255,255,255)),(150,240))

    y = 280
    for i,s in enumerate(board[:5]):
        screen.blit(small.render(f"{i+1}. {s}",True,(200,200,200)),(160,y))
        y += 30