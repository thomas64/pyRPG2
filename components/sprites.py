
"""
class: Button
class: ColorBox
class: Grid
class: Sign
class: TreasureChest
class: Sparkly
class: Person
class: Inn
class: Walking
"""

import pygame

from database import Direction


FILLCOLOR = pygame.Color("gray60")  # gekke kleur vanwege sparkly color bug. hiermee opgelost.

BUTTONFONT = 'impact'
BUTTONFONTCOLOR = pygame.Color("white")
BUTTONFONTSIZE = 14
BUTTONBGCOLOR = pygame.Color("black")
BUTTONPRESSCOLOR = pygame.Color("gray12")

CHESTSPRITE = 'resources/sprites/objects/chest.png'
SPARKLYSPRITE = 'resources/sprites/objects/sparkly.png'
SIGN1SPRITE = 'resources/sprites/objects/sign1.png'
SIGN2SPRITE = 'resources/sprites/objects/sign2.png'

SPARKLYSPEED = .2
HALFBLOCKERWIDTH = 32
HALFBLOCKERHEIGHT = 16

TRANSP = 'resources/sprites/transp.png'


class Button(pygame.sprite.Sprite):
    """
    De gegevens van de knoppen in beeld.
    """
    def __init__(self, width, height, position, label, key, bgcolor=BUTTONBGCOLOR, fontcolor=BUTTONFONTCOLOR):
        super().__init__()

        self.width = width
        self.height = height
        self.bgcolor = bgcolor
        self.visible = True

        self.image = pygame.Surface((self.width, self.height))
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = position

        self.font = pygame.font.SysFont(BUTTONFONT, BUTTONFONTSIZE)
        self.label = self.font.render(label, True, fontcolor).convert_alpha()
        self.labelrect = self.label.get_rect()
        self.labelrect.center = self.rect.width / 2, self.rect.height / 2

        self.key = key

    def single_click(self, event):
        """
        Ontvang mouse event. Kijk of het met de button collide.
        :param event: pygame.MOUSEBUTTONDOWN uit engine.py
        :return: de knop die aan de button verbonden zit
        """
        if self.visible:
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

    def update(self, key_input, bgcolor=BUTTONBGCOLOR):
        """
        Update de kleur van de knop.
        :param key_input: self.key_input uit engine
        :param bgcolor: als hij moet afwijken van de standaard zwart, dan kan dat hier
        """
        if key_input[self.key]:
            self.bgcolor = BUTTONPRESSCOLOR
        else:
            self.bgcolor = bgcolor

    def render(self, surface, linecolor=BUTTONFONTCOLOR, colorkey=False):
        """
        Teken de zichtbare knoppen op de gegeven surface.
        :param surface: self.screen uit engine
        :param linecolor: als hij moet afwijken van de standaard wit, dan kan dat hier
        :param colorkey: als hij transparant moet afwijken ipv de standaard zwart, dan kan dat hier
        """
        if self.visible:
            self.image.fill(self.bgcolor)
            if colorkey:
                self.image.set_colorkey(self.bgcolor)
            pygame.draw.rect(self.image, linecolor, (0, 0, self.width, self.height), 1)
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


class Sign(pygame.sprite.Sprite):
    """
    De Sign Sprite
    """
    def __init__(self, sign_id, rect, objectlayer, sign_type):
        super().__init__()

        self.sign_id = sign_id
        self.rect = rect
        self._layer = objectlayer
        if int(sign_type) == 1:
            self.image = pygame.image.load(SIGN1SPRITE).convert_alpha()
        elif int(sign_type) == 2:
            self.image = pygame.image.load(SIGN2SPRITE).convert_alpha()

    def get_blocker(self):
        """
        :return: Een rect met zijn eigen locatie en opgegeven grootte.
        """
        return pygame.Rect(self.rect.x, self.rect.y, HALFBLOCKERWIDTH, HALFBLOCKERHEIGHT)


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
        return pygame.Rect(self.rect.x, self.rect.y, HALFBLOCKERWIDTH, HALFBLOCKERHEIGHT)


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


