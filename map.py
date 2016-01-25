"""
class: Map
"""

import pygame


class Map(object):
    """
    Bevat allemaal lijsten van rects.
    En de cbox sprites.
    """
    def __init__(self, tmx_data):

        self.width = int(tmx_data.width * tmx_data.tilewidth)
        self.height = int(tmx_data.height * tmx_data.tileheight)
        self.tilewidth = tmx_data.tilewidth
        self.tileheight = tmx_data.tileheight

        self.tree_rects = []
        self.water_rects = []
        self.hero_rects = []
        self.villain_rects = []
        self.obstacle_rects = []
        self.low_obst_rects = []
        self.start_pos_rect = None
        self.warphole_rect = None

        self.current_sprite = None
        self.cbox_sprites = []

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
