import pygame as pg
from parameters import *
from img_file import *
import math
from explosion import *
class Dulo(pg.sprite.Sprite):
    """Дуло танка"""
    images = []

    def __init__(self, tank):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.original = self.image
        self.an = 0
        self.rect = self.image.get_rect()
        self.center = (tank.gunpos())
        self.tank = tank
        self.move()

    def move(self):
        x, y = self.tank.gunpos()
        self.center = (x, y)
        self.rect = self.image.get_rect(center=self.center)

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            d_x = event.pos[0] - self.center[0]
            if d_x * self.tank.facing > 0:
                self.an = -math.atan((event.pos[1] - self.center[1]) / d_x) * 180 / 3.14
                if self.tank.facing < 0:
                    self.an = self.an - 180
            else:
                self.an = 90

    def update(self):
        """called every time around the game loop.        """
        rotate = pg.transform.rotate
        self.image = rotate(self.original, self.an)

    def hide(self):
        # временно скрыть дуло
        self.hidden = True

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
        self.dulo = Dulo(self)

        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.shield = 100
        self.lives = 3
        self.hidden = False
        self.hide_timer = pg.time.get_ticks()

    def move(self, direction):
        if direction:
            self.facing = direction
        self.rect.move_ip(direction * self.speed, 0)
        self.rect = self.rect.clamp(SCREENRECT)
        if direction < 0:
            self.image = self.images[0]
        elif direction > 0:
            self.image = self.images[1]
        self.dulo.move()

    def hide(self):
        # временно скрыть игрока
        self.hidden = True
        self.dulo.hide()
        self.hide_timer = pg.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)  # чтобы нельзя было попасть в отсутствующий танк ))

    def print_self(self):
        print(self)

    def destroy(self):
        self.dulo.kill()
        self.kill()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)  # чтобы нельзя было попасть в отсутствующий ))
#         print('убит')

    def gunpos(self):
        x = self.facing * self.gun_offset_x + self.rect.centerx
        y = self.rect.top + self.gun_offset_y
        return x, y

    def targetting(self, event):
        self.dulo.targetting(event)

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        if self.f2_on == 1:
            new_ball = Shot(self.gunpos())
            self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
            new_ball.vx = self.f2_power * math.cos(self.an)
            new_ball.vy = - self.f2_power * math.sin(self.an)
            self.f2_on = 0
            self.f2_power = 5

        shot1_sound.play()

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
Tank.images = [tank_img, pg.transform.flip(tank_img, 1, 0)]
Shot.images = shot_img
Dulo.images = [dulo_img]