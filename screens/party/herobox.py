
"""
class: HeroBox
"""

import pygame

BACKGROUNDCOLOR = pygame.Color("black")
LINECOLOR = pygame.Color("white")
HEROCOLOR = pygame.Color("gray24")

FONTCOLOR = pygame.Color("white")
FONT = 'impact'
LARGEFONTSIZE = 25
NORMALFONTSIZE = 15

HPCOLORFULL = pygame.Color("green")
HPCOLORHIGH = pygame.Color("green yellow")
HPCOLORNORM = pygame.Color("yellow")
HPCOLORLOW = pygame.Color("orange")
HPCOLORCRIT = pygame.Color("red")


class HeroBox(object):
    """
    Alle weergegeven informatie in een hero boxje in het partyscherm.
    """
    def __init__(self, position, hc, hero):
        self.surface = pygame.Surface((250, 98))
        self.surface = self.surface.convert()
        self.rect = self.surface.get_rect()
        self.rect.topleft = position

        self.background = pygame.Surface(self.surface.get_size())
        self.background.fill(BACKGROUNDCOLOR)
        self.background = self.background.convert()

        self.largefont = pygame.font.SysFont(FONT, LARGEFONTSIZE)
        self.normalfont = pygame.font.SysFont(FONT, NORMALFONTSIZE)

        self.hc = hc
        self.hero = hero

    def _update(self):
        self.face = pygame.image.load(self.hero.FAC)
        self.name = self.largefont.render(self.hero.NAM, True, FONTCOLOR)
        self.level = self.normalfont.render("Level: {:12}".format(self.hero.lev.qty), True, FONTCOLOR)
        self.hitpoints = self.normalfont.render(
                            "HitPoints: {:5}{} {}".format(self.hero.cur_hp, "/", self.hero.max_hp), True, FONTCOLOR)
        # health bars #
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
        # ----------- #

    def draw(self, screen):
        """
        Update eerst de data, en teken dan al die data op de surface en die op de screen.
        :param screen: self.screen van partyscreen
        """
        self._update()

        self.surface.blit(self.background, (0, 0))
        pygame.draw.rect(self.surface, LINECOLOR, self.surface.get_rect(), 1)
        self.surface.blit(self.face, (1, 1))
        self.surface.blit(self.name, (111, 4))
        self.surface.blit(self.level, (111, 36))
        self.surface.blit(self.hitpoints, (111, 56))
        pygame.draw.rect(self.surface, self.color, (111, 81, self.curr_hp, 13), 0)
        pygame.draw.rect(self.surface, LINECOLOR, (111, 81, self.full_hp, 13), 1)

        screen.blit(self.surface, self.rect.topleft)

    def select(self, cur_hc):
        """
        Als het de geselecteerde hero_box is pas dan de achtergrondkleur aan.
        :param cur_hc: het huidige party hero nummer
        """
        if cur_hc == self.hc:
            self.background.fill(HEROCOLOR)
        else:
            self.background.fill(BACKGROUNDCOLOR)

    def single_click(self, event, cur_hc):
        """
        Ontvang mouse event. Kijk of het met de de surface collide.
        :param event: pygame.MOUSEBUTTONDOWN uit engine.py
        :param cur_hc: het huidige party hero nummer
        :return: het volgorde nummer van de hero van de party, of gewoon het oude huidige nummer
        """
        if self.rect.collidepoint(event.pos):
            return self.hc
        return cur_hc
