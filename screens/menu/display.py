
"""
class: Screen
"""

import pygame

import screens.menu.text
import screens.menu.title

BACKGROUNDCOLOR = pygame.Color("black")
BACKGROUNDTRANS = 224       # 1-255 hoger is zwarter

MENUFONT = None             # todo, nog een ander font kiezen?
MENUFONTSIZE = 50
MENUFONTCOLOR1 = pygame.Color("white")
MENUFONTCOLOR2 = pygame.Color("yellow")

UPKEY = pygame.K_UP
DOWNKEY = pygame.K_DOWN
SELECTKEY1 = pygame.K_RETURN
SELECTKEY2 = pygame.K_KP_ENTER


class Display(object):
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
        if self.show_title:
            self.title = screens.menu.title.Title()
            self.title.set_position(bg_width)

        self.menu_items = itemsmenu     # het object OrderedDict genaamd inside
        self.menu_texts = []            # een list van MenuText objecten
        for index, item in enumerate(self.menu_items):
            menu_text = screens.menu.text.Text(item, index, MENUFONT, MENUFONTSIZE, MENUFONTCOLOR1)
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
            if event.key == UPKEY and self.cur_item > 0:
                self.audio.play_sound(self.audio.switch)
                self.cur_item -= 1
            elif event.key == UPKEY and self.cur_item == 0:
                self.audio.play_sound(self.audio.error)
                self.cur_item = 0
            elif event.key == DOWNKEY and self.cur_item < len(self.menu_texts) - 1:
                self.audio.play_sound(self.audio.switch)
                self.cur_item += 1
            elif event.key == DOWNKEY and self.cur_item == len(self.menu_texts) - 1:
                self.audio.play_sound(self.audio.error)
                self.cur_item = len(self.menu_texts) - 1

            if event.key in (SELECTKEY1, SELECTKEY2):
                self.audio.play_sound(self.audio.select)
                return self.menu_texts[self.cur_item].func
