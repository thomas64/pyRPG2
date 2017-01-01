
"""
class: Display
"""

import collections
import importlib

import pygame

from components import Button
from components import ConfirmBox
from components import MessageBox
from components import Parchment
from components import TextBox

from constants import GameState
from constants import Keys
from constants import SFX
from constants import EquipmentType
from constants import WeaponType

from database import PouchItemDatabase
from database import ShopDatabase
import inventoryitems

from .buybox import BuyBox
from .selector import Selector
from .sellbox import SellBox


BACKGROUNDCOLOR = pygame.Color("black")
COLORKEY = pygame.Color("white")

FACEPOSX = 1/16
FACEPOSY = 3/16

FONTCOLOR = pygame.Color("black")

SMALLLINEHEIGHT = 30
EXTRAFACESIZE = 20
LINESNEXTTOFACE = 3

BUYBOXWIDTH = 3/16
BUYBOXHEIGHT = 73/100
BUYBOXPOSX = 2/5
BUYBOXPOSY = 6/32

SELLBOXWIDTH = 5/16     # van het scherm
SELLBOXHEIGHT = 73/100
SELLBOXPOSX = 15/24     # x op 15/24 van het scherm
SELLBOXPOSY = 6/32

EXTRAHEIGHT = 0         # zodat de laatste item er voor helft op komt

BUYTITLE = "Buy"
SELLTITLE = "Sell"
GOLDTITLE = "Gold: "
TITLEPOSY = 1/32

INFOBOXWIDTH = 1/4
INFOBOXHEIGHT = 1/6
INFOBOXPOSX = 1/16
INFOBOXPOSY = 6/8

GOLDTITLEPOSX = 1/16
GOLDTITLEPOSY = 11/16

SELECTORPOSX = 2/32
SELECTORPOSY = 20/32
SELECTORWIDTH = 36

SHOPTITLEPOSX = 1/16

BTNWIDTH = 70
BTNHEIGHT = 40
CLOSELBL = "Close"
CLOSEX, CLOSEY = -100, 40    # negatieve x omdat de positie van rechts bepaald wordt.


