
"""
class: Display
"""

import pygame

from components import Button
from components import MessageBox
from components import Parchment

from constants import EquipmentType as EqTy
from constants import GameState
from constants import Keys
from constants import SFX

from database import PouchItemDatabase

import inventoryitems

from .createbox import CreateBox
from .inventorybox import InventoryBox
from screens.shop.selector import Selector

COLORKEY = pygame.Color("white")
FONTCOLOR = pygame.Color("black")

CREATETITLE = "Create"
INVENTORYTITLE = "Invent."
TITLEPOSX = 1/16
TITLEPOSY = 1/32
FACEPOSX = 1/16
FACEPOSY = 3/16
EXTRAFACESIZEX = 20
EXTRAFACESIZEY = 0
LINESNEXTTOFACE = 4
SMALLLINEHEIGHT = 27

STATITLE = "Stamina {}: "
STATITLEPOSX = 1/16
STATITLEPOSY = 70/100

INFOBOXWIDTH = 30/100
INFOBOXHEIGHT = 16/100
INFOBOXPOSX = 1/16
INFOBOXPOSY = 76/100

BTNWIDTH = 70
BTNHEIGHT = 40
CLOSELBL = "Close"
CLOSEX, CLOSEY = -100, 40    # negatieve x omdat de positie van rechts bepaald wordt.

EXTRAHEIGHT = 0         # zodat de laatste item er voor helft op komt

CREATEBOXWIDTH = 20 / 100
CREATEBOXHEIGHT = 73 / 100
CREATEBOXPOSX = 40 / 100
CREATEBOXPOSY = 6 / 32

INVENTORYBOXWIDTH = 26/100
INVENTORYBOXHEIGHT = 73/100
INVENTORYBOXPOSX = 64/100
INVENTORYBOXPOSY = 6/32

SELECTORPOSX = 2/32
SELECTORPOSY = 65/100
SELECTORWIDTH = 36

CREATELIST = [EqTy.wpn, EqTy.sld, EqTy.hlm, EqTy.arm, EqTy.clk, EqTy.glv, EqTy.blt, EqTy.bts]


