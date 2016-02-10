
"""
class: PartyScreen
"""

import pygame

import screens.sprites


BACKGROUNDCOLOR = pygame.Color("black")
LINECOLOR = pygame.Color("white")

FONTCOLOR = pygame.Color("white")
FONT = 'impact'
LARGEFONTSIZE = 30
NORMALFONTSIZE = 15


class PartyScreen(object):
    """
    ...
    """
    def __init__(self, data, screen):
        self.screen = screen
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(BACKGROUNDCOLOR)
        self.background = self.background.convert()

        self._paint()
        self._init_buttons()

        self.key_input = pygame.key.get_pressed()       # dit is voor de mousepress op een button.

        self.largefont = pygame.font.SysFont(FONT, LARGEFONTSIZE)
        self.normalfont = pygame.font.SysFont(FONT, NORMALFONTSIZE)

        self.party = data.party.values()

        for index, hero in enumerate(self.party):
            self._set_up(hero, index)

    def _set_up(self, hero, index):
        face = pygame.image.load(hero.FAC)
        face_rect = self.background.blit(face, (11 + index * 260, 11))

        name = self.largefont.render(hero.NAM, True, FONTCOLOR)
        name_rect = self.background.blit(name, (16 + index * 260, 116))

    def _paint(self):
        pygame.draw.rect(self.background, LINECOLOR, (10,    10, 250,  150), 1)
        pygame.draw.rect(self.background, LINECOLOR, (270,   10, 250,  150), 1)
        pygame.draw.rect(self.background, LINECOLOR, (530,   10, 250,  150), 1)
        pygame.draw.rect(self.background, LINECOLOR, (790,   10, 250,  150), 1)
        pygame.draw.rect(self.background, LINECOLOR, (1050,  10, 250,  150), 1)

        pygame.draw.rect(self.background, LINECOLOR, (10,   170, 405,  500), 1)
        pygame.draw.rect(self.background, LINECOLOR, (425,  170, 315,  620), 1)
        pygame.draw.rect(self.background, LINECOLOR, (750,  170, 315,  620), 1)
        pygame.draw.rect(self.background, LINECOLOR, (1075, 170, 315,  620), 1)

    def _init_buttons(self):
        bg_width = self.background.get_width()
        button_c = screens.sprites.ButtonSprite(80, 40, (bg_width - 90,  10), "Close", pygame.K_ESCAPE)
        button_q = screens.sprites.ButtonSprite(80, 40, (bg_width - 90,  70), "Previous", pygame.K_q)
        button_w = screens.sprites.ButtonSprite(80, 40, (bg_width - 90, 120), "Next", pygame.K_w)
        self.buttons = [button_c, button_q, button_w]

    def handle_view(self):
        """
        self.background bij button.draw()? moet dit niet self.screen zijn? ik snap nog niet de voorwaarden.
        bij de rest heb overal self.screen gedaan, maar blijkbaar kan het ook anders.
        """
        self.screen.blit(self.background, (0, 0))

        for button in self.buttons:
            button.draw(self.screen, self.key_input)

        for index, hero in enumerate(self.party):
            level = self.normalfont.render("Level: {:12}".format(hero.lev.qty), True, FONTCOLOR)
            level_rect = self.screen.blit(level, (121 + index * 260, 26))

            hitpoints = self.normalfont.render("HitPoints: {:5}{} {}".format(
                                                                    hero.cur_hp, "/", hero.max_hp), True, FONTCOLOR)
            hitpoints_rect = self.screen.blit(hitpoints, (121 + index * 260, 61))

            pygame.draw.rect(self.screen, LINECOLOR, (121, 91, 130, 15), 1)


    def handle_multi_input(self, key_input, mouse_pos):
        """
        Registreert of er op de buttons wordt geklikt. En zet dat om naar keyboard input.
        :param key_input: pygame.key.get_pressed()
        :param mouse_pos: pygame.mouse.get_pos()
        """
        self.key_input = key_input

        for button in self.buttons:
            self.key_input = button.multi_click(mouse_pos, self.key_input)

    def handle_single_mouse_input(self, event):
        """
        Handelt mouse events af.
        :param event: pygame.MOUSEBUTTONDOWN uit engine.py
        """
        if event.button == 1:
            for button in self.buttons:
                button_press = button.single_click(event)
                if button_press == pygame.K_ESCAPE:
                    return button_press
            return                                  # als het niet de ESC button is, return niets.
