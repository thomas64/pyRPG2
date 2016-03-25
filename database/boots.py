
"""
Boots
"""

import collections

from . import EquipmentType


# todo, prijzen nog bepalen

SPRITEPATH = 'resources/sprites/icons/equipment/boots1.png'

b = collections.OrderedDict()

b['leatherboots'] = dict(nam="Leather Boots",         srt=1,  val=100,  shp=True,  wht=1, prt=1, col=0, row=0)
b['bronzeboots'] = dict(nam="Bronze Boots",           srt=2,  val=200,  shp=True,  wht=2, prt=2, col=0, row=0)
b['ironboots'] = dict(nam="Iron Boots",               srt=3,  val=400,  shp=True,  wht=3, prt=3, col=0, row=0)
b['steelboots'] = dict(nam="Steel Boots",             srt=4,  val=800,  shp=True,  wht=4, prt=4, col=0, row=0)
b['silverboots'] = dict(nam="Silver Boots",           srt=5,  val=1600, shp=True,  wht=5, prt=5, col=0, row=0)
b['titaniumboots'] = dict(nam="Titanium Boots",       srt=6,  val=3200, shp=False, wht=1, prt=5, col=0, row=0)

b['bootsofmotion'] = dict(nam="Boots of Motion",      srt=7,  val=1000, shp=True,  wht=2, prt=1, mvp=1, col=0, row=0)
b['bootsofmotion2'] = dict(nam="Boots of Motion +",   srt=8,  val=1100, shp=False, wht=3, prt=2, mvp=1, col=0, row=0)
b['bootsofspeed'] = dict(nam="Boots of Speed",        srt=9,  val=2000, shp=True,  wht=2, prt=1, mvp=2, col=0, row=0)
b['bootsofspeed2'] = dict(nam="Boots of Speed +",     srt=10, val=2200, shp=False, wht=3, prt=2, mvp=2, col=0, row=0)
b['woodsmansboots'] = dict(nam="Woodsman's Boots",    srt=11, val=1000, shp=True,  wht=2, prt=1, ran=1, col=0, row=0)
b['woodsmansboots2'] = dict(nam="Woodsman's Boots +", srt=12, val=1100, shp=False, wht=3, prt=2, ran=1, col=0, row=0)
b['silenceboots'] = dict(nam="Silence Boots",         srt=13, val=1000, shp=True,  wht=2, prt=1, stl=1, col=0, row=0)
b['silenceboots2'] = dict(nam="Silence Boots +",      srt=14, val=1100, shp=False, wht=3, prt=2, stl=1, col=0, row=0)

for value in b.values():
    value['typ'] = EquipmentType.bts
    value['spr'] = SPRITEPATH
