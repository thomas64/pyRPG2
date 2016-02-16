
"""
class: PartyScreen
class: HeroBox
class: InfoBox
class: StatsBox
"""

import pygame

import screens.sprites


BACKGROUNDCOLOR = pygame.Color("black")
LINECOLOR = pygame.Color("white")
HEROCOLOR = pygame.Color("gray38")

FONTCOLOR1 = pygame.Color("white")
FONTCOLOR2 = pygame.Color("yellow")
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
            self.hero_boxes.append(HeroBox((10 + index * 260, 10), index, hero))

        self.stats_box = StatsBox((10, 120))
        self.info_box = InfoBox((10, 630))
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

        name2 = self.largefont.render(cur_hero.NAM, True, FONTCOLOR1)
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
        self.name = self.largefont.render(self.hero.NAM, True, FONTCOLOR1)
        self.level = self.normalfont.render("Level: {:12}".format(self.hero.lev.qty), True, FONTCOLOR1)
        self.hitpoints = self.normalfont.render(
                            "HitPoints: {:5}{} {}".format(self.hero.cur_hp, "/", self.hero.max_hp), True, FONTCOLOR1)
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


class InfoBox(object):
    """
    Waar in het partyscreen alle omschrijvingen worden weergegeven.
    """
    def __init__(self, position):
        self.surface = pygame.Surface((405, 160))
        self.surface = self.surface.convert()
        self.rect = self.surface.get_rect()
        self.rect.topleft = position

        self.background = pygame.Surface(self.surface.get_size())
        self.background.fill(BACKGROUNDCOLOR)
        self.background = self.background.convert()

        self.largefont = pygame.font.SysFont(FONT, LARGEFONTSIZE)
        self.normalfont = pygame.font.SysFont(FONT, NORMALFONTSIZE)

    def draw(self, screen, text):
        """
        Teken het label bovenop de achtergrond.
        :param screen: self.screen van partyscreen
        :param text: de tekst om weer te geven
        """
        self.surface.blit(self.background, (0, 0))
        label = self.normalfont.render(text, True, FONTCOLOR1)
        self.surface.blit(label, (10, 10))
        screen.blit(self.surface, self.rect.topleft)


