
"""
class: Window
"""

import pygame

import screens.character
import screens.map
import screens.sprites


ALIGNKEY = pygame.K_SPACE
GRIDKEY = pygame.K_F10
CBOXKEY = pygame.K_F11

BACKGROUNDCOLOR = pygame.Color("gray12")
GRIDCOLOR = pygame.Color("gray36")
HEROCOLOR = pygame.Color("blue")
TREECOLOR = pygame.Color("yellow")
WATERCOLOR = pygame.Color("purple")

ZOOMSPEED = .1
MAXZOOM = 3.1
DEFZOOM = 1.0
MINZOOM = .5
ZOOMPLUSKEY = pygame.K_KP_PLUS
ZOOMMINKEY = pygame.K_KP_MINUS
ZOOMRESETKEY = pygame.K_KP_DIVIDE

# todo, mooiere map maken met variatie in het gras
OVERWORLDPATH = 'resources/maps/start_forest.tmx'
PLAYERLAYER = 3
GRIDLAYER = 8
CBOXLAYER = 9
GRIDSIZE = 32

# todo, laden van pad van sprite moet nog anders
HEROPATH = 'resources/sprites/heroes/01s_Alagos.png'


class Window(object):
    """
    De window met de kaart en hero's.
    """
    def __init__(self, width, height, audio):
        self.surface = pygame.Surface((width, height))
        self.surface.fill(BACKGROUNDCOLOR)
        self.surface = self.surface.convert()

        self.map1 = screens.map.Map(OVERWORLDPATH, width, height, PLAYERLAYER)
        self.group = self.map1.view

        self.hero = screens.character.Hero(HEROPATH, self.map1.start_pos.topleft, audio)
        self.group.add(self.hero)

        self.grid_sprite = None
        self.cbox_sprites = []

    def handle_view(self):
        """
        Update locaties (indien F11) -> centreer op de hero -> teken de window inhoud.
        """
        if len(self.cbox_sprites) > 0:                                  # de eerste die aan cbox_sprites bij F11 is
            self.cbox_sprites[0].rect.topleft = self.hero.rect.topleft  # toegevoegd is de hero.rect, vandaar [0]

        self.group.center(self.hero.rect.center)
        self.group.draw(self.surface)

    def handle_multi_input(self, key_input, dt):
        """
        Plus en min voor zoomen.
        Handel daarde de input af voor snelheid en richting. Check daarna op collision.
        :param key_input: pygame.key.get_pressed()
        :param dt: self.clock.tick(FPS)/1000.0
        """
        if key_input[ZOOMPLUSKEY]:
            value = self.map1.map_layer.zoom + ZOOMSPEED
            if value < MAXZOOM:
                self.map1.map_layer.zoom = value
        elif key_input[ZOOMMINKEY]:
            value = self.map1.map_layer.zoom - ZOOMSPEED
            if value > MINZOOM:
                self.map1.map_layer.zoom = value
        elif key_input[ZOOMRESETKEY]:
            self.map1.map_layer.zoom = DEFZOOM

        self.hero.speed(key_input)
        self.hero.direction(key_input, dt)
        # todo, moet dit niet naar de hero class?
        self.hero.check_obstacle(self.map1.obstacle_rects, self.map1.low_obst_rects,
                                 None, self.map1.width, self.map1.height, dt)

    def handle_single_input(self, event):
        """
        Handelt keyevents af.
        :param event: pygame.KEYDOWN uit engine.py
        """
        if event.key == ALIGNKEY:
            self.hero.align_to_grid(GRIDSIZE)

        elif event.key == GRIDKEY:
            if self.grid_sprite is None:
                self.grid_sprite = screens.sprites.GridSprite(self.map1.width, self.map1.height,
                                                              GRIDCOLOR, GRIDSIZE, GRIDLAYER)
                self.group.add(self.grid_sprite)
            else:
                self.group.remove(self.grid_sprite)
                self.grid_sprite = None

        elif event.key == CBOXKEY:
            if len(self.cbox_sprites) == 0:                             # als de lijst leeg is.
                self.cbox_sprites.append(screens.sprites.ColorBoxSprite(self.hero.rect, HEROCOLOR, CBOXLAYER))
                for rect in self.map1.tree_rects:
                    self.cbox_sprites.append(screens.sprites.ColorBoxSprite(rect, TREECOLOR, CBOXLAYER))
                for rect in self.map1.water_rects:
                    self.cbox_sprites.append(screens.sprites.ColorBoxSprite(rect, WATERCOLOR, CBOXLAYER))
                self.group.add(self.cbox_sprites)
            else:
                self.group.remove(self.cbox_sprites)
                self.cbox_sprites = []
