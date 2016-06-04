
"""
Helmet
"""

import collections

from . import EquipmentType


# todo, wizard hat stats nog aanpassen, vooral betreffende protection en weight

SPRITEPATH = 'resources/sprites/icons/equipment/helmet1.png'

hlm = collections.OrderedDict()

hlm['leathercap'] = dict(nam="Leather Cap",               srt=1,  val=100,   shp=True,  wht=1, prt=1,        col=0,   row=0)
hlm['bronzehelmet'] = dict(nam="Bronze Helmet",           srt=2,  val=1225,  shp=True,  wht=2, prt=2,        col=32,  row=0)
hlm['ironhelmet'] = dict(nam="Iron Helmet",               srt=3,  val=3600,  shp=True,  wht=3, prt=3,        col=64,  row=0)
hlm['steelhelmet'] = dict(nam="Steel Helmet",             srt=4,  val=7225,  shp=True,  wht=4, prt=4,        col=96,  row=0)
hlm['silverhelmet'] = dict(nam="Silver Helmet",           srt=5,  val=12100, shp=True,  wht=5, prt=5,        col=128, row=0)
hlm['titaniumhelmet'] = dict(nam="Titanium Helmet",       srt=6,  val=24300, shp=False, wht=1, prt=5,        col=160, row=0)

hlm['helmofknowledge'] = dict(nam="Helm of Knowledge",    srt=7,  val=5500,  shp=True,  wht=2, prt=1, int=2, col=0,   row=32)
hlm['helmofknowledge2'] = dict(nam="Helm of Knowledge +", srt=8,  val=6050,  shp=False, wht=3, prt=2, int=2, col=0,   row=32)
hlm['helmofwisdom'] = dict(nam="Helm of Wisdom",          srt=9,  val=5500,  shp=True,  wht=2, prt=1, wil=2, col=32,  row=32)
hlm['helmofwisdom2'] = dict(nam="Helm of Wisdom +",       srt=10, val=6050,  shp=False, wht=3, prt=2, wil=2, col=32,  row=32)
hlm['helmofcharisma'] = dict(nam="Helm of Charisma",      srt=11, val=6600,  shp=True,  wht=2, prt=1, dip=1, col=64,  row=32)
hlm['helmofcharisma2'] = dict(nam="Helm of Charisma +",   srt=12, val=7260,  shp=False, wht=3, prt=2, dip=1, col=64,  row=32)
hlm['helmofinsight'] = dict(nam="Helm of Insight",        srt=13, val=7700,  shp=True,  wht=2, prt=1, lor=1, col=96,  row=32)
hlm['helmofinsight2'] = dict(nam="Helm of Insight +",     srt=14, val=8470,  shp=False, wht=3, prt=2, lor=1, col=96,  row=32)
hlm['helmoftempests'] = dict(nam="Helm of Tempests",      srt=15, val=8800,  shp=True,  wht=2, prt=1, war=1, col=128, row=32)
hlm['helmoftempests2'] = dict(nam="Helm of Tempests +",   srt=16, val=9680,  shp=False, wht=3, prt=2, war=1, col=128, row=32)

hlm['wizardhat'] = dict(nam="Wizard Hat",                 srt=17, val=9900,  shp=True,  wht=2, prt=1, wiz=1, col=160, row=32)
hlm['wizardhat2'] = dict(nam="Wizard Hat +",              srt=18, val=10890, shp=False, wht=3, prt=2, wiz=1, col=160, row=32)

for value in hlm.values():
    value['typ'] = EquipmentType.hlm
    value['spr'] = SPRITEPATH