class Person(pygame.sprite.Sprite):
    """
    Baseclass voor een pc unit in de overworld.
    """
    def __init__(self, person_id, sprite, rect, objectlayer, direction):
        super().__init__()

        self.west_states = {0:  (32, 32, 32, 32), 1: (0, 32, 32, 32), 2: (32, 32, 32, 32), 3: (64, 32, 32, 32)}
        self.east_states = {0:  (32, 64, 32, 32), 1: (0, 64, 32, 32), 2: (32, 64, 32, 32), 3: (64, 64, 32, 32)}
        self.north_states = {0: (32, 96, 32, 32), 1: (0, 96, 32, 32), 2: (32, 96, 32, 32), 3: (64, 96, 32, 32)}
        self.south_states = {0: (32,  0, 32, 32), 1: (0,  0, 32, 32), 2: (32,  0, 32, 32), 3: (64,  0, 32, 32)}

        self.sprite_id = person_id
        self.rect = rect
        self._layer = objectlayer
        self.full_sprite = pygame.image.load(sprite).convert_alpha()
        if direction == Direction.North:
            self.full_sprite.set_clip(self.north_states[0])
        elif direction == Direction.West:
            self.full_sprite.set_clip(self.west_states[0])
        elif direction == Direction.East:
            self.full_sprite.set_clip(self.east_states[0])
        else:
            self.full_sprite.set_clip(self.south_states[0])
        self.image = self.full_sprite.subsurface(self.full_sprite.get_clip())

    def turn(self, player_rect):
        """
        De meegegeven sprite draait naar de speler toe.
        Met welke berekening hij meekrijgt kies een ander subsurface.
        """
        if self.rect.left < player_rect.left and \
                abs(self.rect.centery - player_rect.centery) < \
                abs(self.rect.centerx - player_rect.centerx):
            states = self.east_states[0]
        elif self.rect.left > player_rect.left and \
                abs(self.rect.centery - player_rect.centery) < \
                abs(self.rect.centerx - player_rect.centerx):
            states = self.west_states[0]
        elif self.rect.top < player_rect.top and \
                abs(self.rect.centery - player_rect.centery) > \
                abs(self.rect.centerx - player_rect.centerx):
            states = self.south_states[0]
        elif self.rect.top > player_rect.top and \
                abs(self.rect.centery - player_rect.centery) > \
                abs(self.rect.centerx - player_rect.centerx):
            states = self.north_states[0]
        else:
            states = self.south_states[0]

        self.full_sprite.set_clip(states)
        self.image = self.full_sprite.subsurface(self.full_sprite.get_clip())

    def get_blocker(self):
        """
        :return: Een rect met zijn eigen locatie en opgegeven grootte.
        """
        return pygame.Rect(self.rect.x, self.rect.y, HALFBLOCKERWIDTH, HALFBLOCKERHEIGHT)


class Inn(Person):
    """
    Innkeepster
    """
    def __init__(self, inn_id, sprite, rect, objectlayer, direction, dont_show_sprite):
        super().__init__(inn_id, sprite, rect, objectlayer, direction)

        # als er in dont_show_sprite iets staat, dan is het een transparante sprite.
        self.show_sprite = True
        if dont_show_sprite:
            self.show_sprite = False
            self.image = pygame.image.load(TRANSP).convert_alpha()


class Walking(Person):
    """
    Struinend Persoon
    """
    def __init__(self, person_id, sprite, rect, objectlayer, direction):
        super().__init__(person_id, sprite, rect, objectlayer, direction)

        self.true_position = list(self.rect.topleft)  # true_pos is een float, dat is nodig voor timebased movement
        self.old_position = list(self.rect.topleft)
        self.last_direction = direction
        self.move_direction = None

        self.current_time = 0.0
        self.move_time = 0.0

    def move(self, ct, dt):
        """
        Verzet de positie in de opgegeven richting.
        """
        self.current_time = ct

        if self.move_time < self.current_time - 1:

            from random import randrange
            rnd = randrange(1, 5)
            if rnd == 1:
                self.move_direction = Direction.North
            elif rnd == 2:
                self.move_direction = Direction.South
            elif rnd == 3:
                self.move_direction = Direction.West
            else:
                self.move_direction = Direction.East

            self.move_time = self.current_time
            return

        # self.move_direction = self.last_direction
        self.old_position = list(self.rect.topleft)

        if self.move_direction == Direction.North:
            self.full_sprite.set_clip(self.north_states[0])
        elif self.move_direction == Direction.West:
            self.full_sprite.set_clip(self.west_states[0])
        elif self.move_direction == Direction.East:
            self.full_sprite.set_clip(self.east_states[0])
        else:
            self.full_sprite.set_clip(self.south_states[0])
        self.image = self.full_sprite.subsurface(self.full_sprite.get_clip())

        if self.move_direction == Direction.North:
            self.true_position[1] -= 60 * dt    # todo, 60 naar een movespeed
        elif self.move_direction == Direction.South:
            self.true_position[1] += 60 * dt
        elif self.move_direction == Direction.West:
            self.true_position[0] -= 60 * dt
        elif self.move_direction == Direction.East:
            self.true_position[0] += 60 * dt

        self.rect.x = round(self.true_position[0])
        self.rect.y = round(self.true_position[1])
