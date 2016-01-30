
"""
class: ButtonSprite
class: ColorBoxSprite
class: GridSprite
"""

import pygame

FILLCOLOR = pygame.Color("black")

BUTTONWIDTH = 40
BUTTONHEIGHT = 40
BUTTONFONT = 'sans'
BUTTONFONTCOLOR = pygame.Color("white")
BUTTONFONTSIZE = 14
BUTTONBGCOLOR = pygame.Color("black")
BUTTONPRESSCOLOR = pygame.Color("gray12")


class ButtonSprite(pygame.sprite.Sprite):
    """
    De gegevens van de knoppen in beeld.
    """
    def __init__(self, position, label, key):
        pygame.sprite.Sprite.__init__(self)

        self.width = BUTTONWIDTH
        self.height = BUTTONHEIGHT
        self._bgcolor = BUTTONBGCOLOR
        self._visible = True

        self.image = pygame.Surface((self.width, self.height))
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = position

        self.font = pygame.font.SysFont(BUTTONFONT, BUTTONFONTSIZE)
        self.label = self.font.render(label, True, BUTTONFONTCOLOR)
        self.labelrect = self.label.get_rect()
        self.labelrect.center = self.rect.width / 2, self.rect.height / 2

        self.key = key

        self._update()

    def draw(self, surface, key_input):
        """
        Teken de zichtbare knoppen op de gegeven surface.
        :param surface: self.screen uit engine
        :param key_input: self.key_input uit engine
        """
        if self._visible:
            if key_input[self.key]:
                self.bgcolor = BUTTONPRESSCOLOR
            else:
                self.bgcolor = BUTTONBGCOLOR

            surface.blit(self.image, self.rect.topleft)

    def _update(self):
        self.image.fill(self.bgcolor)
        pygame.draw.rect(self.image, BUTTONFONTCOLOR, (0, 0, self.width, self.height), 1)
        self.image.blit(self.label, self.labelrect)

    @property
    def bgcolor(self):
        """
        :return: backgroundcolor
        """
        return self._bgcolor

    @bgcolor.setter
    def bgcolor(self, value):
        self._bgcolor = value
        self._update()

    @property
    def visible(self):
        """
        :return: of hij zichtbaar is
        """
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value
        self._update()


class ColorBoxSprite(pygame.sprite.Sprite):
    """
    De gekleurde randen wanneer F11 is ingedrukt.
    """
    def __init__(self, rect, color, layer):
        pygame.sprite.Sprite.__init__(self)

        self._layer = layer
        self.image = pygame.Surface((rect.width, rect.height))
        self.image.fill(FILLCOLOR)
        self.image.set_colorkey(FILLCOLOR)
        pygame.draw.rect(self.image, color, (0, 0, rect.width, rect.height), 1)
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = rect.topleft

    def update(self, mobile_rect):
        """
        Update de coordinaten van deze cbox naar de nieuwe positie van het spriteobject.
        :param mobile_rect: de rect van het spriteobject waar de cbox omheen staat
        """
        self.rect.topleft = mobile_rect.topleft


class GridSprite(pygame.sprite.Sprite):
    """
    Een grid over de window wanneer F10 is ingedrukt.
    """
    def __init__(self, map_width, map_height, color, tile_size, layer):
        pygame.sprite.Sprite.__init__(self)

        self._layer = layer
        self.image = pygame.Surface((map_width, map_height))
        self.image.fill(FILLCOLOR)
        self.image.set_colorkey(FILLCOLOR)
        for i in range(0, map_width, tile_size):
            pygame.draw.line(self.image, color, (0, i), (map_width, i))
        for i in range(0, map_height, tile_size):
            pygame.draw.line(self.image, color, (i, 0), (i, map_height))
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
