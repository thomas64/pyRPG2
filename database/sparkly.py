
"""
class: SparklyDatabase
"""

import aenum

from .pouchitem import PouchItemDatabase


class SparklyDatabase(aenum.NoAliasEnum):
    """
    NoAliasEnum mag dezelfde values bevatten in tegenstelling tot Enum.
    Alle glinsteringen met inhoud op een rij.
    """
    # ersin_forest_start
    sparkly1 = dict(content=dict(itm1=dict(nam=PouchItemDatabase.gold,       qty=1)))
    sparkly3 = dict(content=dict(itm1=dict(nam=PouchItemDatabase.spices,     qty=9)))
    sparkly4 = dict(content=dict(itm1=dict(nam=PouchItemDatabase.herbs,      qty=11)))
    sparkly5 = dict(content=dict(itm1=dict(nam=PouchItemDatabase.gold,       qty=1)))
    sparkly8 = dict(content=dict(itm1=dict(nam=PouchItemDatabase.herbs,      qty=2)))
    sparkly9 = dict(content=dict(itm1=dict(nam=PouchItemDatabase.spices,     qty=2)))
    sparkly10 = dict(content=dict(itm1=dict(nam=PouchItemDatabase.gold,      qty=1)))
    sparkly11 = dict(content=dict(itm1=dict(nam=PouchItemDatabase.spices,    qty=1)))
    sparkly12 = dict(content=dict(itm1=dict(nam=PouchItemDatabase.gold,      qty=1)))
    # ersin_cave_room2
    sparkly2 = dict(content=dict(itm1=dict(nam=PouchItemDatabase.herbs,      qty=2)))
    # ersin_forest_hole
    sparkly6 = dict(content=dict(itm1=dict(nam=PouchItemDatabase.gemstones,  qty=1)))
    sparkly7 = dict(content=dict(itm1=dict(nam=PouchItemDatabase.gemstones,  qty=3)))
    # ersin_forest_pond
    sparkly13 = dict(content=dict(itm1=dict(nam=PouchItemDatabase.herbs,     qty=1)))
    sparkly14 = dict(content=dict(itm1=dict(nam=PouchItemDatabase.herbs,     qty=1)))
    sparkly15 = dict(content=dict(itm1=dict(nam=PouchItemDatabase.herbs,     qty=1)))
    sparkly16 = dict(content=dict(itm1=dict(nam=PouchItemDatabase.herbs,     qty=1)))
    sparkly17 = dict(content=dict(itm1=dict(nam=PouchItemDatabase.herbs,     qty=1)))
    # ersin_forest_waterfall
    sparkly18 = dict(content=dict(itm1=dict(nam=PouchItemDatabase.gemstones, qty=1)))
    sparkly19 = dict(content=dict(itm1=dict(nam=PouchItemDatabase.herbs,     qty=2)))


# noinspection PyTypeChecker
for sparkly in SparklyDatabase:
    sparkly.value['taken'] = 0
