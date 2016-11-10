
"""
class: Display
"""

import pygame

from components import Button
from components import ConfirmBox
from constants import GameState
from constants import Keys

from .herobox import HeroBox
from .infobox import InfoBox
from .invclickbox import InvClickBox
from .inventorybox import InventoryBox
from .pouchbox import PouchBox
from .skillsbox import SkillsBox
from .spellsbox import SpellsBox
from .statsbox import StatsBox


BACKGROUNDCOLOR = pygame.Color("black")
LINECOLOR = pygame.Color("white")

CLOSELBL = "Close"
PREVLBL = "Previous"
NEXTLBL = "Next"

CLOSEX, CLOSEY = -81, 10    # negatieve x omdat de positie van rechts bepaald wordt.
PREVX, PREVY = -81, 44
NEXTX, NEXTY = -81, 78
BTNWIDTH = 71
BTNHEIGHT = 30

HEROBOXX, HEROBOXY = 10, 10
HEROBOXVAR = 255
STATBOXX, STATBOXY = 10,  118
STATBOXW, STATBOXH = 329, 490
INFOBOXX, INFOBOXY = 10,  613
INFOBOXW, INFOBOXH = 329, 145
SKILBOXX, SKILBOXY = 349, 118
SKILBOXW, SKILBOXH = 329, 640
INVBOXX, INVBOXY = 688, 118
INVBOXW, INVBOXH = 329, 340
PCHBOXX, PCHBOXY = 688, 468
PCHBOXW, PCHBOXH = 329, 290
SPELBOXX, SPELBOXY = 1027, 118
SPELBOXW, SPELBOXH = 329, 640

NEWMAPTIMEOUT = 0.5


