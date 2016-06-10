
"""
class: Map
"""

import pygame
import pytmx
import pyscroll

import components
import database.shop
import database.inn

MAPPATH = 'resources/maps/'

# de zes object layers in een tmx map
HIGHBLOCKER = "high_blocker"
LOWBLOCKER = "low_blocker"
SOUNDS = "sounds"
STARTPOS = "start_pos"
PORTALS = "portals"
SHOPS = "shops"
INNS = "inns"
SIGNS = "signs"
CHESTS = "chests"
SPARKLY = "sparkly"

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

        self.high_blocker_rects = []
        self.low_blocker_rects = []
        self.sounds = []
        self.start_pos = []
        self.portals = []
        self.shops = []
        self.inns = []
        self.signs = []
        self.chests = []
        self.sparkly = []

        for rect in tmx_data.get_layer_by_name(HIGHBLOCKER):
            self.high_blocker_rects.append(self._pg_rect(rect))
        for rect in tmx_data.get_layer_by_name(LOWBLOCKER):
            self.low_blocker_rects.append(self._pg_rect(rect))
        for nrect in tmx_data.get_layer_by_name(SOUNDS):
            self.sounds.append(components.NamedRect(nrect.name, self._pg_rect(nrect)))
        for obj in tmx_data.get_layer_by_name(STARTPOS):
            self.start_pos.append(obj)
        for obj in tmx_data.get_layer_by_name(PORTALS):
            self.portals.append(components.Portal(name, self._pg_rect(obj), obj.name, obj.type))

        try:
            for obj in tmx_data.get_layer_by_name(SHOPS):
                shop_object = components.Shop(obj.name, database.shop.ShopDatabase[obj.name].value['sprite'],
                                              self._pg_rect(obj), OBJECTLAYER)
                self.high_blocker_rects.append(shop_object.get_blocker())
                self.shops.append(shop_object)
        except ValueError:
            pass

        try:
            for obj in tmx_data.get_layer_by_name(INNS):
                inn_object = components.Inn(obj.name, database.inn.InnDatabase[obj.name].value['sprite'],
                                            self._pg_rect(obj), OBJECTLAYER, obj.type)
                # als er in obj.type iets staat, dan is het een lege sprite en dus geen blocker.
                if not obj.type:
                    self.high_blocker_rects.append(inn_object.get_blocker())
                self.inns.append(inn_object)
        except ValueError:
            pass

        try:
            for obj in tmx_data.get_layer_by_name(SIGNS):
                sign_object = components.Sign(obj.name, self._pg_rect(obj), OBJECTLAYER, obj.type)
                self.low_blocker_rects.append(sign_object.get_blocker())
                self.signs.append(sign_object)
        except ValueError:
            pass
        try:
            for obj in tmx_data.get_layer_by_name(CHESTS):
                chest_object = components.TreasureChest(obj.name, self._pg_rect(obj), OBJECTLAYER)
                self.low_blocker_rects.append(chest_object.get_blocker())
                self.chests.append(chest_object)
        except ValueError:
            pass
        try:
            for obj in tmx_data.get_layer_by_name(SPARKLY):
                sparkly_object = components.Sparkly(obj.name, self._pg_rect(obj), OBJECTLAYER)
                self.sparkly.append(sparkly_object)
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
