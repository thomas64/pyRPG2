
"""
class: Display
"""

import collections
import importlib

import pygame

import audio as sfx
from components import Button
from components import ConfirmBox
from components import MessageBox
from components import Transition
from constants import WeaponType
from database import PouchItemDatabase
import keys
from pouchitems import PouchItem
import screens.shop.buybox
import screens.shop.infobox
import screens.shop.selector
import screens.shop.sellbox
from statemachine import GameState

BACKGROUNDCOLOR = pygame.Color("black")
BACKGROUNDSPRITE = 'resources/sprites/parchment.png'
COLORKEY = pygame.Color("white")

FACEPOSX = 1/16
FACEPOSY = 3/16

FONTCOLOR = pygame.Color("black")
FONT = 'colonna'
LARGEFONTSIZE = 100
NORMALFONTSIZE = 50
SMALLFONTSIZE = 20

SMALLLINEHEIGHT = 30
EXTRAFACESIZE = 20
LINESNEXTTOFACE = 3

BUYBOXWIDTH = 1/4
BUYBOXHEIGHT = 3/4
BUYBOXPOSX = 2/5
BUYBOXPOSY = 1/6

SELLBOXWIDTH = 1/4      # van het scherm
SELLBOXHEIGHT = 3/4
SELLBOXPOSX = 2/3       # x op 2/3 van het scherm
SELLBOXPOSY = 1/6

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

SELECTORPOSX = 1/16
SELECTORPOSY = 10/16
SELECTORWIDTH = 31

SHOPTITLEPOSX = 1/16

BTNWIDTH = 70
BTNHEIGHT = 40
CLOSELBL = "Close"
CLOSEX, CLOSEY = -100, 40    # negatieve x omdat de positie van rechts bepaald wordt.


