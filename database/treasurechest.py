
"""
class: TreasureChestDatabase
"""


# is een class en geen losse dict, want anders wordt de dict niet ververst bij een nieuwe game.
class TreasureChestDatabase(dict):
    """
    Alle schatkisten met inhoud op een rij.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ersin_forest_start
        self['chest1'] = dict(condition=dict(),
                              content=dict(itm1=dict(nam='gold',                qty=100),
                                           itm2=dict(nam='herbs',               qty=3),
                                           eqp1=dict(nam='bronzeshortsword',    qty=1),
                                           eqp2=dict(nam='lightleatherarmor',   qty=2),
                                           eqp3=dict(nam='mediumleatherarmor',  qty=3),
                                           eqp4=dict(nam='heavyleatherarmor',   qty=4),
                                           eqp5=dict(nam='lightbronzearmor',    qty=5),
                                           eqp6=dict(nam='mediumbronzearmor',   qty=6),
                                           eqp7=dict(nam='heavybronzearmor',    qty=7),
                                           eqp8=dict(nam='lightironarmor',      qty=8),
                                           eqp9=dict(nam='mediumironarmor',     qty=9),
                                           eqp10=dict(nam='heavyironarmor',     qty=10),
                                           eqp11=dict(nam='lightsilverarmor',   qty=11),
                                           eqp12=dict(nam='mediumsilverarmor',  qty=12),
                                           eqp13=dict(nam='heavysilverarmor',   qty=13),
                                           eqp14=dict(nam='lighttitaniumarmor', qty=14),
                                           eqp15=dict(nam='mediumtitaniumarmor', qty=15),
                                           eqp16=dict(nam='heavytitaniumarmor', qty=16),
                                           eqp17=dict(nam='lightsteelarmor',    qty=1),
                                           eqp18=dict(nam='leathercap',         qty=18)))
        self['chest2'] = dict(condition=dict(thf=5),
                              content=dict(itm1=dict(nam='gold',             qty=200)))
        self['chest3'] = dict(condition=dict(mec=5),
                              content=dict(itm1=dict(nam='gold',             qty=300)))
        self['chest4'] = dict(condition=dict(mec=5, thf=5),
                              content=dict(itm1=dict(nam='gold',             qty=400)))

        # ersin_cave_room1
        self['chest5'] = dict(condition=dict(),
                              content=dict(itm1=dict(nam='gold',             qty=10)))
        # ersin_cave_room3
        self['chest6'] = dict(condition=dict(),
                              content=dict(itm1=dict(nam='gold',             qty=10)))
        self['chest7'] = dict(condition=dict(),
                              content=dict(itm1=dict(nam='gold',             qty=10)))

        for value in self.values():
            value['opened'] = 0
