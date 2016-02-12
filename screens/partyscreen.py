
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

POSCOLOR = pygame.Color("green")
NEGCOLOR = pygame.Color("red")


class PartyScreen(object):
    """
    Overzicht scherm PartyScreen.
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
            self.hero_boxes.append(HeroBox((10 + index * 260, 10), index, hero))

        self.stats_box = StatsBox((10, 120))
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

        name2 = self.largefont.render(cur_hero.NAM, True, FONTCOLOR)
        name2_rect = self.screen.blit(name2, (500, 300))

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


class StatsBox(object):
    """
    ...
    """
    def __init__(self, position):
        self.surface = pygame.Surface((405, 500))
        self.surface = self.surface.convert()
        self.rect = self.surface.get_rect()
        self.rect.topleft = position

        self.background = pygame.Surface(self.surface.get_size())
        self.background.fill(BACKGROUNDCOLOR)
        self.background = self.background.convert()

        self.largefont = pygame.font.SysFont(FONT, LARGEFONTSIZE)
        self.normalfont = pygame.font.SysFont(FONT, NORMALFONTSIZE)

    def _update(self, hero):
        self.title = self.largefont.render("Stats", True, FONTCOLOR)
        col1 = ("XP Remaining :",
                "Total XP :",
                "Next Level :",
                "",
                "Weight :",
                "Movepoints :",
                "Protection :",
                "Defense :",
                "Base Hit :",
                "Damage :",
                "",
                "Intelligence :",
                "Willpower :",
                "Dexterity :",
                "Agility :",
                "Endurance :",
                "Strength :",
                "Stamina :")

        if hero.lev.qty >= hero.lev.MAX:
            hero_exp_tot = "Max"
            hero_lev_next = "Max"
        else:
            hero_exp_tot = str(hero.exp.tot)
            hero_lev_next = str(hero.lev.next(hero.exp.tot))

        col2 = (str(hero.exp.rem),
                str(hero_exp_tot),
                str(hero_lev_next),
                "",
                str(hero.tot_wht),
                str(hero.sta_mvp),
                str(hero.tot_prt),
                str(hero.tot_des),
                str(hero.tot_hit)+" %",
                str(hero.tot_dam),
                "",
                str(hero.int.qty),
                str(hero.wil.qty),
                str(hero.dex.qty),
                str(hero.agi.qty),
                str(hero.edu.qty),
                str(hero.str.qty),
                str(hero.sta.qty))

        col3 = ("",
                "",
                "3",
                "",
                "",
                "5",
                "",
                "",
                "-8",
                "",
                "",
                str(hero.int.ext),
                str(hero.wil.ext),
                str(hero.dex.ext),
                str(hero.agi.ext),
                str(hero.edu.ext),
                str(hero.str.ext),
                str(hero.sta.ext))

        # todo, ik moet wat verzinnen voor deze ext. in het oude spel worden die gezet bij _set_stats. op dit moment
        # denk ik dat ik wil dat dynamisch geladen worden zoals weight oid. maar ik wil het eigenlijk in de stats
        # class zelf, maar ik heb dat nog niet uitgezocht of dat echt wel logisch zal zijn.
        # ten tweede, vanwege de kleurtjes van de verschillende items, en de klikbaarheid kan het waarschijnlijk toch
        # niet zo makkelijk in kolommen zoals nu. :(

        self.col1 = []
        for line in col1:
            self.col1.append(self.normalfont.render(line, True, FONTCOLOR))
        self.col2 = []
        for line in col2:
            self.col2.append(self.normalfont.render(line, True, FONTCOLOR))
        self.col3 = []
        for line in col3:
            try:
                line = int(line)
                if line == 0:
                    line = ""
                    self.col3.append(self.normalfont.render(line, True, FONTCOLOR))
                elif line > 0:
                    line = "(+"+str(line)+")"
                    self.col3.append(self.normalfont.render(line, True, POSCOLOR))
                elif line < 0:
                    line = "("+str(line)+")"
                    self.col3.append(self.normalfont.render(line, True, NEGCOLOR))
            except (TypeError, ValueError):
                line = ""
                self.col3.append(self.normalfont.render(line, True, FONTCOLOR))

    def draw(self, screen, hero):
        """
        ...
        :param hero:
        :param screen:
        """
        self._update(hero)

        self.surface.blit(self.background, (0, 0))
        pygame.draw.rect(self.background, LINECOLOR, self.surface.get_rect(), 1)

        self.surface.blit(self.title, (7, 1))
        for line, text in enumerate(self.col1):
            self.surface.blit(text, (50, 60 + line * 22))
        for line, text in enumerate(self.col2):
            self.surface.blit(text, (160, 60 + line * 22))
        for line, text in enumerate(self.col3):
            self.surface.blit(text, (200, 60 + line * 22))

        screen.blit(self.surface, self.rect.topleft)
