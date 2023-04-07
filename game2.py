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
from Button_Menu import *
import pygame
import pygame as pg
from img_file import *
from parameters import *
from helicopter import *
from mobs import *
from tank import *
from explosion import *
from priz import *


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

user_text, user_text_2 = main_menu()
pg.mixer.pre_init(44100, -16, 1, 512)  # важно вызвать до pygame.init()


pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))

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

# Initialize Game Groups
shots = pg.sprite.Group()
shot_sm = pg.sprite.Group()
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
Shot_small.containers = shot_sm, all
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
hel = Helicopter()
hel.rect.left = 0
hel.rect.top = HEIGHT / 2

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
                dead2 = False
                tank1 = Tank()
                tank1.rect.left = 0
                hel = Helicopter()
                hel.rect.left = 0
                hel.rect.top = HEIGHT / 2
                screen.blit(background, (0, 0))  # удаляем текст Game
                score1 = 0
                score2 = 0

    tank1.power_up()
    # проверьте, не попал ли танк в ракету
    hits = pg.sprite.groupcollide(miss, shots, True, True)
    for hit in hits:
        score1 += 5
        # random.choice(expl_sounds).play()
        expl_sound.play()  # звук взрыва при попадании в ракету
        Explosion(hit, 'lg')
        newmiss()
    # выстрел вертолета+ракета
    hits = pg.sprite.groupcollide(miss, shot_sm, True, True)
    for hit in hits:
        score2 += 5
        # random.choice(expl_sounds).play()
        expl_sound.play()  # звук взрыва при попадании в ракету
        Explosion(hit, 'lg')
        newmiss()
        # проверьте, не попал ли вертолет в бомбу
    hits = pg.sprite.groupcollide(bombs, shot_sm, True, True)
    for hit in hits:
        score2 += 5
        # random.choice(expl_sounds).play()
        expl_sound.play()  # звук взрыва при попадании в ракету
        Explosion(hit, 'lg')
        newmiss()
    hits = pg.sprite.groupcollide(bombs, shots, True, True)
    for hit in hits:
        score1 += 5
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
    # Проверка на столкновение с призом helicopter
    hits = pg.sprite.spritecollide(hel, priz, True)
    for hit in hits:
        if hit.type == 'shield':
            hel.shield += random.randrange(30, 50)
            if hel.shield >= 100:
                hel.shield = 100
        if hit.type == 'life_h':
            hel.lives += 1
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
            death_explosion = Explosion(hel, 'player')
            hel.hide()
            hel.lives -= 1
            hel.shield = 100
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
        score1 += 10
    for bomber in pg.sprite.groupcollide(bombers, shot_sm, 1, 1).keys():
        bomber.destroy()
        score2 += 10

    # Столкновение вертолета с бомбером
    hits = pg.sprite.spritecollide(hel, bombers, 1)
    for hit in hits:
        hel.shield -= 50
        Explosion(hit, 'sm')
        newmiss()
        if hel.shield <= 0:
            death_explosion = Explosion(hel, 'player')
            hel.hide()
            hel.lives -= 1
            hel.shield = 100

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

    # Попадание бомб в вертолет
    for bomb in pg.sprite.spritecollide(hel, bombs, 1):
        hel.shield -= 10
        Explosion(hit, 'sm')
        newmiss()
        if hel.shield <= 0:
            death_explosion = Explosion(hel, 'player')
            hel.hide()
            hel.lives -= 1
            hel.shield = 100

    # Если игрок умер, игра окончена
    if tank1.lives == 0:
        tank1.destroy()
        dead1 = True
    if hel.lives == 0:
        hel.kill()
        dead2 = True
    # draw the scene
    dirty = all.draw(screen)
    pg.display.update(dirty)

    # отображение очков 1 игрок
    screen.blit(score_img, (0, 0))
    score_text = font.render("Танк: " + str(score1), True, BLACK)
    screen.blit(score_text, (25, 20))

    # отображение очков 2 игрок
    screen.blit(score_img, (1220, 0))
    score_text = font.render("Вертолет: " + str(score2), True, BLACK)
    screen.blit(score_text, (1245, 20))
    print_text(user_text, 20, 60, None, 45, BLACK))
    print_text(user_text_2, 1100, 50, None, 45, BLACK))
    # вывод текста Game Over
    if dead1 and dead2:
        screen.blit(game_over_text, (470, 250))
        screen.blit(font_PS.render(user_text, True, BLACK), (400, 350))
        screen.blit(font_PS.render("Счет:" + str(score1), True, BLACK), (400, 400))
        screen.blit(font_PS.render(user_text_2, True, BLACK), (600, 350))
        screen.blit(font_PS.render("Счет:" + str(score2), True, BLACK), (600, 400))
        screen.blit(press_space_text, (400, 450))
    draw_lives(screen, 25, 6, tank1.lives,
               tank_mini_img)
    draw_shield_bar(screen, 15, 43, tank1.shield)
    draw_lives(screen, 1250, 6, hel.lives,
               hel_mini_img)
    draw_shield_bar(screen, 1250, 43, hel.shield)
    pg.display.flip()

    # увеличиваем сложность игры через каждые DIFF_LEVEL_TIMER кадров
    diff_level_count_fps += 1
    if diff_level_count_fps > DIFF_LEVEL_TIMER:
        diff_level_count_fps = 0
        newmiss()  # добавляем ракету
        BOMBER_ODDS = int(BOMBER_ODDS * 0.7)  # chances a new bomber appears
        BOMB_ODDS = int(BOMB_ODDS * 0.9)  # chances a new bomb will drop 

pg.quit()
