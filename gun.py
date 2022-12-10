import math
import random

import pygame as pg

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

WIDTH = 1366
HEIGHT = 700
SCREENRECT = pg.Rect(0, 0, WIDTH, HEIGHT)

def load_image(file, colorkey=None, scale=1):
    """Загрузка и подготовка изображений"""
    try:
        image = pg.image.load(file)
        image = image.convert()
        
        # изменение размера изображения
        size = image.get_size()
        size = (size[0] * scale, size[1] * scale)
        image = pg.transform.scale(image, size)

        # Установка цвета прозрачности
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pg.RLEACCEL)        
    except pg.error:
        raise SystemExit(f'Не удалось загрузить изображение "{file}" {pg.get_error()}')
    return image


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
        self.color = random.choice(GAME_COLORS)
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
    gun_offset_x = 20
    gun_offset_y = 12
    images = []

    def __init__(self):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.reloading = 0
        self.origtop = self.rect.top
        self.facing = 1
        # добавить дуло танку
        
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        

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
        x = self.facing * self.gun_offset_x + self.rect.centerx
        y = self.rect.top+self.gun_offset_y
        return x, y
    
    def targetting(self, event):
        pass
        
    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        if self.f2_on == 1:
            new_ball = Shot(self.gunpos())
            self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
            new_ball.vx = self.f2_power * math.cos(self.an)
            new_ball.vy = - self.f2_power * math.sin(self.an)
            self.f2_on = 0
            self.f2_power = 5
    
    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
                
    def update(self):
        # вызывается на каждом цикле игры
        ...

            
class Shot(pg.sprite.Sprite):
    """Снаряды которыми стреляет танк"""

    images = []

    def __init__(self, pos):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=pos)
        self.x = pos[0]
        self.y = pos[1]
        self.vx = 1
        self.vy = 1
        self.live = 30

    def update(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна.
        """
        self.rect.move_ip(self.vx, -self.vy)
        self.vy = self.vy - 1
        if not SCREENRECT.contains(self.rect):
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
bgdtile = load_image("data/bg1366x768.jpg")
background = pg.Surface(SCREENRECT.size)
for x in range(0, SCREENRECT.width, bgdtile.get_width()):
     background.blit(bgdtile, (x, 0))
screen.blit(background, (0, 0))
# screen.blit(bgdtile, (0, 0))
pg.display.flip()

# доДЕЛАТЬ: звуки

# Загрузка изображений и назначение спрайтов классам
# (до использования классов, после настройки screen)
img = load_image("data/tank1.png", -1, 0.5)
Tank.images = [img, pg.transform.flip(img, 1, 0)]
Shot.images = [load_image("data/ball.png", -1)]

# Initialize Game Groups
shots = pg.sprite.Group()
all = pg.sprite.RenderUpdates()

# assign default groups to each sprite class
Tank.containers = all
Shot.containers = shots, all


clock = pg.time.Clock()
# gun = Gun(screen)
tank1 = Tank()
tank1.rect.left = 0
tank2 = Tank()
tank2.rect.right = WIDTH
# target = Target()
finished = False

while not finished:

    keystate = pg.key.get_pressed()
    # clear/erase the last drawn sprites
    all.clear(screen, background)
    # update all the sprites
    all.update()   
    # handle player input
  
    direction = keystate[pg.K_d] - keystate[pg.K_a]
    tank1.move(direction)
    
    direction = keystate[pg.K_RIGHT] - keystate[pg.K_LEFT]
    tank2.move(direction)
    
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            but1, but2, but3 = pg.mouse.get_pressed()
            if but1:
                tank1.fire2_start(event)
        elif event.type == pg.MOUSEBUTTONUP:
            tank1.fire2_end(event)
        elif event.type == pg.MOUSEMOTION:
            tank1.targetting(event)

    tank1.power_up()
    
    # draw the scene
    dirty = all.draw(screen)
    pg.display.update(dirty)   

    
pg.quit()
