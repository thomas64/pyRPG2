
"""
class: Map
"""

import pygame
import pytmx
import pyscroll

from .namedrect import NamedRect
from .person import Person
from .person import Walking
from .portal import Portal
from .sprites import Sign
from .sprites import Sparkly
from .sprites import TreasureChest

from constants import Direction
from constants import MapTitle

from database import InnDatabase
from database import HeroDatabase
from database import PeopleDatabase
from database import SchoolDatabase
from database import ShopDatabase


MAPPATH = 'resources/maps/'

# de zes object layers in een tmx map
OBJECTS = "objects"
HIGHBLOCKER = "high_blocker"
LOWBLOCKER = "low_blocker"
SOUNDS = "sounds"
STARTPOS = "start_pos"
PORTALS = "portals"

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

        self.title = MapTitle[name].value

        self.high_blocker_rects = []
        self.low_blocker_rects = []
        self.temp_blocker_rects = []
        self.sounds = []
        self.start_pos = []
        self.portals = []
        self.heroes = []
        self.shops = []
        self.schools = []
        self.inns = []
        self.people = []
        self.notes = []
        self.signs = []
        self.chests = []
        self.sparkly = []

        for rect in tmx_data.get_layer_by_name(HIGHBLOCKER):
            self.high_blocker_rects.append(self._pg_rect(rect))
        for rect in tmx_data.get_layer_by_name(LOWBLOCKER):
            self.low_blocker_rects.append(self._pg_rect(rect))
        for nrect in tmx_data.get_layer_by_name(SOUNDS):
            self.sounds.append(NamedRect(nrect.name, self._pg_rect(nrect)))
        for obj in tmx_data.get_layer_by_name(STARTPOS):
            self.start_pos.append(obj)
        for obj in tmx_data.get_layer_by_name(PORTALS):
            self.portals.append(Portal(name, self._pg_rect(obj), obj.name, obj.type))
        for obj in tmx_data.get_layer_by_name(OBJECTS):
            if obj.name == 'blocker':
                # in obj.type staat de bijbehorende quest key.
                self.temp_blocker_rects.append(NamedRect(obj.type, self._pg_rect(obj)))
            elif obj.name.startswith('shop'):
                shop_object = Person(obj.name, ShopDatabase[obj.name].value['sprite'],
                                     self._pg_rect(obj), OBJECTLAYER, self._has_dir(obj, 'direction'), obj.type)
                # als er in obj.type iets staat, dan is het een lege sprite en dus geen blocker.
                if not obj.type:
                    self.high_blocker_rects.append(shop_object.get_blocker())
                self.shops.append(shop_object)
            elif obj.name.startswith('school'):
                school_object = Person(obj.name, SchoolDatabase[obj.name].value['sprite'],
                                       self._pg_rect(obj), OBJECTLAYER, self._has_dir(obj, 'direction'), obj.type)
                if not obj.type:
                    self.high_blocker_rects.append(school_object.get_blocker())
                self.schools.append(school_object)
            elif obj.name.startswith('inn'):
                inn_object = Person(obj.name, InnDatabase[obj.name].value['sprite'],
                                    self._pg_rect(obj), OBJECTLAYER, self._has_dir(obj, 'direction'), obj.type)
                if not obj.type:
                    self.high_blocker_rects.append(inn_object.get_blocker())
                self.inns.append(inn_object)
            elif obj.name.startswith('person'):
                # als er in obj.type iets staat, dan is het een walking person
                if obj.type:
                    person_object = Walking(obj.name, PeopleDatabase[obj.name].value['sprite'],
                                            self._pg_rect(obj), OBJECTLAYER, self._has_dir(obj, 'direction'))
                    # geen blocker voor walking people, die worden actueel in window geladen bij check_blocker.
                else:
                    person_object = Person(obj.name, PeopleDatabase[obj.name].value['sprite'],
                                           self._pg_rect(obj), OBJECTLAYER, self._has_dir(obj, 'direction'), None)
                    self.high_blocker_rects.append(person_object.get_blocker())
                self.people.append(person_object)
            elif obj.name.startswith('note'):
                self.notes.append(NamedRect(obj.name, self._pg_rect(obj)))
            elif obj.name.startswith('sign'):
                sign_object = Sign(obj.name, self._pg_rect(obj), OBJECTLAYER, obj.type)
                self.high_blocker_rects.append(sign_object.get_blocker())
                self.signs.append(sign_object)
            elif obj.name.startswith('chest'):
                chest_object = TreasureChest(obj.name, self._pg_rect(obj), OBJECTLAYER)
                self.low_blocker_rects.append(chest_object.get_blocker())
                self.chests.append(chest_object)
            elif obj.name.startswith('sparkly'):
                sparkly_object = Sparkly(obj.name, self._pg_rect(obj), OBJECTLAYER)
                self.sparkly.append(sparkly_object)
            else:  # 'heroes'
                hero_object = Person(obj.name, HeroDatabase[obj.name].value['spr'],
                                     self._pg_rect(obj), OBJECTLAYER, self._has_dir(obj, 'direction'), None)
                # geen high_blocker zoals bij bijv shops, omdat hero's er soms niet op de map kunnen staat,
                # het laden van high_blockers gebeurt in window.
                self.heroes.append(hero_object)

    @staticmethod
    def _pg_rect(rect):
        """
        Converteert een rect uit tmx_data naar een pygame rect.
        :param rect: tmx rect
        :return: pygame rect
        """
        return pygame.Rect(rect.x, rect.y, rect.width, rect.height)

    @staticmethod
    def _has_dir(obj, attr):
        """
        Kijkt of de attribute direction bestaat en converteer die.
        :param obj: Het object
        :param attr: De attribute
        :return: de waarde of None
        """
        if hasattr(obj, attr):
            return Direction[obj.direction.title()]
        return None
