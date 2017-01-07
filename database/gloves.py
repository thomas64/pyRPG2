
"""
class: GlovesDatabase
"""

import enum

from constants import EquipmentType
from constants import ItemMaterial


SPRITEPATH = 'resources/sprites/icons/equipment/gloves1.png'


class GlovesDatabase(enum.Enum):
    """..."""
    #                                                             val=prt**2+5
    customgauntlets = dict(nam="Custom Gauntlets",        srt=1,  val=1,  shp=False, wht='X', prt='X',  col=0,   row=64,
                           min_wht=1, max_wht=6, min_prt=1, max_prt=6,
                           cus=True, clt=3, ltr=2, wod=0, mtl=7,
                           desc="The Weight of custom made Gauntlets may vary between 1-6 and Protection between 1-6. "
                                "Creating Custom Gauntlets requires 3 Cloth, 2 Leather and 7 metals.")

    leathergloves = dict(nam="Leather Gloves",            srt=2,  val=6,  shp=True,  wht=1, prt=1,        col=0,   row=0, mtr=ItemMaterial.ltr)
    bronzegauntlets = dict(nam="Bronze Gauntlets",        srt=3,  val=9,  shp=True,  wht=2, prt=2,        col=32,  row=0, mtr=ItemMaterial.brz)
    irongauntlets = dict(nam="Iron Gauntlets",            srt=5,  val=14, shp=True,  wht=3, prt=3,        col=64,  row=0, mtr=ItemMaterial.irn)
    steelgauntlets = dict(nam="Steel Gauntlets",          srt=7,  val=21, shp=True,  wht=4, prt=4,        col=96,  row=0, mtr=ItemMaterial.stl)
    silvergauntlets = dict(nam="Silver Gauntlets",        srt=9,  val=30, shp=True,  wht=5, prt=5,        col=128, row=0, mtr=ItemMaterial.slv)
    titaniumgauntlets = dict(nam="Titanium Gauntlets",    srt=11, val=41, shp=False, wht=2, prt=5,        col=160, row=0, mtr=ItemMaterial.tnm)

    gauntletsofmight = dict(nam="Gauntlets of Might",     srt=13, val=6,  shp=False, wht=2, prt=2, str=3, col=0,   row=32)
    laboratorygloves = dict(nam="Laboratory Gloves",      srt=14, val=6,  shp=False, wht=0,        alc=2, col=32,  row=32)
    tinkersgloves = dict(nam="Tinker's Gloves",           srt=15, val=6,  shp=False, wht=0, dex=1, mec=2, col=64,  row=32)
    glovesofhealing = dict(nam="Gloves of Healing",       srt=16, val=6,  shp=False, wht=0,        hlr=2, col=96,  row=32)
    stickygloves = dict(nam="Sticky Gloves",              srt=17, val=6,  shp=False, wht=0,        thf=2, col=128, row=32)
    bardicgloves = dict(nam="Bardic Gloves",              srt=18, val=6,  shp=False, wht=0,        trb=2, col=160, row=32)
    heroesgauntlets = dict(nam="Heroes Gauntlets",        srt=19, val=6,  shp=False, wht=2, prt=2, war=2, col=192, row=32)


for glv in GlovesDatabase:
    glv.value['typ'] = EquipmentType.glv
    glv.value['spr'] = SPRITEPATH
