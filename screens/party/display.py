
"""
class: Display
"""

import pygame

from components import Button
from components import ConfirmBox
from components import MessageBox
from components import Parchment
from components import TextBox
from components import Transition

from constants import GameState
from constants import Keys
from constants import SFX

from screens.alchemist.display import Display as Alchemist
from .herobox import HeroBox
from .invclickbox import InvClickBox
from .inventorybox import InventoryBox
from .pouchbox import PouchBox
from .skillsbox import SkillsBox
from .spellsbox import SpellsBox
from .statsbox import StatsBox


BACKGROUNDCOLOR = pygame.Color("black")
COLORKEY = pygame.Color("white")
LINECOLOR = pygame.Color("black")

CLOSELBL = "Close"
PREVLBL = "Prev"
NEXTLBL = "Next"

CLOSEX, CLOSEY = -93, 30    # negatieve x omdat de positie van rechts bepaald wordt.
PREVX, PREVY =   -93, 64
NEXTX, NEXTY =   -93, 98
BTNWIDTH = 60
BTNHEIGHT = 30

HEROBOXX, HEROBOXY = 43, 30
HEROBOXW, HEROBOXH = 241, 98
HEROBOXVAR = 246
STATBOXX, STATBOXY = 43,  133
STATBOXW, STATBOXH = 270, 460
INVBOXX, INVBOXY =   323, 133
INVBOXW, INVBOXH =   200, 460
INFOBOXX, INFOBOXY = 43,  598
INFOBOXW, INFOBOXH = 480, 135
SKILBOXX, SKILBOXY = 533, 133
SKILBOXW, SKILBOXH = 300, 600
SPELBOXX, SPELBOXY = 843, 133
SPELBOXW, SPELBOXH = 240, 600
PCHBOXX, PCHBOXY =  1093, 133
PCHBOXW, PCHBOXH =   240, 600

NEWMAPTIMEOUT = 0.5


