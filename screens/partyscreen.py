
"""
class: PartyScreen
"""

import pygame

import screens.sprites


BACKGROUNDCOLOR = pygame.Color("black")
LINECOLOR = pygame.Color("white")

# todo, faces van heroes goed implementeren
PATH = 'resources/sprites/heroes/'
HEROFACE1 = PATH+'01f_Alagos.png'
HEROFACE2 = PATH+'02f_Luana.png'
HEROFACE3 = PATH+'03f_Grindan.png'
HEROFACE4 = PATH+'04f_Rydalin.png'
HEROFACE5 = PATH+'05f_Codrif.png'
HEROFACE6 = PATH+'06f_Galen.png'
HEROFACE7 = PATH+'07f_Raiko.png'
HEROFACE8 = PATH+'08f_Kiara.png'
HEROFACE9 = PATH+'09f_Luthais.png'
HEROFACE10 = PATH+'10f_Elias.png'
HEROFACE11 = PATH+'11f_Onarr.png'
HEROFACE12 = PATH+'12f_Duilio.png'
HEROFACE13 = PATH+'13f_Iellwen.png'
HEROFACE14 = PATH+'14f_Faeron.png'


class PartyScreen(object):
    """
    ...
    """
    def __init__(self, data, screen):
        self.data = data
        self.screen = screen
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(BACKGROUNDCOLOR)
        self.background = self.background.convert()

        self._paint()
        self._init_buttons()

        self.key_input = pygame.key.get_pressed()       # dit is voor de mousepress op een button.

        party = self.data.party.values()
        for index, hero in enumerate(party):
            self._set_up(hero, index)

    def _set_up(self, hero, index):
        face = pygame.image.load(hero.FAC)
        self.background.blit(face, (11 + index * 260, 11))

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
