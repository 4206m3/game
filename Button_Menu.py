import pygame as pg
from parameters import *
from img_file import *

def print_text(message,x,y, textFont, textSize, textColor=(200,200,150)):
    newFont=pg.font.Font(textFont, textSize)
    newText=newFont.render(message, True, textColor)
    screen.blit(newText, (x,y))
    return newText

class Button:
    def __init__(self, width, heigth):
        self.width = width
        self.height = heigth
        self.inactive_color = (26, 31, 25)
        self.active_color = WHITE

    def draw(self, x, y, message, action=None, font_size=20):
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pg.draw.rect(screen, self.active_color, (x, y, self.width, self.height))
            if click[0] == 1 and action is not None:
                action()

        else:
            pg.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))
        print_text(message=message, x=x + 5, y=y + 5, textFont=None, textSize=font_size)
class But_little:
    def __init__(self, width, heigth):
        self.width = width
        self.height = heigth
        self.inactive_color = (26, 31, 25)
        self.active_color = WHITE

    def draw(self, surf,img, x, y, player, font_size=20):
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            if click[0] == 1 and not player:
                pg.draw.rect(screen, self.active_color, (x, y, self.width, self.height))
                player=True
            elif click[0] == 1 and player:
                pg.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))
                player=False
        else:
            if player:
                pg.draw.rect(screen, self.active_color, (x, y, self.width, self.height))
            else:
                pg.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))
        img_rect = img.get_rect()
        img_rect.x=x+2
        img_rect.y = y+2
        surf.blit(img, img_rect)
        return player
def game():
    global menu
    menu = False
    return menu


def main_menu():
    
    screen = pg.display.set_mode((WIDTH, HEIGHT))

    bgdtile = load_image("data/menu_bg1.jpg")
    screen.blit(bgdtile, (0, 0))
    pg.display.flip()
    
    clock = pg.time.Clock()
    start = Button(200, 20)
    quit_but = Button(200, 20)
    tank_bttn=But_little(30,20)
    hel_bttn=But_little(45,20)
    base_font = pg.font.Font(None, 20)
    global user_text
    # create rectangle
    input_rect = pg.Rect(600, 550, 200, 20)
    input_rect_2=pg.Rect(600, 575, 200, 20)
    # color_active stores color(lightskyblue3) which
    # gets active when input box is clicked by user
    color_active = pg.Color(45, 45, 30)
    # color_passive store color(chartreuse4) which is
    # color of input box.
    color_passive = pg.Color(BLUE)
    color = color_passive
    color2 = color_passive
    active = False
    active2 = False
    user_text_2= "Имя(вертолет)"
    player_tank = True
    player_helicopter = False
    global menu
    menu= True
    while menu:
        clock.tick(1000)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            start.draw(600, 475, "Играть!", game)
            quit_but.draw(600, 500, "Выход", quit)
            player_tank=tank_bttn.draw(screen,tank_mini_img, 720, 525, player_tank)
            player_helicopter=hel_bttn.draw(screen,hel_mini_img, 754, 525, player_helicopter)
            print_text("Режим игры", 607, 527, None, 20)
            if event.type == pg.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            if active:
                if event.type == pg.KEYDOWN:
                    # Check for backspace
                    if event.key == pg.K_RETURN:
                        active = False
                    elif event.key == pg.K_BACKSPACE:
                        # get text input from 0 to -1 i.e. end.
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode
                        # user_text += event.Text.Unicode
                color = color_active
            else:
                color = color_passive
            if event.type == pg.MOUSEBUTTONDOWN:
                if input_rect_2.collidepoint(event.pos):
                    active2 = True
                else:
                    active2 = False
            if active2:
                if event.type == pg.KEYDOWN:
                # Check for backspace
                    if event.key == pg.K_RETURN:
                        active = False
                    elif event.key == pg.K_BACKSPACE:
                    # get text input from 0 to -1 i.e. end.
                        user_text_2 = user_text_2[:-1]
                    else:
                        user_text_2 += event.unicode
                    # user_text += event.Text.Unicode
                color2 = color_active
            else:
                color2 = color_passive
        # draw rectangle and argument passed which should
        # be on screen
        pg.draw.rect(screen, color, input_rect)
        text_surface = base_font.render(user_text, True, (255, 255, 255))
        # render at position stated in arguments
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

        # set width of textfield so that text cannot get
        # outside of user's text input
        input_rect.w = max(100, text_surface.get_width() + 10)


        pg.draw.rect(screen, color2, input_rect_2)
        text_surface_2 = base_font.render(user_text_2, True, (255, 255, 255))
        # render at position stated in arguments
        screen.blit(text_surface_2, (input_rect_2.x + 5, input_rect_2.y + 5))

        # set width of textfield so that text cannot get
        # outside of user's text input
        input_rect_2.w = max(100, text_surface_2.get_width() + 10)
        pg.display.update()
    return user_text, user_text_2, player_tank, player_helicopter


