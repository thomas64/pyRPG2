
"""
class: PartyScreen
class: HeroBox
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

        self.key_input = pygame.key.get_pressed()       # dit is voor de mousepress op een button.

        self.largefont = pygame.font.SysFont(FONT, LARGEFONTSIZE)
        self.normalfont = pygame.font.SysFont(FONT, NORMALFONTSIZE)

        cur_hero = data.party['alagos']

        self.party = list(data.party.values())
        self.hc = self.party.index(cur_hero)

        self._init_buttons()
        self._init_boxes()

    def _init_buttons(self):
        bg_width = self.background.get_width()
        button_c = screens.sprites.ButtonSprite(80, 30, (bg_width - 90, 10), "Close", pygame.K_ESCAPE)
        button_q = screens.sprites.ButtonSprite(80, 30, (bg_width - 90, 45), "Previous", pygame.K_q)
        button_w = screens.sprites.ButtonSprite(80, 30, (bg_width - 90, 80), "Next", pygame.K_w)
        self.buttons = (button_c, button_q, button_w)

    def _init_boxes(self):
        self.hero_boxes = []
        for index, hero in enumerate(self.party):
            self.hero_boxes.append(HeroBox((10 + index * 260, 10), hero))

        pygame.draw.rect(self.background, LINECOLOR, (10,   120, 405, 500), 1)
        pygame.draw.rect(self.background, LINECOLOR, (425,  120, 315, 670), 1)
        pygame.draw.rect(self.background, LINECOLOR, (750,  120, 315, 670), 1)
        pygame.draw.rect(self.background, LINECOLOR, (1075, 120, 315, 670), 1)

    def handle_view(self):
        """
        ...
        """
        self.screen.blit(self.background, (0, 0))

        for button in self.buttons:
            button.draw(self.background, self.key_input)

        cur_hero = self.party[self.hc]

        for hero_box in self.hero_boxes:
            hero_box.draw(self.background)
            hero_box.select(cur_hero)

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


class HeroBox(object):
    """
    ...
    """
    def __init__(self, position, hero):
        self.surface = pygame.Surface((250, 98))
        self.surface.fill(BACKGROUNDCOLOR)
        self.surface = self.surface.convert()
        self.rect = self.surface.get_rect()
        self.rect.topleft = position

        self.background = pygame.Surface((250, 98))
        self.background.fill(BACKGROUNDCOLOR)
        self.background = self.background.convert()

        self.hero = hero

    def _update(self):
        largefont = pygame.font.SysFont(FONT, LARGEFONTSIZE)
        normalfont = pygame.font.SysFont(FONT, NORMALFONTSIZE)

        self.face = pygame.image.load(self.hero.FAC)
        self.name = largefont.render(self.hero.NAM, True, FONTCOLOR)
        self.level = normalfont.render("Level: {:12}".format(self.hero.lev.qty), True, FONTCOLOR)
        self.hitpoints = normalfont.render(
                                "HitPoints: {:5}{} {}".format(self.hero.cur_hp, "/", self.hero.max_hp), True, FONTCOLOR)
        # health bars ##########
        self.full_hp = 135
        self.curr_hp = (self.full_hp / self.hero.max_hp) * self.hero.cur_hp
        self.color = HPCOLORFULL
        if self.hero.lev.cur < self.hero.lev.qty:
            self.color = HPCOLORHIGH
        if self.hero.sta.cur < self.hero.sta.qty:
            self.color = HPCOLORNORM
        if self.hero.edu.cur < self.hero.edu.qty:
            self.color = HPCOLORCRIT
        if self.hero.edu.cur < self.hero.edu.qty and self.hero.sta.cur > 0:
            self.color = HPCOLORLOW
        ########################

    def draw(self, screen):
        """
        ...
        :param screen:
        """
        self._update()

        self.surface.blit(self.background, (0, 0))
        pygame.draw.rect(self.surface, LINECOLOR, (0, 0, 250, 98), 1)
        self.surface.blit(self.face, (1, 1))
        self.surface.blit(self.name, (111, 4))
        self.surface.blit(self.level, (111, 36))
        self.surface.blit(self.hitpoints, (111, 56))
        pygame.draw.rect(self.surface, self.color, (111, 81, self.curr_hp, 13), 0)
        pygame.draw.rect(self.surface, LINECOLOR, (111, 81, self.full_hp, 13), 1)

        screen.blit(self.surface, self.rect.topleft)

    def select(self, hero):
        """
        ...
        :param hero:
        """
        if hero == self.hero:
            self.background.fill(HEROCOLOR)
        else:
            self.background.fill(BACKGROUNDCOLOR)