class Display(object):
    """
    Overzicht scherm PartyScreen.
    """
    def __init__(self, engine):
        self.engine = engine
        self.screen = pygame.display.get_surface()
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(BACKGROUNDCOLOR)
        self.background = self.background.convert()

        self.name = GameState.PartyScreen

        self.key_input = None           # dit is voor de mousepress op een button.

        self.cur_hero = self.engine.data.party['alagos']    # todo, dit moet nog de hero die aan de beurt is worden

        self.party = list(self.engine.data.party.values())
        self.hc = self.party.index(self.cur_hero)

        self.inventory = self.engine.data.inventory
        self.pouch = self.engine.data.pouch

        self._init_buttons()
        self._init_boxes()

        self.invclick_box = None
        self.info_label = ""
        self.hovered_equipment_item = None

        self.leave_box = None
        self.party_changed = False

    def _init_buttons(self):
        bg_width = self.background.get_width()
        button_c = Button(BTNWIDTH, BTNHEIGHT, (bg_width + CLOSEX, CLOSEY), CLOSELBL, Keys.Exit.value)
        button_q = Button(BTNWIDTH, BTNHEIGHT, (bg_width + PREVX,  PREVY),  PREVLBL,  Keys.Prev.value)
        button_w = Button(BTNWIDTH, BTNHEIGHT, (bg_width + NEXTX,  NEXTY),  NEXTLBL,  Keys.Next.value)
        self.buttons = (button_c, button_q, button_w)

    def _init_boxes(self):
        self.hero_boxes = []
        for index, hero in enumerate(self.party):
            self.hero_boxes.append(HeroBox((HEROBOXX + index * HEROBOXVAR, HEROBOXY), index, hero))

        self.stats_box = StatsBox((STATBOXX,        STATBOXY), STATBOXW, STATBOXH)
        self.info_box = InfoBox((INFOBOXX,          INFOBOXY), INFOBOXW, INFOBOXH)
        self.skills_box = SkillsBox((SKILBOXX,      SKILBOXY), SKILBOXW, SKILBOXH)
        self.inventory_box = InventoryBox((INVBOXX, INVBOXY),  INVBOXW,  INVBOXH)
        self.pouch_box = PouchBox((PCHBOXX,         PCHBOXY),  PCHBOXW,  PCHBOXH)
        self.spells_box = SpellsBox((SPELBOXX,      SPELBOXY), SPELBOXW, SPELBOXH)

    def on_enter(self):
        """
        Wanneer deze state op de stack komt, voer dit uit.
        Zet muziek en achtergrond geluiden indien nodig.
        """
        self.engine.audio.set_bg_music(self.name)
        self.engine.audio.set_bg_sounds(self.name)

        # Als de leave party confirmbox in beeld is geweest.
        if self.leave_box:
            choice = self.leave_box.cur_item
            yes = self.leave_box.TOPINDEX
            if choice == yes:
                self.engine.data.party.remove(self.cur_hero)
                # update daarna het party scherm
                self.cur_hero = self.engine.data.party['alagos']
                self.party = list(self.engine.data.party.values())
                self.hc = self.party.index(self.cur_hero)
                self._init_boxes()
                self.party_changed = True
            self.leave_box = None

    def on_exit(self):
        """
        Wanneer deze state onder een andere state van de stack komt, voer dit uit.
        Wanneer de party is aangepast herlaadt dan de map voor visuele update.
        """
        if self.party_changed:
            self.engine.key_timer = NEWMAPTIMEOUT
            self.engine.gamestate.deep_peek().window.load_map()

    def single_input(self, event):
        """
        Handelt de muis en keyboard input af.
        :param event: pygame.event.get()
        """

        if event.type == pygame.MOUSEMOTION:

            self.hovered_equipment_item = None
            self.info_label = ""

            if self.stats_box.rect.collidepoint(event.pos):
                self.info_label = self.stats_box.mouse_hover(event)
            elif self.skills_box.rect.collidepoint(event.pos):
                self.info_label = self.skills_box.mouse_hover(event)
            elif self.invclick_box and self.invclick_box.rect.collidepoint(event.pos):
                self.info_label, self.hovered_equipment_item = self.invclick_box.mouse_hover(event)
            elif self.inventory_box.rect.collidepoint(event.pos):
                self.info_label = self.inventory_box.mouse_hover(event)
            elif self.pouch_box.rect.collidepoint(event.pos):
                self.info_label = self.pouch_box.mouse_hover(event)
            elif self.spells_box.rect.collidepoint(event.pos):
                self.info_label = self.spells_box.mouse_hover(event)

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == Keys.Leftclick.value:

                # als de clickbox er is en er wordt buiten geklikt, laat hem dan verdwijnen.
                if self.invclick_box and not self.invclick_box.rect.collidepoint(event.pos):
                    self.invclick_box = None

                elif self.invclick_box and self.invclick_box.rect.collidepoint(event.pos):
                    if self.invclick_box.mouse_click(event, self.engine.gamestate, self.cur_hero):
                        self.invclick_box = None
                    return  # anders vangt hij ook nog andere clicks hieronder in deze methode af

                for hero_box in self.hero_boxes:
                    self.hc, leave_party = hero_box.mouse_click(event, self.hc)
                    if leave_party:
                        text = ["Do you want me to leave your party?",
                                "",
                                "Yes, you may leave.",
                                "No, I want you to stay."]
                        self.leave_box = ConfirmBox(self.engine.gamestate, self.engine.audio, text, self.cur_hero.FAC)
                        self.engine.gamestate.push(self.leave_box)

                # als er in de inventory box wordt geklikt
                if self.inventory_box.rect.collidepoint(event.pos):
                    # krijg de positie en equipment_type terug
                    boxpos, equipment_type = self.inventory_box.mouse_click(event)
                    # als er geen clickbox is en wel een equipment_type, geef dan een clickbox weer
                    if not self.invclick_box and equipment_type:
                        self.invclick_box = InvClickBox(boxpos, equipment_type, self.party, self.inventory)

                for button in self.buttons:
                    button_press = button.single_click(event)
                    if button_press == Keys.Exit.value:
                        self.engine.gamestate.pop()
                    elif button_press == Keys.Prev.value:
                        self._previous()
                    elif button_press == Keys.Next.value:
                        self._next()

            elif event.button in (Keys.Scrollup.value, Keys.Scrolldown.value):
                if self.invclick_box and self.invclick_box.rect.collidepoint(event.pos):
                    self.invclick_box.mouse_scroll(event)

        elif event.type == pygame.KEYDOWN:

            # als de clickbox er is en er wordt een toets gedrukt, laat hem dan verdwijnen.
            if self.invclick_box:
                self.invclick_box = None
            self.info_label = ""

            if event.key in (Keys.Exit.value, Keys.Inv.value):
                self.engine.gamestate.pop()
            elif event.key == Keys.Prev.value:
                self._previous()
            elif event.key == Keys.Next.value:
                self._next()
            # elif event.key == pygame.K_m:
            #     self.party[0].lev.qty += 1

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

    def update(self, dt):
        """
        Update alle waarden in de boxen.
        :param dt: self.clock.tick(FPS)/1000.0
        """
        for button in self.buttons:
            button.update(self.key_input)

        for hero_box in self.hero_boxes:
            hero_box.update(self.hc)

        self.cur_hero = self.party[self.hc]

        self.stats_box.update(self.cur_hero, self.hovered_equipment_item)
        self.skills_box.update(self.cur_hero, self.hovered_equipment_item)
        self.inventory_box.update(self.cur_hero)
        self.pouch_box.update(self.pouch)
        self.spells_box.update(self.cur_hero)

    def render(self):
        """
        screen -> achtergond -> knoppen -> heroboxes -> verder
        """
        self.screen.blit(self.background, (0, 0))

        for button in self.buttons:
            button.render(self.screen)

        for hero_box in self.hero_boxes:
            hero_box.render(self.screen, self.hc)

        self.stats_box.render(self.screen)
        self.info_box.render(self.screen, self.info_label)
        self.skills_box.render(self.screen)
        self.inventory_box.render(self.screen)
        self.pouch_box.render(self.screen)
        self.spells_box.render(self.screen)
        if self.invclick_box:
            self.invclick_box.render(self.screen)

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
