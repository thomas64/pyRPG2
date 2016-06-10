
"""
class: TreasureChestDatabase
"""


def mec_text(value):
    """..."""
    return ["There's a dangerous trap on this treasurechest.",
            "You need a level {} of the Mechanic Skill to".format(value),
            "disarm the trap."]


def thf_text(value):
    """..."""
    return ["There's a lock on this treasurechest.",
            "You need a level {} of the Thief Skill".format(value),
            "to pick the lock."]


# is een class en geen losse dict, want anders wordt de dict niet ververst bij een nieuwe game.
class TreasureChestDatabase(dict):
    """
    Alle schatkisten met inhoud op een rij.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ersin_forest_start
        self['chest1'] = dict(content=dict(itm1=dict(nam='gold',             qty=100),
                                           itm2=dict(nam='herbs',            qty=3),
                                           eqp1=dict(nam='bronzeshortsword', qty=1),
                                           eqp2=dict(nam='leathercap',       qty=1)))
        self['chest2'] = dict(condition=dict(thf=3),
                              content=dict(itm1=dict(nam='gold',             qty=200)))
        self['chest3'] = dict(condition=dict(mec=3),
                              content=dict(itm1=dict(nam='gold',             qty=300)))
        self['chest4'] = dict(condition=dict(mec=1, thf=1),
                              content=dict(itm1=dict(nam='gold',             qty=400)))

        # ersin_cave_room1
        self['chest5'] = dict(content=dict(itm1=dict(nam='gold',             qty=10)))
        # ersin_cave_room3
        self['chest6'] = dict(content=dict(itm1=dict(nam='gold',             qty=10)))
        self['chest7'] = dict(content=dict(itm1=dict(nam='gold',             qty=10)))

        for value in self.values():
            value['opened'] = 0
            if value.get('condition'):
                if value['condition'].get('mec'):
                    value['mec_text'] = mec_text(value['condition']['mec'])
                if value['condition'].get('thf'):
                    value['thf_text'] = thf_text(value['condition']['thf'])
