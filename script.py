
"""
class: Script
"""

import characters
import database.hero
import database.treasurechest
import equipment
import screens.direction


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
        self.engine.data.heroes = characters.factory_all_heroes(database.hero.HeroDatabase)
        # Treasure chest worden geen objecten, maar blijven een object met dicts.
        self.engine.data.treasure_chests = database.treasurechest.TreasureChestDatabase()

        # Vul de party aan met de eerste hero
        self.engine.data.party.add(self.engine.data.heroes['alagos'], verbose=False)
        # De hieronder zijn om te testen
        self.engine.data.party.add(self.engine.data.heroes['raiko'], verbose=False)
        self.engine.data.party.add(self.engine.data.heroes['luana'], verbose=False)
        self.engine.data.party.add(self.engine.data.heroes['grindan'], verbose=False)
        self.engine.data.party.add(self.engine.data.heroes['rydalin'], verbose=False)

        eqp_item = equipment.factory_equipment_item('bronzemace')
        self.engine.data.inventory.add(eqp_item, verbose=False)

        self.engine.data.map_name = 'ersin_forest_start'
        self.engine.data.map_pos = 'start_game'     # dit is de naam van de startpositie object in de tmx map
        self.engine.data.map_dir = screens.direction.Direction.South
