"""
racer.py  –  Core game-loop and all game objects for TSIS-3 Turbo Racer.
"""
import pygame
import random
import math

# ── colours ──────────────────────────────────────────────────────────────────
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
GRAY   = (130, 130, 130)
DARK   = (20, 20, 30)
ROAD   = (45,  45,  55)
LANE_L = (200, 200, 50)
GRASS  = (40,  100, 40)
ACCENT = (255, 200, 0)
RED    = (220, 50,  50)
GREEN  = (50,  200, 80)
BLUE   = (50,  130, 255)
ORANGE = (255, 140, 0)
PURPLE = (170, 80,  220)
TEAL   = (0,   210, 180)
YELLOW = (255, 220, 0)

CAR_COLORS = {
    "red":    (220, 50,  50),
    "blue":   (50,  130, 255),
    "green":  (50,  200, 80),
    "yellow": (255, 220, 0),
    "purple": (170, 80,  220),
}

DIFF_PARAMS = {
    "easy":   dict(base_speed=4, traffic_int=3.0, obstacle_int=4.0, density_mult=0.5),
    "normal": dict(base_speed=6, traffic_int=2.0, obstacle_int=2.5, density_mult=1.0),
    "hard":   dict(base_speed=9, traffic_int=1.2, obstacle_int=1.5, density_mult=1.5),
}

LANES = 4          # number of driving lanes
GOAL_DIST = 5000   # metres to finish


# ── helpers ───────────────────────────────────────────────────────────────────

def lane_x(lane: int, W: int) -> int:
    road_left  = int(W * 0.15)
    road_right = int(W * 0.85)
    road_w     = road_right - road_left
    lane_w     = road_w // LANES
    return road_left + lane_w * lane + lane_w // 2


def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


# ── drawing helpers ───────────────────────────────────────────────────────────

