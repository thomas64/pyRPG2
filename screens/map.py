
"""
class: Map
"""

import pygame
import pytmx
import pyscroll

STARTPOSOBJECT = "start_pos"
HIGHBLOCKERLAYER = "high_blocker"
LOWBLOCKERLAYER = "low_blocker"


class Map(object):
    """
    Bevat allemaal lijsten van rects.
    """
    def __init__(self, tmxpath, windowwidth, windowheight, layer):

        tmx_data = pytmx.load_pygame(tmxpath)
        map_data = pyscroll.TiledMapData(tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, (windowwidth, windowheight))
        self.view = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=layer)

        tilewidth = tmx_data.tilewidth
        tileheight = tmx_data.tileheight
        self.width = int(tmx_data.width * tilewidth)
        self.height = int(tmx_data.height * tileheight)

        self.high_blocker_rects = []
        self.low_blocker_rects = []

        try:
            rect = tmx_data.get_object_by_name(STARTPOSOBJECT)
            self.start_pos = self._pg_rect(rect)
        except (AttributeError, ValueError):
            pass

        try:
            for rect in tmx_data.get_layer_by_name(HIGHBLOCKERLAYER):
                self._add_rect_to_list(rect, self.high_blocker_rects)
        except (AttributeError, ValueError):
            pass

        try:
            for rect in tmx_data.get_layer_by_name(LOWBLOCKERLAYER):
                self._add_rect_to_list(rect, self.low_blocker_rects)
        except (AttributeError, ValueError):
            pass

    def _add_rect_to_list(self, rect, alist):
        """
        Voeg een rect toe aan een lijst.
        :param rect: de rect
        :param alist: een lijst
        """
        alist.append(self._pg_rect(rect))

    def _del_rect_from_list(self, rect, alist):
        """
        Haal een rect uit een lijst.
        :param rect: de rect
        :param alist: een lijst
        """
        alist.remove(self._pg_rect(rect))

    @staticmethod
    def _pg_rect(rect):
        """
        Converteert een rect uit tmx_data naar een pygame rect.
        :param rect: tmx rect
        :return: pygame rect
        """
        return pygame.Rect(rect.x, rect.y, rect.width, rect.height)
