
"""
class: Map
"""

import datetime

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

from console import Console

from constants import Direction
from constants import MapTitle

from database import InnDatabase
from database import HeroDatabase
from database import PeopleDatabase
from database import SchoolDatabase
from database import ShopDatabase
from database import TrainerDatabase


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
    def __init__(self, name, treasure_chests_database):
        map_tmx = MAPPATH + name + '.tmx'

        tmx_data = pytmx.load_pygame(map_tmx)
        map_data = pyscroll.TiledMapData(tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, (WINDOWWIDTH, WINDOWHEIGHT))
        self.map_layer.zoom = 2
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
        self.trainers = []
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
            self.start_pos.append(Portal(obj.name, self._pg_rect(obj), name, obj.type, self._has_dir(obj, 'direction')))
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
            elif obj.name.startswith('trainer'):
                trainer_object = Person(obj.name, TrainerDatabase[obj.name].value['sprite'],
                                        self._pg_rect(obj), OBJECTLAYER, self._has_dir(obj, 'direction'), obj.type)
                if not obj.type:
                    self.high_blocker_rects.append(trainer_object.get_blocker())
                self.trainers.append(trainer_object)
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
                else:
                    person_object = Person(obj.name, PeopleDatabase[obj.name].value['sprite'],
                                           self._pg_rect(obj), OBJECTLAYER, self._has_dir(obj, 'direction'), None)
                # als er een tijdspanne aan de personage zit
                if PeopleDatabase[obj.name].value.get('time1'):
                    time1 = PeopleDatabase[obj.name].value['time1']
                    time2 = PeopleDatabase[obj.name].value['time2']
                    timestamp = datetime.datetime.now()
                    # print(timestamp)
                    if time1 < timestamp < time2:
                        self.people.append(person_object)
                        # geen blocker voor walking people, die worden actueel in window geladen bij check_blocker.
                        if not obj.type:
                            self.high_blocker_rects.append(person_object.get_blocker())
                else:
                    self.people.append(person_object)
                    # geen blocker voor walking people, die worden actueel in window geladen bij check_blocker.
                    if not obj.type:
                        self.high_blocker_rects.append(person_object.get_blocker())

            elif obj.name.startswith('note'):
                self.notes.append(NamedRect(obj.name, self._pg_rect(obj)))
            elif obj.name.startswith('sign'):
                sign_object = Sign(obj.name, self._pg_rect(obj), OBJECTLAYER, obj.type)
                self.high_blocker_rects.append(sign_object.get_blocker())
                self.signs.append(sign_object)
            elif obj.name.startswith('chest'):
                if treasure_chests_database[obj.name].get('time1'):
                    time1 = treasure_chests_database[obj.name]['time1']
                    time2 = treasure_chests_database[obj.name]['time2']
                    timestamp = datetime.datetime.now()
                    if time1 < timestamp < time2:
                        chest_object = TreasureChest(obj.name, self._pg_rect(obj), OBJECTLAYER)
                        self.low_blocker_rects.append(chest_object.get_blocker())
                        self.chests.append(chest_object)
                else:
                    chest_object = TreasureChest(obj.name, self._pg_rect(obj), OBJECTLAYER)
                    self.low_blocker_rects.append(chest_object.get_blocker())
                    self.chests.append(chest_object)
            elif obj.name.startswith('sparkly'):
                # als er in obj.type iets staat, dan is het een lege sprite.
                sparkly_object = Sparkly(obj.name, self._pg_rect(obj), OBJECTLAYER, obj.type)
                self.sparkly.append(sparkly_object)
            elif obj.name == 'hero':
                hero_object = Person(obj.type, HeroDatabase[obj.type].value['spr'],
                                     self._pg_rect(obj), OBJECTLAYER, self._has_dir(obj, 'direction'), None)
                # geen high_blocker zoals bij bijv shops, omdat hero's er soms niet op de map kunnen staan,
                # het laden van high_blockers gebeurt in window.
                self.heroes.append(hero_object)
            else:
                Console.error_unknown_map_object()
                raise NameError

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

    def get_position(self, from_map_name, from_pos_nr):
        """
        :param from_map_name: de string naam van de kaart waarvan je vandaan komt
        :param from_pos_nr: als er een nr in de portal zat waar je vandaan kwam, dan is dit het nr.
        :return: een x en y punt.
        """
        for pos in self.start_pos:                      # kijk in de start_pos list van de map van alle start_possen,
            if pos.from_name == from_map_name:          # welke komt overeen met 'start_game' of de naam van de vorige
                if pos.to_nr:                           # map. als er ook een type is '1' of '9' is een to_nr waarde,
                    if pos.to_nr == from_pos_nr:        # kijk dan of die overeen komt met to_nr van de portal waaruit
                        return pos.rect.x, pos.rect.y   # je gezonden bent. neem dan die positie aan.
                    else:                               # komt het nr niet overeen, dan moet ie nog komen,
                        continue                        # zoek daarom door.
                else:                                   # als er geen .type is, dan is er maar 1 warp en moet je die
                    return pos.rect.x, pos.rect.y       # gewoon hebben. zet dan de x,y waarde op dié start_pos,
        #                                               # maak van de string dus weer een point.
        return from_map_name                            # als het gelukt is, dat betekent dat from_map_name geen naam
        #                                               # is maar al een point was, return dan gewoon deze point.

    def get_direction(self, start_pos, last_direction):
        """
        Loop alle start_possen door.
        Als er een start_pos is met een gedefinieerde direction, kijk dan of de huidige plek waar hij nu staat
        overeen komt met de locatie van deze start_pos.
        Als dat zo is geef dan die direction terug.
        Anders de oude onaangepaste originele direction.
        :param start_pos: de nieuwe x en y positie
        :param last_direction: welke richting de character heen keek op het laatst op de vorige kaart.
        :return: een Enum richtings positie.
        """
        for pos in self.start_pos:                                       # in een .tmx map kun je bij start_pos
            if pos.direction and (pos.rect.x, pos.rect.y) == start_pos:  # een 'direction' property meegeven.
                return pos.direction                                     # als dat een Direction Enum is dan
        return last_direction                          # start de unit in de nieuw geladen map in die kijkrichting.
