
"""
class: Script
"""

import characters
from constants import Direction
from database import HeroDatabase
from database import QuestDatabase
from database import SparklyDatabase
from database import TreasureChestDatabase
import equipment
import pouchitems


class Script(object):
    """
    Alle momenten van het spel
    """
    def __init__(self, engine):
        self.engine = engine

    def new_game(self):
        """
        Wat te doen bij het starten van een nieuw spel.
        """
        # Vul de heroes database met alle hero objecten die in factory zijn gemaakt.
        self.engine.data.heroes = characters.factory_all_heroes(HeroDatabase)
        # Treasure chest en Sparklies worden geen losse objecten, maar blijven 1 object met meerdere dicts.
        self.engine.data.treasure_chests = TreasureChestDatabase()
        self.engine.data.sparklies = SparklyDatabase()
        self.engine.data.quests = QuestDatabase()

        # Vul de party aan met de eerste hero
        self.engine.data.party.add(self.engine.data.heroes['alagos'], verbose=False)

        eqp_item = equipment.factory_equipment_item('bronzemace')
        self.engine.data.inventory.add_i(eqp_item, verbose=False)
        pouch_item = pouchitems.factory_pouch_item('gold')
        self.engine.data.pouch.add(pouch_item, 1, verbose=False)

        self.engine.data.map_name = 'ersin_forest_start'
        self.engine.data.map_pos = 'start_game'     # dit is de naam van de startpositie object in de tmx map
        self.engine.data.map_dir = Direction.South
