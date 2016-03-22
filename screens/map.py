
"""
class: Map
"""

import pygame
import pytmx
import pyscroll

import components.portal

# de vier object layers in een tmx map
STARTPOS = "start_pos"
PORTALS = "portals"
HIGHBLOCKER = "high_blocker"
LOWBLOCKER = "low_blocker"


class Map(object):
    """
    Bevat allemaal lijsten van rects.
    """
    def __init__(self, name, tmxpath, windowwidth, windowheight, layer):
        self.name = name

        tmx_data = pytmx.load_pygame(tmxpath)
        map_data = pyscroll.TiledMapData(tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, (windowwidth, windowheight))
        self.view = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=layer)

        tilewidth = tmx_data.tilewidth
        tileheight = tmx_data.tileheight
        self.width = int(tmx_data.width * tilewidth)
        self.height = int(tmx_data.height * tileheight)

        self.start_pos = []
        self.portals = []
        self.high_blocker_rects = []
        self.low_blocker_rects = []

        try:
            for obj in tmx_data.get_layer_by_name(STARTPOS):
                self.start_pos.append(obj)
        except (AttributeError, ValueError):
            pass
        try:
            for obj in tmx_data.get_layer_by_name(PORTALS):
                self.portals.append(components.portal.Portal(self.name, self._pg_rect(obj), obj.name))
        except (AttributeError, ValueError):
            pass
        try:
            for rect in tmx_data.get_layer_by_name(HIGHBLOCKER):
                self.high_blocker_rects.append(self._pg_rect(rect))
        except (AttributeError, ValueError):
            pass
        try:
            for rect in tmx_data.get_layer_by_name(LOWBLOCKER):
                self.low_blocker_rects.append(self._pg_rect(rect))
        except (AttributeError, ValueError):
            pass

    @staticmethod
    def _pg_rect(rect):
        """
        Converteert een rect uit tmx_data naar een pygame rect.
        :param rect: tmx rect
        :return: pygame rect
        """
        return pygame.Rect(rect.x, rect.y, rect.width, rect.height)
