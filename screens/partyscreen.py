
"""
class: PartyScreen
"""

import pygame

import screens.sprites


BACKGROUNDCOLOR = pygame.Color("black")
LINECOLOR = pygame.Color("white")
HEROCOLOR = pygame.Color("gray38")

FONTCOLOR = pygame.Color("white")
FONT = 'impact'
LARGEFONTSIZE = 25
NORMALFONTSIZE = 15

HPCOLORFULL = pygame.Color("green")
HPCOLORHIGH = pygame.Color("green yellow")
HPCOLORNORM = pygame.Color("yellow")
HPCOLORLOW = pygame.Color("orange")
HPCOLORCRIT = pygame.Color("red")


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

        cur_hero = data.party['alagos']

        self.party = list(data.party.values())
        self.hc = self.party.index(cur_hero)

    def _paint(self):
        hero1_rect = pygame.draw.rect(self.background, LINECOLOR, (10,   10, 250, 98), 1)
        hero2_rect = pygame.draw.rect(self.background, LINECOLOR, (270,  10, 250, 98), 1)
        hero3_rect = pygame.draw.rect(self.background, LINECOLOR, (530,  10, 250, 98), 1)
        hero4_rect = pygame.draw.rect(self.background, LINECOLOR, (790,  10, 250, 98), 1)
        hero5_rect = pygame.draw.rect(self.background, LINECOLOR, (1050, 10, 250, 98), 1)
        self.hero_rect = (hero1_rect, hero2_rect, hero3_rect, hero4_rect, hero5_rect)

        pygame.draw.rect(self.background, LINECOLOR, (10,   120, 405, 500), 1)
        pygame.draw.rect(self.background, LINECOLOR, (425,  120, 315, 670), 1)
        pygame.draw.rect(self.background, LINECOLOR, (750,  120, 315, 670), 1)
        pygame.draw.rect(self.background, LINECOLOR, (1075, 120, 315, 670), 1)

    def _init_buttons(self):
        bg_width = self.background.get_width()
        button_c = screens.sprites.ButtonSprite(80, 30, (bg_width - 90, 10), "Close", pygame.K_ESCAPE)
        button_q = screens.sprites.ButtonSprite(80, 30, (bg_width - 90, 45), "Previous", pygame.K_q)
        button_w = screens.sprites.ButtonSprite(80, 30, (bg_width - 90, 80), "Next", pygame.K_w)
        self.buttons = (button_c, button_q, button_w)

    def handle_view(self):
        """
        self.background bij button.draw()? moet dit niet self.screen zijn? ik snap nog niet de voorwaarden.
        bij de rest heb overal self.screen gedaan, maar blijkbaar kan het ook anders.
        """

        # todo, aparte classen voor de verschillende onderdelen

        self.screen.blit(self.background, (0, 0))

        for button in self.buttons:
            button.draw(self.screen, self.key_input)

        cur_hero = self.party[self.hc]

        pygame.draw.rect(self.screen, HEROCOLOR, self.hero_rect[self.hc], 0)
        pygame.draw.rect(self.screen, LINECOLOR, self.hero_rect[self.hc], 1)

        for index, hero in enumerate(self.party):

            face = pygame.image.load(hero.FAC)
            face_rect = self.screen.blit(face, (11 + index * 260, 11))

            name = self.largefont.render(hero.NAM, True, FONTCOLOR)
            name_rect = self.screen.blit(name, (121 + index * 260, 14))

            level = self.normalfont.render("Level: {:12}".format(hero.lev.qty), True, FONTCOLOR)
            level_rect = self.screen.blit(level, (121 + index * 260, 46))

            hitpoints = self.normalfont.render(
                                        "HitPoints: {:5}{} {}".format(hero.cur_hp, "/", hero.max_hp), True, FONTCOLOR)
            hitpoints_rect = self.screen.blit(hitpoints, (121 + index * 260, 66))

            # health bars ##########
            full_hp = 135
            curr_hp = (full_hp / hero.max_hp) * hero.cur_hp
            color = HPCOLORFULL
            if hero.lev.cur < hero.lev.qty:
                color = HPCOLORHIGH
            if hero.sta.cur < hero.sta.qty:
                color = HPCOLORNORM
            if hero.edu.cur < hero.edu.qty:
                color = HPCOLORCRIT
            if hero.edu.cur < hero.edu.qty and hero.sta.cur > 0:
                color = HPCOLORLOW
            pygame.draw.rect(self.screen, color, (121 + index * 260, 91, curr_hp, 13), 0)
            pygame.draw.rect(self.screen, LINECOLOR, (121 + index * 260, 91, full_hp, 13), 1)
            ########################

        name2 = self.largefont.render(cur_hero.NAM, True, FONTCOLOR)
        name2_rect = self.screen.blit(name2, (300, 300))

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

    def _previous(self):
        self.hc -= 1
        if self.hc < 0:
            self.hc = len(self.party) - 1

    def _next(self):
        self.hc += 1
        if self.hc > len(self.party) - 1:
            self.hc = 0
