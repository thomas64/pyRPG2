
"""
class: CloakDatabase
"""

import collections

import console
import equipment

SPRITEPATH = 'resources/sprites/icons/equipment/cloak1.png'


class CloakDatabase(collections.OrderedDict):
    """
    Zie accessory
    """
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

        self['cottoncloak'] = dict(nam="Cotton Cloak",                srt=1,  val=100,   shp=True,  wht=1, prt=1,        col=0, row=0)
        self['leathercloak'] = dict(nam="Leather Cloak",              srt=2,  val=1000,  shp=True,  wht=2, prt=2,        col=0, row=0)

        self['covercloak'] = dict(nam="Cover Cloak",                  srt=3,  val=100,   shp=True,  wht=1, stl=1,        col=0, row=0)
        self['covercloak2'] = dict(nam="Cover Cloak +",               srt=4,  val=110,   shp=False, wht=2, stl=1, prt=1, col=0, row=0)
        self['darkcloak'] = dict(nam="Dark Cloak",                    srt=5,  val=300,   shp=True,  wht=1, stl=2,        col=0, row=0)
        self['darkcloak2'] = dict(nam="Dark Cloak +",                 srt=6,  val=330,   shp=False, wht=2, stl=2, prt=1, col=0, row=0)
        self['disguisecloak'] = dict(nam="Disguise Cloak",            srt=7,  val=700,   shp=True,  wht=1, stl=3,        col=0, row=0)
        self['disguisecloak2'] = dict(nam="Disguise Cloak +",         srt=8,  val=770,   shp=False, wht=2, stl=3, prt=1, col=0, row=0)
        self['concealcloak'] = dict(nam="Conceal Cloak",              srt=9,  val=1500,  shp=True,  wht=1, stl=4,        col=0, row=0)
        self['concealcloak2'] = dict(nam="Conceal Cloak +",           srt=10, val=1650,  shp=False, wht=2, stl=4, prt=1, col=0, row=0)
        self['nightcloak'] = dict(nam="Night Cloak",                  srt=11, val=3100,  shp=True,  wht=1, stl=5,        col=0, row=0)
        self['nightcloak2'] = dict(nam="Night Cloak +",               srt=12, val=3410,  shp=False, wht=2, stl=5, prt=1, col=0, row=0)
        self['stealthcloak'] = dict(nam="Stealth Cloak",              srt=13, val=6300,  shp=True,  wht=1, stl=6,        col=0, row=0)
        self['stealthcloak2'] = dict(nam="Stealth Cloak +",           srt=14, val=6930,  shp=False, wht=2, stl=6, prt=1, col=0, row=0)
        self['phantomcloak'] = dict(nam="Phantom Cloak",              srt=15, val=12700, shp=True,  wht=1, stl=7,        col=0, row=0)
        self['phantomcloak2'] = dict(nam="Phantom Cloak +",           srt=16, val=13970, shp=False, wht=2, stl=7, prt=1, col=0, row=0)
        self['invisibilitycloak'] = dict(nam="Invisibility Cloak",    srt=17, val=25500, shp=True,  wht=1, stl=8,        col=0, row=0)
        self['invisibilitycloak2'] = dict(nam="Invisibility Cloak +", srt=18, val=28050, shp=False, wht=2, stl=8, prt=1, col=0, row=0)

        self['silkcloak'] = dict(nam="Silk Cloak",                    srt=19, val=2500,  shp=True,  wht=1, thf=1,        col=0, row=0)
        self['silkcloak2'] = dict(nam="Silk Cloak +",                 srt=20, val=2750,  shp=False, wht=2, thf=1, prt=1, col=0, row=0)
        self['thievescloak'] = dict(nam="Thieves Cloak",              srt=21, val=5000,  shp=True,  wht=1, thf=2,        col=0, row=0)
        self['thievescloak2'] = dict(nam="Thieves Cloak +",           srt=22, val=5500,  shp=False, wht=2, thf=2, prt=1, col=0, row=0)

    def factory(self, key_name):
        """
        Zie accessory
        :param key_name:
        """
        if key_name is None:
            return equipment.EquipmentItem(equipment.EquipmentType.clk.value)
        try:
            cloak = self[key_name]
            cloak['spr'] = SPRITEPATH
            return equipment.EquipmentItem(equipment.EquipmentType.clk.value, **cloak)
        except KeyError:
            console.equipment_item_name_not_in_database(key_name)
