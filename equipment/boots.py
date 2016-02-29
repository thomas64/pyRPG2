
"""
class: BootsDatabase
"""

import collections

import console
import equipment

# todo, prijzen nog bepalen

SPRITEPATH = 'resources/sprites/icons/equipment/boots1.png'


class BootsDatabase(collections.OrderedDict):
    """
    Zie accessory
    """
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

        self['leatherboots'] = dict(nam="Leather Boots",         srt=1,  val=100,  shp=True,  wht=1, prt=1, col=0, row=0)
        self['bronzeboots'] = dict(nam="Bronze Boots",           srt=2,  val=200,  shp=True,  wht=2, prt=2, col=0, row=0)
        self['ironboots'] = dict(nam="Iron Boots",               srt=3,  val=400,  shp=True,  wht=3, prt=3, col=0, row=0)
        self['steelboots'] = dict(nam="Steel Boots",             srt=4,  val=800,  shp=True,  wht=4, prt=4, col=0, row=0)
        self['silverboots'] = dict(nam="Silver Boots",           srt=5,  val=1600, shp=True,  wht=5, prt=5, col=0, row=0)
        self['titaniumboots'] = dict(nam="Titanium Boots",       srt=6,  val=3200, shp=False, wht=1, prt=5, col=0, row=0)

        self['bootsofmotion'] = dict(nam="Boots of Motion",      srt=7,  val=1000, shp=True,  wht=2, prt=1, mvp=1, col=0, row=0)
        self['bootsofmotion2'] = dict(nam="Boots of Motion +",   srt=8,  val=1100, shp=False, wht=3, prt=2, mvp=1, col=0, row=0)
        self['bootsofspeed'] = dict(nam="Boots of Speed",        srt=9,  val=2000, shp=True,  wht=2, prt=1, mvp=2, col=0, row=0)
        self['bootsofspeed2'] = dict(nam="Boots of Speed +",     srt=10, val=2200, shp=False, wht=3, prt=2, mvp=2, col=0, row=0)
        self['woodsmansboots'] = dict(nam="Woodsman's Boots",    srt=11, val=1000, shp=True,  wht=2, prt=1, ran=1, col=0, row=0)
        self['woodsmansboots2'] = dict(nam="Woodsman's Boots +", srt=12, val=1100, shp=False, wht=3, prt=2, ran=1, col=0, row=0)
        self['silenceboots'] = dict(nam="Silence Boots",         srt=13, val=1000, shp=True,  wht=2, prt=1, stl=1, col=0, row=0)
        self['silenceboots2'] = dict(nam="Silence Boots +",      srt=14, val=1100, shp=False, wht=3, prt=2, stl=1, col=0, row=0)

    def factory(self, key_name):
        """
        Zie accessory
        :param key_name:
        """
        if key_name is None:
            return equipment.EquipmentItem(equipment.EquipmentType.bts.value)
        try:
            boots = self[key_name]
            boots['spr'] = SPRITEPATH
            return equipment.EquipmentItem(equipment.EquipmentType.bts.value, **boots)
        except KeyError:
            console.equipment_item_name_not_in_database(key_name)
