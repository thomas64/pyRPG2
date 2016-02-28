
"""
class: HeroBox
"""

import pygame

BACKGROUNDCOLOR = pygame.Color("black")
LINECOLOR = pygame.Color("white")
HEROCOLOR = pygame.Color("gray24")

BOXWIDTH = 250
BOXHEIGHT = 98

FACEX, FACEY = 1, 1
NAMEX, NAMEY = 111, 4
LEVELX, LEVELY = 111, 36
HITPOINTSX, HITPOINTSY = 111, 56
HEALTHBARX, HEALTHBARY = 111, 81
HEALTHBARWIDTH = 135
HEALTHBARHEIGHT = 13

LEVEL = "Level: {:12}"
HITPOINTS = "HitPoints: {:5}/ {}"

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
        self.surface = pygame.Surface((BOXWIDTH, BOXHEIGHT))
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
        self.face = pygame.image.load(self.hero.FAC).convert_alpha()
        self.name = self.largefont.render(self.hero.NAM, True, FONTCOLOR).convert_alpha()
        self.level = self.normalfont.render(LEVEL.format(self.hero.lev.qty), True, FONTCOLOR).convert_alpha()
        self.hitpoints = self.normalfont.render(
                        HITPOINTS.format(self.hero.cur_hp, self.hero.max_hp), True, FONTCOLOR).convert_alpha()
        # health bars #
        self.full_hp = HEALTHBARWIDTH
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
        self.surface.blit(self.face, (FACEX, FACEY))
        self.surface.blit(self.name, (NAMEX, NAMEY))
        self.surface.blit(self.level, (LEVELX, LEVELY))
        self.surface.blit(self.hitpoints, (HITPOINTSX, HITPOINTSY))
        pygame.draw.rect(self.surface, self.color, (HEALTHBARX, HEALTHBARY, self.curr_hp, HEALTHBARHEIGHT), 0)
        pygame.draw.rect(self.surface, LINECOLOR, (HEALTHBARX, HEALTHBARY, self.full_hp, HEALTHBARHEIGHT), 1)

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

    def mouse_click(self, event, cur_hc):
        """
        Ontvang mouse event. Kijk of het met de de surface collide.
        :param event: pygame.MOUSEBUTTONDOWN uit engine.py
        :param cur_hc: het huidige party hero nummer
        :return: het volgorde nummer van de hero van de party, of gewoon het oude huidige nummer
        """
        if self.rect.collidepoint(event.pos):
            return self.hc
        return cur_hc
