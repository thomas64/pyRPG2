
"""
class: HeroBox
"""

import pygame

import components

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

LEAVEW, LEAVEH = 18, 18
LEAVEX, LEAVEY = -20, +2
LEAVELBL = "X"


class HeroBox(object):
    """
    Alle weergegeven informatie in een hero boxje in het partyscherm.
    """
    def __init__(self, position, index, hero):
        self.surface = pygame.Surface((BOXWIDTH, BOXHEIGHT))
        self.surface = self.surface.convert()
        self.rect = self.surface.get_rect()
        self.rect.topleft = position

        self.background = pygame.Surface(self.surface.get_size())
        self.background.fill(BACKGROUNDCOLOR)
        self.background = self.background.convert()

        self.largefont = pygame.font.SysFont(FONT, LARGEFONTSIZE)
        self.normalfont = pygame.font.SysFont(FONT, NORMALFONTSIZE)

        self.party_index = index
        self.hero = hero

        self.face = pygame.image.load(self.hero.FAC).convert_alpha()
        self.name = self.largefont.render(self.hero.NAM, True, FONTCOLOR).convert_alpha()
        self.leave = components.Button(LEAVEW, LEAVEH,
                                       (self.rect.right + LEAVEX, self.rect.top + LEAVEY), LEAVELBL, True)
        self.level = None
        self.hitpoints = None
        self.full_hp = None
        self.curr_hp = None
        self.color = None

    def mouse_click(self, event, cur_hc):
        """
        Ontvang mouse event. Kijk of het met de de surface collide.
        :param event: pygame.MOUSEBUTTONDOWN uit party display.py
        :param cur_hc: het huidige party hero nummer
        :return: het volgorde nummer van de hero van de party, of gewoon het oude huidige nummer,
        :return: ook de key van het leave knopje, wanneer die gedrukt is, anders is dat None.
        """
        leave_press = self.leave.single_click(event)

        if self.rect.collidepoint(event.pos):
            return self.party_index, leave_press
        return cur_hc, leave_press

    def update(self, cur_hc):
        """
        Update eerst alle data.
        :param cur_hc: het huidige party hero nummer uit display
        """
        # alagos moet zo'n knop niet hebben, en hij heeft index 0.
        if cur_hc == self.party_index:
            if self.party_index:
                self.leave.visible = True
            else:
                self.leave.visible = False
        else:
            self.leave.visible = False

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

    def render(self, screen, cur_hc):
        """
        En teken dan al die data op de surface en die op de screen.
        Als het de geselecteerde hero_box is pas dan eerst de achtergrondkleur aan.
        :param screen: self.screen van partyscreen
        :param cur_hc: het huidige party hero nummer uit display
        """
        if cur_hc == self.party_index:
            self.background.fill(HEROCOLOR)
        else:
            self.background.fill(BACKGROUNDCOLOR)

        self.surface.blit(self.background, (0, 0))
        pygame.draw.rect(self.surface, LINECOLOR, self.surface.get_rect(), 1)
        self.surface.blit(self.face, (FACEX, FACEY))
        self.surface.blit(self.name, (NAMEX, NAMEY))
        self.surface.blit(self.level, (LEVELX, LEVELY))
        self.surface.blit(self.hitpoints, (HITPOINTSX, HITPOINTSY))
        pygame.draw.rect(self.surface, self.color, (HEALTHBARX, HEALTHBARY, self.curr_hp, HEALTHBARHEIGHT), 0)
        pygame.draw.rect(self.surface, LINECOLOR, (HEALTHBARX, HEALTHBARY, self.full_hp, HEALTHBARHEIGHT), 1)

        screen.blit(self.surface, self.rect.topleft)

        self.leave.render(screen)
