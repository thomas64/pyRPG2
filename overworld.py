
"""
class: OverWorld
"""

import pygame
import pytmx
import pyscroll
import pyscroll.data

import map
import character


WINDOWWIDTH = 800
WINDOWHEIGHT = 600
WINDOWPOS = 100, 100

BACKGROUNDCOLOR = pygame.Color("black")
WINDOWCOLOR = pygame.Color("gray12")

OVERWORLDPATH = 'resources/maps/start_forest.tmx'
PLAYERLAYER = 1


class OverWorld(object):
    """
    Overworld layout.
    """
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(BACKGROUNDCOLOR)
        self.background = self.background.convert()
        self.window = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
        self.window.fill(WINDOWCOLOR)
        self.window = self.window.convert()

        self._init_map()
        self._init_hero()

    def _init_map(self):
        """
        Laad de tmx data en maak daaruit een group variabele.
        Maak een map aan en vul bomen.
        """
        tmx_data = pytmx.load_pygame(OVERWORLDPATH)
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.BufferedRenderer(map_data, (WINDOWWIDTH, WINDOWHEIGHT), clamp_camera=True)
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=PLAYERLAYER)

        self.map1 = map.Map(tmx_data)

        for rect in tmx_data.get_layer_by_name("trees"):
            self.map1.add_rect_to_list(rect, self.map1.tree_rects)
            self.map1.add_rect_to_list(rect, self.map1.obstacle_rects)

    def _init_hero(self):
        """
        Maak de hero aan en voeg toe aan de group.
        """
        # todo, laden van pad van sprite moet nog anders
        self.hero = character.Hero('resources/sprites/heroes/01_Alagos.png', [640, 768])
        self.group.add(self.hero)

    def handle_view(self):
        """
        Teken de achtergrond -> centreer op de hero -> teken de window.
        """
        self.screen.blit(self.background, (0, 0))
        self.group.center(self.hero.rect.center)
        self.group.draw(self.window)
        self.screen.blit(self.window, WINDOWPOS)

    def handle_multi_input(self, key_input):
        """
        Handel de input af voor snelheid en richting. Check daarna op collision.
        :param key_input: pygame.key.get_pressed()
        """
        self.hero.speed(key_input)
        self.hero.direction(key_input)
        # todo, moet dit niet naar de hero class?
        self.hero.check_obstacle(self.map1.obstacle_rects, self.map1.low_obst_rects,
                                 None, self.map1.width, self.map1.height)
