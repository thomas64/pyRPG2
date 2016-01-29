
"""
class: Map
"""

import pygame
import pytmx
import pyscroll
import pyscroll.data


class Map(object):
    """
    Bevat allemaal lijsten van rects.
    """
    def __init__(self, tmxpath, windowwidth, windowheight, layer):

        tmx_data = pytmx.load_pygame(tmxpath)
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.BufferedRenderer(map_data, (windowwidth, windowheight), clamp_camera=True)
        self.view = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=layer)

        tilewidth = tmx_data.tilewidth
        tileheight = tmx_data.tileheight
        self.width = int(tmx_data.width * tilewidth)
        self.height = int(tmx_data.height * tileheight)

        self.tree_rects = []
        self.water_rects = []
        self.obstacle_rects = []
        self.low_obst_rects = []

        for rect in tmx_data.get_layer_by_name("trees"):
            self.add_rect_to_list(rect, self.tree_rects)
            self.add_rect_to_list(rect, self.obstacle_rects)

        # for rect in tmx_data.get_layer_by_name("water"):
        #     self.add_rect_to_list(rect, self.water_rects)
        #     self.add_rect_to_list(rect, self.low_obst_rects)

    @staticmethod
    def add_rect_to_list(rect, alist):
        """
        Voeg een rect toe aan een lijst.
        :param rect: de rect
        :param alist: een lijst
        """
        alist.append(pygame.Rect(rect.x, rect.y, rect.width, rect.height))

    @staticmethod
    def del_rect_from_list(rect, alist):
        """
        Haal een rect uit een lijst.
        :param rect: de rect
        :param alist: een lijst
        """
        alist.remove(pygame.Rect(rect.x, rect.y, rect.width, rect.height))
