import pygame as pg
from parameters import *

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
pg.mixer.pre_init(44100, -16, 1, 512)  # важно вызвать до pygame.init()

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
# доДЕЛАТЬ: звуки
shot1_sound = pg.mixer.Sound('data/shot_1.wav')  # загрузка звукового файла выстрела
expl_sound = pg.mixer.Sound('data/rumble1.ogg')  # загрузка звукового файла взрыва
bomb_sound = pg.mixer.Sound('data/bomba-padaet.wav')  # звук падающей сверху бомбы

if pg.mixer:
    pg.mixer.music.load("data/house_lo.wav")  # подобрать подходящую музыку, эта с примера alien
    pg.mixer.music.play(-1)

score_img = pg.image.load('data/score_fon.png').convert_alpha()  # фон для счета
GameOver_img = pg.image.load('data/bg1366x768.jpg').convert_alpha()  # GameOver



# загрузка фона
# create the background, tile the bgd image
bgdtile = load_image("data/bg1366x768.jpg")
background = pg.Surface(SCREENRECT.size)
for x in range(0, SCREENRECT.width, bgdtile.get_width()):
    background.blit(bgdtile, (x, 0))
screen.blit(background, (0, 0))
# screen.blit(bgdtile, (0, 0))
pg.display.flip()

# Загрузка изображений и назначение спрайтов классам
# (до использования классов, после настройки screen)

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
powerup_images["life_h"] = load_image("data/helicopter_0.png", -1, 0.5)
hel_mini_img= load_image("data/helicopter_0.png", -1, 0.25)
img = load_image("data/bomber.gif")
score_img = pg.image.load('data/score_fon.png').convert_alpha()  # фон для счета
GameOver_img = pg.image.load('data/bg1366x768.jpg').convert_alpha()  # GameOver
tank_img = load_image("data/tank1.png", -1, 0.5)
tank_mini_img = load_image("data/tank1.png", -1, 0.1)
dulo_img = load_image("data/dulo2.png", -1, 0.5)
shot_img=[load_image("data/ball.png", -1)]

