
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
        self.quests = dict()

        self.party = containers.Party()
        self.inventory = containers.Inventory()
        self.pouch = containers.Pouch()

        self.map_name = None
        self.map_pos = None
        self.map_dir = None
