
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
        self.bgcolor = BUTTONBGCOLOR
        self.visible = True

        self.image = pygame.Surface((self.width, self.height))
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = position

        self.font = pygame.font.SysFont(BUTTONFONT, BUTTONFONTSIZE)
        self.label = self.font.render(label, True, BUTTONFONTCOLOR)
        self.labelrect = self.label.get_rect()
        self.labelrect.center = self.rect.width / 2, self.rect.height / 2

        self.key = key

    def draw(self, surface, key_input):
        """
        Teken de zichtbare knoppen op de gegeven surface.
        :param surface: self.screen uit engine
        :param key_input: self.key_input uit engine
        """
        if self.visible:
            if key_input[self.key]:
                self.bgcolor = BUTTONPRESSCOLOR
            else:
                self.bgcolor = BUTTONBGCOLOR
            self.image.fill(self.bgcolor)
            pygame.draw.rect(self.image, BUTTONFONTCOLOR, (0, 0, self.width, self.height), 1)
            self.image.blit(self.label, self.labelrect)
            surface.blit(self.image, self.rect.topleft)

    def click(self, mouse_pos, key_input):
        """
        Als er geklikt is met de muis en op de knop.
        Maak dan van de tuple een list en zet de key van deze button in de list op 1.
        Die ingedrukt knop wordt dan teruggestuurd als het waarde keyboard input.
        :param mouse_pos: pygame.mouse.get_pos()
        :param key_input: pygame.key.get_pressed()
        :return: aangepaste key_input waarde
        """
        if mouse_pos is not None:
            if self.rect.collidepoint(mouse_pos):
                key_input = list(key_input)
                key_input[self.key] = 1
        return key_input


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
