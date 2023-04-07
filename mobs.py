import pygame as pg
from img_file import *
from parameters import *
import random
from explosion import *

class Missle(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = self.images[0]
        self.image = pg.transform.flip(self.image, 1, 0)
        self.image.set_colorkey(WHITE)
        self.image = self.image.copy()
        self.rect = self.image.get_rect()
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = WIDTH - 10
        self.rect.y = random.randrange(HEIGHT - self.rect.height)
        self.vx = random.randrange(-8, 10)
        self.vy = random.randrange(1, 8)
        self.last_update = pg.time.get_ticks()

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy - 1
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 50:
            self.rect.x = WIDTH - 10
            self.rect.y = random.randrange(HEIGHT - self.rect.height)
            self.vx = random.randrange(-8, 10)
            self.vy = random.randrange(1, 8)



class Bomber(pg.sprite.Sprite):
    """Бомбардировщики"""

    speed = 6
    animcycle = 12
    images = []

    def __init__(self):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.top = random.randint(1, HEIGHT / 2)
        self.facing = random.choice((-1, 1)) * Bomber.speed
        self.frame = 0
        if self.facing < 0:
            self.rect.right = SCREENRECT.right
            self.image = self.images[1]

    def destroy(self):
        self.kill()
        Explosion(self, 'lg')
        expl_sound.play()

    def update(self):
        self.rect.move_ip(self.facing, 0)
        if not SCREENRECT.contains(self.rect):
            self.kill()


class Bomb(pg.sprite.Sprite):
    """Бомба"""

    speed = 9
    images = []

    def __init__(self, alien):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=alien.rect.move(0, 5).midbottom)
        bomb_sound.play()

    def update(self):
        """called every time around the game loop.
        Every frame we move the sprite 'rect' down.
        When it reaches the bottom we:
        - make an explosion.
        - remove the Bomb.
        """
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom >= HEIGHT:
            #             Explosion(self)  # доДЕЛАТЬ взрыв
            self.kill()


Missle.images = [load_image("data/spr_missile.png", 1)]
Bomber.images = [img, pg.transform.flip(img, 1, 0)]
Bomb.images = [load_image("data/bomb.gif")]