class Display(Parchment):
    """
    ...
    """
    def __init__(self, engine, hero):
        super().__init__(engine)

        self.eqptype = CREATELIST[0]

        self.name = GameState.Shop

        self.create_title = self.largefont.render(CREATETITLE, True, FONTCOLOR).convert_alpha()
        self.inventory_title = self.largefont.render(INVENTORYTITLE, True, FONTCOLOR).convert_alpha()

        self.cur_hero = hero
        self._init_selectors()
        self._init_face()
        self._init_boxes()

        self.close_button = Button(
            BTNWIDTH, BTNHEIGHT, (self.background.get_width() + CLOSEX, CLOSEY), CLOSELBL, Keys.Exit.value,
            COLORKEY, FONTCOLOR)

    def _init_face(self):
        face_image = pygame.image.load(self.cur_hero.FAC).convert_alpha()
        self.background.blit(face_image, (self._set_x(FACEPOSX), self._set_y(FACEPOSY)))

        for index, line in enumerate(self.cur_hero.mec.welcome_text(self.cur_hero.NAM)):
            rline = self.smallfont.render(line, True, FONTCOLOR).convert_alpha()
            if index < LINESNEXTTOFACE:
                self.background.blit(rline,
                                     (self._set_x(FACEPOSX) + face_image.get_width() + EXTRAFACESIZEX,
                                      self._set_y(FACEPOSY) + EXTRAFACESIZEY + index * SMALLLINEHEIGHT))
            else:
                self.background.blit(rline,
                                     (self._set_x(FACEPOSX),
                                      self._set_y(FACEPOSY) + EXTRAFACESIZEY + index * SMALLLINEHEIGHT))

    def _init_selectors(self):
        self.selectors = pygame.sprite.Group()

        for index, eqp_type in enumerate(CREATELIST):
            self.selectors.add(Selector(self._set_x(SELECTORPOSX) + index * SELECTORWIDTH,
                                        self._set_y(SELECTORPOSY), eqp_type))

        self.selectors.draw(self.background)

    def _init_boxes(self):
        self._init_infobox(INFOBOXWIDTH, INFOBOXHEIGHT, INFOBOXPOSX, INFOBOXPOSY)
        self._init_createbox()
        self._init_inventorybox()

    def _init_createbox(self):
        width = self.screen.get_width() * CREATEBOXWIDTH
        height = self.screen.get_height() * CREATEBOXHEIGHT + EXTRAHEIGHT

        if self.eqptype == EqTy.wpn:
            from database.weapon import WeaponDatabase as DataBase
        elif self.eqptype == EqTy.sld:
            from database.shield import ShieldDatabase as DataBase
        elif self.eqptype == EqTy.hlm:
            from database.helmet import HelmetDatabase as DataBase
        elif self.eqptype == EqTy.arm:
            from database.armor import ArmorDatabase as DataBase
        elif self.eqptype == EqTy.clk:
            from database.cloak import CloakDatabase as DataBase
        elif self.eqptype == EqTy.glv:
            from database.gloves import GlovesDatabase as DataBase
        elif self.eqptype == EqTy.blt:
            from database.belt import BeltDatabase as DataBase
        elif self.eqptype == EqTy.bts:
            from database.boots import BootsDatabase as DataBase
        else:
            raise AttributeError

        self.createbox = CreateBox(self._set_x(CREATEBOXPOSX), self._set_y(CREATEBOXPOSY), int(width), int(height),
                                   DataBase)

    def _init_inventorybox(self):
        width = self.screen.get_width() * INVENTORYBOXWIDTH
        height = self.screen.get_height() * INVENTORYBOXHEIGHT + EXTRAHEIGHT
        self.inventorybox = InventoryBox(self._set_x(INVENTORYBOXPOSX), self._set_y(INVENTORYBOXPOSY),
                                         int(width), int(height),
                                         self.eqptype, self.engine.data.party,
                                         self.engine.data.pouch, self.engine.data.inventory)

    def single_input(self, event):
        """
        Handelt de muis en keyboard input af.
        :param event: pygame.event.get()
        """
        if event.type == pygame.MOUSEMOTION:
            self.info_label = ""
            self.createbox.cur_item = None
            self.inventorybox.cur_item = None

            if self.createbox.rect.collidepoint(event.pos):
                selected_name, self.info_label = self.createbox.mouse_hover(event)
            if self.inventorybox.rect.collidepoint(event.pos):
                selected_name, self.info_label = self.inventorybox.mouse_hover(event)

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == Keys.Leftclick.value:

                if self.close_button.single_click(event) == Keys.Exit.value:
                    self._close()
                if self._handle_create_box_click(event):
                    return

                for selector in self.selectors:
                    eqptype = selector.mouse_click(event)
                    if eqptype:
                        if eqptype != self.eqptype:
                            self.engine.audio.play_sound(SFX.menu_switch)
                            self.eqptype = eqptype
                            self._init_boxes()
                            break

            elif event.button in (Keys.Scrollup.value, Keys.Scrolldown.value):
                if self.createbox.rect.collidepoint(event.pos):
                    self.createbox.mouse_scroll(event)
                if self.inventorybox.rect.collidepoint(event.pos):
                    self.inventorybox.mouse_scroll(event)

        elif event.type == pygame.KEYDOWN:
            if event.key == Keys.Exit.value:
                self._close()
            elif event.key == Keys.Prev.value:
                self._previous()
            elif event.key == Keys.Next.value:
                self._next()

    def update(self, dt):
        """
        Update de selector border color.
        Update de gold quantity.
        :param dt: self.clock.tick(FPS)/1000.0
        """
        for selector in self.selectors:
            selector.update(self.eqptype)

    def render(self):
        """
        Teken alles op het scherm.
        """
        super().render()

        mec_title = self.largefont.render(self.cur_hero.mec.NAM, True, FONTCOLOR).convert_alpha()
        self.screen.blit(mec_title, (self._set_x(TITLEPOSX), self._set_y(TITLEPOSY)))

        self.screen.blit(self.create_title, ((self._set_x(CREATEBOXPOSX)) +
                                             (self.screen.get_width() * CREATEBOXWIDTH / 2) -
                                             (self.create_title.get_width() / 2),
                                             self._set_y(TITLEPOSY)))
        self.screen.blit(self.inventory_title, ((self._set_x(INVENTORYBOXPOSX)) +
                                                (self.screen.get_width() * INVENTORYBOXWIDTH / 2) -
                                                (self.inventory_title.get_width() / 2),
                                                self._set_y(TITLEPOSY)))

        sta_title = self.middlefont.render(
                    STATITLE.format(self.cur_hero.NAM) + str(self.cur_hero.sta.cur), True, FONTCOLOR).convert_alpha()
        self.screen.blit(sta_title, (self._set_x(STATITLEPOSX), self._set_y(STATITLEPOSY)))

        self.selectors.draw(self.background)

        self.createbox.render(self.screen)
        self.inventorybox.render(self.screen)
        self.close_button.render(self.screen, FONTCOLOR)

    def _handle_create_box_click(self, event):
        create_click, selected_equipment = self.createbox.mouse_click(event)
        if create_click:
            cloth = inventoryitems.factory_pouch_item(PouchItemDatabase.cloth)
            leather = inventoryitems.factory_pouch_item(PouchItemDatabase.leather)
            wood = inventoryitems.factory_pouch_item(PouchItemDatabase.wood)
            metals = inventoryitems.factory_pouch_item(PouchItemDatabase.metals)
            clt_qty = self.engine.data.pouch.get_quantity(cloth)
            ltr_qty = self.engine.data.pouch.get_quantity(leather)
            wod_qty = self.engine.data.pouch.get_quantity(wood)
            mtl_qty = self.engine.data.pouch.get_quantity(metals)

            if selected_equipment.CLT > clt_qty or \
               selected_equipment.LTR > ltr_qty or \
               selected_equipment.WOD > wod_qty or \
               selected_equipment.MTL > mtl_qty:
                text = ["You do not have the right components",
                        "to create that {}.".format(selected_equipment.NAM)]
                push_object = MessageBox(self.engine.gamestate, self.engine.audio, text, sound=SFX.menu_cancel)
                self.engine.gamestate.push(push_object)
                return True
            elif self.cur_hero.sta.cur < self.cur_hero.mec.STA_COST:
                text = ["You do not have enough stamina",
                        "to create that {}.".format(selected_equipment.NAM)]
                push_object = MessageBox(self.engine.gamestate, self.engine. audio, text, sound=SFX.menu_cancel)
                self.engine.gamestate.push(push_object)
                return True
            elif 'pouch is full' is False:  # todo, moet 'pouch is vol' hier? of in pouch?
                self.engine.audio.play_sound(SFX.menu_cancel)
                return True

            self.engine.data.pouch.remove(cloth, selected_equipment.CLT, force=True)  # want kan ook 0 zijn.
            self.engine.data.pouch.remove(leather, selected_equipment.LTR, force=True)
            self.engine.data.pouch.remove(wood, selected_equipment.WOD, force=True)
            self.engine.data.pouch.remove(metals, selected_equipment.MTL, force=True)

            self.cur_hero.sta.cur -= self.cur_hero.mec.STA_COST

            # hoog het custom nummer op en zet die achter de .RAW zodat er meerdere customs in de inventory kunnen
            self.engine.data.custom_inventory_counter += 1
            selected_equipment.RAW += str(self.engine.data.custom_inventory_counter)

            # loop door alle attributen van selected_equipment heen
            # list(), zodat uit de iterate verwijderd kan worden
            for attr, value in list(vars(selected_equipment).items()):
                # als er een waarde van een attribute op 'X' vanuit de database staat,
                # dat betekent dat hij nog gevuld moet worden.
                if value == 'X':
                    # wat is de waarde van de gelijknamige attribute met 'MIN_' ervoor
                    min_value = getattr(selected_equipment, 'MIN_'+attr)
                    max_value = getattr(selected_equipment, 'MAX_'+attr)
                    # vraag bij de Mechanic Skill de berekende waarden op. en zet attribute op die waarde.
                    setattr(selected_equipment, attr, self.cur_hero.mec.get_eqp_itm_attr_value(min_value, max_value))
                    # en verwijder de overblijfselen
                    delattr(selected_equipment, 'MIN_'+attr)
                    delattr(selected_equipment, 'MAX_'+attr)

            text = ["{} successfully created.".format(selected_equipment.NAM)]
            self.engine.data.inventory.add_i(selected_equipment)
            push_object = MessageBox(self.engine.gamestate, self.engine.audio, text, sound=SFX.message)
            self.engine.gamestate.push(push_object)

            self._init_boxes()
            return True
        return False

    def _previous(self):
        self.engine.audio.play_sound(SFX.menu_switch)
        for index, eqptype in enumerate(CREATELIST):
            if eqptype == self.eqptype:
                i = index - 1
                if i < 0:
                    i = len(CREATELIST) - 1
                self.eqptype = CREATELIST[i]
                self._init_boxes()
                break

    def _next(self):
        self.engine.audio.play_sound(SFX.menu_switch)
        for index, eqptype in enumerate(CREATELIST):
            if eqptype == self.eqptype:
                i = index + 1
                if i >= len(CREATELIST):
                    i = 0
                self.eqptype = CREATELIST[i]
                self._init_boxes()
                break
