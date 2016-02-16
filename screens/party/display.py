
"""
class: Screen
"""

import pygame

import screens.party.herobox
import screens.party.infobox
import screens.party.statsbox
import screens.sprites


BACKGROUNDCOLOR = pygame.Color("black")
LINECOLOR = pygame.Color("white")


class Display(object):
    """
    Overzicht scherm PartyScreen.
    """
    def __init__(self, data, screen):
        self.screen = screen
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(BACKGROUNDCOLOR)
        self.background = self.background.convert()

        self.key_input = pygame.key.get_pressed()       # dit is voor de mousepress op een button.

        cur_hero = data.party['alagos']

        self.party = list(data.party.values())
        self.hc = self.party.index(cur_hero)

        self._init_buttons()
        self._init_boxes()

        self.info_label = ""

    def _init_buttons(self):
        bg_width = self.background.get_width()
        button_c = screens.sprites.ButtonSprite(80, 30, (bg_width - 90, 10), "Close", pygame.K_ESCAPE)
        button_q = screens.sprites.ButtonSprite(80, 30, (bg_width - 90, 45), "Previous", pygame.K_q)
        button_w = screens.sprites.ButtonSprite(80, 30, (bg_width - 90, 80), "Next", pygame.K_w)
        self.buttons = (button_c, button_q, button_w)

    def _init_boxes(self):
        self.hero_boxes = []
        for index, hero in enumerate(self.party):
            self.hero_boxes.append(screens.party.herobox.HeroBox((10 + index * 260, 10), index, hero))

        self.stats_box = screens.party.statsbox.StatsBox((10, 120))
        self.info_box = screens.party.infobox.InfoBox((10, 630))
        pygame.draw.rect(self.background, LINECOLOR, (425,  120, 315, 670), 1)
        pygame.draw.rect(self.background, LINECOLOR, (750,  120, 315, 670), 1)
        pygame.draw.rect(self.background, LINECOLOR, (1075, 120, 315, 670), 1)

    def handle_view(self):
        """
        screen -> achtergond -> knoppen -> heroboxes -> verder
        """
        self.screen.blit(self.background, (0, 0))

        for button in self.buttons:
            button.draw(self.screen, self.key_input)

        for hero_box in self.hero_boxes:
            hero_box.select(self.hc)
            hero_box.draw(self.screen)

        cur_hero = self.party[self.hc]

        self.stats_box.draw(self.screen, cur_hero)
        self.info_box.draw(self.screen, self.info_label)

        # name2 = self.largefont.render(cur_hero.NAM, True, FONTCOLOR)   = voorbeeld van hoe een naam buiten een herobox
        # name2_rect = self.screen.blit(name2, (500, 300))

    def handle_multi_input(self, key_input, mouse_pos):
        """
        Registreert of er op de buttons wordt geklikt. En zet dat om naar keyboard input.
        :param key_input: pygame.key.get_pressed()
        :param mouse_pos: pygame.mouse.get_pos()
        """
        self.key_input = key_input

        for button in self.buttons:
            self.key_input = button.multi_click(mouse_pos, self.key_input)

    def handle_single_mouse_motion(self, event):
        """
        Handelt mouse events af.
        :param event: pygame.MOUSEMOTION uit engine.py
        """
        if self.stats_box.rect.collidepoint(event.pos):
            self.info_label = self.stats_box.mouse_hover(event)

    def handle_single_mouse_input(self, event):
        """
        Handelt mouse events af.
        :param event: pygame.MOUSEBUTTONDOWN uit engine.py
        """
        if event.button == 1:
            for hero_box in self.hero_boxes:
                self.hc = hero_box.single_click(event, self.hc)

            for button in self.buttons:
                button_press = button.single_click(event)
                if button_press == pygame.K_ESCAPE:
                    return button_press
                elif button_press == pygame.K_q:
                    self._previous()
                    break
                elif button_press == pygame.K_w:
                    self._next()
                    break
            return                                  # als het niet de ESC button is, return niets.

    def handle_single_keyboard_input(self, event):
        """
        Handelt keyboard events af.
        :param event: pygame.KEYDOWN uit engine.py
        """
        if event.key == pygame.K_q:
            self._previous()
        elif event.key == pygame.K_w:
            self._next()
        # elif event.key == pygame.K_m:
        #     self.party[0].lev.qty += 1

    def _previous(self):
        self.hc -= 1
        if self.hc < 0:
            self.hc = len(self.party) - 1

    def _next(self):
        self.hc += 1
        if self.hc > len(self.party) - 1:
            self.hc = 0
