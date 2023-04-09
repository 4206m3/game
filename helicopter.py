import pygame as pg
from parameters import *
from img_file import *
from explosion import *
import random
import math
class Shot_small(pg.sprite.Sprite):
    """Пули которыми стреляет вертолет"""
    speed = 15
    images = []

    def __init__(self, pos, direction):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=pos)
        self.x = pos[0]
        self.y = pos[1]
        self.vx = direction * self.speed
        self.vy = 0

    def update(self):
        self.rect.move_ip(self.vx, -self.vy)
        if not SCREENRECT.contains(self.rect):
            self.kill()


class Helicopter(pg.sprite.Sprite):
    speed = 0.3
    g = 0.1
    gun_offset_x = 50
    gun_offset_y = 52
    num_img = 0
    images = []

    def __init__(self):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images['left'][0]
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.reloading = 0
        self.facing = 1
        self.vx = 0
        self.vy = 0

        self.shield = 100
        self.lives = 3
        self.hidden = False
        self.hide_timer = pg.time.get_ticks()

        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 30

    def move(self, direction):
        self.vx = self.vx + direction * self.speed
        if direction:
            self.facing = direction

    def vert_move(self, direction):
        self.vy = self.vy + direction * self.speed

    def destroy(self):
        expl_sound.play()
        Explosion(self, 'player')
        self.kill()

    def gunpos(self):
        x = self.facing * self.gun_offset_x + self.rect.centerx
        y = self.rect.top + self.gun_offset_y
        return x, y

    def fire(self):
        if not self.reloading:  # and len(small_shots) < MAX_SHOTS:
            Shot_small(self.gunpos(), self.facing)
            self.reloading = 10
            shot1_sound.play()

    def update(self):
        # вызывается на каждом цикле игры
        self.rect.move_ip(self.vx, -self.vy)
        self.rect = self.rect.clamp(SCREENRECT)
        if self.rect.bottom < HEIGHT:
            self.vy = self.vy - self.g

        if self.reloading > 0:
            self.reloading -= 1

        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == self.num_img:
                self.frame = 0
            if self.facing < 0:
                self.image = self.images['right'][self.frame]
            else:
                self.image = self.images['left'][self.frame]

    def hide(self):
        # временно скрыть игрока
        self.hidden = True
        self.hide_timer = pg.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)  # чтобы нельзя было попасть в отсутствующий ))
    def destroy(self):
        self.kill()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)  # чтобы нельзя было попасть в отсутствующий ))
Shot_small.images = [load_image("data/small_shot.png", -1)]
Helicopter.images = {}
Helicopter.images['left'] = []
Helicopter.images['right'] = []
Helicopter.num_img = 4
for i in range(4):
    img = load_image("data/helicopter_{}.png".format(i), -1, 1)
    Helicopter.images['left'].append(img)
    Helicopter.images['right'].append(pg.transform.flip(img, 1, 0))
