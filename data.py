
"""
class: Data
"""

import containers


class Data(object):
    """
    Hier is alle gamedata.
    """
    def __init__(self):

        self.heroes = dict()
        self.treasure_chests = dict()
        self.sparklies = dict()

        self.party = containers.Party()
        self.inventory = containers.Inventory()
        self.pouch = containers.Pouch()
        self.logbook = containers.Logbook()

        self.map_name = None
        self.map_pos = None
        self.map_dir = None

        self.custom_inventory_counter = 0
