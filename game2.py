"""
доДЕЛАТЬ:
По нашему собственному ТЗ не хватает:
- возможность ввести имя игрока
- выбора режима игры – 1 или 2 игрока
- сохранить свой рекорд по имени.
- таблица с рекордами
- отражаются очки, жизни и уровень здоровья (доделать для вертолета).
- вывод информации где можно увидеть какими кнопками управлять

Также нужно устранить ряд глюков
- после взрыва игрока (вертолет), спрайт пропадает, но можно продолжать стрелять и играть
- не обязательно: укоротить звук падающей бомбы или прекратить его когда она упала уже...

Дополнительно (если будет время):
- сбалансировать управление вертолетом, он очень быстро умирает....

"""

import math
import random

import pygame
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
clock = pg.time.Clock()

def load_image(file, colorkey=None, scale=1):
    """Загрузка и подготовка изображений load_image(file, colorkey=None, scale=1)
        file - имя файла,
        colorkey - цвет прозрачности или указать -1, тогда цвет прозрачнои будет = пикселю в левом верхнем углу
        scale - это коэфф маштабирования
    """
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


def newmiss():
    m = Missle()
    all.add(m)
    miss.add(m)


def newpriz():
    p = Priz()
    all.add(p)
    priz.add(p)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, GREEN, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)
    
def print_text(message,x,y, textFont, textSize, textColor=(0,0,0)):
    newFont=pg.font.Font(textFont, textSize)
    newText=newFont.render(message, True, textColor)
    screen.blit(newText, (x,y))
    return newText

class Button:
    def __init__(self,width,heigth):
        self.width=width
        self.height=heigth
        self.inactive_color=BLUE
        self.active_color=WHITE
    def draw(self, x,y,message,action=None, font_size=30):
        mouse=pg.mouse.get_pos()
        click=pg.mouse.get_pressed()
        if x< mouse[0]<x+self.width and   y< mouse[1]<y+self.height:
                pg.draw.rect(screen,self.active_color,(x,y,self.width,self.height))
                if click[0] ==1 and action is not None:
                    action()

        else:
            pg.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))
        print_text(message=message, x=x+30, y=y+30, textFont=None, textSize=font_size)
        
def input_text2():
    clock = pygame.time.Clock()
    # basic font for user typed
    base_font = pygame.font.Font(None, 32)
    global user_text
    # create rectangle
    input_rect = pg.Rect(650, 400, 150, 70)
    # color_active stores color(lightskyblue3) which
    # gets active when input box is clicked by user
    color_active = pg.Color(WHITE)
    # color_passive store color(chartreuse4) which is
    # color of input box.
    color_passive = pygame.Color(BLUE)
    color = color_passive
    active = False
    user_text= "Напишите имя"
    run=True
    while run:
       for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quite()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            if event.type == pygame.KEYDOWN:
                # Check for backspace
                if event.key == pygame.K_BACKSPACE:
                    # get text input from 0 to -1 i.e. end.
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode
            if active:
                color = color_active
            else:
                 color = color_passive
        # draw rectangle and argument passed which should
        # be on screen
            pygame.draw.rect(screen, color, input_rect)
            text_surface = base_font.render(user_text, True, (255, 255, 255))
        # render at position stated in arguments
            screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

        # set width of textfield so that text cannot get
        # outside of user's text input
            input_rect.w = max(100, text_surface.get_width() + 10)
        # display.flip() will update only a portion of the
        # screen to updated, not full area
            pygame.display.flip()

        # clock.tick(60) means that for every second at most
        # 60 frames should be passed.
           # clock.tick(60)


def game():
    global menu
    menu=False
    return menu

