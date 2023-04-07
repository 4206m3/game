import pygame as pg
from img_file import *
from parameters import *
import random

class Priz(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield','life','life_h'])
        self.image = powerup_images[self.type]
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = -10
        self.vx = random.randrange(-5, 5)
        self.vy = random.randrange(2, 4)
        self.wait = 10000
        self.live = 10000
        self.last_update = pg.time.get_ticks()
        self.last_update2 = pg.time.get_ticks()

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        now = pg.time.get_ticks()
        if now - self.last_update > self.wait:
            self.type = random.choice(['shield', 'life', 'life_h'])
            self.image = powerup_images[self.type]
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = -10
            self.vx = random.randrange(-5, 5)
            self.vy = random.randrange(2, 4)
            self.last_update = pg.time.get_ticks()
        if self.rect.bottom > HEIGHT or self.rect.top < -10:
            self.vy *= -1
        if self.rect.top > self.rect.left < 0 or self.rect.right > WIDTH:
            self.vx *= -1
        if now - self.last_update > self.live:
            self.rect.x = WIDTH + 50
            self.rect.y = HEIGHT + 50
            self.last_update2 = pg.time.get_ticks()


    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY