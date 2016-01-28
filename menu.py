
"""
class: MenuTitel
class: MenuText
class: GameMenu
"""

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


class MenuTitle(object):
    """
    De mainmenu titel.
    """
    def __init__(self):
        self.text = TITLETEXT
        self.font = pygame.font.SysFont(TITLEFONT, TITLEFONTSIZE)
        self.font_color = TITLEFONTCOLOR
        self.label = self.font.render(self.text, 1, self.font_color)
        self.width = self.label.get_width()
        self.height = self.label.get_height()
        self.position = (0, 0)


class MenuText(object):
    """
    Een mainmenu item.
    """
    def __init__(self, item, font, size, color):
        self.func = item[0]     # de eerste van de double tuple, bijv NewGame
        self.text = item[1]     # de tweede van de double tuple, bijv New Game
        self.font = pygame.font.SysFont(font, size)
        self.font_color = color
        self.label = self.font.render(self.text, 1, self.font_color)
        self.width = self.label.get_width()
        self.height = self.label.get_height()
        self.position = (0, 0)

    def set_font_color(self, color):
        """
        Geef een menu item een bepaalde kleur.
        :param color: pygame.Color("kleurnaam")
        """
        self.font_color = color
        self.label = self.font.render(self.text, 1, self.font_color)


class GameMenu(object):
    """
    Een menuscherm.
    """
    def __init__(self, screen, audio, itemsmenu, title):
        self.screen = screen
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(BACKGROUNDCOLOR)
        self.background.set_alpha(224)  # hij doet niets met de alpha als bij handle_view geen bg wordt meegegeven
        self.background = self.background.convert()

        bg_width = self.background.get_width()
        bg_height = self.background.get_height()

        self.audio = audio

        self.show_title = title
        self.title = MenuTitle()        # ook als hij geen title heeft doet hij dit, maar hij laat het toch niet zien
        pos_x = (bg_width/2) - (self.title.width/2)
        pos_y = TITLEPOSY
        self.title.position = (pos_x, pos_y)

        self.menu_items = itemsmenu     # het object OrderedDict genaamd inside
        self.menu_texts = []            # een list van MenuText objecten
        for index, item in enumerate(self.menu_items):
            menu_text = MenuText(item, MENUFONT, MENUFONTSIZE, MENUFONTCOLOR1)
            t_h = len(self.menu_items) * menu_text.height                 # t_h: total height of text block
            pos_x = (bg_width/2) - (menu_text.width/2)
            pos_y = ((bg_height/2) - (t_h/2)) + (menu_text.height * index * 2)

            menu_text.position = (pos_x, pos_y)
            self.menu_texts.append(menu_text)

        self.cur_item = 0

    def handle_view(self, bg=None):
        """
        Reset eerst alle kleuren.
        Zet dan de geselecteerde op een andere kleur.
        Teken de (overworld screencapture) -> achtergrond -> (titel) -> menuitems.
        :param bg: screen capture van de overworld
        """
        for item in self.menu_texts:
            item.set_font_color(MENUFONTCOLOR1)
        self.menu_texts[self.cur_item].set_font_color(MENUFONTCOLOR2)

        if bg is not None:
            self.screen.blit(bg, (0, 0))

        self.screen.blit(self.background, (0, 0))

        if self.show_title:
            self.screen.blit(self.title.label, self.title.position)

        for item in self.menu_texts:
            self.screen.blit(item.label, item.position)

    def handle_single_input(self, event):
        """
        Geef de tekst van het geselecteerde menuitem terug aan het spel.
        :param event: pygame.event.get() uit screen.py
        """
        if event.key == pygame.K_UP and self.cur_item > 0:
            self.audio.play_sound(self.audio.switch)
            self.cur_item -= 1
        elif event.key == pygame.K_UP and self.cur_item == 0:
            self.audio.play_sound(self.audio.error)
            self.cur_item = 0
        elif event.key == pygame.K_DOWN and self.cur_item < len(self.menu_texts) - 1:
            self.audio.play_sound(self.audio.switch)
            self.cur_item += 1
        elif event.key == pygame.K_DOWN and self.cur_item == len(self.menu_texts) - 1:
            self.audio.play_sound(self.audio.error)
            self.cur_item = len(self.menu_texts) - 1

        if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
            self.audio.play_sound(self.audio.select)
            return self.menu_texts[self.cur_item].func
