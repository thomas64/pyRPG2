
"""
class: Data
"""

import collections

import containers


class Data(object):
    """
    Hier is alle gamedata.
    """
    def __init__(self):

        self.heroes = collections.OrderedDict()
        self.treasure_chests = dict()

        self.party = containers.Party()
        self.inventory = containers.Inventory()
