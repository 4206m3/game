import math
from random import choice

import pygame as pg

MAX_SHOTS = 2  # сколько снарядов может быть на экране

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600
SCREENRECT = pg.Rect(0, 0, WIDTH, HEIGHT)

def load_image(file):
    """Загрузка и подготовка изображений"""
    try:
        surface = pg.image.load(file)
    except pg.error:
        raise SystemExit(f'Не удалось загрузить изображение "{file}" {pg.get_error()}')
    return surface.convert()

class Ball:
    def __init__(self, screen: pg.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # FIXME
        self.x += self.vx
        self.y -= self.vy

    def draw(self):
        pg.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        # FIXME
        return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        # FIXIT don't know how to do it
        pg.draw.circle(
            self.screen,
            self.color,
            (10, HEIGHT-10),
            10
        )        

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    # self.points = 0
    # self.live = 1
    # FIXME: don't work!!! How to call this functions when object is created?
    # self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(2, 50)
        color = self.color = RED

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        ...


class Tank(pg.sprite.Sprite):

    speed = 10
    gun_offset = -11
    images = []

    def __init__(self):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.reloading = 0
        self.origtop = self.rect.top
        self.facing = -1

    def move(self, direction):
        if direction:
            self.facing = direction
        self.rect.move_ip(direction * self.speed, 0)
        self.rect = self.rect.clamp(SCREENRECT)
        if direction < 0:
            self.image = self.images[0]
        elif direction > 0:
            self.image = self.images[1]

    def gunpos(self):
        pos = self.facing * self.gun_offset + self.rect.centerx
        return pos, self.rect.top

    
class Shot(pg.sprite.Sprite):
    """Снаряды которыми стреляет танк"""

    speed = -11
    images = []

    def __init__(self, pos):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=pos)

    def update(self):
        """called every time around the game loop.
        Every tick we move the shot upwards.
        """
        self.rect.move_ip(0, self.speed)
        if self.rect.top <= 0:
            self.kill()


# Initialize pygame
if pg.get_sdl_version()[0] == 2:
    pg.mixer.pre_init(44100, 32, 2, 1024)
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

# доДЕЛАТЬ: загрузку фона
# create the background, tile the bgd image
bgdtile = load_image("data/background.gif")
background = pg.Surface(SCREENRECT.size)
for x in range(0, SCREENRECT.width, bgdtile.get_width()):
    background.blit(bgdtile, (x, 0))
screen.blit(background, (0, 0))
pg.display.flip()

# доДЕЛАТЬ: звуки

# Загрузка изображений и назначение спрайтов классам
# (до использования классов, после настройки screen)
img = load_image("data/player1.gif")
Tank.images = [img, pg.transform.flip(img, 1, 0)]
Shot.images = [load_image("data/shot.gif")]

# Initialize Game Groups
# aliens = pg.sprite.Group()
shots = pg.sprite.Group()
# bombs = pg.sprite.Group()
all = pg.sprite.RenderUpdates()
# lastalien = pg.sprite.GroupSingle()

# assign default groups to each sprite class
Tank.containers = all
# Alien.containers = aliens, all, lastalien
Shot.containers = shots, all
# Bomb.containers = bombs, all
# Explosion.containers = all
# Score.containers = all

clock = pg.time.Clock()
gun = Gun(screen)
tank1 = Tank()
target = Target()
finished = False

while not finished:
#     screen.fill(WHITE)

    keystate = pg.key.get_pressed()
    # clear/erase the last drawn sprites
    all.clear(screen, background)
    # update all the sprites
    all.update()   
    # handle player input
    direction = keystate[pg.K_RIGHT] - keystate[pg.K_LEFT]
    tank1.move(direction)
    firing = keystate[pg.K_SPACE]
    if not tank1.reloading and firing and len(shots) < MAX_SHOTS:
        Shot(tank1.gunpos())
#         if pg.mixer:
#             shoot_sound.play()
    tank1.reloading = firing    
    
    gun.draw()
    target.draw()
    for b in balls:
        b.draw()

    # draw the scene
    dirty = all.draw(screen)
    pg.display.update(dirty)     

    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pg.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pg.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move()
        if b.hittest(target) and target.live:
            target.live = 0
            target.hit()
            target.new_target()
    gun.power_up()

pg.quit()
