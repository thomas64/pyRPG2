
"""
class: MenuItem
class: MainMenu
class: OptionsMenu
class: PauseMenu
class: MenuTitel
class: MenuText
class: GameMenu
"""

import collections

import pygame


BACKGROUNDCOLOR = pygame.Color("black")
BACKGROUNDTRANS = 224       # 1-255 hoger is zwarter

TITLETEXT = "pyRPG"
TITLEFONT = 'colonna'
TITLEFONTSIZE = 150
TITLEFONTCOLOR = pygame.Color("red")
TITLEPOSY = 125

MENUFONT = None             # todo, nog een ander font kiezen?
MENUFONTSIZE = 50
MENUFONTCOLOR1 = pygame.Color("white")
MENUFONTCOLOR2 = pygame.Color("yellow")


class MenuItem(object):
    """
    Base class voor de verschillende menu's.
    Je kan er dan de lengte van bepalen, er doorheen loopen, en de attr van opvragen.
    Enums zijn niet aan te passen.
    Gewone attribute strings staan niet op volgorde
    Vandaar gekozen voor een ordereddict.
    """
    def __init__(self):
        self.inside = collections.OrderedDict()

    def __len__(self):                      # om de totale hoogte van alle items te kunnen berekenen, om het blok
        return len(self.inside)             # verticaal te kunnen centreren.

    def __iter__(self):                     # zodat de GameMenu class door alle enum items kan heen lopen
        return iter(self.inside.items())    # om ze te kunnen projecteren.

    def __getattr__(self, key):             # om te controleren op een key zoals 'NewGame' of die gekozen wordt
        return key


class MainMenu(MenuItem):
    """
    De mainmenu items.
    """
    def __init__(self):
        super().__init__()
        self.inside['NewGame'] = 'New Game'
        self.inside['LoadGame'] = 'Load Game'
        self.inside['Options'] = 'Options'
        self.inside['ExitGame'] = 'Exit'


class OptionsMenu(MenuItem):
    """
    De options items. Deze worden geladen uit een bestand en op aangepast.
    """
    def __init__(self, music=None, sound=None):
        super().__init__()

        if music == 1:
            self.inside['Music'] = 'Music: On'
        else:
            self.inside['Music'] = 'Music: Off'
        if sound == 1:
            self.inside['Sound'] = 'Sound: On'
        else:
            self.inside['Sound'] = 'Sound: Off'
        self.inside['Back'] = 'Back'


class PauseMenu(MenuItem):
    """
    De pausemenu items.
    """
    def __init__(self):
        super().__init__()
        self.inside['ContinueGame'] = 'Continue'
        self.inside['SaveGame'] = 'Save Game'
        self.inside['MainMenu'] = 'Main Menu'


class MenuTitle(object):
    """
    De mainmenu titel.
    """
    def __init__(self):
        self.text = TITLETEXT
        self.font = pygame.font.SysFont(TITLEFONT, TITLEFONTSIZE)
        self.font_color = TITLEFONTCOLOR
        self.label = self.font.render(self.text, True, self.font_color)
        self.width = self.label.get_width()
        self.height = self.label.get_height()
        self.position = (0, 0)


class MenuText(object):
    """
    Een mainmenu item.
    """
    def __init__(self, item, index, font, size, color):
        self.func = item[0]     # de eerste van de double tuple, bijv NewGame
        self.text = item[1]     # de tweede van de double tuple, bijv New Game
        self.index = index
        self.font = pygame.font.SysFont(font, size)
        self.font_color = color
        self.label = self.font.render(self.text, True, self.font_color)
        self.rect = self.label.get_rect()
        self.width = self.label.get_width()
        self.height = self.label.get_height()
        self.position = (0, 0)

    def set_font_color(self, color):
        """
        Geef een menu item een bepaalde kleur.
        :param color: pygame.Color("kleurnaam")
        """
        self.font_color = color
        self.label = self.font.render(self.text, True, self.font_color)


class GameMenu(object):
    """
    Een menuscherm.
    """
    def __init__(self, screen, audio, itemsmenu, title):
        self.screen = screen
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(BACKGROUNDCOLOR)
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
            menu_text = MenuText(item, index, MENUFONT, MENUFONTSIZE, MENUFONTCOLOR1)
            t_h = len(self.menu_items) * menu_text.height                 # t_h: total height of text block
            pos_x = (bg_width/2) - (menu_text.width/2)
            pos_y = ((bg_height/2) - (t_h/2)) + (menu_text.height * index * 2)

            menu_text.position = (pos_x, pos_y)
            menu_text.rect.topleft = menu_text.position
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
            self.screen.blit(bg, (0, 0))                    # gooi over het hele scherm de overworld achtergrond
            self.background.set_alpha(BACKGROUNDTRANS)      # maak de zwarte 'background' transparant

        self.screen.blit(self.background, (0, 0))

        if self.show_title:
            self.screen.blit(self.title.label, self.title.position)

        for item in self.menu_texts:
            self.screen.blit(item.label, item.position)

    def handle_single_input(self, event):
        """
        Geef de key van het geselecteerde menuitem terug aan het spel.
        :param event: pygame.event.get() uit engine.py
        :return: de key, bijv. 'LoadGame'
        """
        if event.type == pygame.MOUSEMOTION:
            for item in self.menu_texts:
                if item.rect.collidepoint(event.pos):
                    if self.cur_item != item.index:
                        self.cur_item = item.index
                        self.audio.play_sound(self.audio.switch)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for item in self.menu_texts:
                    if item.rect.collidepoint(event.pos):
                        self.audio.play_sound(self.audio.select)
                        return item.func

        elif event.type == pygame.KEYDOWN:
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