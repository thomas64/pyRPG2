
"""
class: Display
"""

import pygame

import audio as sfx
import keys
import screens.menu.manager
import screens.menu.text
from statemachine import States

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
    def __init__(self, audio, state_name, menu_content, title, animation, scr_capt, cur_item=0):
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

        self.menu_content = menu_content                        # het object OrderedDict genaamd inside
        self.menu_texts = []                                    # een list van MenuText objecten
        for index, item in enumerate(self.menu_content):
            menu_text = screens.menu.text.Text(item, index, self.color1)
            t_h = len(self.menu_content) * menu_text.height     # t_h: total height of text block
            pos_x = (bg_width - menu_text.width) / 2
            pos_y = ((bg_height - t_h) / 2) + (menu_text.height * index * MENUH)
            if self.animation:
                pos_x += MENUX
                pos_y += MENUY

            menu_text.set_position(pos_x, pos_y)
            self.menu_texts.append(menu_text)

        if cur_item == -1:                          # als -1 wordt meegegeven als argument, selecteer dan de laatste
            self.cur_item = len(self.menu_texts)-1
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
        # if self.name == States.MainMenu:
        #     print(str(self.name) + " on_exit")

    def single_input(self, event):
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
                        self.audio.play_sound(sfx.MENUSWITCH)
                    break

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == keys.LEFTCLICK:
                for item in self.menu_texts:
                    if item.rect.collidepoint(event.pos):
                        self.audio.play_sound(sfx.MENUSELECT)
                        self.menu_content.on_select(item,
                                                    self.title, self.animation, self.scr_capt, self.cur_item)
                        break

        elif event.type == pygame.KEYDOWN:
            if event.key == keys.UP and self.cur_item > 0:
                self.audio.play_sound(sfx.MENUSWITCH)
                self.cur_item -= 1
            elif event.key == keys.UP and self.cur_item == 0:
                self.audio.play_sound(sfx.MENUERROR)
                self.cur_item = 0
            elif event.key == keys.DOWN and self.cur_item < len(self.menu_texts) - 1:
                self.audio.play_sound(sfx.MENUSWITCH)
                self.cur_item += 1
            elif event.key == keys.DOWN and self.cur_item == len(self.menu_texts) - 1:
                self.audio.play_sound(sfx.MENUERROR)
                self.cur_item = len(self.menu_texts) - 1

            if event.key in keys.SELECT:
                self.audio.play_sound(sfx.MENUSELECT)
                self.menu_content.on_select(self.menu_texts[self.cur_item],
                                            self.title, self.animation, self.scr_capt, self.cur_item)
            elif event.key == keys.DELETE:
                self.audio.play_sound(sfx.MENUSELECT)
                self.menu_content.on_delete(self.menu_texts[self.cur_item],
                                            self.scr_capt, self.cur_item)
            elif event.key == keys.EXIT:
                self.audio.play_sound(sfx.MENUSELECT)
                self.menu_content.on_exit()

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
        for item in self.menu_texts:
            item.set_font_color(self.color1)
        self.menu_texts[self.cur_item].set_font_color(self.color2)

        self.screen.blit(self.background, (0, 0))

        if self.scr_capt:
            self.scr_capt.render()

        if self.animation:
            self.animation.render(self.screen)

        if self.title:
            self.title.render(self.screen)

        for item in self.menu_texts:
            self.screen.blit(item.label, item.position)
