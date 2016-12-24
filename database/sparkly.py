
"""
class: SparklyDatabase
"""

from .pouchitem import PouchItemDatabase


# is een class en geen losse dict, want anders wordt de dict niet ververst bij een nieuwe game.
class SparklyDatabase(dict):
    """
    Alle glinsteringen met inhoud op een rij.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ersin_forest_start
        self['sparkly1'] = dict(content=dict(itm1=dict(nam=PouchItemDatabase.gold,       qty=1)))
        self['sparkly3'] = dict(content=dict(itm1=dict(nam=PouchItemDatabase.spices,     qty=9)))
        self['sparkly4'] = dict(content=dict(itm1=dict(nam=PouchItemDatabase.herbs,      qty=11)))
        self['sparkly5'] = dict(content=dict(itm1=dict(nam=PouchItemDatabase.gold,       qty=1)))
        self['sparkly8'] = dict(content=dict(itm1=dict(nam=PouchItemDatabase.herbs,      qty=2)))
        self['sparkly9'] = dict(content=dict(itm1=dict(nam=PouchItemDatabase.spices,     qty=2)))
        self['sparkly10'] = dict(content=dict(itm1=dict(nam=PouchItemDatabase.gold,      qty=1)))
        self['sparkly11'] = dict(content=dict(itm1=dict(nam=PouchItemDatabase.spices,    qty=1)))
        self['sparkly12'] = dict(content=dict(itm1=dict(nam=PouchItemDatabase.gold,      qty=1)))
        # ersin_cave_room2
        self['sparkly2'] = dict(content=dict(itm1=dict(nam=PouchItemDatabase.herbs,      qty=2)))
        # ersin_forest_hole
        self['sparkly6'] = dict(content=dict(itm1=dict(nam=PouchItemDatabase.gemstones,  qty=1)))
        self['sparkly7'] = dict(content=dict(itm1=dict(nam=PouchItemDatabase.gemstones,  qty=3)))
        # ersin_forest_pond
        self['sparkly13'] = dict(content=dict(itm1=dict(nam=PouchItemDatabase.herbs,     qty=1)))
        self['sparkly14'] = dict(content=dict(itm1=dict(nam=PouchItemDatabase.herbs,     qty=1)))
        self['sparkly15'] = dict(content=dict(itm1=dict(nam=PouchItemDatabase.herbs,     qty=1)))
        self['sparkly16'] = dict(content=dict(itm1=dict(nam=PouchItemDatabase.herbs,     qty=1)))
        self['sparkly17'] = dict(content=dict(itm1=dict(nam=PouchItemDatabase.herbs,     qty=1)))
        # ersin_forest_waterfall
        self['sparkly18'] = dict(content=dict(itm1=dict(nam=PouchItemDatabase.gemstones, qty=1)))
        self['sparkly19'] = dict(content=dict(itm1=dict(nam=PouchItemDatabase.herbs,     qty=2)))

        for value in self.values():
            value['taken'] = 0
