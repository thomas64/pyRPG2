
"""
class: Display
"""

import pygame

# from constants import GameState
from constants import Keys
from constants import SFX

from .text import MenuText


BACKGROUNDCOLOR1 = pygame.Color("black")
BACKGROUNDCOLOR2 = pygame.Color("white")

MENUFONTCOLOR1 = pygame.Color("white")
MENUFONTCOLOR2 = pygame.Color("yellow")
MENUFONTCOLOR3 = pygame.Color("black")
MENUFONTCOLOR4 = pygame.Color("red")

MENUH = 1.5
MENUX = -305
MENUY = -50


class Display(object):
    """
    Een menuscherm.
    """
    def __init__(self, audio, state_name, menu_object, title, animation, scr_capt, cur_item=0):
        self.screen = pygame.display.get_surface()
        self.background = pygame.Surface(self.screen.get_size())
        if animation:
            self.background.fill(BACKGROUNDCOLOR2)
            self.color1 = MENUFONTCOLOR3
            self.color2 = MENUFONTCOLOR4
        else:
            self.background.fill(BACKGROUNDCOLOR1)
            self.color1 = MENUFONTCOLOR1
            self.color2 = MENUFONTCOLOR2
        self.background = self.background.convert()

        bg_width = self.background.get_width()
        bg_height = self.background.get_height()

        self.audio = audio
        self.name = state_name
        self.title = title
        self.scr_capt = scr_capt
        self.animation = animation
        if self.animation:
            self.animation.set_position(bg_width, bg_height)

        self.menu_content_object = menu_object                          # het menu object met list() genaamd content
        self.list_text_objects = []                                     # een list van MenuText objecten
        for index, item in enumerate(self.menu_content_object.content):
            menu_text_object = MenuText(item, index, self.color1)
            t_h = len(self.menu_content_object.content) * menu_text_object.height   # t_h: total height of text block
            pos_x = (bg_width - menu_text_object.width) / 2
            pos_y = ((bg_height - t_h) / 2) + (menu_text_object.height * index * MENUH)
            if self.animation:
                pos_x += MENUX
                pos_y += MENUY

            menu_text_object.set_position(pos_x, pos_y)
            self.list_text_objects.append(menu_text_object)

        if cur_item == -1:                          # als -1 wordt meegegeven als argument, selecteer dan de laatste
            self.cur_item = len(self.list_text_objects)-1
        else:
            self.cur_item = cur_item

    def on_enter(self):
        """
        Wanneer deze state op de stack komt, voer dit uit.
        Zet muziek en achtergrond geluiden indien nodig.
        """
        self.audio.set_bg_music(self.name)
        self.audio.set_bg_sounds(self.name)

    # noinspection PyMethodMayBeStatic
    def on_exit(self):
        """
        Wanneer deze state onder een andere state van de stack komt, voer dit uit.
        Op dit moment nog niets echts
        """
        pass
        # voorbeeld van gebruik on_exit:
        # if self.name == GameState.MainMenu:
        #     print(str(self.name) + " on_exit")

    def single_input(self, event):
        """
        Geef de key van het geselecteerde menuitem terug aan het spel.
        :param event: pygame.event.get() uit engine.py
        :return: de key, bijv. 'LoadGame'
        """
        if event.type == pygame.MOUSEMOTION:
            for item in self.list_text_objects:
                if item.rect.collidepoint(event.pos):
                    if self.cur_item != item.index:
                        self.cur_item = item.index
                        self.audio.play_sound(SFX.menu_switch)
                    break

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == Keys.Leftclick.value:
                for item in self.list_text_objects:
                    if item.rect.collidepoint(event.pos):
                        self.audio.play_sound(SFX.menu_select)
                        self.menu_content_object.on_select(item,
                                                           self.title, self.animation, self.scr_capt, self.cur_item)
                        break

        elif event.type == pygame.KEYDOWN:
            if event.key == Keys.Up.value and self.cur_item > 0:
                self.audio.play_sound(SFX.menu_switch)
                self.cur_item -= 1
            elif event.key == Keys.Up.value and self.cur_item == 0:
                self.audio.play_sound(SFX.menu_error)
                self.cur_item = 0
            elif event.key == Keys.Down.value and self.cur_item < len(self.list_text_objects) - 1:
                self.audio.play_sound(SFX.menu_switch)
                self.cur_item += 1
            elif event.key == Keys.Down.value and self.cur_item == len(self.list_text_objects) - 1:
                self.audio.play_sound(SFX.menu_error)
                self.cur_item = len(self.list_text_objects) - 1

            if event.key in Keys.Select.value:
                self.audio.play_sound(SFX.menu_select)
                self.menu_content_object.on_select(self.list_text_objects[self.cur_item],
                                                   self.title, self.animation, self.scr_capt, self.cur_item)
            elif event.key == Keys.Delete.value:
                self.audio.play_sound(SFX.menu_select)
                self.menu_content_object.on_delete(self.list_text_objects[self.cur_item],
                                                   self.scr_capt, self.cur_item)
            elif event.key == Keys.Exit.value:
                self.audio.play_sound(SFX.menu_select)
                self.menu_content_object.on_quit()

    # noinspection PyMethodMayBeStatic
    def multi_input(self, key_input, mouse_pos, dt):
        """
        Handelt de ingedrukt-houden muis en keyboard input af.
        :param key_input: pygame.key.get_pressed()
        :param mouse_pos: pygame.mouse.get_pos()
        :param dt: self.clock.tick(FPS)/1000.0
        """
        pass

    def update(self, dt):
        """
        Update de achtergrond animatie.
        :param dt: self.clock.tick(FPS)/1000.0
        """
        if self.animation:
            self.animation.update(dt)

    def render(self):
        """
        Reset eerst alle kleuren.
        Zet dan de geselecteerde op een andere kleur.
        Teken de (overworld screencapture) -> achtergrond -> (titel) -> menuitems.
        """
        for item in self.list_text_objects:
            item.set_font_color(self.color1)
        self.list_text_objects[self.cur_item].set_font_color(self.color2)

        self.screen.blit(self.background, (0, 0))

        if self.scr_capt:
            self.scr_capt.render()

        if self.animation:
            self.animation.render(self.screen)

        if self.title:
            self.title.render(self.screen)

        for item in self.list_text_objects:
            self.screen.blit(item.label, item.position)
