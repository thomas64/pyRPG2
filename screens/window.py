
"""
class: Window
"""

import pygame

import keys
import screens.character
import screens.map
import screens.sprites

BACKGROUNDCOLOR = pygame.Color("gray12")
GRIDCOLOR = pygame.Color("gray36")
HEROCOLOR = pygame.Color("blue")
TREECOLOR = pygame.Color("yellow")
WATERCOLOR = pygame.Color("purple")

ZOOMSPEED = .1
MAXZOOM = 3.1
DEFZOOM = 1.0
MINZOOM = .5

# todo, mooiere map maken met variatie in het gras
OVERWORLDPATH = 'resources/maps/start_forest.tmx'
PLAYERLAYER = 3
GRIDLAYER = 8
CBOXLAYER = 9
GRIDSIZE = 32


class Window(object):
    """
    De window met de kaart en hero's.
    """
    def __init__(self, width, height, engine):
        self.engine = engine
        self.surface = pygame.Surface((width, height))
        self.surface.fill(BACKGROUNDCOLOR)
        self.surface = self.surface.convert()

        self.map1 = screens.map.Map(OVERWORLDPATH, width, height, PLAYERLAYER)
        self.group = self.map1.view

        self.heroes = []
        party = list(self.engine.data.party.values())
        for hero in party:
            self.heroes.append(screens.character.Hero(hero.SPR, self.map1.start_pos.topleft, self.engine.audio))
        self.heroes.reverse()           # voeg de heroes in juiste volgorde toe
        self.group.add(self.heroes)     # maar als sprites moeten ze precies andersom staan
        self.heroes.reverse()           # want daar wil je heroes[0] bovenop weergegeven hebben

        self.grid_sprite = None
        self.cbox_sprites = []

    def single_input(self, event):
        """
        Handelt de muis en keyboard input af.
        :param event: pygame.event.get()
        """
        if event.type == pygame.KEYDOWN:

            if event.key == keys.ALIGN:
                self.heroes[0].align_to_grid(GRIDSIZE)

            elif event.key == keys.GRID:
                if self.grid_sprite is None:
                    self.grid_sprite = screens.sprites.GridSprite(self.map1.width, self.map1.height,
                                                                  GRIDCOLOR, GRIDSIZE, GRIDLAYER)
                    self.group.add(self.grid_sprite)
                else:
                    self.group.remove(self.grid_sprite)
                    self.grid_sprite = None

            elif event.key == keys.CBOX:
                if len(self.cbox_sprites) == 0:                             # als de lijst leeg is.
                    self.cbox_sprites.append(screens.sprites.ColorBoxSprite(self.heroes[0].rect, HEROCOLOR, CBOXLAYER))
                    for rect in self.map1.tree_rects:
                        self.cbox_sprites.append(screens.sprites.ColorBoxSprite(rect, TREECOLOR, CBOXLAYER))
                    for rect in self.map1.water_rects:
                        self.cbox_sprites.append(screens.sprites.ColorBoxSprite(rect, WATERCOLOR, CBOXLAYER))
                    self.group.add(self.cbox_sprites)
                else:
                    self.group.remove(self.cbox_sprites)
                    self.cbox_sprites = []

    def multi_input(self, key_input, mouse_pos, dt):
        """
        Plus en min voor zoomen.
        Handel daarde de input af voor snelheid en richting. Check daarna op collision.
        :param key_input: pygame.key.get_pressed()
        :param mouse_pos: pygame.mouse.get_pos()
        :param dt: self.clock.tick(FPS)/1000.0
        """
        if key_input[keys.ZOOMPLUS]:
            value = self.map1.map_layer.zoom + ZOOMSPEED
            if value < MAXZOOM:
                self.map1.map_layer.zoom = value
        elif key_input[keys.ZOOMMIN]:
            value = self.map1.map_layer.zoom - ZOOMSPEED
            if value > MINZOOM:
                self.map1.map_layer.zoom = value
        elif key_input[keys.ZOOMRESET]:
            self.map1.map_layer.zoom = DEFZOOM

        self.heroes[0].speed(key_input)
        self.heroes[0].direction(key_input, dt)
        # todo, moet dit niet naar de hero class?
        self.heroes[0].check_obstacle(self.map1.obstacle_rects, self.map1.low_obst_rects,
                                      None, self.map1.width, self.map1.height, dt)

    # noinspection PyMethodMayBeStatic
    def update(self, dt):
        """
        Update de waarden van de bovenste state.
        :param dt: self.clock.tick(FPS)/1000.0
        """
        pass

    def render(self):
        """
        Update locaties (indien F11) -> centreer op de hero -> teken de window inhoud.
        """
        if len(self.cbox_sprites) > 0:                                       # de eerste die aan cbox_sprites bij F11 is
            self.cbox_sprites[0].rect.topleft = self.heroes[0].rect.topleft  # toegevoegd is de hero.rect, vandaar [0]

        self.group.center(self.heroes[0].rect.center)
        self.group.draw(self.surface)


# self.position_hist = collections.deque(maxlen=(len(self.party)-1)*32)
# self.direction_hist = collections.deque(maxlen=(len(self.party)-1)*32)
#
# for _ in range(0, (len(self.party)-1)*32):
#     self.position_hist.append((self.heroes[0].rect.x, self.heroes[0].rect.y))
#     self.direction_hist.append(self.heroes[0].last_direction)


# pos, drn = self.heroes[0].update_history()
# if pos[0] == self.position_hist[-1][0] and \
#    pos[1] == self.position_hist[-1][1]:
#     return
# self.position_hist.append(pos)
# self.direction_hist.append(drn)
#
# for index, i in enumerate(range(len(self.party)-1, 0, -1)):
#     self.heroes[i].rect.x = self.position_hist[index*32][0]
#     self.heroes[i].rect.y = self.position_hist[index*32][1]
#     self.heroes[i].move_direction = self.direction_hist[index*32]
#     self.heroes[i].movespeed = self.heroes[0].movespeed
#     self.heroes[i].animate(dt)
