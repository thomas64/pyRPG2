
"""
class: Display
"""

import pygame

from components import Button
from components import ConfirmBox
from components import MessageBox
from components import Parchment

from constants import GameState
from constants import Keys
from constants import SFX

from database import SchoolDatabase
from database import PouchItemDatabase
import inventoryitems

from .knownbox import KnownBox
from .learnbox import LearnBox
from .selector import Selector


COLORKEY = pygame.Color("white")

FACEPOSX = 1/16
FACEPOSY = 3/16

FONTCOLOR = pygame.Color("black")

SMALLLINEHEIGHT = 30
EXTRAFACESIZE = 20
LINESNEXTTOFACE = 3

KNOWNBOXWIDTH = 7/32    # van het scherm
KNOWNBOXHEIGHT = 24/32
KNOWNBOXPOSX = 2/5      # x op 2/5 van het scherm
KNOWNBOXPOSY = 6/32

LEARNBOXWIDTH = 9/32
LEARNBOXHEIGHT = 24/32
LEARNBOXPOSX = 21/32
LEARNBOXPOSY = 6/32

EXTRAHEIGHT = 0         # zodat de laatste item er voor helft op komt

HEROTITLEPOSX = 1/16
LEARNTITLE = "Learn"
KNOWNTITLE = "Known"
TITLEPOSY = 1/32
GOLDTITLE = "Gold: "
XPTITLE = "XP Remaining: "

OBJECTDATABASE = SchoolDatabase
OBJECTTYPE = "spell"

CURRENTRANK1 = "Current"
CURRENTRANK2 = "Rank:"
SPELLNAME1 = "Spell"
SPELLNAME2 = "Name:"
NEXTRANK1 = "Next"
NEXTRANK2 = "Rank:"
GOLDCOST1 = "Gold"
GOLDCOST2 = "Cost:"
XPCOST1 = "XP"
XPCOST2 = "Cost:"
SUBTITLEPOSX = 5
SUBTITLEPOSY1 = 15/100
SUBTITLEPOSY2 = 17/100

INFOBOXWIDTH = 8/32
INFOBOXHEIGHT = 7/32
INFOBOXPOSX = 2/32
INFOBOXPOSY = 23/32

SELECTORPOSX = 2/32
SELECTORPOSY = 18/32
SELECTORWIDTH = 36

GOLDTITLEPOSX = 1/16
GOLDTITLEPOSY = 39/64
XPTITLEPOSX = 1/16
XPTITLEPOSY = 42/64

BTNWIDTH = 70
BTNHEIGHT = 40
CLOSELBL = "Close"
CLOSEX, CLOSEY = -100, 40    # negatieve x omdat de positie van rechts bepaald wordt.


