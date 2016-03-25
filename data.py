
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

        self.party = containers.Party()
        self.inventory = containers.Inventory()
