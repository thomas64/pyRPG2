
"""
class: PartyScreen
"""

import pygame

import screens.sprites


BACKGROUNDCOLOR = pygame.Color("black")
LINECOLOR = pygame.Color("white")

# todo, faces van heroes goed implementeren
HEROFACE1 = 'resources/sprites/heroes/01f_Alagos.png'
HEROFACE2 = 'resources/sprites/heroes/02f_Luana.png'
HEROFACE3 = 'resources/sprites/heroes/03f_Grindan.png'
HEROFACE4 = 'resources/sprites/heroes/04f_Rydalin.png'
HEROFACE5 = 'resources/sprites/heroes/05f_Codrif.png'
HEROFACE6 = 'resources/sprites/heroes/06f_Galen.png'
HEROFACE7 = 'resources/sprites/heroes/07f_Raiko.png'
HEROFACE8 = 'resources/sprites/heroes/08f_Kiara.png'
HEROFACE9 = 'resources/sprites/heroes/09f_Luthais.png'
HEROFACE10 = 'resources/sprites/heroes/10f_Elias.png'
HEROFACE11 = 'resources/sprites/heroes/11f_Onarr.png'
HEROFACE12 = 'resources/sprites/heroes/12f_Duilio.png'
HEROFACE13 = 'resources/sprites/heroes/13f_Iellwen.png'
HEROFACE14 = 'resources/sprites/heroes/14f_Faeron.png'


class PartyScreen(object):
    """
    ...
    """
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(BACKGROUNDCOLOR)
        self.background = self.background.convert()

        pygame.draw.rect(self.background, LINECOLOR, (10,    10, 250,  150), 1)
        pygame.draw.rect(self.background, LINECOLOR, (270,   10, 250,  150), 1)
        pygame.draw.rect(self.background, LINECOLOR, (530,   10, 250,  150), 1)
        pygame.draw.rect(self.background, LINECOLOR, (790,   10, 250,  150), 1)
        pygame.draw.rect(self.background, LINECOLOR, (1050,  10, 250,  150), 1)

        pygame.draw.rect(self.background, LINECOLOR, (10,   170, 405,  500), 1)
        pygame.draw.rect(self.background, LINECOLOR, (425,  170, 315,  620), 1)
        pygame.draw.rect(self.background, LINECOLOR, (750,  170, 315,  620), 1)
        pygame.draw.rect(self.background, LINECOLOR, (1075, 170, 315,  620), 1)

        bg_width = self.background.get_width()
        button_c = screens.sprites.ButtonSprite(80, 40, (bg_width - 90,  10), "Close", pygame.K_ESCAPE)
        button_q = screens.sprites.ButtonSprite(80, 40, (bg_width - 90,  70), "Previous", pygame.K_q)
        button_w = screens.sprites.ButtonSprite(80, 40, (bg_width - 90, 120), "Next", pygame.K_w)
        self.buttons = [button_c, button_q, button_w]

        self.key_input = pygame.key.get_pressed()       # dit is voor de mousepress op een button.

    def handle_view(self):
        """
        self.background bij button.draw()? moet dit niet self.screen zijn? ik snap nog niet de voorwaarden.
        bij de rest heb overal self.screen gedaan, maar blijkbaar kan het ook anders.
        """
        self.screen.blit(self.background, (0, 0))

        for button in self.buttons:
            button.draw(self.screen, self.key_input)

        # heroface1 = pygame.image.load(HEROFACE1)
        # heroface2 = pygame.image.load(HEROFACE2)
        # heroface3 = pygame.image.load(HEROFACE3)
        # heroface4 = pygame.image.load(HEROFACE4)
        # heroface5 = pygame.image.load(HEROFACE5)
        # heroface6 = pygame.image.load(HEROFACE6)
        # heroface7 = pygame.image.load(HEROFACE7)
        # heroface8 = pygame.image.load(HEROFACE8)
        # heroface9 = pygame.image.load(HEROFACE9)
        # heroface10 = pygame.image.load(HEROFACE10)
        # heroface11 = pygame.image.load(HEROFACE11)
        # heroface12 = pygame.image.load(HEROFACE12)
        # heroface13 = pygame.image.load(HEROFACE13)
        # heroface14 = pygame.image.load(HEROFACE14)
        # self.screen.blit(heroface1, (0, 0))
        # self.screen.blit(heroface2, (100, 0))
        # self.screen.blit(heroface3, (200, 0))
        # self.screen.blit(heroface4, (300, 0))
        # self.screen.blit(heroface5, (400, 0))
        # self.screen.blit(heroface6, (500, 0))
        # self.screen.blit(heroface7, (600, 0))
        # self.screen.blit(heroface8, (700, 0))
        # self.screen.blit(heroface9, (800, 0))
        # self.screen.blit(heroface10, (900, 0))
        # self.screen.blit(heroface11, (1000, 0))
        # self.screen.blit(heroface12, (1100, 0))
        # self.screen.blit(heroface13, (1200, 0))
        # self.screen.blit(heroface14, (1300, 0))

    def handle_multi_input(self, key_input, mouse_pos):
        """
        Registreert of er op de buttons wordt geklikt. En zet dat om naar keyboard input.
        :param key_input: pygame.key.get_pressed()
        :param mouse_pos: pygame.mouse.get_pos()
        """
        self.key_input = key_input

        for button in self.buttons:
            self.key_input = button.multi_click(mouse_pos, self.key_input)

    def handle_single_input(self, event):
        """
        ...
        :param event:
        """
        pass
