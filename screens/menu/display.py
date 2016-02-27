
"""
class: Screen
"""

import pygame

import screens.menu.animation
import screens.menu.text
import screens.menu.title

BACKGROUNDCOLOR1 = pygame.Color("black")
BACKGROUNDCOLOR2 = pygame.Color("white")
BACKGROUNDTRANS = 224       # 1-255 hoger is zwarter

MENUFONT = None             # todo, nog een ander font kiezen?
MENUFONTSIZE = 50
MENUFONTCOLOR1 = pygame.Color("white")
MENUFONTCOLOR2 = pygame.Color("yellow")
MENUFONTCOLOR3 = pygame.Color("black")
MENUFONTCOLOR4 = pygame.Color("red")

MENUH = 1.5
MENUX = -400
MENUY = -100

CLICKBUTTON = 1
UPKEY = pygame.K_UP
DOWNKEY = pygame.K_DOWN
SELECTKEYS = pygame.K_RETURN, pygame.K_KP_ENTER     # 2 mogelijkheden voor dezelfde constante


class Display(object):
    """
    Een menuscherm.
    """
    def __init__(self, screen, audio, itemsmenu, title, animation):
        self.screen = screen
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

        self.show_title = title
        if self.show_title:
            self.title = screens.menu.title.Title()

        self.show_animation = animation
        if self.show_animation:
            self.animation = screens.menu.animation.Animation()
            self.animation.set_position(bg_width, bg_height)

        self.menu_items = itemsmenu     # het object OrderedDict genaamd inside
        self.menu_texts = []            # een list van MenuText objecten
        for index, item in enumerate(self.menu_items):
            menu_text = screens.menu.text.Text(item, index, MENUFONT, MENUFONTSIZE, self.color1)
            t_h = len(self.menu_items) * menu_text.height                 # t_h: total height of text block
            pos_x = (bg_width - menu_text.width) / 2
            pos_y = ((bg_height - t_h) / 2) + (menu_text.height * index * MENUH)
            if self.show_animation:
                pos_x += MENUX
                pos_y += MENUY

            menu_text.position = (pos_x, pos_y)
            menu_text.rect.topleft = menu_text.position
            self.menu_texts.append(menu_text)

        self.cur_item = 0

    def handle_view(self, dt, bg=None):
        """
        Reset eerst alle kleuren.
        Zet dan de geselecteerde op een andere kleur.
        Teken de (overworld screencapture) -> achtergrond -> (titel) -> menuitems.
        :param dt: self.clock.tick(FPS)/1000.0
        :param bg: screen capture van de overworld
        """
        for item in self.menu_texts:
            item.set_font_color(self.color1)
        self.menu_texts[self.cur_item].set_font_color(self.color2)

        if bg is not None:
            self.screen.blit(bg, (0, 0))                    # gooi over het hele scherm de overworld achtergrond
            self.background.set_alpha(BACKGROUNDTRANS)      # maak de zwarte 'background' transparant

        self.screen.blit(self.background, (0, 0))

        if self.show_animation:
            self.animation.animate(self.screen, dt)

        if self.show_title:
            self.title.draw(self.screen)

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
            if event.button == CLICKBUTTON:
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

            if event.key in SELECTKEYS:
                self.audio.play_sound(self.audio.select)
                return self.menu_texts[self.cur_item].func
