
"""
class: Button
class: ColorBox
class: Grid
class: TreasureChest
"""

import pygame

FILLCOLOR = pygame.Color("gray60")  # gekke kleur vanwege sparkly color bug. hiermee opgelost.

BUTTONFONT = 'impact'
BUTTONFONTCOLOR = pygame.Color("white")
BUTTONFONTSIZE = 14
BUTTONBGCOLOR = pygame.Color("black")
BUTTONPRESSCOLOR = pygame.Color("gray12")

CHESTSPRITE = 'resources/sprites/objects/chest.png'
CHESTBLOCKERWIDTH = 32
CHESTBLOCKERHEIGHT = 16
SPARKLYSPRITE = 'resources/sprites/objects/sparkly.png'
SPARKLYSPEED = .2
TRANSP = 'resources/sprites/transp.png'


class Button(pygame.sprite.Sprite):
    """
    De gegevens van de knoppen in beeld.
    """
    def __init__(self, width, height, position, label, key):
        super().__init__()

        self.width = width
        self.height = height
        self.bgcolor = BUTTONBGCOLOR
        self.visible = True

        self.image = pygame.Surface((self.width, self.height))
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = position

        self.font = pygame.font.SysFont(BUTTONFONT, BUTTONFONTSIZE)
        self.label = self.font.render(label, True, BUTTONFONTCOLOR).convert_alpha()
        self.labelrect = self.label.get_rect()
        self.labelrect.center = self.rect.width / 2, self.rect.height / 2

        self.key = key

    def single_click(self, event):
        """
        Ontvang mouse event. Kijk of het met de button collide.
        :param event: pygame.MOUSEBUTTONDOWN uit engine.py
        :return: de knop die aan de button verbonden zit
        """
        if self.rect.collidepoint(event.pos):
            return self.key

    def multi_click(self, mouse_pos, key_input):
        """
        Als er geklikt is met de muis en op de knop.
        Maak dan van de key_input-tuple een list en zet de key van deze button in de list op 1.
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

    def update(self, key_input):
        """
        Update de kleur van de knop.
        :param key_input: self.key_input uit engine
        """
        if key_input[self.key]:
            self.bgcolor = BUTTONPRESSCOLOR
        else:
            self.bgcolor = BUTTONBGCOLOR

    def render(self, surface):
        """
        Teken de zichtbare knoppen op de gegeven surface.
        :param surface: self.screen uit engine
        """
        if self.visible:
            self.image.fill(self.bgcolor)
            pygame.draw.rect(self.image, BUTTONFONTCOLOR, (0, 0, self.width, self.height), 1)
            self.image.blit(self.label, self.labelrect)
            surface.blit(self.image, self.rect.topleft)


class ColorBox(pygame.sprite.Sprite):
    """
    De gekleurde randen wanneer F11 is ingedrukt.
    """
    def __init__(self, rect, color, layer):
        super().__init__()

        self._layer = layer
        self.image = pygame.Surface((rect.width, rect.height))
        self.image.fill(FILLCOLOR)
        self.image.set_colorkey(FILLCOLOR)
        pygame.draw.rect(self.image, color, (0, 0, rect.width, rect.height), 1)
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = rect.topleft


class Grid(pygame.sprite.Sprite):
    """
    Een grid over de window wanneer F10 is ingedrukt.
    """
    def __init__(self, map_width, map_height, color, grid_size, layer):
        super().__init__()

        self._layer = layer
        self.image = pygame.Surface((map_width, map_height))
        self.image.fill(FILLCOLOR)
        self.image.set_colorkey(FILLCOLOR)
        for i in range(0, map_width, grid_size):
            pygame.draw.line(self.image, color, (0, i), (map_width, i))
        for i in range(0, map_height, grid_size):
            pygame.draw.line(self.image, color, (i, 0), (i, map_height))
        self.image = self.image.convert()
        self.rect = self.image.get_rect()


def get_image(x, y, width, height, spritesheet):
    """
    Extracts image from spritesheet.
    :param x:
    :param y:
    :param width:
    :param height:
    :param spritesheet:
    """
    image = pygame.Surface((width, height))
    image.fill(FILLCOLOR)
    image.blit(spritesheet, (0, 0), (x, y, width, height))
    image.set_colorkey(FILLCOLOR)
    return image


class TreasureChest(pygame.sprite.Sprite):
    """
    De TreasureChest Sprite.
    """
    def __init__(self, chest_id, rect, objectlayer):
        super().__init__()

        self.chest_id = chest_id
        self.rect = rect
        self._layer = objectlayer
        self.image = None

        spritesheet = pygame.image.load(CHESTSPRITE).convert_alpha()

        self.image_list = (get_image(0,  0, 32, 32, spritesheet),  # closed
                           get_image(32, 0, 32, 32, spritesheet))  # opened

    def update(self, opened):
        """
        Geef de weergave van de chest.
        :param opened: integer 0 of 1, uit de TreasureChestDatabase.
        """
        self.image = self.image_list[opened]

    def get_blocker(self):
        """
        :return: Een rect met zijn eigen locatie en opgegeven grootte.
        """
        return pygame.Rect(self.rect.x, self.rect.y, CHESTBLOCKERWIDTH, CHESTBLOCKERHEIGHT)


class Sparkly(pygame.sprite.Sprite):
    """
    De animerende Sparkly Sprite.
    """
    def __init__(self, sparkly_id, rect, objectlayer):
        super().__init__()

        self.sparkly_id = sparkly_id
        self.rect = rect
        self._layer = objectlayer

        spritesheet = pygame.image.load(SPARKLYSPRITE).convert_alpha()
        self.speed = 0
        self.index = 0
        self.image_list = (get_image(0,  0, 32, 32, pygame.image.load(TRANSP).convert_alpha()),
                           get_image(0,  0, 32, 32, spritesheet),
                           get_image(32, 0, 32, 32, spritesheet),
                           get_image(64, 0, 32, 32, spritesheet),
                           get_image(32, 0, 32, 32, spritesheet))

        self.image = self.image_list[self.index]

    def update(self, taken, dt):
        """
        Verandert elke zoveel milliseconde het sub plaatje.
        :param taken: integer 0 of 1, uit de SparklyDatabase
        :param dt: self.clock.tick(FPS)/1000.0
        """
        if taken == 1:
            self.image = self.image_list[0]
            return

        self.speed += dt
        if self.speed > SPARKLYSPEED:
            self.speed = 0
            self.index += 1
            if self.index >= len(self.image_list):
                self.index = 1
            self.image = self.image_list[self.index]
