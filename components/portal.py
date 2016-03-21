
"""
class: Portal
"""

import pygame
import pytmx

MAPSPATH = 'resources/maps/'
STARTPOS = "start_pos"


class Portal(object):
    """
    Een portal knoopt 2 maps aan elkaar.
    Hij krijgt een van en een naar naam mee. Hij laadt dan de naarmap en zoekt daarin naar de naam van de vanmap.
    Wanneer gevonden, dan wordt dat object de startpositie van de naarmap.
    """
    def __init__(self, from_name, from_rect, to_name):
        self.from_name = from_name
        self.rect = from_rect
        self.to_name = to_name
        self.to_rect = (0, 0, 0, 0)

        temp_tmx_data = pytmx.load_pygame(MAPSPATH+to_name+".tmx")
        for obj in temp_tmx_data.get_layer_by_name(STARTPOS):
            if obj.name == from_name:
                self.to_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
