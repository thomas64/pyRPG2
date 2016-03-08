
"""
class: Screen
"""

import pygame

import keys
import screens.party.herobox
import screens.party.infobox
import screens.party.invclickbox
import screens.party.inventorybox
import screens.party.skillsbox
import screens.party.statsbox
import screens.sprites
import statemachine


BACKGROUNDCOLOR = pygame.Color("black")
LINECOLOR = pygame.Color("white")

CLOSELBL = "Close"
PREVLBL = "Previous"
NEXTLBL = "Next"

CLOSEX, CLOSEY = -90, 10    # negatieve x omdat de positie van rechts bepaald wordt.
PREVX, PREVY = -90, 45
NEXTX, NEXTY = -90, 80
BTNWIDTH = 80
BTNHEIGHT = 30

HEROBOXX, HEROBOXY = 10, 10
HEROBOXVAR = 260
STATBOXX, STATBOXY = 10, 120
INFOBOXX, INFOBOXY = 10, 630
SKILBOXX, SKILBOXY = 425, 120
INVBOXX, INVBOXY = 750, 120
SPELBOXX, SPELBOXY = 1075, 120


class Display(object):
    """
    Overzicht scherm PartyScreen.
    """
    def __init__(self, screen, engine):
        self.engine = engine
        self.screen = screen
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(BACKGROUNDCOLOR)
        self.background = self.background.convert()

        self.name = statemachine.States.PartyScreen

        self.key_input = pygame.key.get_pressed()           # dit is voor de mousepress op een button.

        self.cur_hero = self.engine.data.party['alagos']    # todo, dit moet nog de hero die aan de beurt is worden

        self.party = list(self.engine.data.party.values())
        self.hc = self.party.index(self.cur_hero)

        self.inventory = self.engine.data.inventory

        self._init_buttons()
        self._init_boxes()

        self.invclick_box = None
        self.info_label = ""

    def _init_buttons(self):
        bg_width = self.background.get_width()
        button_c = screens.sprites.ButtonSprite(BTNWIDTH, BTNHEIGHT, (bg_width + CLOSEX, CLOSEY), CLOSELBL, keys.EXIT)
        button_q = screens.sprites.ButtonSprite(BTNWIDTH, BTNHEIGHT, (bg_width + PREVX, PREVY), PREVLBL, keys.PREV)
        button_w = screens.sprites.ButtonSprite(BTNWIDTH, BTNHEIGHT, (bg_width + NEXTX, NEXTY), NEXTLBL, keys.NEXT)
        self.buttons = (button_c, button_q, button_w)

    def _init_boxes(self):
        self.hero_boxes = []
        for index, hero in enumerate(self.party):
            self.hero_boxes.append(screens.party.herobox.HeroBox(
                                                                (HEROBOXX + index * HEROBOXVAR, HEROBOXY), index, hero))

        self.stats_box = screens.party.statsbox.StatsBox((STATBOXX, STATBOXY))
        self.info_box = screens.party.infobox.InfoBox((INFOBOXX, INFOBOXY))
        self.skills_box = screens.party.skillsbox.SkillsBox((SKILBOXX, SKILBOXY))         # de grootte zit in de class
        self.inventory_box = screens.party.inventorybox.InventoryBox((INVBOXX, INVBOXY))  # zelf, de positie zit in deze
        pygame.draw.rect(self.background, LINECOLOR, (SPELBOXX, SPELBOXY, 315, 670), 1)   # class, moet dat anders?

    # noinspection PyMethodMayBeStatic
    def on_enter(self):
        """
        Wanneer deze state op de stack komt, voer dit uit.
        Op dit moment nog niets echts.
        """
        pass

    # noinspection PyMethodMayBeStatic
    def on_exit(self):
        """
        Wanneer deze state onder een andere state van de stack komt, voer dit uit.
        Op dit moment nog niets echts
        """
        pass

    def single_input(self, event):
        """
        Handelt de muis en keyboard input af.
        :param event: pygame.event.get()
        """

        if event.type == pygame.MOUSEMOTION:

            if self.stats_box.rect.collidepoint(event.pos):
                self.info_label = self.stats_box.mouse_hover(event)
            elif self.skills_box.rect.collidepoint(event.pos):
                self.info_label = self.skills_box.mouse_hover(event)
            elif self.inventory_box.rect.collidepoint(event.pos):
                self.info_label = self.inventory_box.mouse_hover(event, self.cur_hero)

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == keys.LEFTCLICK:

                # als de clickbox er is en er wordt buiten geklikt, laat hem dan verdwijnen.
                if self.invclick_box and not self.invclick_box.rect.collidepoint(event.pos):
                    self.invclick_box = None

                for hero_box in self.hero_boxes:
                    self.hc = hero_box.mouse_click(event, self.hc)

                # als er in de inventory box wordt geklikt
                if self.inventory_box.rect.collidepoint(event.pos):
                    # krijg de positie en equipment_type terug
                    boxpos, equipment_type = self.inventory_box.mouse_click(event, self.cur_hero)
                    # als er geen clickbox is en wel een equipment_type, geef dan een clickbox weer
                    if not self.invclick_box and equipment_type:
                        self.invclick_box = screens.party.invclickbox.InvClickBox(
                                                                    boxpos, equipment_type, self.party, self.inventory)

                for button in self.buttons:
                    button_press = button.single_click(event)
                    if button_press == keys.EXIT:
                        self.engine.gamestate.pop()
                    elif button_press == keys.PREV:
                        self._previous()
                    elif button_press == keys.NEXT:
                        self._next()

            elif event.button in (keys.SCROLLUP, keys.SCROLLDOWN):
                if self.invclick_box and self.invclick_box.rect.collidepoint(event.pos):
                    self.invclick_box.mouse_scroll(event)

        elif event.type == pygame.KEYDOWN:

            # als de clickbox er is en er wordt een toets gedrukt, laat hem dan verdwijnen.
            if self.invclick_box:
                self.invclick_box = None
            self.info_label = ""

            if event.key in (keys.EXIT, keys.INV):
                self.engine.gamestate.pop()
            elif event.key == keys.PREV:
                self._previous()
            elif event.key == keys.NEXT:
                self._next()
            # elif event.key == pygame.K_m:
            #     self.party[0].lev.qty += 1

    # noinspection PyUnusedLocal
    def multi_input(self, key_input, mouse_pos, dt):
        """
        Registreert of er op de buttons wordt geklikt. En zet dat om naar keyboard input.
        Dit is alleen maar voor het visuele oplichten van de knoppen,
        self.key_input wordt hier niet gebruikt voor input.
        :param key_input: pygame.key.get_pressed()
        :param mouse_pos: pygame.mouse.get_pos()
        :param dt: self.clock.tick(FPS)/1000.0
        """
        self.key_input = key_input

        for button in self.buttons:
            self.key_input = button.multi_click(mouse_pos, self.key_input)

    # noinspection PyMethodMayBeStatic
    def update(self, dt):
        """
        Update de waarden van de bovenste state.
        :param dt: self.clock.tick(FPS)/1000.0
        """
        pass

    def render(self):
        """
        screen -> achtergond -> knoppen -> heroboxes -> verder
        """
        self.screen.blit(self.background, (0, 0))

        for button in self.buttons:
            button.draw(self.screen, self.key_input)

        for hero_box in self.hero_boxes:
            hero_box.select(self.hc)
            hero_box.draw(self.screen)

        self.cur_hero = self.party[self.hc]

        self.stats_box.draw(self.screen, self.cur_hero)
        self.info_box.draw(self.screen, self.info_label)
        self.skills_box.draw(self.screen, self.cur_hero)
        self.inventory_box.draw(self.screen, self.cur_hero)
        if self.invclick_box:
            self.invclick_box.draw(self.screen)

        # name2 = self.largefont.render(cur_hero.NAM, True, FONTCOLOR)   = voorbeeld van hoe een naam buiten een herobox
        # name2_rect = self.screen.blit(name2, (500, 300))

    def _previous(self):
        self.hc -= 1
        if self.hc < 0:
            self.hc = len(self.party) - 1

    def _next(self):
        self.hc += 1
        if self.hc > len(self.party) - 1:
            self.hc = 0
