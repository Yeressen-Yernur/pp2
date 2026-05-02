import pygame
import random
import json
from config import *
from db import *

class SnakeGame:
    def __init__(self, username):
        self.username = username
        self.player_id = get_or_create_player(username)

        self.snake = [(100,100)]
        self.direction = (GRID_SIZE, 0)

        self.food = self.spawn_food()
        self.poison = self.spawn_poison()

        self.score = 0
        self.level = 1
        self.speed = 10

        self.settings = self.load_settings()

        self.power_up = None
        self.power_timer = 0

        self.obstacles = []

    def load_settings(self):
        with open("settings.json") as f:
            return json.load(f)

    def spawn_food(self):
        return (random.randint(0, 30)*GRID_SIZE,
                random.randint(0, 30)*GRID_SIZE)

    def spawn_poison(self):
        return (random.randint(0, 30)*GRID_SIZE,
                random.randint(0, 30)*GRID_SIZE)

    def update(self):
        head = self.snake[0]
        new_head = (head[0]+self.direction[0], head[1]+self.direction[1])

        # collision wall
        if new_head[0]<0 or new_head[1]<0 or new_head[0]>=WIDTH or new_head[1]>=HEIGHT:
            return False

        # self collision
        if new_head in self.snake:
            return False

        # obstacles
        if new_head in self.obstacles:
            return False

        self.snake.insert(0, new_head)

        # food
        if new_head == self.food:
            self.score += 10
            self.food = self.spawn_food()
        else:
            self.snake.pop()

        # poison
        if new_head == self.poison:
            self.snake = self.snake[:-2]
            if len(self.snake) <= 1:
                return False
            self.poison = self.spawn_poison()

        return True

    def game_over(self):
        save_game(self.player_id, self.score, self.level)