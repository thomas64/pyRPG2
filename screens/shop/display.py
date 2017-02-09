
"""
class: Display
"""

import collections
import importlib

import pygame

from components import ConfirmBox
from components import MessageBox
from components import Parchment

from constants import GameState
from constants import SFX
from constants import EquipmentType
from constants import WeaponType

from database import PouchItemDatabase
from database import ShopDatabase
import inventoryitems

from .buybox import BuyBox
from .selector import Selector
from .sellbox import SellBox


SOURCETITLE1 = "Gold: {}"


class Display(Parchment):
    """
    ...
    """
    def __init__(self, engine, shoptype_list, shopmaterial_list, face):
        super().__init__(engine, "Buy", "Sell")

        # is een list van bijv: [EquipmentType.arm, WeaponType.swd]
        self.subtype_list = list(shoptype_list)  # het moet een kopie van de lijst zijn, niet de lijst zelf,
        # vanwege de _init_selectors(), waar iets uit de lijst vervangen wordt. door een kopie te maken kan dat.
        self.subtype = self.subtype_list[0]
        self.material_list = shopmaterial_list
        self.databases = {}

        self.name = GameState.Shop

        self.main_title_pos_x = 1 / 16
        self.main_title_pos_y = 1 / 32
        self.source_title1 = SOURCETITLE1
        self.source_title1_pos_x = 1 / 16
        self.source_title1_pos_y = 11 / 16
        self.sub_title_pos_x = 5
        self.sub_title_pos_y1 = 15 / 100
        self.sub_title_pos_y2 = 17 / 100

        self.face_pos_x = 1 / 16
        self.face_pos_y = 3 / 16
        self.extra_face_size_x = 20
        self.extra_face_size_y = 20
        self.lines_next_to_face = 3
        self.small_line_height = 30

        self.leftbox_width = 3 / 16
        self.leftbox_height = 73 / 100
        self.leftbox_pos_x = 2 / 5
        self.leftbox_pos_y = 6 / 32
        self.rightbox_width = 5 / 16
        self.rightbox_height = 73 / 100
        self.rightbox_pos_x = 15 / 24
        self.rightbox_pos_y = 6 / 32
        self.infobox_width = 1 / 4
        self.infobox_height = 1 / 6
        self.infobox_pos_x = 1 / 16
        self.infobox_pos_y = 6 / 8

        self.selector_pos_x = 2 / 32
        self.selector_pos_y = 20 / 32
        self.selector_width = 36

        self.gold_amount = None
        self.gold_object = inventoryitems.factory_pouch_item(PouchItemDatabase.gold)
        self.sum_merchant = self.engine.data.party.get_sum_value_of_skill("mer")

        self._init_face_and_text(face, ShopDatabase.welcome_text())
        self._init_selectors()
        self._init_boxes()
        self._init_buttons()

        self._reset_vars()

    def _reset_vars(self):
        self.buy_click = False
        self.sell_click = False
        self.selected_item = None
        self.tot_quantity = 0
        self.sel_quantity = []
        self.value = 0
        self.confirm_box = None

    def _init_selectors(self):
        for index, shoptype in enumerate(self.subtype_list):

            if type(shoptype) == WeaponType:
                self.databases[shoptype.name] = collections.OrderedDict()
                from database import WeaponDatabase
                # omdat alle wapens in wpn zitten moet de database opnieuw opgebouwd worden met alleen de juiste wapens
                for weapon_itm in WeaponDatabase:
                    if weapon_itm.value['skl'] == shoptype:
                        self.databases[shoptype.name][weapon_itm.name] = weapon_itm

            # pouchitems zijn een tuple, zie shopdatabase, equipmentitems zijn enum.
            elif type(shoptype) == tuple:
                self.databases[shoptype[0].name] = collections.OrderedDict()
                for pouch_itm in shoptype[1]:
                    self.databases[shoptype[0].name][pouch_itm.name] = pouch_itm

                # maak van de tuple in de lijst een enum, net zoals de rest uit lijst.
                self.subtype_list[index] = shoptype[0]
                # doe deze ook eventjes voor hieronder in de selectors.add()
                shoptype = shoptype[0]

            else:
                self.databases[shoptype.name] = collections.OrderedDict()
                db_select = dict(acy='AccessoryDatabase', amu='AmuletDatabase', arm='ArmorDatabase', blt='BeltDatabase',
                                 bts='BootsDatabase', brc='BraceletDatabase', clk='CloakDatabase', glv='GlovesDatabase',
                                 hlm='HelmetDatabase', rng='RingDatabase', sld='ShieldDatabase')
                # importeer de juiste db's voor de shop
                lib = importlib.import_module("database." + shoptype.value.lower())
                # zet de enum_db vanuit die import in een dict.
                enum_db = getattr(lib, db_select[shoptype.name])  # enum_db is bijv HelmetDatabase
                for equipment_itm in enum_db:
                    if equipment_itm.value['typ'] == shoptype:
                        self.databases[shoptype.name][equipment_itm.name] = equipment_itm

            # voeg selector objecten toe
            self.selectors.add(Selector(self._set_x(self.selector_pos_x) + index * self.selector_width,
                                        self._set_y(self.selector_pos_y), shoptype))

    def _init_boxes(self):
        self._init_infobox()
        self._init_buybox()
        self._init_sellbox()

    def _init_buybox(self):
        width = self.screen.get_width() * self.leftbox_width
        height = self.screen.get_height() * self.leftbox_height
        database = self.databases[self.subtype.name]
        # extra stukje voor als er een bepaalde materiaal lijst is, voeg alleen die met de juiste materiaal toe.
        if self.material_list:
            # maak eerst buy_db weer leeg
            database = collections.OrderedDict()
            for itm_enum in self.databases[self.subtype.name].values():
                if itm_enum.value.get('mtr') in self.material_list:
                    database[itm_enum.name] = itm_enum
        self.leftbox = BuyBox(self._set_x(self.leftbox_pos_x), self._set_y(self.leftbox_pos_y),
                              int(width), int(height), database, self.sum_merchant)

    def _init_sellbox(self):
        width = self.screen.get_width() * self.rightbox_width
        height = self.screen.get_height() * self.rightbox_height
        # een speciale sellbox voor pouchitems, geeft de data.pouch en de shoptypedb mee, ipv data.inv en party.
        if self.subtype == EquipmentType.itm:
            self.rightbox = SellBox(self._set_x(self.rightbox_pos_x), self._set_y(self.rightbox_pos_y),
                                    int(width), int(height),
                                    self.subtype, self.databases[self.subtype.name], self.engine.data.pouch,
                                    self.sum_merchant)
        else:
            self.rightbox = SellBox(self._set_x(self.rightbox_pos_x), self._set_y(self.rightbox_pos_y),
                                    int(width), int(height),
                                    self.subtype, self.engine.data.party, self.engine.data.inventory,
                                    self.sum_merchant)

    def on_enter(self):
        """
        Wanneer deze state op de stack komt, voer dit uit.
        Handel af als er een sell of buy confirmbox is geweest.
        """
        if self.sell_click or self.buy_click:
            if self.buy_click:
                choice = self.confirm_box.cur_item
                yes = self.confirm_box.TOPINDEX
                if choice == yes:
                    if self.engine.data.pouch.remove(self.gold_object, self.value):  # deze if is eigenlijk overbodig
                        # maar als het een pouchitem is moet het in de pouch
                        if self.selected_item.TYP == EquipmentType.itm:
                            self.engine.data.pouch.add(self.selected_item)
                        else:
                            self.engine.data.inventory.add_i(self.selected_item)  # van origineel zit hij erin. maar hij
                        self.engine.audio.play_sound(SFX.coins)                   # filtert nu al bij het klikken.
                        self._init_sellbox()
                else:
                    self.engine.audio.play_sound(SFX.menu_select)

            elif self.sell_click:
                selected_quantity = self.confirm_box.cur_item
                # dit gaat helemaal uit van dat de tekst van de shop maar 1 regel heeft en dan 1 regel niets.
                quantity = None
                if selected_quantity:   # omdat selected_quantity None kan zijn vanwege ESC toets.
                    quantity = self.sel_quantity[selected_quantity]

                if quantity:
                    # als het een pouchitem is moet het in de pouch
                    if self.selected_item.TYP == EquipmentType.itm:
                        self.engine.data.pouch.remove(self.selected_item, quantity)
                    else:
                        self.engine.data.inventory.remove_i(self.selected_item, quantity)
                    self.engine.data.pouch.add(self.gold_object, self.value * quantity)
                    self.engine.audio.play_sound(SFX.coins)
                    self._init_sellbox()
                else:
                    self.engine.audio.play_sound(SFX.menu_select)

            self._reset_vars()

    def multi_input(self, key_input, mouse_pos, dt):
        """
        :param key_input: pygame.key.get_pressed()
        :param mouse_pos: pygame.mouse.get_pos()
        :param dt: self.clock.tick(FPS)/1000.0
        """
        if self.engine.debug_mode:
            # todo, weghalen uiteindelijk. cheat voor geld erbij ctrl+
            if key_input[pygame.K_LCTRL] or key_input[pygame.K_RCTRL]:
                if key_input[pygame.K_KP_PLUS]:
                    self.engine.data.pouch.add(self.gold_object, 1, False)
                elif key_input[pygame.K_KP_MINUS]:
                    self.engine.data.pouch.remove(self.gold_object, 1, False)

    def update(self, dt, gamestate, audio):
        """
        Update de selector border color.
        Update de gold quantity.
        :param dt: self.clock.tick(FPS)/1000.0
        :param gamestate:
        :param audio:
        """
        for selector in self.selectors:
            selector.update(self.subtype)
        self.gold_amount = self.engine.data.pouch.get_quantity(self.gold_object)
        self.main_title = self.subtype.value
        self.source_title1 = SOURCETITLE1.format(str(self.gold_amount))

    def _handle_leftbox_click(self, event):
        self.buy_click, self.selected_item, self.value = self.leftbox.mouse_click(event)
        if self.buy_click and self.value <= self.gold_amount:
            text = ["You may buy 1 {} for {} gold.".format(self.selected_item.NAM, self.value),
                    "",
                    "Yes please.",
                    "No thanks."]
            self.confirm_box = ConfirmBox(text, sound=SFX.message)
            self.engine.gamestate.push(self.confirm_box)
            return True
        elif self.buy_click and self.value > self.gold_amount:
            text = ["You need {} more gold to".format(self.value - self.gold_amount),
                    "buy that {}.".format(self.selected_item.NAM)]
            push_object = MessageBox(text, sound=SFX.menu_cancel)
            self.engine.gamestate.push(push_object)
            self.buy_click = False
            self.selected_item = None
            self.value = 0
            return True
        return False

    def _handle_rightbox_click(self, event):
        self.sell_click, self.selected_item, self.tot_quantity, self.value = self.rightbox.mouse_click(event)
        # als een item maar 0 gc oplevert.
        if self.sell_click and self.value == 0:
            text = ["I do not want that item."]
            push_object = MessageBox(text, sound=SFX.menu_cancel)
            self.engine.gamestate.push(push_object)
            self.sell_click = False
            return True
        elif self.sell_click and self.selected_item:
            text = self._fill_confirm_box_with_sell_text()
            self.confirm_box = ConfirmBox(text, sound=SFX.message)
            self.engine.gamestate.push(self.confirm_box)
            return True
        elif self.sell_click and not self.selected_item:
            text = ["You must unequip that to sell it."]
            push_object = MessageBox(text, sound=SFX.menu_cancel)
            self.engine.gamestate.push(push_object)
            self.sell_click = False
            return True
        return False

    def _fill_confirm_box_with_sell_text(self):
        text = ["I'll give you " + str(self.value) + " gold for 1 " + self.selected_item.NAM + ".",
                "",
                "Oops, don't sell any."]

        # dit begin moet omdat er ook eerst tekst is voor 1 regel en 1 regel met niets.
        self.sel_quantity = ["",
                             "",
                             0]

        if self.tot_quantity > 0:
            if self.tot_quantity == 1:
                text.append("Sell 1 for " + str(int(self.value * 1)) + " gold.")
                self.sel_quantity.append(1)
            else:
                text.append("Sell 1 of them for " + str(int(self.value * 1)) + " gold.")
                self.sel_quantity.append(1)
            if self.tot_quantity > 1:
                text.append("Sell 2 of them for " + str(int(self.value * 2)) + " gold.")
                self.sel_quantity.append(2)
                if self.tot_quantity == 3:
                    text.append("Sell 3 of them for " + str(int(self.value * 3)) + " gold.")
                    self.sel_quantity.append(3)
                elif self.tot_quantity == 4:
                    text.append("Sell 3 of them for " + str(int(self.value * 3)) + " gold.")
                    text.append("Sell 4 of them for " + str(int(self.value * 4)) + " gold.")
                    self.sel_quantity.append(3)
                    self.sel_quantity.append(4)
                elif self.tot_quantity == 5:
                    text.append("Sell 3 of them for " + str(int(self.value * 3)) + " gold.")
                    text.append("Sell 4 of them for " + str(int(self.value * 4)) + " gold.")
                    text.append("Sell 5 of them for " + str(int(self.value * 5)) + " gold.")
                    self.sel_quantity.append(3)
                    self.sel_quantity.append(4)
                    self.sel_quantity.append(5)
                elif self.tot_quantity > 5:
                    text.append("Sell " + str(int(self.tot_quantity / 2)) +
                                " of them for " + str(int(self.value * (self.tot_quantity / 2))) + " gold.")
                    self.sel_quantity.append(int(self.tot_quantity / 2))
                    text.append("Sell " + str(self.tot_quantity - 1) +
                                " of them for " + str(int(self.value * (self.tot_quantity - 1))) + " gold.")
                    self.sel_quantity.append(self.tot_quantity - 1)
                    text.append("Sell " + str(self.tot_quantity) +
                                " of them for " + str(int(self.value * self.tot_quantity)) + " gold.")
                    self.sel_quantity.append(self.tot_quantity)
        return text