class Display(Parchment):
    """
    ...
    """
    def __init__(self, engine, shoptype_list, shopmaterial_list, face):
        super().__init__(engine)

        # is een list van bijv: [EquipmentType.arm, WeaponType.swd]
        self.shoptype_list = list(shoptype_list)  # het moet een kopie van de lijst zijn, niet de lijst zelf,
        # vanwege de _init_selectors(), waar iets uit de lijst vervangen wordt. door een kopie te maken kan dat.
        self.shoptype = self.shoptype_list[0]
        self.material_list = shopmaterial_list
        self.databases = {}

        self.name = GameState.Shop

        self.buy_title = self.largefont.render(BUYTITLE, True, FONTCOLOR).convert_alpha()
        self.sell_title = self.largefont.render(SELLTITLE, True, FONTCOLOR).convert_alpha()
        self.gold_amount = None

        self.sum_merchant = self.engine.data.party.get_sum_value_of_skill("mer")

        self._init_selectors()
        self._init_face(face)
        self._init_boxes()

        self.close_button = Button(
            BTNWIDTH, BTNHEIGHT, (self.background.get_width() + CLOSEX, CLOSEY), CLOSELBL, Keys.Exit.value,
            COLORKEY, FONTCOLOR)

        self.gold_object = inventoryitems.factory_pouch_item(PouchItemDatabase.gold)

        self.info_label = ""
        self._reset_vars()

    def _init_selectors(self):
        self.selectors = pygame.sprite.Group()
        for index, shoptype in enumerate(self.shoptype_list):

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
                self.shoptype_list[index] = shoptype[0]
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
            self.selectors.add(Selector(self._set_x(SELECTORPOSX) + index * SELECTORWIDTH,
                                        self._set_y(SELECTORPOSY), shoptype))
        self.selectors.draw(self.background)

    def _init_face(self, face):
        face_image = pygame.image.load(face).convert_alpha()
        self.background.blit(face_image, (self._set_x(FACEPOSX), self._set_y(FACEPOSY)))

        for index, line in enumerate(ShopDatabase.welcome_text()):
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
        self._init_sellbox()
        self._init_buybox()
        self._init_infobox()

    def _init_sellbox(self):
        width = self.screen.get_width() * SELLBOXWIDTH
        height = self.screen.get_height() * SELLBOXHEIGHT + EXTRAHEIGHT

        # een speciale sellbox voor pouchitems, geeft de data.pouch en de shoptypedb mee, ipv data.inv en party.
        if self.shoptype == EquipmentType.itm:
            self.sellbox = SellBox(self._set_x(SELLBOXPOSX), self._set_y(SELLBOXPOSY), int(width), int(height),
                                   self.shoptype, self.databases[self.shoptype.name], self.engine.data.pouch,
                                   self.sum_merchant)
        else:
            self.sellbox = SellBox(self._set_x(SELLBOXPOSX), self._set_y(SELLBOXPOSY), int(width), int(height),
                                   self.shoptype, self.engine.data.party, self.engine.data.inventory, self.sum_merchant)

    def _init_buybox(self):
        width = self.screen.get_width() * BUYBOXWIDTH
        height = self.screen.get_height() * BUYBOXHEIGHT + EXTRAHEIGHT

        buy_database = self.databases[self.shoptype.name]
        # extra stukje voor als er een bepaalde materiaal lijst is, voeg alleen die met de juiste materiaal toe.
        if self.material_list:
            # maak eerst buy_db weer leeg
            buy_database = collections.OrderedDict()
            for itm_enum in self.databases[self.shoptype.name].values():
                if itm_enum.value.get('mtr') in self.material_list:
                    buy_database[itm_enum.name] = itm_enum
        self.buybox = BuyBox(self._set_x(BUYBOXPOSX), self._set_y(BUYBOXPOSY), int(width), int(height),
                             buy_database, self.sum_merchant)

    def _init_infobox(self):
        width = self.screen.get_width() * INFOBOXWIDTH
        height = self.screen.get_height() * INFOBOXHEIGHT
        self.infobox = TextBox((self._set_x(INFOBOXPOSX), self._set_y(INFOBOXPOSY)), int(width), int(height))

    def _reset_vars(self):
        self.buy_click = False
        self.sell_click = False
        self.selected_item = None
        self.tot_quantity = 0
        self.sel_quantity = []
        self.value = 0
        self.confirm_box = None

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
                        self.engine.audio.play_sound(SFX.coins)             # filtert nu al bij het klikken.
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

    def single_input(self, event):
        """
        Handelt de muis en keyboard input af.
        :param event: pygame.event.get()
        """

        # todo, sellbox en buybox met toetsenbord
        # todo, equipment die hero's aanhebben kunnen sellen

        if event.type == pygame.MOUSEMOTION:

            self.info_label = ""
            self.buybox.cur_item = None
            self.sellbox.cur_item = None

            if self.buybox.rect.collidepoint(event.pos):
                selected_name, self.info_label = self.buybox.mouse_hover(event)
                self.sellbox.duplicate_selection(selected_name)
            if self.sellbox.rect.collidepoint(event.pos):
                selected_name, self.info_label = self.sellbox.mouse_hover(event)
                self.buybox.duplicate_selection(selected_name)

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == Keys.Leftclick.value:

                if self.close_button.single_click(event) == Keys.Exit.value:
                    self._close()

                for selector in self.selectors:
                    shoptype = selector.mouse_click(event)
                    if shoptype:
                        if shoptype != self.shoptype:
                            self.engine.audio.play_sound(SFX.menu_switch)
                            self.shoptype = shoptype
                            self._init_boxes()
                            break

                # return of anders worden sommigen variabelen weer overschreven.
                if self._handle_buy_box_click(event):
                    return
                if self._handle_sell_box_click(event):
                    return

            elif event.button in (Keys.Scrollup.value, Keys.Scrolldown.value):
                if self.buybox.rect.collidepoint(event.pos):
                    self.buybox.mouse_scroll(event)
                if self.sellbox.rect.collidepoint(event.pos):
                    self.sellbox.mouse_scroll(event)

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
        # cheat voor geld erbij ctrl+
        if key_input[pygame.K_LCTRL] or key_input[pygame.K_RCTRL]:
            if key_input[pygame.K_KP_PLUS]:
                self.engine.data.pouch.add(self.gold_object, 1, False)
            elif key_input[pygame.K_KP_MINUS]:
                self.engine.data.pouch.remove(self.gold_object, 1, False)

    def update(self, dt):
        """
        Update de selector border color.
        Update de gold quantity.
        :param dt: self.clock.tick(FPS)/1000.0
        """
        for selector in self.selectors:
            selector.update(self.shoptype)
        self.gold_amount = self.engine.data.pouch.get_quantity(self.gold_object)

    def render(self):
        """
        Teken alles op het scherm, de titels, de boxen.
        """
        self.screen.fill(BACKGROUNDCOLOR)
        self.screen.blit(self.background, (0, 0))
        # titels midden boven de boxen
        self.screen.blit(self.buy_title, ((self._set_x(BUYBOXPOSX)) +
                                          (self.screen.get_width() * BUYBOXWIDTH / 2) -
                                          (self.buy_title.get_width() / 2),
                                          self._set_y(TITLEPOSY)))
        self.screen.blit(self.sell_title, ((self._set_x(SELLBOXPOSX)) +
                                           (self.screen.get_width() * SELLBOXWIDTH / 2) -
                                           (self.sell_title.get_width() / 2),
                                           self._set_y(TITLEPOSY)))
        gold_title = self.normalfont.render(GOLDTITLE + str(self.gold_amount), True, FONTCOLOR).convert_alpha()
        self.screen.blit(gold_title, (self._set_x(GOLDTITLEPOSX), self._set_y(GOLDTITLEPOSY)))
        shoptype_title = self.largefont.render(self.shoptype.value, True, FONTCOLOR).convert_alpha()
        self.screen.blit(shoptype_title, (self._set_x(SHOPTITLEPOSX), self._set_y(TITLEPOSY)))

        self.selectors.draw(self.background)

        self.infobox.render(self.screen, self.info_label)
        self.buybox.render(self.screen)
        self.sellbox.render(self.screen)
        self.close_button.render(self.screen, FONTCOLOR)

    def _handle_buy_box_click(self, event):
        self.buy_click, self.selected_item, self.value = self.buybox.mouse_click(event)
        if self.buy_click and self.value <= self.gold_amount:
            text = ["You may buy 1 {} for {} gold.".format(self.selected_item.NAM, self.value),
                    "",
                    "Yes please.",
                    "No thanks."]
            self.confirm_box = ConfirmBox(self.engine.gamestate, self.engine.audio, text, sound=SFX.message)
            self.engine.gamestate.push(self.confirm_box)
            return True
        elif self.buy_click and self.value > self.gold_amount:
            text = ["You need {} more gold to".format(self.value - self.gold_amount),
                    "buy that {}.".format(self.selected_item.NAM)]
            push_object = MessageBox(self.engine.gamestate, self.engine.audio, text, sound=SFX.menu_cancel)
            self.engine.gamestate.push(push_object)
            self.buy_click = False
            self.selected_item = None
            self.value = 0
            return True
        return False

    def _handle_sell_box_click(self, event):
        self.sell_click, self.selected_item, self.tot_quantity, self.value = self.sellbox.mouse_click(event)
        # als een item maar 0 gc oplevert.
        if self.sell_click and self.value == 0:
            text = ["I do not want that item."]
            push_object = MessageBox(self.engine.gamestate, self.engine.audio, text, sound=SFX.menu_cancel)
            self.engine.gamestate.push(push_object)
            self.sell_click = False
            return True
        elif self.sell_click and self.selected_item:
            text = self._fill_confirm_box_with_sell_text()
            self.confirm_box = ConfirmBox(self.engine.gamestate, self.engine.audio, text, sound=SFX.message)
            self.engine.gamestate.push(self.confirm_box)
            return True
        elif self.sell_click and not self.selected_item:
            text = ["You must unequip that to sell it."]
            push_object = MessageBox(self.engine.gamestate, self.engine.audio, text, sound=SFX.menu_cancel)
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

    def _previous(self):
        self.engine.audio.play_sound(SFX.menu_switch)
        for index, shoptype in enumerate(self.shoptype_list):
            if shoptype == self.shoptype:
                i = index - 1
                if i < 0:
                    i = len(self.shoptype_list)-1
                self.shoptype = self.shoptype_list[i]
                self._init_boxes()
                break

    def _next(self):
        self.engine.audio.play_sound(SFX.menu_switch)
        for index, shoptype in enumerate(self.shoptype_list):
            if shoptype == self.shoptype:
                i = index + 1
                if i >= len(self.shoptype_list):
                    i = 0
                self.shoptype = self.shoptype_list[i]
                self._init_boxes()
                break
