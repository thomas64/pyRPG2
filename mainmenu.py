
"""
class: MenuItem
class: MenuTitel
class: MenuText
class: MainMenu
"""

import enum
import os

import pygame


BACKGROUNDCOLOR = pygame.Color("black")

TITLETEXT = "pyRPG"
TITLEFONT = 'colonna'
TITLEFONTSIZE = 150
TITLEFONTCOLOR = pygame.Color("red")
TITLEPOSY = 125

MENUFONT = None
MENUFONTSIZE = 50
MENUFONTCOLOR1 = pygame.Color("white")
MENUFONTCOLOR2 = pygame.Color("yellow")

SOUNDSPATH = 'resources/sounds'
MENUSWITCHSOUND = os.path.join(SOUNDSPATH, 'mainmenu_switch.wav')
MENUSELECTSOUND = os.path.join(SOUNDSPATH, 'mainmenu_select.wav')
MENUERRORSOUND = os.path.join(SOUNDSPATH,  'mainmenu_error.wav')


class MenuItem(enum.Enum):
    """
    De menuitems.
    """
    NewGame = 'New Game'
    LoadGame = 'Load Game'
    ExitGame = 'Exit'

    def __iter__(self):
        return iter(self)


class MenuTitle(object):
    """
    De mainmenu titel.
    """
    def __init__(self):
        self.text = TITLETEXT
        self.font = pygame.font.SysFont(TITLEFONT, TITLEFONTSIZE)
        self.font_color = TITLEFONTCOLOR
        self.label = self.font.render(self.text, 1, self.font_color)
        self.width = self.label.get_rect().width
        self.height = self.label.get_rect().height
        self.position = (0, 0)

    def set_position(self, x, y):
        """
        Zet de titel op een bepaalde positie.
        :param x: x-positie
        :param y: y-positie
        """
        self.position = (x, y)


class MenuText(object):
    """
    Een mainmenu item.
    """
    def __init__(self, item, font, size, color):
        self.func = item
        self.text = item.value
        self.font = pygame.font.SysFont(font, size)
        self.font_color = color
        self.label = self.font.render(self.text, 1, self.font_color)
        self.width = self.label.get_rect().width
        self.height = self.label.get_rect().height
        self.position = (0, 0)

    def set_position(self, x, y):
        """
        Zet een menu item op een bepaalde positie.
        :param x: x-positie
        :param y: y-positie
        """
        self.position = (x, y)

    def set_font_color(self, color):
        """
        Geef een menu item een bepaalde kleur.
        :param color: pygame.Color("kleurnaam")
        """
        self.font_color = color
        self.label = self.font.render(self.text, 1, self.font_color)


class MainMenu(object):
    """
    Het startscherm hoofdmenu.
    """
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(BACKGROUNDCOLOR)
        self.background = self.background.convert()

        bg_width = self.background.get_rect().width
        bg_height = self.background.get_rect().height

        self.title = MenuTitle()
        pos_x = (bg_width/2) - (self.title.width/2)
        pos_y = TITLEPOSY
        self.title.set_position(pos_x, pos_y)

        self.menu_items = []
        all_menu_items = list(MenuItem)
        for index, item in enumerate(all_menu_items):
            menu_item = MenuText(item, MENUFONT, MENUFONTSIZE, MENUFONTCOLOR1)
            t_h = len(all_menu_items) * menu_item.height                 # t_h: total height of text block
            pos_x = (bg_width/2) - (menu_item.width/2)
            pos_y = ((bg_height/2) - (t_h/2)) + (menu_item.height * index * 2)

            menu_item.set_position(pos_x, pos_y)
            self.menu_items.append(menu_item)

        self.cur_item = 0

        self.switch = pygame.mixer.Sound(MENUSWITCHSOUND)
        self.select = pygame.mixer.Sound(MENUSELECTSOUND)
        self.error = pygame.mixer.Sound(MENUERRORSOUND)

    def handle_view(self):
        """
        Reset eerst alle kleuren.
        Zet dan de geselecteerde op een andere kleur.
        Teken de achtergrond -> titel -> menuitems.
        """
        for item in self.menu_items:
            item.set_font_color(MENUFONTCOLOR1)
        self.menu_items[self.cur_item].set_font_color(MENUFONTCOLOR2)

        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.title.label, self.title.position)
        for item in self.menu_items:
            self.screen.blit(item.label, item.position)

    def handle_input(self, event):
        """
        Geef de tekst van het geselecteerde menuitem terug aan het spel.
        :param event: pygame.event.get() uit screen.py
        """
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP and self.cur_item > 0:
                self.switch.play()
                self.cur_item -= 1
            elif event.key == pygame.K_UP and self.cur_item == 0:
                self.error.play()
                self.cur_item = 0
            elif event.key == pygame.K_DOWN and self.cur_item < len(self.menu_items) - 1:
                self.switch.play()
                self.cur_item += 1
            elif event.key == pygame.K_DOWN and self.cur_item == len(self.menu_items) - 1:
                self.error.play()
                self.cur_item = len(self.menu_items) - 1

            if event.key == pygame.K_RETURN:
                self.select.play()
                return self.menu_items[self.cur_item].func