class StatsBox(object):
    """
    Alle weergegeven informatie van alle stats van een hero.
    """
    COLSY = 60
    COL1X = 50
    COL2X = 160
    COL3X = 200
    LINEH = 22

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

        self.cur_item = None

    def _update(self, hero):
        self.title = self.largefont.render("Stats", True, FONTCOLOR1)

        # zet eerst even wat bepaalde waarden vast.
        if hero.lev.qty >= hero.lev.MAX:
            hero_exp_tot = "Max"
            hero_lev_next = "Max"
        else:
            hero_exp_tot = str(hero.exp.tot)
            hero_lev_next = str(hero.lev.next(hero.exp.tot))

        # zet dan alles in deze tabel met drie kolommen.
        # todo, testen hoe dit: hero.war.bonus(hero.wpn), gaat met hero zonder wapen. bonus() checken.
        self.table_data = (["XP Remaining :", str(hero.exp.rem),      "",                        ""],
                           ["Total XP :",     str(hero_exp_tot),      "",                        ""],
                           ["Next Level :",   str(hero_lev_next),     "",                        ""],
                           ["",               "",                     "",                        ""],
                           ["Weight :",       str(hero.tot_wht),      "",                        ""],
                           ["Movepoints :",   str(hero.sta_mvp),      "",                        ""],
                           ["Protection :",   str(hero.tot_prt),      "",                        ""],
                           ["Defense :",      str(hero.tot_des),      "",                        ""],
                           ["Base Hit :",     str(hero.tot_hit)+" %", hero.war.bonus(hero.wpn),  ""],
                           ["Damage :",       str(hero.tot_dam),      "",                        ""],
                           ["",               "",                     "",                        ""],
                           ["Intelligence :", str(hero.int.qty),      hero.int.ext,              hero.int.DESC],
                           ["Willpower :",    str(hero.wil.qty),      hero.wil.ext,              ""],
                           ["Dexterity :",    str(hero.dex.qty),      hero.dex.ext,              ""],
                           ["Agility :",      str(hero.agi.qty),      hero.agi.ext,              ""],
                           ["Endurance :",    str(hero.edu.qty),      hero.edu.ext,              ""],
                           ["Strength :",     str(hero.str.qty),      hero.str.ext,              ""],
                           ["Stamina :",      str(hero.sta.qty),      hero.sta.ext,              ""])

        # maak een extra 4e kolom aan. hierin staan de rects.
        for index, row in enumerate(self.table_data):
            row.append(self._rect(index, row[0]))

        # maak dan een nieuwe tabel aan met de tekst, maar dan gerendered.
        self.table_view = []
        for index, row in enumerate(self.table_data):
            self.table_view.append(list())
            if index == self.cur_item:              # als de index van deze rij gelijk is aan waar de muis over zit,
                color = FONTCOLOR2                  # maak hem geel
            else:                                   # anders gewoon wit.
                color = FONTCOLOR1
            self.table_view[index].append(self.normalfont.render(row[0], True, color))
            self.table_view[index].append(self.normalfont.render(row[1], True, FONTCOLOR1))
            self._line(row[2], self.table_view[index])

    def _rect(self, index, text):
        """
        self.rect is de hele box zelf. Die heeft ook een position op het scherm, vandaar dat de position een soort
        offset moet krijgen hier.
        """
        rect = self.normalfont.render(text, True, FONTCOLOR1).get_rect()
        rect.topleft = self.rect.left + self.COL1X, (self.rect.top + self.COLSY) + index * self.LINEH
        return rect

    def _line(self, value, col):
        """
        Geef een regel in een kolom een bepaalde format en kleur mee aan de hand van de waarde.
        :param value: dit is een van die waarden
        :param col: in welke kolom de regel zich bevind
        """
        if value == "":
            value = 0
        if value == 0:
            value = ""
            col.append(self.normalfont.render(value, True, FONTCOLOR1))
        elif value > 0:
            value = "(+"+str(value)+")"
            col.append(self.normalfont.render(value, True, POSCOLOR))
        elif value < 0:
            value = "("+str(value)+")"
            col.append(self.normalfont.render(value, True, NEGCOLOR))

    def draw(self, screen, hero):
        """
        Update eerst de data, en teken dan al die data op de surface en die op de screen.
        :param screen: self.screen van partyscreen
        :param hero: de huidige geselecteerde hero
        """
        self._update(hero)

        self.surface.blit(self.background, (0, 0))
        pygame.draw.rect(self.background, LINECOLOR, self.surface.get_rect(), 1)

        self.surface.blit(self.title, (7, 1))
        for index, row in enumerate(self.table_view):
            self.surface.blit(row[0], (self.COL1X, self.COLSY + index * self.LINEH))
        for index, row in enumerate(self.table_view):
            self.surface.blit(row[1], (self.COL2X, self.COLSY + index * self.LINEH))
        for index, row in enumerate(self.table_view):
            self.surface.blit(row[2], (self.COL3X, self.COLSY + index * self.LINEH))

        screen.blit(self.surface, self.rect.topleft)

    def mouse_hover(self, event):
        """
        Als de muis over een item in uit de eerst visuele gaat. row[4] dat zijn de rects.
        Zet cur_item op de index van degene waar de muis over gaat.
        :param event: pygame.MOUSEMOTION uit engine.py
        :return: row[3] is de kolom met de info.
        """
        self.cur_item = None
        for index, row in enumerate(self.table_data):
            if row[4].collidepoint(event.pos):
                self.cur_item = index
                return row[3]

# todo, de extra benodigde kolommen bekijken in vb en implementeren. ook de kolommen uit pyRPG1.