class Display(Parchment):
    """
    Overzicht scherm PartyScreen.
    """
    def __init__(self, engine):
        super().__init__(engine)
        self.engine = engine

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

        self._reset_vars()

    def _init_buttons(self):
        bg_width = self.background.get_width()
        button_c = Button(BTNWIDTH, BTNHEIGHT, (bg_width + CLOSEX, CLOSEY), CLOSELBL, Keys.Exit.value, COLORKEY, LINECOLOR)
        button_q = Button(BTNWIDTH, BTNHEIGHT, (bg_width + PREVX,  PREVY),  PREVLBL,  Keys.Prev.value, COLORKEY, LINECOLOR)
        button_w = Button(BTNWIDTH, BTNHEIGHT, (bg_width + NEXTX,  NEXTY),  NEXTLBL,  Keys.Next.value, COLORKEY, LINECOLOR)
        self.buttons = (button_c, button_q, button_w)

    def _init_boxes(self):
        self.hero_boxes = []
        for index, hero in enumerate(self.party):
            self.hero_boxes.append(HeroBox((HEROBOXX + index * HEROBOXVAR, HEROBOXY), HEROBOXW, HEROBOXH, index, hero))

        self.stats_box = StatsBox((STATBOXX,        STATBOXY), STATBOXW, STATBOXH)
        self.info_box = TextBox((INFOBOXX,          INFOBOXY), INFOBOXW, INFOBOXH)
        self.skills_box = SkillsBox((SKILBOXX,      SKILBOXY), SKILBOXW, SKILBOXH)
        self.inventory_box = InventoryBox((INVBOXX, INVBOXY),  INVBOXW,  INVBOXH)
        self.spells_box = SpellsBox((SPELBOXX,      SPELBOXY), SPELBOXW, SPELBOXH)
        self.pouch_box = PouchBox((PCHBOXX,         PCHBOXY),  PCHBOXW,  PCHBOXH)

    def _reset_vars(self):
        # variabelen voor klikken van upgrade stat
        self.upgrade_click = None
        self.selected_stat = None
        self.xp_cost = 0
        self.confirm_box = None

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
            self.engine.audio.play_sound(SFX.menu_select)
            if choice == yes:
                self.engine.data.party.remove(self.cur_hero)
                # update daarna het party scherm
                self.cur_hero = self.engine.data.party['alagos']
                self.party = list(self.engine.data.party.values())
                self.hc = self.party.index(self.cur_hero)
                self._init_boxes()
                self.party_changed = True
            self.leave_box = None

        # Als de upgrade stat confirmbox in beeld is geweest.
        elif self.upgrade_click:
            choice = self.confirm_box.cur_item
            yes = self.confirm_box.TOPINDEX
            if choice == yes:
                self.engine.audio.play_sound(SFX.upgrade)
                self.cur_hero.exp.rem -= self.xp_cost
                self.selected_stat.upgrade()
                self._init_boxes()
            else:
                self.engine.audio.play_sound(SFX.menu_select)

            self._reset_vars()

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
            self.stats_box.cur_item = None
            self.skills_box.cur_item = None
            self.spells_box.cur_item = None
            self.pouch_box.cur_item = None

            if self.invclick_box and self.invclick_box.rect.collidepoint(event.pos):
                self.info_label, self.hovered_equipment_item = self.invclick_box.mouse_hover(event)
            elif self.stats_box.rect.collidepoint(event.pos):
                self.info_label = self.stats_box.mouse_hover(event)
            elif self.skills_box.rect.collidepoint(event.pos):
                self.info_label = self.skills_box.mouse_hover(event)
            elif self.inventory_box.rect.collidepoint(event.pos):
                self.info_label = self.inventory_box.mouse_hover(event)
            elif self.spells_box.rect.collidepoint(event.pos):
                self.info_label = self.spells_box.mouse_hover(event)
            elif self.pouch_box.rect.collidepoint(event.pos):
                self.info_label = self.pouch_box.mouse_hover(event)

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == Keys.Leftclick.value:

                # als de clickbox er is en er wordt buiten geklikt, laat hem dan verdwijnen.
                if self.invclick_box and not self.invclick_box.rect.collidepoint(event.pos):
                    self.invclick_box = None

                elif self.invclick_box and self.invclick_box.rect.collidepoint(event.pos):
                    if self.invclick_box.mouse_click(event, self.engine.gamestate, self.engine.audio, self.cur_hero):
                        self.invclick_box = None
                    return  # anders vangt hij ook nog andere clicks hieronder in deze methode af

                if self._handle_stat_box_click(event):   # als er op een statsbox item geklikt wordt
                    return
                if self._handle_skill_box_click(event):  # of skillbox
                    return
                if self._handle_pouch_box_click(event):  # of pouchbox
                    return

                # als er op een herobox wordt geklikt of het kruisje daarvan.
                old_hc = self.hc
                for hero_box in self.hero_boxes:
                    self.hc, leave_party = hero_box.mouse_click(event, self.hc)
                    if leave_party:
                        self._leave_party()
                        return
                new_hc = self.hc
                if new_hc != old_hc:
                    self.engine.audio.play_sound(SFX.menu_switch)
                    self._init_boxes()

                # als er in de inventory box wordt geklikt
                if self.inventory_box.rect.collidepoint(event.pos):
                    # krijg de positie en equipment_type terug
                    boxpos, equipment_type = self.inventory_box.mouse_click(event)
                    # als er geen clickbox is en wel een equipment_type, geef dan een clickbox weer
                    if not self.invclick_box and equipment_type:
                        self.engine.audio.play_sound(SFX.menu_switch)
                        self.invclick_box = InvClickBox(boxpos, equipment_type, self.party, self.inventory)
                    return

                for button in self.buttons:
                    button_press = button.single_click(event)
                    if button_press == Keys.Exit.value:
                        self._close()
                    elif button_press == Keys.Prev.value:
                        self._previous()
                    elif button_press == Keys.Next.value:
                        self._next()

            elif event.button in (Keys.Scrollup.value, Keys.Scrolldown.value):
                if self.invclick_box and self.invclick_box.rect.collidepoint(event.pos):
                    self.invclick_box.mouse_scroll(event)
                if self.skills_box.rect.collidepoint(event.pos):
                    self.skills_box.mouse_scroll(event)
                if self.spells_box.rect.collidepoint(event.pos):
                    self.spells_box.mouse_scroll(event)
                if self.pouch_box.rect.collidepoint(event.pos):
                    self.pouch_box.mouse_scroll(event)
                return

        elif event.type == pygame.KEYDOWN:

            # als de clickbox er is en er wordt een toets gedrukt, laat hem dan verdwijnen.
            if self.invclick_box:
                self.invclick_box = None
            self.info_label = ""

            if event.key in (Keys.Exit.value, Keys.Inv.value):
                self._close()
            elif event.key == Keys.Prev.value:
                self._previous()
            elif event.key == Keys.Next.value:
                self._next()
            elif event.key == Keys.Delete.value:
                self._leave_party()
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
            button.update(self.key_input, COLORKEY)

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
        self.screen.fill(BACKGROUNDCOLOR)
        self.screen.blit(self.background, (0, 0))

        for button in self.buttons:
            button.render(self.screen, LINECOLOR)

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

    def _handle_stat_box_click(self, event):
        """
        ...
        :param event:
        :return:
        """
        if self.stats_box.rect.collidepoint(event.pos):
            self.upgrade_click, self.selected_stat = self.stats_box.mouse_click(event)
            if self.upgrade_click:
                self.xp_cost = self.selected_stat.xp_cost
                success, text = self.selected_stat.is_able_to_upgrade(self.cur_hero.exp.rem)
                if success:
                    text = ["{}: {}  --> {}.".format(self.selected_stat.NAM,
                                                     self.selected_stat.qty, self.selected_stat.qty + 1),
                            "You have {} XP Remaining.".format(self.cur_hero.exp.rem),
                            "Are you sure you wish to train",
                            "the stat {} for {} XP?".format(self.selected_stat.NAM, self.xp_cost),
                            "",
                            "Yes",
                            "No"]
                    self.confirm_box = ConfirmBox(self.engine.gamestate, self.engine.audio, text, sound=SFX.message)
                    self.engine.gamestate.push(self.confirm_box)
                else:
                    push_object = MessageBox(self.engine.gamestate, self.engine.audio, text, sound=SFX.menu_cancel)
                    self.engine.gamestate.push(push_object)
                    self._reset_vars()
            return True
        return False

    def _handle_skill_box_click(self, event):
        """
        ...
        :param event:
        :return:
        """
        if self.skills_box.rect.collidepoint(event.pos):
            skill_click, selected_skill = self.skills_box.mouse_click(event)
            if skill_click:
                if selected_skill == self.cur_hero.alc:
                    self.engine.audio.play_sound(SFX.scroll)
                    push_object = Alchemist(self.engine, self.cur_hero)
                    self.engine.gamestate.push(push_object)
                    self.engine.gamestate.push(Transition(self.engine.gamestate))
            return True
        return False

    def _handle_pouch_box_click(self, event):
        """
        ...
        :param event:
        :return:
        """
        if self.pouch_box.rect.collidepoint(event.pos):
            pouch_click, selected_item = self.pouch_box.mouse_click(event)
            if pouch_click:
                # todo, maken dat in battle je niet op deze manier potions kan drinken.
                able, message = selected_item.use(self.cur_hero)
                if able and message:
                    push_object = MessageBox(self.engine.gamestate, self.engine.audio, message, sound=SFX.message)
                    self.engine.gamestate.push(push_object)
                elif not able and message:
                    push_object = MessageBox(self.engine.gamestate, self.engine.audio, message, sound=SFX.menu_cancel)
                    self.engine.gamestate.push(push_object)
            return True
        return False

    def _leave_party(self):
        if self.hc != 0:    # als het niet alagos zelf is.
            text = ["Do you want me to leave your party?",
                    "",
                    "Yes, you may leave.",
                    "No, I want you to stay."]
            self.leave_box = ConfirmBox(self.engine.gamestate, self.engine.audio,
                                        text, self.cur_hero.FAC, sound=SFX.message)
            self.engine.gamestate.push(self.leave_box)

    def _previous(self):
        self.engine.audio.play_sound(SFX.menu_switch)
        self.hc -= 1
        if self.hc < 0:
            self.hc = len(self.party) - 1
        self._init_boxes()

    def _next(self):
        self.engine.audio.play_sound(SFX.menu_switch)
        self.hc += 1
        if self.hc > len(self.party) - 1:
            self.hc = 0
        self._init_boxes()