class Display(object):
    """
    ...
    """
    def __init__(self, engine, shoptype_list, shopmaterial_list, face):
        self.engine = engine
        # is een list van bijv: [EquipmentType.arm, WeaponType.swd]
        self.shoptype_list = shoptype_list
        self.shoptype = self.shoptype_list[0]
        self.material_list = shopmaterial_list
        self.databases = {}

        self.screen = pygame.display.get_surface()
        self.name = GameState.Shop
        self.background = pygame.image.load(BACKGROUNDSPRITE).convert_alpha()
        self.background = pygame.transform.scale(self.background, self.screen.get_size())

        self.largefont = pygame.font.SysFont(FONT, LARGEFONTSIZE)
        self.normalfont = pygame.font.SysFont(FONT, NORMALFONTSIZE)
        self.smallfont = pygame.font.SysFont(FONT, SMALLFONTSIZE)
        self.buy_title = self.largefont.render(BUYTITLE, True, FONTCOLOR).convert_alpha()
        self.sell_title = self.largefont.render(SELLTITLE, True, FONTCOLOR).convert_alpha()
        self.gold_amount = None

        self.sum_merchant = self.engine.data.party.get_sum_value_of_skill("mer")

        self._init_selectors()
        self._init_face(face)
        self._init_boxes()

        self.close_button = Button(
            BTNWIDTH, BTNHEIGHT, (self.background.get_width() + CLOSEX, CLOSEY), CLOSELBL, keys.EXIT,
            COLORKEY, FONTCOLOR)

        self.info_label = ""

        self.buy_click = False
        self.sell_click = False
        self.selected_item = None
        self.tot_quantity = 0
        self.sel_quantity = []
        self.value = 0
        self.confirm_box = None

    def _init_selectors(self):
        self.selectors = pygame.sprite.Group()
        for index, shoptype in enumerate(self.shoptype_list):
            self.databases[shoptype.name] = collections.OrderedDict()
            if isinstance(shoptype, WeaponType):
                from database import WeaponDatabase
                # omdat alle wapens in wpn zitten moet de database opnieuw opgebouwd worden met alleen de juiste wapens
                for weapon_itm in WeaponDatabase:
                    if weapon_itm.value['skl'] == shoptype:
                        self.databases[shoptype.name][weapon_itm.name] = weapon_itm.value
            else:
                db_select = dict(acy='AccessoryDatabase', amu='AmuletDatabase', arm='ArmorDatabase', blt='BeltDatabase',
                                 bts='BootsDatabase', brc='BraceletDatabase', clk='CloakDatabase', glv='GlovesDatabase',
                                 hlm='HelmetDatabase', rng='RingDatabase', sld='ShieldDatabase')
                # importeer de juiste db's voor de shop
                lib = importlib.import_module("database." + shoptype.value.lower())
                # zet de enum_db vanuit die import in een dict.
                enum_db = getattr(lib, db_select[shoptype.name])  # enum_db is bijv HelmetDatabase
                for equipment_itm in enum_db:
                    if equipment_itm.value['typ'] == shoptype:
                        self.databases[shoptype.name][equipment_itm.name] = equipment_itm.value

            # voeg selector objecten toe
            self.selectors.add(screens.shop.selector.Selector(self._set_x(SELECTORPOSX) + index * SELECTORWIDTH,
                                                              self._set_y(SELECTORPOSY), shoptype))
        self.selectors.draw(self.background)

    def _init_face(self, face):
        face_image = pygame.image.load(face).convert_alpha()
        self.background.blit(face_image, (self._set_x(FACEPOSX), self._set_y(FACEPOSY)))

        line01 = "Good day sir, and welcome to my shop."
        line02 = "In the 'Buy' box you can find all what"
        line03 = "my shop has to offer.  And in the 'Sell'"
        line04 = "box your own inventory is shown."
        line05 = "Click once on a selected item to buy or to sell."
        line06 = "You can scroll through the lists with your mouse-"
        line07 = "wheel if the list is longer than what you can see."
        line08 = "Below here, you see one or multiple icons."
        line09 = "They represent different sections of my shop."
        line10 = "Click on it to enter one of those sections."
        lines = (line01, line02, line03, line04, line05, line06, line07, line08, line09, line10)
        for index, line in enumerate(lines):
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
        self.sellbox = screens.shop.sellbox.SellBox(self._set_x(SELLBOXPOSX), self._set_y(SELLBOXPOSY),
                                                    int(width), int(height),
                                                    self.shoptype,
                                                    self.engine.data.party, self.engine.data.inventory,
                                                    self.sum_merchant)

    def _init_buybox(self):
        width = self.screen.get_width() * BUYBOXWIDTH
        height = self.screen.get_height() * BUYBOXHEIGHT + EXTRAHEIGHT

        buy_database = self.databases[self.shoptype.name]
        # extra stukje voor als er een bepaalde materiaal lijst is, voeg alleen die met de juiste materiaal toe.
        if self.material_list:
            # maak eerst buy_db weer leeg
            buy_database = collections.OrderedDict()
            for itm_key, itm_value in self.databases[self.shoptype.name].items():
                if itm_value.get('mtr') in self.material_list:
                    buy_database[itm_key] = itm_value
        self.buybox = screens.shop.buybox.BuyBox(self._set_x(BUYBOXPOSX), self._set_y(BUYBOXPOSY),
                                                 int(width), int(height),
                                                 buy_database,
                                                 self.sum_merchant)

    def _init_infobox(self):
        width = self.screen.get_width() * INFOBOXWIDTH
        height = self.screen.get_height() * INFOBOXHEIGHT
        self.infobox = screens.shop.infobox.InfoBox(self._set_x(INFOBOXPOSX), self._set_y(INFOBOXPOSY),
                                                    int(width), int(height))

    def on_enter(self):
        """
        Wanneer deze state op de stack komt, voer dit uit.
        Handel af als er een sell of buy confirmbox is geweest.
        """
        if self.sell_click or self.buy_click:
            if self.buy_click:
                # hij gebruikt nothing=scr_capt hier niet
                choice, yes, nothing = self.confirm_box.on_exit()
                if choice == yes:
                    gold = PouchItem(**PouchItemDatabase.gold.value)
                    if self.engine.data.pouch.remove(gold, self.value):     # deze if is eigenlijk overbodig maar
                        self.engine.data.inventory.add_i(self.selected_item)  # van origineel zit hij erin. maar hij
                        self.engine.audio.play_sound(sfx.COINS)             # filtert nu al bij het klikken.
                        self._init_sellbox()
                else:
                    self.engine.audio.play_sound(sfx.MENUSELECT)

            elif self.sell_click:
                # hij gebruikt nothing hier niet
                selected_quantity, nothing, nothing = self.confirm_box.on_exit()
                # dit gaat helemaal uit van dat de tekst van de shop maar 1 regel heeft en dan 1 regel niets.
                quantity = None
                if selected_quantity:   # omdat selected_quantity None kan zijn vanwege ESC toets.
                    quantity = self.sel_quantity[selected_quantity]

                if quantity:
                    self.engine.data.inventory.remove_i(self.selected_item, quantity)
                    gold = PouchItem(**PouchItemDatabase.gold.value)
                    self.engine.data.pouch.add(gold, self.value * quantity)
                    self.engine.audio.play_sound(sfx.COINS)
                    self._init_sellbox()
                else:
                    self.engine.audio.play_sound(sfx.MENUSELECT)

            self.buy_click = False
            self.sell_click = False
            self.selected_item = None
            self.tot_quantity = 0
            self.sel_quantity = []
            self.value = 0
            self.confirm_box = None

    # noinspection PyMethodMayBeStatic
    def on_exit(self):
        """
        Wanneer deze state onder een andere state van de stack komt, voer dit uit.
        Op dit moment nog niets echts.
        """
        pass

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
                self.info_label = self.buybox.mouse_hover(event)

            if self.sellbox.rect.collidepoint(event.pos):
                self.info_label = self.sellbox.mouse_hover(event)

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == keys.LEFTCLICK:

                if self.close_button.single_click(event) == keys.EXIT:
                    self._close()

                for selector in self.selectors:
                    shoptype = selector.mouse_click(event)
                    if shoptype:
                        self.shoptype = shoptype
                        self._init_boxes()
                        break

                # return of anders worden sommigen variabelen weer overschreven.
                if self._handle_buy_box_click(event):
                    return
                if self._handle_sell_box_click(event):
                    return

            elif event.button in (keys.SCROLLUP, keys.SCROLLDOWN):
                if self.buybox.rect.collidepoint(event.pos):
                    self.buybox.mouse_scroll(event)
                if self.sellbox.rect.collidepoint(event.pos):
                    self.sellbox.mouse_scroll(event)

        elif event.type == pygame.KEYDOWN:
            if event.key == keys.EXIT:
                self._close()
            elif event.key == keys.PREV:
                self._previous()
            elif event.key == keys.NEXT:
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
                gold = PouchItem(**PouchItemDatabase.gold.value)
                self.engine.data.pouch.add(gold, 1, False)
            elif key_input[pygame.K_KP_MINUS]:
                gold = PouchItem(**PouchItemDatabase.gold.value)
                self.engine.data.pouch.remove(gold, 1, False)

    def update(self, dt):
        """
        Update de gold quantity.
        :param dt: self.clock.tick(FPS)/1000.0
        """
        self.gold_amount = self.engine.data.pouch['gold'].qty

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

        self.infobox.render(self.screen, self.info_label)
        self.buybox.render(self.screen)
        self.sellbox.render(self.screen)
        self.close_button.render(self.screen, FONTCOLOR, True)

    def _handle_buy_box_click(self, event):
        self.buy_click, self.selected_item, self.value = self.buybox.mouse_click(event)
        if self.buy_click and self.value <= self.gold_amount:
            self.engine.audio.play_sound(sfx.MENUSELECT)
            text = ["You may buy 1 {} for {} gold.".format(self.selected_item.NAM, self.value),
                    "",
                    "Yes please.",
                    "No thanks."]
            self.confirm_box = ConfirmBox(self.engine.gamestate, self.engine.audio, text)
            self.engine.gamestate.push(self.confirm_box)
            return True
        elif self.buy_click and self.value > self.gold_amount:
            self.engine.audio.play_sound(sfx.MENUERROR)
            text = ["You need {} more gold to".format(self.value - self.gold_amount),
                    "buy that {}.".format(self.selected_item.NAM)]
            push_object = MessageBox(self.engine.gamestate, text)
            self.engine.gamestate.push(push_object)
            self.buy_click = False
            self.selected_item = None
            self.value = 0
            return True
        return False

    def _handle_sell_box_click(self, event):
        self.sell_click, self.selected_item, self.tot_quantity, self.value = self.sellbox.mouse_click(event)
        if self.sell_click and self.selected_item:
            self.engine.audio.play_sound(sfx.MENUSELECT)
            text = self._fill_confirm_box_with_sell_text()
            self.confirm_box = ConfirmBox(self.engine.gamestate, self.engine.audio, text)
            self.engine.gamestate.push(self.confirm_box)
            return True
        elif self.sell_click and not self.selected_item:
            self.engine.audio.play_sound(sfx.MENUERROR)
            text = ["You can not sell it to me",
                    "if you won't unequip it first."]
            push_object = MessageBox(self.engine.gamestate, text)
            self.engine.gamestate.push(push_object)
            self.sell_click = False
            return True
        return False

    def _set_x(self, posx):
        return self.screen.get_width() * posx

    def _set_y(self, posy):
        return self.screen.get_height() * posy

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
        for index, shoptype in enumerate(self.shoptype_list):
            if shoptype == self.shoptype:
                i = index - 1
                if i < 0:
                    i = len(self.shoptype_list)-1
                self.shoptype = self.shoptype_list[i]
                self._init_boxes()
                break

    def _next(self):
        for index, shoptype in enumerate(self.shoptype_list):
            if shoptype == self.shoptype:
                i = index + 1
                if i >= len(self.shoptype_list):
                    i = 0
                self.shoptype = self.shoptype_list[i]
                self._init_boxes()
                break

    def _close(self):
        self.engine.gamestate.pop()
        self.engine.gamestate.push(Transition(self.engine.gamestate))
