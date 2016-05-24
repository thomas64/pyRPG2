
"""
class: Display
"""

import pygame

import database
import database.armor
import keys
import screens.shop.buybox
import screens.shop.infobox
import screens.shop.sellbox
import statemachine

BACKGROUNDCOLOR = pygame.Color("black")
BACKGROUNDSPRITE = 'resources/sprites/parchment.png'

FONTCOLOR = pygame.Color("black")
FONT = 'colonna'
LARGEFONTSIZE = 100

BUYBOXWIDTH = 1/4
BUYBOXHEIGHT = 2/3
BUYBOXPOSX = 1/3
BUYBOXPOSY = 1/6

SELLBOXWIDTH = 1/4      # van het scherm
SELLBOXHEIGHT = 2/3
SELLBOXPOSX = 2/3       # x op 2/3 van het scherm
SELLBOXPOSY = 1/6

EXTRAHEIGHT = 16        # zodat de laatste item er voor helft op komt

BUYTITLE = "Buy"
SELLTITLE = "Sell"
TITLEPOSY = 25

INFOBOXX, INFOBOXY = 30, 600


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

        largefont = pygame.font.SysFont(FONT, LARGEFONTSIZE)
        self.buy_title = largefont.render(BUYTITLE, True, FONTCOLOR).convert_alpha()
        self.sell_title = largefont.render(SELLTITLE, True, FONTCOLOR).convert_alpha()

        self._init_boxes()

        self.info_label = ""

    def _init_boxes(self):
        sum_merchant = self.engine.data.party.get_sum_value_of_skill("mer")

        width = self.screen.get_width() * SELLBOXWIDTH
        height = self.screen.get_height() * SELLBOXHEIGHT + EXTRAHEIGHT
        x = self.screen.get_width() * SELLBOXPOSX
        y = self.screen.get_height() * SELLBOXPOSY
        self.sellbox = screens.shop.sellbox.SellBox(int(x), int(y), int(width), int(height),
                                                    database.EquipmentType.arm,
                                                    self.engine.data.party, self.engine.data.inventory, sum_merchant)
        width = self.screen.get_width() * BUYBOXWIDTH
        height = self.screen.get_height() * BUYBOXHEIGHT + EXTRAHEIGHT
        x = self.screen.get_width() * BUYBOXPOSX
        y = self.screen.get_height() * BUYBOXPOSY
        self.buybox = screens.shop.buybox.BuyBox(int(x), int(y), int(width), int(height),
                                                 database.armor.a.items(), sum_merchant)

        self.infobox = screens.shop.infobox.InfoBox((INFOBOXX, INFOBOXY))

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

            if self.buybox.rect.collidepoint(event.pos):
                self.info_label = self.buybox.mouse_hover(event)
            else:
                self.buybox.cur_item = None

            if self.sellbox.rect.collidepoint(event.pos):
                self.info_label = self.sellbox.mouse_hover(event)
            else:
                self.sellbox.cur_item = None

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in (keys.SCROLLUP, keys.SCROLLDOWN):
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
        :param dt: self.clock.tick(FPS)/1000.0
        """
        pass

    def render(self):
        """
        Teken
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
        self.infobox.render(self.screen, self.info_label)
        self.buybox.render(self.screen)
        self.sellbox.render(self.screen)
