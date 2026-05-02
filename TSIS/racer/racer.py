import pygame

LANES = [140, 200, 260, 320]


class Racer:

    def __init__(self):

        self.lane = 1
        self.x = LANES[self.lane]
        self.y = 560

        self.target_x = self.x

        self.cooldown = 0  # 🔥 защита от спама

    def move_left(self):

        if self.cooldown <= 0:
            self.lane = max(0, self.lane - 1)
            self.target_x = LANES[self.lane]
            self.cooldown = 0.15

    def move_right(self):

        if self.cooldown <= 0:
            self.lane = min(3, self.lane + 1)
            self.target_x = LANES[self.lane]
            self.cooldown = 0.15

    def update(self):

        self.x += (self.target_x - self.x) * 0.25

        self.cooldown -= 0.016

    def rect(self):
        return pygame.Rect(self.x - 12, self.y - 24, 24, 48)

    def draw(self, screen):

        x = int(self.x)
        y = int(self.y)

        pygame.draw.polygon(screen,(80,160,255),[
            (x,y-25),
            (x+12,y-10),
            (x+12,y+20),
            (x-12,y+20),
            (x-12,y-10)
        ])