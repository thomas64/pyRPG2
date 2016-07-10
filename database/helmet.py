
"""
class: HelmetDatabase
"""

import enum

from constants import EquipmentType
from constants import ItemMaterial


SPRITEPATH = 'resources/sprites/icons/equipment/helmet1.png'


class HelmetDatabase(enum.Enum):
    """..."""
    #                                                       val=prt**2+6
    leathercap = dict(nam="Leather Cap",            srt=1,  val=7,  shp=True,  wht=1, prt=1,        col=0,   row=0, mtr=ItemMaterial.ltr)

    bronzehelmet = dict(nam="Bronze Helmet",        srt=3,  val=10, shp=True,  wht=2, prt=2,        col=32,  row=0, mtr=ItemMaterial.brz)
    bronzehelmet2 = dict(nam="Bronze Helmet +",     srt=4,  val=11, shp=False, wht=1, prt=2,        col=32,  row=0, mtr=ItemMaterial.brz)
    ironhelmet = dict(nam="Iron Helmet",            srt=5,  val=15, shp=True,  wht=3, prt=3,        col=64,  row=0, mtr=ItemMaterial.irn)
    ironhelmet2 = dict(nam="Iron Helmet +",         srt=6,  val=16, shp=False, wht=2, prt=3,        col=64,  row=0, mtr=ItemMaterial.irn)
    steelhelmet = dict(nam="Steel Helmet",          srt=7,  val=22, shp=True,  wht=4, prt=4,        col=96,  row=0, mtr=ItemMaterial.stl)
    steelhelmet2 = dict(nam="Steel Helmet +",       srt=8,  val=23, shp=False, wht=3, prt=4,        col=96,  row=0, mtr=ItemMaterial.stl)
    silverhelmet = dict(nam="Silver Helmet",        srt=9,  val=31, shp=True,  wht=5, prt=5,        col=128, row=0, mtr=ItemMaterial.slv)
    silverhelmet2 = dict(nam="Silver Helmet +",     srt=10, val=32, shp=False, wht=4, prt=5,        col=128, row=0, mtr=ItemMaterial.slv)
    titaniumhelmet = dict(nam="Titanium Helmet",    srt=11, val=42, shp=False, wht=2, prt=5,        col=160, row=0, mtr=ItemMaterial.tnm)
    titaniumhelmet2 = dict(nam="Titanium Helmet +", srt=12, val=43, shp=False, wht=1, prt=5,        col=160, row=0, mtr=ItemMaterial.tnm)

    helmofknowledge = dict(nam="Helm of Knowledge", srt=13, val=7,  shp=False, wht=2, prt=1, int=3, col=0,   row=32)
    helmofwisdom = dict(nam="Helm of Wisdom",       srt=14, val=7,  shp=False, wht=2, prt=1, wil=5, col=32,  row=32)
    helmofcharisma = dict(nam="Helm of Charisma",   srt=15, val=7,  shp=False, wht=2, prt=1, dip=2, col=64,  row=32)
    helmofinsight = dict(nam="Helm of Insight",     srt=16, val=7,  shp=False, wht=2, prt=1, lor=2, col=96,  row=32)
    helmoftempests = dict(nam="Helm of Tempests",   srt=17, val=7,  shp=False, wht=2, prt=1, war=2, col=128, row=32)

    # todo, spell battery +15 ook nog toevoegen
    wizardhat = dict(nam="Wizard Hat",              srt=18, val=6,  shp=False, wht=0,        wiz=1, col=160, row=32)


for hlm in HelmetDatabase:
    hlm.value['typ'] = EquipmentType.hlm
    hlm.value['spr'] = SPRITEPATH
