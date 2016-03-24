
"""
class: TreasureChestDatabase
"""

from equipment import EquipmentType as Eqp


class TreasureChestDatabase(dict):
    """
    Alle schatkisten met inhoud op een rij.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # start_forest
        self['chest1'] = dict(content=dict(eqp1=dict(typ=Eqp.wpn, nam='bronzeshortsword', qty=1),
                                           eqp2=dict(typ=Eqp.hlm, nam='leathercap',       qty=1)))
        # self['chest1'] = dict(content=dict(gold=100,
        #                                    herbs=3,
        #                                    eqp1=dict(typ='wpn', nam='bronzeshortsword', qty=1),
        #                                    eqp2=dict(typ='hlm', nam='leathercap',       qty=1)))

        for key, value in self.items():
            value['opened'] = 0
