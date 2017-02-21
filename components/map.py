
"""
class: Map
"""

import datetime

import pygame
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
from database import TreasureChestDatabase


# de zeven object layers in een tmx map
EVENTS = "events"
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


class Tile(pygame.Rect):
    """..."""
    total_tiles = 0

    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.solid = False
        self.number = Tile.total_tiles
        Tile.total_tiles += 1


class Map(object):
    """
    Bevat allemaal lijsten van rects.
    """
    def __init__(self, data):
        tmx_data = MapTitle[data.map_name].value[1]
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

        self.title = MapTitle[data.map_name].value[0]

        self.high_blocker_rects = []
        self.low_blocker_rects = []
        self.quest_blocker_rects = []
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
        self.locations = []
        self.text_events = []
        self.move_events = []
        self.chests = []
        self.sparkly = []

        for rect in tmx_data.get_layer_by_name(HIGHBLOCKER):
            self.high_blocker_rects.append(self._pg_rect(rect))
        for rect in tmx_data.get_layer_by_name(LOWBLOCKER):
            self.low_blocker_rects.append(self._pg_rect(rect))
        for nrect in tmx_data.get_layer_by_name(SOUNDS):
            self.sounds.append(NamedRect(nrect.name, self._pg_rect(nrect)))
        for obj in tmx_data.get_layer_by_name(STARTPOS):
            self.start_pos.append(Portal(obj.name, self._pg_rect(obj), data.map_name, obj.type,
                                         self._has_dir(obj, 'direction')))
        for obj in tmx_data.get_layer_by_name(PORTALS):
            self.portals.append(Portal(data.map_name, self._pg_rect(obj), obj.name, obj.type))
        for obj in tmx_data.get_layer_by_name(EVENTS):
            if obj.name == 'location':
                self.locations.append(NamedRect(obj.type, self._pg_rect(obj)))
            elif obj.name.startswith('text'):
                # in obj.type kan iets staan, als daar bijv zwart staat, dan heeft het text_event een zwarte achtergrond
                self.text_events.append(NamedRect(obj.name, self._pg_rect(obj), obj.type))
            elif obj.name.startswith('move'):
                self.move_events.append(NamedRect(obj.name, self._pg_rect(obj)))

        for obj in tmx_data.get_layer_by_name(OBJECTS):
            if obj.name == 'blocker':
                # in obj.type staat de bijbehorende quest key.
                self.quest_blocker_rects.append(NamedRect(obj.type, self._pg_rect(obj)))
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
                elif PeopleDatabase[obj.name].value.get('chapter'):
                    # zoek de .name op van de chapter in de peopledatabase. (als die er is)
                    chapter_name = PeopleDatabase[obj.name].value['chapter'].name
                    # die bevat een dict met 1 waarde
                    chapter_dict = data.chapters[chapter_name]
                    # dat is een boolean
                    chapter_bool = chapter_dict['condition']
                    if chapter_bool:
                        self.people.append(person_object)
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
                if 'time1' in TreasureChestDatabase[obj.name].value:
                    time1 = TreasureChestDatabase[obj.name].value['time1']
                    time2 = TreasureChestDatabase[obj.name].value['time2']
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

        self.grid = list()
        Tile.total_tiles = 0
        for y in range(0, self.height, tileheight):
            for x in range(0, self.width, tilewidth):
                tile = Tile(x, y, tilewidth, tileheight)
                if len(tile.collidelistall(self.high_blocker_rects)) == 1 or \
                   len(tile.collidelistall(self.low_blocker_rects)) == 1:
                    tile.solid = True
                self.grid.append(tile)

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

    def remove_rewarded_quest_blockers(self, logbook):
        """
        verwijder eventueel quest blockers weer
        """
        # als er iets in de lijst van quest blockers staat:
        if len(self.quest_blocker_rects) > 0:
            # van 0 tot 3 bijv
            for i in range(0, len(self.quest_blocker_rects), 1):
                # de naam van de quest blocker is de key van de quest. haal die uit het logbook op basis van de naam.
                the_quest = logbook.get(self.quest_blocker_rects[i].name)
                # bekijk dan of hij al rewarded is:
                if the_quest is not None and the_quest.is_rewarded():
                    # haal dan die quest blocker uit de lijst
                    del self.quest_blocker_rects[i]

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
