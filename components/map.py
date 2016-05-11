
"""
class: Map
"""

import pygame
import pytmx
import pyscroll

import components.namedrect
import components.portal
import components.sprites

MAPPATH = 'resources/maps/'

# de zes object layers in een tmx map
STARTPOS = "start_pos"
PORTALS = "portals"
HIGHBLOCKER = "high_blocker"
LOWBLOCKER = "low_blocker"
CHESTS = "chests"
SOUNDS = "sounds"

WINDOWWIDTH = 900
WINDOWHEIGHT = 718

OBJECTLAYER = 4
PLAYERLAYER = 5


class Map(object):
    """
    Bevat allemaal lijsten van rects.
    """
    def __init__(self, name):
        map_tmx = MAPPATH + name + '.tmx'

        tmx_data = pytmx.load_pygame(map_tmx)
        map_data = pyscroll.TiledMapData(tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, (WINDOWWIDTH, WINDOWHEIGHT))
        self.view = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=PLAYERLAYER)

        tilewidth = tmx_data.tilewidth
        tileheight = tmx_data.tileheight
        self.width = int(tmx_data.width * tilewidth)
        self.height = int(tmx_data.height * tileheight)
        self.window_width = WINDOWWIDTH
        self.window_height = WINDOWHEIGHT

        self.title = tmx_data.properties['title']

        self.start_pos = []
        self.portals = []
        self.high_blocker_rects = []
        self.low_blocker_rects = []
        self.chests = []
        self.sounds = []

        for obj in tmx_data.get_layer_by_name(STARTPOS):
            self.start_pos.append(obj)
        for obj in tmx_data.get_layer_by_name(PORTALS):
            self.portals.append(components.portal.Portal(name, self._pg_rect(obj), obj.name, obj.type))
        for rect in tmx_data.get_layer_by_name(HIGHBLOCKER):
            self.high_blocker_rects.append(self._pg_rect(rect))
        for rect in tmx_data.get_layer_by_name(LOWBLOCKER):
            self.low_blocker_rects.append(self._pg_rect(rect))
        for nrect in tmx_data.get_layer_by_name(SOUNDS):
            self.sounds.append(components.namedrect.NamedRect(nrect.name, self._pg_rect(nrect)))

        try:
            for obj in tmx_data.get_layer_by_name(CHESTS):
                chest_object = components.sprites.TreasureChest(obj.name, self._pg_rect(obj), OBJECTLAYER)
                self.low_blocker_rects.append(chest_object.get_blocker())
                self.chests.append(chest_object)
        except ValueError:
            pass

    @staticmethod
    def _pg_rect(rect):
        """
        Converteert een rect uit tmx_data naar een pygame rect.
        :param rect: tmx rect
        :return: pygame rect
        """
        return pygame.Rect(rect.x, rect.y, rect.width, rect.height)