def draw_car(surface, x, y, color, w=34, h=56, shadow=True):
    if shadow:
        pygame.draw.ellipse(surface, (0, 0, 0), (x - w // 2 + 4, y - h // 2 + h - 6, w, 12))
    body = pygame.Rect(x - w // 2, y - h // 2, w, h)
    pygame.draw.rect(surface, color, body, border_radius=8)
    # windshield
    ww, wh = w - 8, h // 3
    pygame.draw.rect(surface, (150, 230, 255), (x - ww // 2, y - h // 2 + 10, ww, wh), border_radius=4)
    # wheels
    for dx in (-w // 2 - 3, w // 2 - 5):
        for dy in (-h // 3, h // 4):
            pygame.draw.rect(surface, (30, 30, 30), (x + dx, y + dy, 8, 14), border_radius=3)


def draw_enemy_car(surface, x, y, color=(150, 0, 0)):
    draw_car(surface, x, y, color, w=32, h=52, shadow=False)


def draw_road(surface, W, H, scroll_y):
    road_left  = int(W * 0.15)
    road_right = int(W * 0.85)
    # grass
    surface.fill(GRASS)
    # road surface
    pygame.draw.rect(surface, ROAD, (road_left, 0, road_right - road_left, H))
    # shoulder lines
    pygame.draw.line(surface, (200, 200, 0), (road_left,  0), (road_left,  H), 4)
    pygame.draw.line(surface, (200, 200, 0), (road_right, 0), (road_right, H), 4)
    # dashed lane markers
    dash_h, gap = 40, 30
    lane_w = (road_right - road_left) // LANES
    for lane in range(1, LANES):
        lx = road_left + lane * lane_w
        off = scroll_y % (dash_h + gap)
        y = -off
        while y < H:
            pygame.draw.rect(surface, WHITE, (lx - 2, y, 4, dash_h))
            y += dash_h + gap


# ── game object classes ───────────────────────────────────────────────────────

class PlayerCar:
    W_CAR, H_CAR = 34, 56

    def __init__(self, lane: int, W: int, H: int, color):
        self.lane   = lane
        self.W      = W
        self.H      = H
        self.color  = color
        self.x      = float(lane_x(lane, W))
        self.y      = float(H * 0.75)
        self.target_x = self.x
        self.speed  = 0.0          # nitro extra speed (visual)
        self.shield = False
        self.alive  = True

    def move(self, direction: int):
        new = self.lane + direction
        if 0 <= new < LANES:
            self.lane = new
            self.target_x = lane_x(self.lane, self.W)

    def update(self):
        # smooth horizontal slide
        self.x += (self.target_x - self.x) * 0.18

    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x - self.W_CAR // 2, self.y - self.H_CAR // 2,
                           self.W_CAR, self.H_CAR)

    def draw(self, surface):
        draw_car(surface, int(self.x), int(self.y), self.color)
        if self.shield:
            pygame.draw.circle(surface, TEAL,
                                (int(self.x), int(self.y)), 36, 3)


class TrafficCar:
    def __init__(self, lane, W, speed):
        self.lane  = lane
        self.x     = float(lane_x(lane, W))
        self.y     = float(-60)
        self.speed = speed
        colors = [(150, 0, 0), (0, 0, 160), (0, 120, 0), (120, 80, 0)]
        self.color = random.choice(colors)

    def update(self, extra=0.0):
        self.y += self.speed + extra

    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x - 16, self.y - 26, 32, 52)

    def draw(self, surface):
        draw_enemy_car(surface, int(self.x), int(self.y), self.color)

    def off_screen(self, H):
        return self.y > H + 80


class Obstacle:
    """Oil spill, pothole, barrier, speed bump, or nitro strip."""
    TYPES = {
        "oil":       {"color": (80,  80,  100), "w": 60, "h": 30, "label": "OIL"},
        "pothole":   {"color": (40,  30,  20),  "w": 36, "h": 36, "label": "HOLE"},
        "barrier":   {"color": (220, 80,  0),   "w": 44, "h": 18, "label": "WALL"},
        "speedbump": {"color": (200, 200, 0),   "w": 70, "h": 12, "label": "BUMP"},
        "nitrostrip":{"color": (0,   220, 255), "w": 70, "h": 16, "label": "NITRO"},
    }

    def __init__(self, lane, W, scroll_speed):
        self.lane  = lane
        self.x     = float(lane_x(lane, W))
        self.y     = float(-50)
        self.speed = scroll_speed
        self.kind  = random.choice(list(self.TYPES.keys()))
        info       = self.TYPES[self.kind]
        self.w, self.h = info["w"], info["h"]
        self.color = info["color"]
        self.label = info["label"]

    def update(self, extra=0.0):
        self.y += self.speed + extra

    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x - self.w // 2, self.y - self.h // 2, self.w, self.h)

    def draw(self, surface):
        r = self.rect()
        pygame.draw.rect(surface, self.color, r, border_radius=6)
        f = pygame.font.SysFont("consolas", 11, bold=True)
        s = f.render(self.label, True, WHITE)
        surface.blit(s, s.get_rect(center=r.center))

    def off_screen(self, H):
        return self.y > H + 60


class Coin:
    WEIGHTS = [("bronze", 1, (180, 120, 40)),
               ("silver", 3, (200, 200, 210)),
               ("gold",   5, (255, 215, 0)),
               ("gem",   10, (150, 80,  255))]

    def __init__(self, lane, W, scroll_speed):
        self.lane  = lane
        self.x     = float(lane_x(lane, W))
        self.y     = float(-40)
        self.speed = scroll_speed
        pop = random.choices(self.WEIGHTS, weights=[50, 30, 15, 5])[0]
        self.kind, self.value, self.color = pop

    def update(self, extra=0.0):
        self.y += self.speed + extra

    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x - 12, self.y - 12, 24, 24)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 12)
        f = pygame.font.SysFont("consolas", 13, bold=True)
        s = f.render(str(self.value), True, BLACK)
        surface.blit(s, s.get_rect(center=(int(self.x), int(self.y))))

    def off_screen(self, H):
        return self.y > H + 60


class PowerUp:
    KINDS = {
        "nitro":  (ORANGE, "N"),
        "shield": (TEAL,   "S"),
        "repair": (GREEN,  "R"),
    }

    def __init__(self, lane, W, scroll_speed):
        self.lane  = lane
        self.x     = float(lane_x(lane, W))
        self.y     = float(-50)
        self.speed = scroll_speed
        self.kind  = random.choice(list(self.KINDS.keys()))
        self.color, self.symbol = self.KINDS[self.kind]
        self.lifetime = 8.0   # disappear after 8 s if not collected
        self.age      = 0.0

    def update(self, dt, extra=0.0):
        self.y   += self.speed + extra
        self.age += dt

    def expired(self):
        return self.age >= self.lifetime

    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x - 16, self.y - 16, 32, 32)

    def draw(self, surface, t):
        pulse = abs(math.sin(t * 3)) * 0.4 + 0.6
        r = self.rect()
        pygame.draw.rect(surface, self.color, r, border_radius=8)
        # pulsing border
        bw = int(pulse * 3) + 1
        pygame.draw.rect(surface, WHITE, r, bw, border_radius=8)
        f = pygame.font.SysFont("consolas", 18, bold=True)
        s = f.render(self.symbol, True, BLACK)
        surface.blit(s, s.get_rect(center=r.center))

    def off_screen(self, H):
        return self.y > H + 60


# ── main game class ────────────────────────────────────────────────────────────

class RacerGame:
    FPS = 60

    def __init__(self, W, H, settings, username):
        self.W        = W
        self.H        = H
        self.username = username
        self.settings = settings

        diff = settings.get("difficulty", "normal")
        dp   = DIFF_PARAMS.get(diff, DIFF_PARAMS["normal"])
        self.base_speed      = dp["base_speed"]
        self.traffic_int     = dp["traffic_int"]
        self.obstacle_int    = dp["obstacle_int"]
        self.density_mult    = dp["density_mult"]

        car_color_name = settings.get("car_color", "red")
        car_color      = CAR_COLORS.get(car_color_name, (220, 50, 50))
        self.player    = PlayerCar(lane=LANES // 2, W=W, H=H, color=car_color)

        self.scroll_y      = 0.0
        self.scroll_speed  = float(self.base_speed)
        self.distance      = 0       # metres driven
        self.goal_dist     = GOAL_DIST
        self.coins_count   = 0
        self.score         = 0
        self.alive         = True
        self.won           = False
        self.time_elapsed  = 0.0

        self.traffic:   list[TrafficCar] = []
        self.obstacles: list[Obstacle]   = []
        self.coins_objs:list[Coin]       = []
        self.powerups:  list[PowerUp]    = []

        self._traffic_timer  = 0.0
        self._obs_timer      = 0.0
        self._coin_timer     = 0.0
        self._pu_timer_spawn = 0.0

        # power-up state
        self.active_pu       = None   # "nitro" | "shield" | "repair" | None
        self.pu_time_left    = 0.0
        self.nitro_speed_add = 0.0

        # key state
        self._moved = False
        self._move_cooldown = 0.0

    # ── internal helpers ──────────────────────────────────────────────────────

    def _player_safe(self, lane, y_range=120):
        return abs(lane_x(lane, self.W) - self.player.x) > 40 or \
               abs(y_range) > 200

    def _spawn_traffic(self):
        lane = random.randint(0, LANES - 1)
        spd  = self.scroll_speed * 0.7 + random.uniform(-1, 1)
        self.traffic.append(TrafficCar(lane, self.W, spd))

    def _spawn_obstacle(self):
        safe_lane = self.player.lane
        lanes = [l for l in range(LANES) if l != safe_lane or random.random() < 0.15]
        lane = random.choice(lanes) if lanes else random.randint(0, LANES - 1)
        self.obstacles.append(Obstacle(lane, self.W, self.scroll_speed))

    def _spawn_coin(self):
        lane = random.randint(0, LANES - 1)
        self.coins_objs.append(Coin(lane, self.W, self.scroll_speed))

    def _spawn_powerup(self):
        lane = random.randint(0, LANES - 1)
        self.powerups.append(PowerUp(lane, self.W, self.scroll_speed))

    def _activate_pu(self, kind):
        if self.active_pu is not None and self.active_pu != kind:
            return   # only one active at a time
        self.active_pu = kind
        if kind == "nitro":
            self.pu_time_left    = 4.0
            self.nitro_speed_add = self.scroll_speed * 0.6
        elif kind == "shield":
            self.pu_time_left  = 0.0   # until hit
            self.player.shield = True
        elif kind == "repair":
            # instant effect: clear all on-screen obstacles
            self.obstacles.clear()
            self.active_pu = None

    # ── public API ────────────────────────────────────────────────────────────

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT,  pygame.K_a) and self._move_cooldown <= 0:
                self.player.move(-1)
                self._move_cooldown = 0.18
            if event.key in (pygame.K_RIGHT, pygame.K_d) and self._move_cooldown <= 0:
                self.player.move(+1)
                self._move_cooldown = 0.18

    def update(self, dt):
        if not self.alive:
            return

        self._move_cooldown = max(0, self._move_cooldown - dt)
        self.time_elapsed  += dt
        self.scroll_y      += self.scroll_speed
        self.distance      += int(self.scroll_speed * 0.4)

        # difficulty scale: every 500m add a bit of speed
        level = self.distance // 500
        self.scroll_speed = self.base_speed + level * 0.4 * self.density_mult
        extra = self.nitro_speed_add

        # nitro timer
        if self.active_pu == "nitro":
            self.pu_time_left -= dt
            if self.pu_time_left <= 0:
                self.active_pu       = None
                self.nitro_speed_add = 0.0

        # ── spawning ──
        self._traffic_timer  += dt
        self._obs_timer      += dt
        self._coin_timer     += dt
        self._pu_timer_spawn += dt

        spawn_int_traffic = max(0.5, self.traffic_int - level * 0.05 * self.density_mult)
        spawn_int_obs     = max(0.6, self.obstacle_int - level * 0.06 * self.density_mult)

        if self._traffic_timer  >= spawn_int_traffic:
            self._spawn_traffic()
            self._traffic_timer = 0.0
        if self._obs_timer      >= spawn_int_obs:
            self._spawn_obstacle()
            self._obs_timer = 0.0
        if self._coin_timer     >= 1.0:
            self._spawn_coin()
            self._coin_timer = 0.0
        if self._pu_timer_spawn >= 6.0:
            self._spawn_powerup()
            self._pu_timer_spawn = 0.0

        # ── update objects ──
        self.player.update()

        for t in self.traffic:
            t.update(extra)
        for o in self.obstacles:
            o.update(extra)
        for c in self.coins_objs:
            c.update(extra)
        for p in self.powerups:
            p.update(dt, extra)

        # ── collisions ──
        pr = self.player.rect()

        # traffic collision
        for t in self.traffic[:]:
            if pr.colliderect(t.rect()):
                if self.player.shield:
                    self.player.shield = False
                    self.active_pu = None
                    self.traffic.remove(t)
                else:
                    self.alive = False
                    return

        # obstacle collision
        for o in self.obstacles[:]:
            if pr.colliderect(o.rect()):
                if o.kind == "nitrostrip":
                    self._activate_pu("nitro")
                    self.obstacles.remove(o)
                elif o.kind == "speedbump":
                    self.scroll_speed = max(2, self.scroll_speed * 0.6)
                    self.obstacles.remove(o)
                elif o.kind == "oil":
                    self.scroll_speed = max(2, self.scroll_speed * 0.7)
                    self.obstacles.remove(o)
                else:   # pothole / barrier
                    if self.player.shield:
                        self.player.shield = False
                        self.active_pu = None
                        self.obstacles.remove(o)
                    else:
                        self.alive = False
                        return

        # coin pickup
        for c in self.coins_objs[:]:
            if pr.colliderect(c.rect()):
                self.coins_count += c.value
                self.score       += c.value * 10
                self.coins_objs.remove(c)

        # power-up pickup
        for p in self.powerups[:]:
            if pr.colliderect(p.rect()):
                self._activate_pu(p.kind)
                self.score += 50
                self.powerups.remove(p)

        # ── prune off-screen ──
        self.traffic    = [t for t in self.traffic    if not t.off_screen(self.H)]
        self.obstacles  = [o for o in self.obstacles  if not o.off_screen(self.H)]
        self.coins_objs = [c for c in self.coins_objs if not c.off_screen(self.H)]
        self.powerups   = [p for p in self.powerups   if not p.off_screen(self.H) and not p.expired()]

        # distance score
        self.score = self.coins_count * 10 + self.distance // 10

        if self.distance >= self.goal_dist:
            self.won   = True
            self.alive = False

    def draw(self, surface):
        draw_road(surface, self.W, self.H, self.scroll_y)

        for o in self.obstacles:
            o.draw(surface)
        for c in self.coins_objs:
            c.draw(surface)
        for p in self.powerups:
            p.draw(surface, self.time_elapsed)
        for t in self.traffic:
            t.draw(surface)
        self.player.draw(surface)

    @property
    def pu_display_time(self):
        return self.pu_time_left if self.active_pu == "nitro" else -1