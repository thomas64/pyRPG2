
"""
class: BraceletDatabase
"""

import enum

from constants import EquipmentType


SPRITEPATH = 'resources/sprites/icons/equipment/bracelet1.png'


class BraceletDatabase(enum.Enum):
    """..."""
    silverbracelet = dict(nam="Regular Silver Bracelet",    srt=1,  val=1, shp=True,                      col=0,   row=0)
    goldbracelet = dict(nam="Regular Gold Bracelet",        srt=2,  val=2, shp=True,                      col=32,  row=0)

    powerbracelet = dict(nam="Power Bracelet",              srt=3,  val=8, shp=False, min_wil=20, str=5,  col=64,  row=0)
    braceletofprecision = dict(nam="Bracelet of Precision", srt=4,  val=8, shp=False,             hit=10, col=96,  row=0)
    braceletofblades = dict(nam="Bracelet of Blades",       srt=5,  val=8, shp=False,             swd=1,  col=0,   row=32)
    braceletofhafts = dict(nam="Bracelet of Hafts",         srt=6,  val=8, shp=False,             haf=1,  col=32,  row=32)
    braceletofpoles = dict(nam="Bracelet of Poles",         srt=7,  val=8, shp=False,             pol=1,  col=64,  row=32)
    braceletofarchery = dict(nam="Bracelet of Archery",     srt=8,  val=8, shp=False,             mis=1,  col=96,  row=32)
    braceletofpropel = dict(nam="Bracelet of Propel",       srt=9,  val=8, shp=False,             thr=1,  col=128, row=32)
    braceletofshielding = dict(nam="Bracelet of Shielding", srt=10, val=8, shp=False,             shd=1,  col=160, row=32)

for brc in BraceletDatabase:
    brc.value['typ'] = EquipmentType.brc
    brc.value['spr'] = SPRITEPATH
    brc.value['wht'] = 0
