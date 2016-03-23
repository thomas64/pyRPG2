
"""
class: Map
"""

import pygame
import pytmx
import pyscroll

import components.namedrect
import components.portal
import components.sprites

# de zes object layers in een tmx map
STARTPOS = "start_pos"
PORTALS = "portals"
HIGHBLOCKER = "high_blocker"
LOWBLOCKER = "low_blocker"
OBJECTS = "objects"
SOUNDS = "sounds"

OBJECTLAYER = 2
TREASURECHEST = "treasurechest"


class Map(object):
    """
    Bevat allemaal lijsten van rects.
    """
    def __init__(self, name, tmxpath, windowwidth, windowheight, layer):
        self.name = name
        self.tmxpath = tmxpath

        tmx_data = pytmx.load_pygame(self.tmxpath)
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
        self.objects = []
        self.sounds = []

        for obj in tmx_data.get_layer_by_name(STARTPOS):
            self.start_pos.append(obj)
        for obj in tmx_data.get_layer_by_name(PORTALS):
            self.portals.append(components.portal.Portal(self.name, self._pg_rect(obj), obj.name))
        for rect in tmx_data.get_layer_by_name(HIGHBLOCKER):
            self.high_blocker_rects.append(self._pg_rect(rect))
        for rect in tmx_data.get_layer_by_name(LOWBLOCKER):
            self.low_blocker_rects.append(self._pg_rect(rect))

        for obj in tmx_data.get_layer_by_name(OBJECTS):
            if obj.name == TREASURECHEST:
                content_dict = {}
                for prop_key, prop_value in obj.properties.items():
                    content_dict[prop_key] = prop_value
                chest_object = components.sprites.TreasureChest(obj.name, self._pg_rect(obj), OBJECTLAYER, content_dict)
                self.low_blocker_rects.append(chest_object.get_blocker())
                self.objects.append(chest_object)
                # todo, identificatie met id? om status te kunnen saven bijv.

        for nrect in tmx_data.get_layer_by_name(SOUNDS):
            self.sounds.append(components.namedrect.NamedRect(nrect.name, self._pg_rect(nrect)))

    @staticmethod
    def _pg_rect(rect):
        """
        Converteert een rect uit tmx_data naar een pygame rect.
        :param rect: tmx rect
        :return: pygame rect
        """
        return pygame.Rect(rect.x, rect.y, rect.width, rect.height)
