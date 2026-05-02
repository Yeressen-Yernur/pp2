import pygame
import random

LANES = [140,200,260,320]

class Obstacle:

    def __init__(self):
        self.x = random.choice(LANES)
        self.y = -60
        self.kind = random.choice(["oil","barrier"])
        self.size = 30

        self.color = (40,40,40) if self.kind=="oil" else (200,50,50)
        self.speed = 6

    def update(self):
        self.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen,self.color,(self.x,self.y,self.size,self.size))

    def rect(self):
        return pygame.Rect(self.x,self.y,self.size,self.size)