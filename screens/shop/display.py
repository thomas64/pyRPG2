
"""
class: Display
"""

import pygame

import audio as sfx
import database
import database.armor
import keys
import pouchitems
import screens.shop.buybox
import screens.shop.confirmbox
import screens.shop.infobox
import screens.shop.sellbox
import statemachine

BACKGROUNDCOLOR = pygame.Color("black")
BACKGROUNDSPRITE = 'resources/sprites/parchment.png'

FONTCOLOR = pygame.Color("black")
FONT = 'colonna'
LARGEFONTSIZE = 100
NORMALFONTSIZE = 50

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
TITLEPOSY = 25

INFOBOXWIDTH = 1/4
INFOBOXHEIGHT = 1/6
INFOBOXPOSX = 1/16
INFOBOXPOSY = 6/8

GOLDTITLEPOSY = -50    # -50 boven infobox


class Display(object):
    """
    ...
    """
    def __init__(self, engine):
        self.engine = engine
        self.screen = pygame.display.get_surface()
        self.name = statemachine.States.Shop
        self.background = pygame.image.load(BACKGROUNDSPRITE).convert_alpha()
        self.background = pygame.transform.scale(self.background, self.screen.get_size())

        self.largefont = pygame.font.SysFont(FONT, LARGEFONTSIZE)
        self.normalfont = pygame.font.SysFont(FONT, NORMALFONTSIZE)
        self.buy_title = self.largefont.render(BUYTITLE, True, FONTCOLOR).convert_alpha()
        self.sell_title = self.largefont.render(SELLTITLE, True, FONTCOLOR).convert_alpha()
        self.gold_amount = None
        self.gold_title = None

        self.sum_merchant = self.engine.data.party.get_sum_value_of_skill("mer")
        self._init_boxes()

        self.info_label = ""

        self.sell_click = False
        self.selected_item = None
        self.tot_quantity = 0
        self.sel_quantity = []
        self.value = 0
        self.confirm_box = None

    def _init_boxes(self):
        self._init_sellbox()
        self._init_buybox()
        self._init_infobox()

    def _init_sellbox(self):
        width = self.screen.get_width() * SELLBOXWIDTH
        height = self.screen.get_height() * SELLBOXHEIGHT + EXTRAHEIGHT
        x = self.screen.get_width() * SELLBOXPOSX
        y = self.screen.get_height() * SELLBOXPOSY
        self.sellbox = screens.shop.sellbox.SellBox(int(x), int(y), int(width), int(height),
                                                    database.EquipmentType.arm,
                                                    self.engine.data.party, self.engine.data.inventory,
                                                    self.sum_merchant)

    def _init_buybox(self):
        width = self.screen.get_width() * BUYBOXWIDTH
        height = self.screen.get_height() * BUYBOXHEIGHT + EXTRAHEIGHT
        x = self.screen.get_width() * BUYBOXPOSX
        y = self.screen.get_height() * BUYBOXPOSY
        self.buybox = screens.shop.buybox.BuyBox(int(x), int(y), int(width), int(height),
                                                 database.armor.a.items(),
                                                 self.sum_merchant)

    def _init_infobox(self):
        width = self.screen.get_width() * INFOBOXWIDTH
        height = self.screen.get_height() * INFOBOXHEIGHT
        x = self.screen.get_width() * INFOBOXPOSX
        y = self.screen.get_height() * INFOBOXPOSY
        self.infobox = screens.shop.infobox.InfoBox(int(x), int(y), int(width), int(height))

    def on_enter(self):
        """
        Wanneer deze state op de stack komt, voer dit uit.
        Op dit moment nog niets echts.
        """
        pass

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
                self.sell_click, self.selected_item, self.tot_quantity, self.value = self.sellbox.mouse_click(event)
                if self.sell_click:
                    text = ["I'll give you " + str(self.value) + " gold for 1 " + self.selected_item.NAM + ".",
                            "",
                            "Oops, don't sell any."]
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
                            if self.tot_quantity == 4:
                                text.append("Sell 3 of them for " + str(int(self.value * 3)) + " gold.")
                                text.append("Sell 4 of them for " + str(int(self.value * 4)) + " gold.")
                                self.sel_quantity.append(3)
                                self.sel_quantity.append(4)
                            if self.tot_quantity == 5:
                                text.append("Sell 3 of them for " + str(int(self.value * 3)) + " gold.")
                                text.append("Sell 4 of them for " + str(int(self.value * 4)) + " gold.")
                                text.append("Sell 5 of them for " + str(int(self.value * 5)) + " gold.")
                                self.sel_quantity.append(3)
                                self.sel_quantity.append(4)
                                self.sel_quantity.append(5)
                            if self.tot_quantity > 5:
                                text.append("Sell " + str(int(self.tot_quantity/2)) +
                                            " of them for " + str(int(self.value * (self.tot_quantity/2))) + " gold.")
                                self.sel_quantity.append(int(self.tot_quantity/2))
                                text.append("Sell " + str(self.tot_quantity-1) +
                                            " of them for " + str(int(self.value * (self.tot_quantity-1))) + " gold.")
                                self.sel_quantity.append(self.tot_quantity - 1)
                                text.append("Sell " + str(self.tot_quantity) +
                                            " of them for " + str(int(self.value * self.tot_quantity)) + " gold.")
                                self.sel_quantity.append(self.tot_quantity)

                    self.engine.audio.play_sound(sfx.MENUSELECT)
                    self.confirm_box = screens.shop.confirmbox.ConfirmBox(self.engine.gamestate, self.engine.audio,
                                                                          text)
                    self.engine.gamestate.push(self.confirm_box)

            elif event.button in (keys.SCROLLUP, keys.SCROLLDOWN):
                if self.buybox.rect.collidepoint(event.pos):
                    self.buybox.mouse_scroll(event)
                if self.sellbox.rect.collidepoint(event.pos):
                    self.sellbox.mouse_scroll(event)

        elif event.type == pygame.KEYDOWN:
            if event.key == keys.EXIT:
                self.engine.gamestate.pop()

    def multi_input(self, key_input, mouse_pos, dt):
        """
        :param key_input: pygame.key.get_pressed()
        :param mouse_pos: pygame.mouse.get_pos()
        :param dt: self.clock.tick(FPS)/1000.0
        """
        pass

    def update(self, dt):
        """
        Update de gold quantity.
        :param dt: self.clock.tick(FPS)/1000.0
        """
        self.gold_amount = self.engine.data.pouch['gold'].qty

        if self.sell_click:
            selected_quantity = self.confirm_box.on_exit()
            quantity = self.sel_quantity[selected_quantity]

            if quantity:
                self.engine.data.inventory.remove(self.selected_item, quantity)
                gold = pouchitems.factory_pouch_item('gold')
                self.engine.data.pouch.add(gold, self.value * quantity)
                self.engine.audio.play_sound(sfx.COINS)
                self._init_sellbox()
            else:
                self.engine.audio.play_sound(sfx.MENUSELECT)

            self.sell_click = False
            self.selected_item = None
            self.tot_quantity = 0
            self.sel_quantity = []
            self.value = 0
            self.confirm_box = None

    def render(self):
        """
        Teken alles op het scherm, de titels, de boxen.
        """
        self.screen.fill(BACKGROUNDCOLOR)
        self.screen.blit(self.background, (0, 0))
        # titels midden boven de boxen
        self.screen.blit(self.buy_title, ((self.screen.get_width() * BUYBOXPOSX) +
                                          (self.screen.get_width() * BUYBOXWIDTH / 2) -
                                          (self.buy_title.get_width() / 2), TITLEPOSY))
        self.screen.blit(self.sell_title, ((self.screen.get_width() * SELLBOXPOSX) +
                                           (self.screen.get_width() * SELLBOXWIDTH / 2) -
                                           (self.sell_title.get_width() / 2), TITLEPOSY))
        self.gold_title = self.normalfont.render(GOLDTITLE + str(self.gold_amount), True, FONTCOLOR).convert_alpha()
        self.screen.blit(self.gold_title, (self.screen.get_width() * INFOBOXPOSX,
                                           self.screen.get_height() * INFOBOXPOSY + GOLDTITLEPOSY))
        self.infobox.render(self.screen, self.info_label)
        self.buybox.render(self.screen)
        self.sellbox.render(self.screen)
