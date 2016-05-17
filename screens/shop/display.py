
"""
class: Display
"""

import pygame

import database
import keys
import screens.shop.buybox
import screens.shop.sellbox
import statemachine

BACKGROUNDCOLOR = pygame.Color("black")
BACKGROUNDSPRITE = 'resources/sprites/parchment.png'

BUYBOXWIDTH = 1/4
BUYBOXHEIGHT = 2/3
BUYBOXPOSX = 1/3
BUYBOXPOSY = 1/6

SELLBOXWIDTH = 1/4      # van het scherm
SELLBOXHEIGHT = 2/3
SELLBOXPOSX = 2/3       # x op 2/3 van het scherm
SELLBOXPOSY = 1/6

EXTRAHEIGHT = 16        # zodat de laatste item er voor helft op komt


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

        self.party = list(engine.data.party.values())
        self.inventory = engine.data.inventory

        self._init_boxes()

    def _init_boxes(self):
        width = self.screen.get_width() * SELLBOXWIDTH + EXTRAHEIGHT
        height = self.screen.get_height() * SELLBOXHEIGHT + EXTRAHEIGHT
        x = self.screen.get_width() * SELLBOXPOSX
        y = self.screen.get_height() * SELLBOXPOSY
        self.sellbox = screens.shop.sellbox.SellBox(int(x), int(y), int(width), int(height),
                                                    database.EquipmentType.arm, self.party, self.inventory)
        width = self.screen.get_width() * BUYBOXWIDTH
        height = self.screen.get_height() * BUYBOXHEIGHT
        x = self.screen.get_width() * BUYBOXPOSX
        y = self.screen.get_height() * BUYBOXPOSY
        self.buybox = screens.shop.buybox.BuyBox(x, y, width, height)

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

            if self.sellbox.rect.collidepoint(event.pos):
                # in partyscreen display geeft deze functie waarden terug, moet nog aanpassen later
                self.sellbox.mouse_hover(event)
            else:
                self.sellbox.cur_item = None

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in (keys.SCROLLUP, keys.SCROLLDOWN):
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
        self.buybox.render(self.screen)
        self.sellbox.render(self.screen)
