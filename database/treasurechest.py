
"""
class: TreasureChestDatabase
"""

import datetime

from .weapon import WeaponDatabase
from .helmet import HelmetDatabase
from .pouchitem import PouchItemDatabase


# is een class en geen losse dict, want anders wordt de dict niet ververst bij een nieuwe game.
class TreasureChestDatabase(dict):
    """
    Alle schatkisten met inhoud op een rij.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ersin_forest_start
        self['chest1'] = dict(content=dict(itm1=dict(nam=PouchItemDatabase.gold,          qty=2),
                                           itm2=dict(nam=PouchItemDatabase.herbs,         qty=3),
                                           eqp1=dict(nam=WeaponDatabase.bronzeshortsword, qty=1),
                                           eqp2=dict(nam=HelmetDatabase.leathercap,       qty=1)))
        self['chest2'] = dict(condition=dict(thf=3),
                              content=dict(itm1=dict(nam=PouchItemDatabase.gold,          qty=3)),
                              time1=datetime.datetime(2016, 10, 19, 2, 00),
                              time2=datetime.datetime(2099, 10, 19, 2, 15))
        self['chest3'] = dict(condition=dict(mec=2),
                              content=dict(itm1=dict(nam=PouchItemDatabase.gold,          qty=4)))
        self['chest4'] = dict(condition=dict(mec=1, thf=1),
                              content=dict(itm1=dict(nam=PouchItemDatabase.gold,          qty=5)))

        # ersin_cave_room1
        self['chest5'] = dict(content=dict(itm1=dict(nam=PouchItemDatabase.gold,          qty=2)))
        # ersin_cave_room3
        self['chest6'] = dict(content=dict(itm1=dict(nam=PouchItemDatabase.gold,          qty=2)))
        self['chest7'] = dict(content=dict(itm1=dict(nam=PouchItemDatabase.gold,          qty=2)))

        for value in self.values():
            value['opened'] = 0

    @staticmethod
    def mec_text(value):
        """..."""
        return ["There's a dangerous trap on this treasurechest.",
                "You need a level {} of the Mechanic Skill to".format(value),
                "disarm the trap."]

    @staticmethod
    def thf_text(value):
        """..."""
        return ["There's a lock on this treasurechest.",
                "You need a level {} of the Thief Skill".format(value),
                "to pick the lock."]

    @staticmethod
    def open_chest(condition, mec_v, mec_h, thf_v, thf_h):
        """..."""
        text = ["Found:"]
        if condition:
            if mec_v and not thf_v:
                text = ["{} disarmed the trap and found:".format(mec_h)]
            elif thf_v and not mec_v:
                text = ["{} picked the lock and found:".format(thf_h)]
            elif mec_v and thf_v:
                text = ["{} disarmed the trap and {} picked the lock:".format(mec_h, thf_h)]
            if mec_h == thf_h:
                text = ["{} disarmed the trap and picked the lock:".format(mec_h)]
        return text