class Display(Parchment):
    """
    ...
    """
    def __init__(self, engine, schooltype_list, face):
        super().__init__(engine)

        self.schooltype_list = schooltype_list

        self.selected_hero = self.engine.data.party['alagos']  # todo, alagos moet eigenlijk niet hard coded zijn

        self.name = GameState.Shop

        self.learn_title = self.largefont.render(LEARNTITLE, True, FONTCOLOR).convert_alpha()
        self.known_title = self.largefont.render(KNOWNTITLE, True, FONTCOLOR).convert_alpha()
        self.gold_amount = None
        self.xp_amount = None

        self._init_database()
        self._init_selectors()
        self._init_face(face)
        self._init_boxes()

        self.close_button = Button(
            BTNWIDTH, BTNHEIGHT, (self.background.get_width() + CLOSEX, CLOSEY), CLOSELBL, Keys.Exit.value,
            COLORKEY, FONTCOLOR)

        self.gold_object = inventoryitems.factory_pouch_item(PouchItemDatabase.gold)

        self._reset_vars()

        self.object_type = OBJECTTYPE

    def _init_database(self):
        self.object_database = OBJECTDATABASE

    def _init_selectors(self):

        self.selectors = pygame.sprite.Group()

        for index, hero in enumerate(self.engine.data.party.values()):
            self.selectors.add(Selector(self._set_x(SELECTORPOSX) + index * SELECTORWIDTH,
                                        self._set_y(SELECTORPOSY), hero))

        self.selectors.draw(self.background)

    def _init_face(self, face):
        face_image = pygame.image.load(face).convert_alpha()
        self.background.blit(face_image, (self._set_x(FACEPOSX), self._set_y(FACEPOSY)))

        for index, line in enumerate(self.object_database.welcome_text()):
            rline = self.smallfont.render(line, True, FONTCOLOR).convert_alpha()
            if index < LINESNEXTTOFACE:
                self.background.blit(rline,
                                     (self._set_x(FACEPOSX) + face_image.get_width() + EXTRAFACESIZE,
                                      self._set_y(FACEPOSY) + EXTRAFACESIZE + index * SMALLLINEHEIGHT))
            else:
                self.background.blit(rline,
                                     (self._set_x(FACEPOSX),
                                      self._set_y(FACEPOSY) + EXTRAFACESIZE + index * SMALLLINEHEIGHT))

    def _init_boxes(self):
        self._init_knownbox()
        self._init_learnbox()
        self._init_infobox(INFOBOXWIDTH, INFOBOXHEIGHT, INFOBOXPOSX, INFOBOXPOSY)

    def _init_knownbox(self):
        width = self.screen.get_width() * KNOWNBOXWIDTH
        height = self.screen.get_height() * KNOWNBOXHEIGHT + EXTRAHEIGHT
        self.knownbox = KnownBox(self._set_x(KNOWNBOXPOSX), self._set_y(KNOWNBOXPOSY), int(width), int(height),
                                 self.selected_hero)

    def _init_learnbox(self):
        width = self.screen.get_width() * LEARNBOXWIDTH
        height = self.screen.get_height() * LEARNBOXHEIGHT + EXTRAHEIGHT
        self.learnbox = LearnBox(self._set_x(LEARNBOXPOSX), self._set_y(LEARNBOXPOSY), int(width), int(height),
                                 self.schooltype_list, self.selected_hero)

    def _reset_vars(self):
        self.learn_click = False
        self.selected_spell = None
        self.gold_cost = 0
        self.xp_cost = 0
        self.confirm_box = None

    def on_enter(self):
        """
        Wanneer deze state op de stack komt, voer dit uit.
        Handel af als er een learn confirmbox is geweest.
        """
        if self.learn_click:
            choice = self.confirm_box.cur_item
            yes = self.confirm_box.TOPINDEX
            if choice == yes:
                self.engine.audio.play_sound(SFX.upgrade)
                self.engine.data.pouch.remove(self.gold_object, self.gold_cost)
                self.selected_hero.exp.rem -= self.xp_cost
                # hier staat selected_spell eventueel nog op 0
                self._on_enter2()
                self._init_boxes()
            else:
                self.engine.audio.play_sound(SFX.menu_select)

            self._reset_vars()

    def _on_enter2(self):
        """
        polymorph met trainer display
        """
        self.selected_hero.scl.add_s(self.selected_spell)

    def single_input(self, event):
        """
        Handelt de muis en keyboard input af.
        :param event: pygame.event.get()
        """

        if event.type == pygame.MOUSEMOTION:

            self.info_label = ""
            self.knownbox.cur_item = None
            self.learnbox.cur_item = None

            if self.knownbox.rect.collidepoint(event.pos):
                selected_name, self.info_label = self.knownbox.mouse_hover(event)
                self.learnbox.duplicate_selection(selected_name)
            if self.learnbox.rect.collidepoint(event.pos):
                selected_name, self.info_label = self.learnbox.mouse_hover(event)
                self.knownbox.duplicate_selection(selected_name)

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == Keys.Leftclick.value:

                if self.close_button.single_click(event) == Keys.Exit.value:
                    self._close()

                for selector in self.selectors:
                    hero = selector.mouse_click(event)
                    if hero:
                        if hero != self.selected_hero:
                            self.engine.audio.play_sound(SFX.menu_switch)
                            self.selected_hero = hero
                            self._init_boxes()
                            break

                if self._handle_learn_box_click(event):
                    return

            elif event.button in (Keys.Scrollup.value, Keys.Scrolldown.value):
                if self.knownbox.rect.collidepoint(event.pos):
                    self.knownbox.mouse_scroll(event)
                if self.learnbox.rect.collidepoint(event.pos):
                    self.learnbox.mouse_scroll(event)

        elif event.type == pygame.KEYDOWN:
            if event.key == Keys.Exit.value:
                self._close()
            elif event.key == Keys.Prev.value:
                self._previous()
            elif event.key == Keys.Next.value:
                self._next()

    def multi_input(self, key_input, mouse_pos, dt):
        """
        :param key_input: pygame.key.get_pressed()
        :param mouse_pos: pygame.mouse.get_pos()
        :param dt: self.clock.tick(FPS)/1000.0
        """
        # cheat voor xp erbij ctrl+
        if key_input[pygame.K_LCTRL] or key_input[pygame.K_RCTRL]:
            if key_input[pygame.K_KP_PLUS]:
                self.selected_hero.gain_experience(1)
            elif key_input[pygame.K_KP_MINUS]:
                self.selected_hero.gain_experience(-1)

    def update(self, dt):
        """
        Update de selector border color.
        Update de gold en xp quantity.
        :param dt: self.clock.tick(FPS)/1000.0
        """
        for selector in self.selectors:
            selector.update(self.selected_hero)
        self.gold_amount = self.engine.data.pouch.get_quantity(self.gold_object)
        self.xp_amount = self.selected_hero.exp.rem

    def render(self):
        """
        Teken alles op het scherm, de titels, de boxen.
        """
        super().render()

        # titels midden boven de boxen
        self.screen.blit(self.learn_title, ((self._set_x(LEARNBOXPOSX)) +
                                            (self.screen.get_width() * LEARNBOXWIDTH / 2) -
                                            (self.learn_title.get_width() / 2),
                                            self._set_y(TITLEPOSY)))
        self.screen.blit(self.known_title, ((self._set_x(KNOWNBOXPOSX)) +
                                            (self.screen.get_width() * KNOWNBOXWIDTH / 2) -
                                            (self.known_title.get_width() / 2),
                                            self._set_y(TITLEPOSY)))

        hero_title = self.largefont.render(self.selected_hero.NAM, True, FONTCOLOR).convert_alpha()
        self.screen.blit(hero_title, (self._set_x(HEROTITLEPOSX), self._set_y(TITLEPOSY)))
        gold_title = self.middlefont.render(GOLDTITLE + str(self.gold_amount), True, FONTCOLOR).convert_alpha()
        self.screen.blit(gold_title, (self._set_x(GOLDTITLEPOSX), self._set_y(GOLDTITLEPOSY)))
        xp_title = self.middlefont.render(XPTITLE + str(self.xp_amount), True, FONTCOLOR).convert_alpha()
        self.screen.blit(xp_title, (self._set_x(XPTITLEPOSX), self._set_y(XPTITLEPOSY)))

        # afwijkende SPELLNAME1. object_type gebruikt. vanwege polymorph van trainer.
        spellname1 = self.tinyfont.render(self.object_type.title(), True, FONTCOLOR).convert_alpha()
        spellname2 = self.tinyfont.render(SPELLNAME2, True, FONTCOLOR).convert_alpha()
        currentrank1 = self.tinyfont.render(CURRENTRANK1, True, FONTCOLOR).convert_alpha()
        currentrank2 = self.tinyfont.render(CURRENTRANK2, True, FONTCOLOR).convert_alpha()
        spellname3 = self.tinyfont.render(self.object_type.title(), True, FONTCOLOR).convert_alpha()
        spellname4 = self.tinyfont.render(SPELLNAME2, True, FONTCOLOR).convert_alpha()
        nextrank1 = self.tinyfont.render(NEXTRANK1, True, FONTCOLOR).convert_alpha()
        nextrank2 = self.tinyfont.render(NEXTRANK2, True, FONTCOLOR).convert_alpha()
        goldcost1 = self.tinyfont.render(GOLDCOST1, True, FONTCOLOR).convert_alpha()
        goldcost2 = self.tinyfont.render(GOLDCOST2, True, FONTCOLOR).convert_alpha()
        xpcost1 = self.tinyfont.render(XPCOST1, True, FONTCOLOR).convert_alpha()
        xpcost2 = self.tinyfont.render(XPCOST2, True, FONTCOLOR).convert_alpha()

        import screens.school.knownbox as kb  # importeer het hele bestand, niet alleen de class zoals hier bovenaan.
        xpos = self._set_x(KNOWNBOXPOSX) + SUBTITLEPOSX
        self.screen.blit(spellname1, (xpos + kb.COLUMN2X, self._set_y(SUBTITLEPOSY1)))
        self.screen.blit(spellname2, (xpos + kb.COLUMN2X, self._set_y(SUBTITLEPOSY2)))
        self.screen.blit(currentrank1, (xpos + kb.COLUMN3X, self._set_y(SUBTITLEPOSY1)))
        self.screen.blit(currentrank2, (xpos + kb.COLUMN3X, self._set_y(SUBTITLEPOSY2)))

        import screens.school.learnbox as lb
        xpos = self._set_x(LEARNBOXPOSX) + SUBTITLEPOSX
        self.screen.blit(spellname3, (xpos + lb.COLUMN2X, self._set_y(SUBTITLEPOSY1)))
        self.screen.blit(spellname4, (xpos + lb.COLUMN2X, self._set_y(SUBTITLEPOSY2)))
        self.screen.blit(nextrank1, (xpos + lb.COLUMN3X, self._set_y(SUBTITLEPOSY1)))
        self.screen.blit(nextrank2, (xpos + lb.COLUMN3X, self._set_y(SUBTITLEPOSY2)))
        self.screen.blit(goldcost1, (xpos + lb.COLUMN4X, self._set_y(SUBTITLEPOSY1)))
        self.screen.blit(goldcost2, (xpos + lb.COLUMN4X, self._set_y(SUBTITLEPOSY2)))
        self.screen.blit(xpcost1, (xpos + lb.COLUMN5X, self._set_y(SUBTITLEPOSY1)))
        self.screen.blit(xpcost2, (xpos + lb.COLUMN5X, self._set_y(SUBTITLEPOSY2)))

        self.selectors.draw(self.background)

        self.knownbox.render(self.screen)
        self.learnbox.render(self.screen)
        self.close_button.render(self.screen, FONTCOLOR)

    def _handle_learn_box_click(self, event):
        self.learn_click, self.selected_spell = self.learnbox.mouse_click(event)
        # selected_spell is hier eventueel .qty = 0
        if self.learn_click:
            self.gold_cost = self.selected_spell.gold_cost
            self.xp_cost = self.selected_spell.xp_cost
            succes, text = self._handle_learn_box_click2()
            if succes:
                text = ["{}: {}  --> {}.".format(self.selected_spell.NAM,
                                                 self.selected_spell.qty, self.selected_spell.qty + 1),
                        "Are you sure you wish to learn the",
                        "{} {} for {} XP and {} gold?".format(self.object_type, self.selected_spell.NAM,
                                                              self.xp_cost, self.gold_cost),
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

    def _handle_learn_box_click2(self):
        """
        polymorph met trainer display
        """
        return self.selected_hero.scl.is_able_to_learn(self.selected_spell, self.selected_hero.wiz.qty,
                                                       self.xp_amount, self.gold_amount)

    def _previous(self):
        self.engine.audio.play_sound(SFX.menu_switch)
        party_list = list(self.engine.data.party.values())
        index = party_list.index(self.selected_hero)
        index -= 1
        if index < 0:
            index = len(party_list)-1
        self.selected_hero = party_list[index]
        self._init_boxes()

    def _next(self):
        self.engine.audio.play_sound(SFX.menu_switch)
        party_list = list(self.engine.data.party.values())
        index = party_list.index(self.selected_hero)
        index += 1
        if index > len(party_list)-1:
            index = 0
        self.selected_hero = party_list[index]
        self._init_boxes()
