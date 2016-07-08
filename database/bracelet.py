
"""
class: BraceletDatabase
"""

import enum

from constants import EquipmentType


SPRITEPATH = 'resources/sprites/icons/equipment/bracelet1.png'


class BraceletDatabase(enum.Enum):
    """..."""
    powerbracelet = dict(nam="Power Bracelet",              srt=1, val=50, shp=True,  wht=0, str=5,  col=0,   row=0)
    braceletofprecision = dict(nam="Bracelet of Precision", srt=2, val=50, shp=True,  wht=0, hit=10, col=32,  row=0)
    braceletofblades = dict(nam="Bracelet of Blades",       srt=3, val=50, shp=False, wht=0, swd=1,  col=0,   row=32)
    braceletofhafts = dict(nam="Bracelet of Hafts",         srt=4, val=50, shp=False, wht=0, haf=1,  col=32,  row=32)
    braceletofpoles = dict(nam="Bracelet of Poles",         srt=5, val=50, shp=False, wht=0, pol=1,  col=64,  row=32)
    braceletofarchery = dict(nam="Bracelet of Archery",     srt=6, val=50, shp=False, wht=0, mis=1,  col=96,  row=32)
    braceletofpropel = dict(nam="Bracelet of Propel",       srt=7, val=50, shp=False, wht=0, thr=1,  col=128, row=32)
    braceletofshielding = dict(nam="Bracelet of Shielding", srt=8, val=50, shp=False, wht=0, shd=1,  col=160, row=32)

for brc in BraceletDatabase:
    brc.value['typ'] = EquipmentType.brc
    brc.value['spr'] = SPRITEPATH
