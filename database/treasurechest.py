
"""
class: TreasureChestDatabase
"""

from pouchitems import PouchItem


class TreasureChestDatabase(dict):
    """
    Alle schatkisten met inhoud op een rij.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # start_forest
        self['chest1'] = dict(content=dict(itm1=dict(nam=PouchItem.Gold,     qty=100),
                                           itm2=dict(nam=PouchItem.Herbs,    qty=3),
                                           eqp1=dict(nam='bronzeshortsword', qty=1),
                                           eqp2=dict(nam='leathercap',       qty=1)))

        for value in self.values():
            value['opened'] = 0
