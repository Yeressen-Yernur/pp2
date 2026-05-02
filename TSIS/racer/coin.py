import pygame
import random

LANES = [140,200,260,320]

class Coin:

    def __init__(self):
        self.x = random.choice(LANES)
        self.y = -40
        self.value = random.choice([1,3,5])
        self.size = 10 + self.value

        self.color = {
            1:(205,127,50),
            3:(192,192,192),
            5:(255,215,0)
        }[self.value]

        self.speed = 5

    def update(self):
        self.y += self.speed

    def draw(self, screen):
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.size)

    def rect(self):
        return pygame.Rect(self.x-self.size,self.y-self.size,self.size*2,self.size*2)