def main_menu():
    clock = pygame.time.Clock()
    start=Button(150,70)
    quit_but=Button(150,70)
    base_font = pygame.font.Font(None, 32)
    global user_text
    # create rectangle
    input_rect = pg.Rect(650, 400, 150, 70)
    # color_active stores color(lightskyblue3) which
    # gets active when input box is clicked by user
    color_active = pg.Color(WHITE)
    # color_passive store color(chartreuse4) which is
    # color of input box.
    color_passive = pygame.Color(BLUE)
    color = color_passive
    active = False
    user_text = "Напишите имя"
    while menu:
        clock.tick(1000)
        for event in pygame.event.get():
         if event.type == pg.QUIT:
             pg.quit()
             quit()
         screen.fill(BLUE)
        pg.draw.rect(screen,RED, pg.Rect(500,70,450,500))
        start.draw(650,200, "Играть!",game)
        quit_but.draw(650,300, "Выход",quit)
        print_text("ТАНКИ", 620,100,None,85)
        for event in pygame.event.get():
          if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                active = True
            else:
                active = False
          if active:
            if event.type == pygame.KEYDOWN:
            # Check for backspace
              if event.key == pygame.K_RETURN:
                 active=False
              elif event.key == pygame.K_BACKSPACE:
                # get text input from 0 to -1 i.e. end.
                 user_text = user_text[:-1]
              else:
                user_text += event.unicode
                #user_text += event.Text.Unicode
            color = color_active
          else:
            color = color_passive
        # draw rectangle and argument passed which should
        # be on screen
        pygame.draw.rect(screen, color, input_rect)
        text_surface = base_font.render(user_text, True, (255, 255, 255))
        # render at position stated in arguments
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

        # set width of textfield so that text cannot get
        # outside of user's text input
        input_rect.w = max(100, text_surface.get_width() + 10)
        pygame.display.update()




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


class Priz(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'life'])
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
            self.type = random.choice(['shield', 'life'])
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


