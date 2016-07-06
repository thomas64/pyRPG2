
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
        self['sparkly1'] = dict(content=dict(itm1=dict(nam=PouchItemDatabase.gold,  qty=1)))
        # ersin_cave_room2
        self['sparkly2'] = dict(content=dict(itm1=dict(nam=PouchItemDatabase.herbs, qty=4)))

        for value in self.values():
            value['taken'] = 0
