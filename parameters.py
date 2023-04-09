import pygame as pg
MAX_SHOTS = 2  # сколько снарядов может быть на экране
MAX_MISSILES = 3  # сколько ракет может быть на экране
BOMBER_ODDS = 100  # chances a new bomber appears
BOMB_ODDS = 100  # chances a new bomb will drop
BOMBER_RELOAD = 30  # frames between new bomber
TANK_RELOAD = 30  # frames between shots
menu=True
FPS = 30
DIFF_LEVEL_TIMER = FPS * 10  # таймер повышения сложности игры каждые 10 сек

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D

user_text=""
WIDTH = 1366
HEIGHT = 700
SCREENRECT = pg.Rect(0, 0, WIDTH, HEIGHT)
bullet = 0
balls = []
score1=0
score2=0
diff_level_count_fps = 0
dead1 = False
dead2 = False
finished = False
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
user_text="Имя(танк)"