class Explosion(pg.sprite.Sprite):
    def __init__(self, actor, size):
        pg.sprite.Sprite.__init__(self, self.containers)
        # pg.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = actor.rect.center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


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
        self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1] - 450) / (event.pos[0] - 20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        # FIXIT don't know how to do it
        pg.draw.circle(
            self.screen,
            self.color,
            (10, HEIGHT - 10),
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
        expl_sound.play()
        Explosion(self, 'player')
        self.dulo.kill()
        self.kill()
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
        self.vx = direction*self.speed
        self.vy = 0

    def update(self):
        self.rect.move_ip(self.vx, -self.vy)
        if not SCREENRECT.contains(self.rect):
            self.kill()
            
class Helicopter(pg.sprite.Sprite):

    speed = 0.5
    g = 0.2
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

# Initialize pygame

# if pg.get_sdl_version()[0] == 2:
#    pg.mixer.pre_init(44100, 32, 2, 1024)

pg.mixer.pre_init(44100, -16, 1, 512)  # важно вызвать до pygame.init()

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
#input_text2()
main_menu()


# загрузка фона
# create the background, tile the bgd image
bgdtile = load_image("data/bg1366x768.jpg")
background = pg.Surface(SCREENRECT.size)
for x in range(0, SCREENRECT.width, bgdtile.get_width()):
    background.blit(bgdtile, (x, 0))
screen.blit(background, (0, 0))
# screen.blit(bgdtile, (0, 0))
pg.display.flip()

# доДЕЛАТЬ: звуки
shot1_sound = pg.mixer.Sound('data/shot_1.wav')  # загрузка звукового файла выстрела
expl_sound = pg.mixer.Sound('data/rumble1.ogg')  # загрузка звукового файла взрыва
bomb_sound = pg.mixer.Sound('data/bomba-padaet.wav')  # звук падающей сверху бомбы

if pg.mixer:
    pg.mixer.music.load("data/house_lo.wav")  # подобрать подходящую музыку, эта с примера alien
    pg.mixer.music.play(-1)

# Загрузка изображений и назначение спрайтов классам
# (до использования классов, после настройки screen)
img = load_image("data/tank1.png", -1, 0.5)
tank_mini_img=load_image("data/tank1.png", -1, 0.1)
Tank.images = [img, pg.transform.flip(img, 1, 0)]
Shot.images = [load_image("data/ball.png", -1)]
Shot_small.images = [load_image("data/small_shot.png", -1)]
img = load_image("data/dulo2.png", -1, 0.5)
Dulo.images = [img]
Missle.images = [load_image("data/spr_missile.png", 1)]
score_img = pg.image.load('data/score_fon.png').convert_alpha()  # фон для счета
GameOver_img = pg.image.load('data/bg1366x768.jpg').convert_alpha()  # GameOver
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    img_lg = load_image('data/regularExplosion0{}.png'.format(i), BLACK, 0.5)
    explosion_anim['lg'].append(img_lg)
    img_sm = pg.transform.scale(img_lg, (32, 32))
    explosion_anim['sm'].append(img_sm)

    img = load_image('data/sonicExplosion0{}.png'.format(i), BLACK)
    explosion_anim['player'].append(img)
powerup_images = {}
powerup_images['shield'] = load_image('data/shield.png', WHITE)
powerup_images["life"] = load_image("data/tank1.png", -1, 0.3)

img = load_image("data/bomber.gif")
Bomber.images = [img, pg.transform.flip(img, 1, 0)]
Bomb.images = [load_image("data/bomb.gif")]
Helicopter.images = {}
Helicopter.images['left']=[]
Helicopter.images['right']=[]
Helicopter.num_img = 4
for i in range(4):
    img = load_image("data/helicopter_{}.png".format(i), -1, 1)
    Helicopter.images['left'].append(img)
    Helicopter.images['right'].append(pg.transform.flip(img, 1, 0))
    
    
# Initialize Game Groups
shots = pg.sprite.Group()
bombers = pg.sprite.Group()
bombs = pg.sprite.Group()
lastbomber = pg.sprite.GroupSingle()
all = pg.sprite.RenderUpdates()
miss = pg.sprite.Group()
priz = pg.sprite.Group()
for i in range(MAX_MISSILES):
    newmiss()
newpriz()

# assign default groups to each sprite class
Tank.containers = all
Dulo.containers = all
Shot.containers = shots, all
Shot_small.containers = shots, all
Explosion.containers = all
Bomber.containers = bombers, all, lastbomber
Bomb.containers = bombs, all
Helicopter.containers = all
bomberreload = BOMBER_RELOAD

clock = pg.time.Clock()
# gun = Gun(screen)
tank1 = Tank()
tank1.rect.left = 0
# tank2 = Tank()
# tank2.rect.right = WIDTH
# target = Target()
finished = False
hel = Helicopter()
hel.rect.left = 0
hel.rect.top = HEIGHT/2

score = 0
diff_level_count_fps = 0
dead1 = False

font = pg.font.Font(None, 25)  # шрифт для счета очков

# текст GameOver
font_GO = pg.font.Font(None, 112)
game_over_text = font_GO.render("Game Over", True, BLACK)
font_PS = pg.font.Font(None, 42)
press_space_text = font_PS.render("нажмите пробел для продолжения игры", True, BLACK)

while not finished:
    
    clock.tick(FPS)
        
    keystate = pg.key.get_pressed()
    # clear/erase the last drawn sprites
    all.clear(screen, background)
    # update all the sprites
    all.update()
    # handle player input

    direction = keystate[pg.K_d] - keystate[pg.K_a]
    tank1.move(direction)

    direction = keystate[pg.K_RIGHT] - keystate[pg.K_LEFT]
    hel.move(direction)
    hel.vert_move(keystate[pg.K_UP] - keystate[pg.K_DOWN])
    if keystate[pg.K_RCTRL]:
        hel.fire()
    
    for event in pg.event.get():

        if event.type == pg.QUIT:
            finished = True

        elif event.type == pg.MOUSEBUTTONDOWN:
            but1, but2, but3 = pg.mouse.get_pressed()
            if but1:
                tank1.fire2_start(event)

        elif event.type == pg.MOUSEBUTTONUP and not dead1:  # мертвый танк не стреляет
            tank1.fire2_end(event)

        elif event.type == pg.MOUSEMOTION:
            tank1.targetting(event)

        # продолжение игры после смерти по нажатию ПРОБЕЛ
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                dead1 = False
                tank1 = Tank()
                tank1.rect.left = 0
                screen.blit(background, (0, 0))  # удаляем текст Game

    tank1.power_up()
    # проверьте, не попал ли танк в ракету
    hits = pg.sprite.groupcollide(miss, shots, True, True)
    for hit in hits:
        score += 5
        # random.choice(expl_sounds).play()
        expl_sound.play()  # звук взрыва при попадании в ракету
        Explosion(hit, 'lg')
        newmiss()

    # Проверка на столкновение с призом
    hits = pg.sprite.spritecollide(tank1, priz, True)
    for hit in hits:
        if hit.type == 'shield':
            tank1.shield += random.randrange(30, 50)
            if tank1.shield >= 100:
                tank1.shield = 100
        if hit.type == 'life':
            tank1.lives += 1
        newpriz()

    #  Проверка, не ударил ли моб игрока
    if not dead1:
        hits = pg.sprite.spritecollide(tank1, miss, True)
    for hit in hits:
        expl_sound.play()
        tank1.shield -= 10
        Explosion(hit, 'sm')
        newmiss()
        if tank1.shield <= 0:
            death_explosion = Explosion(tank1, 'player')
            tank1.hide()
            tank1.lives -= 1
            tank1.shield = 100
    hits = pg.sprite.spritecollide(hel, miss, True)
    for hit in hits:
        hel.shield -= 10
        Explosion(hit, 'sm')
        newmiss()
        if hel.shield <= 0:
            hel.destroy()
    if bomberreload:
        bomberreload = bomberreload - 1
    elif not int(random.random() * BOMBER_ODDS):
        Bomber()
        bomberreload = BOMBER_RELOAD

    # Сброс бомбы
    if lastbomber and not int(random.random() * BOMB_ODDS):
        Bomb(lastbomber.sprite)

    # Попадание снарядов в цели
    for bomber in pg.sprite.groupcollide(bombers, shots, 1, 1).keys():
        bomber.destroy()
        score += 10
        
#     # Попадание снарядов в вертолет
#     for shot in pg.sprite.spritecollide(hel, shots, 1):
#         hel.destroy()
        
    # Столкновение вертолета с бомбером
    for bomber in pg.sprite.spritecollide(hel, bombers, 1):
        hel.destroy() 
        
    # Попадание бомб в игрока
    if not dead1:
        hits = pg.sprite.spritecollide(tank1, bombs, 1)
        for hit in hits:
            expl_sound.play()
            tank1.shield -= 50
            Explosion(hit, 'sm')
            if tank1.shield <= 0:
                death_explosion = Explosion(tank1, 'player')
                tank1.hide()
                tank1.lives -= 1
                tank1.shield = 100
                
        # Попадание бомб в танк
        for bomb in pg.sprite.spritecollide(tank1, bombs, 1):
            tank1.destroy()

    # Столкновение вертолета с бомбером
    for bomber in pg.sprite.spritecollide(hel, bombers, 1):
        hel.destroy()
    # Попадание бомб в вертолет
    for bomb in pg.sprite.spritecollide(hel, bombs, 1):
        hel.destroy()

    # Если игрок умер, игра окончена
    if tank1.lives == 0:
        tank1.destroy()
        dead1 = True

    # draw the scene
    dirty = all.draw(screen)
    pg.display.update(dirty)

    # отображение очков 1 игрок
    screen.blit(score_img, (0, 0))
    score_text = font.render("Score 1: " + str(score), True, BLACK)
    screen.blit(score_text, (25, 20))

    # отображение очков 2 игрок
    screen.blit(score_img, (1220, 0))
    score_text = font.render("Score 2:  0", True, BLACK)
    screen.blit(score_text, (1245, 20))
    print_text(user_text, 30,50,None,45,WHITE)
    # вывод текста Game Over
    if dead1:
        screen.blit(game_over_text, (470, 250))
        screen.blit(font_PS.render(user_text, True, BLACK), (400,350))
        screen.blit(font_PS.render("Счет:"+str(score),True,BLACK),(400,400))
        screen.blit(press_space_text, (400, 450))
    draw_lives(screen, 25, 6, tank1.lives,
               tank_mini_img)
    draw_shield_bar(screen, 15, 43, tank1.shield)

    pg.display.flip()
    
    # увеличиваем сложность игры через каждые DIFF_LEVEL_TIMER кадров
    diff_level_count_fps += 1
    if diff_level_count_fps > DIFF_LEVEL_TIMER:
        diff_level_count_fps = 0
        newmiss()  # добавляем ракету
        BOMBER_ODDS = int(BOMBER_ODDS * 0.7)  # chances a new bomber appears
        BOMB_ODDS = int(BOMB_ODDS * 0.9)  # chances a new bomb will drop 
    

pg.quit()

