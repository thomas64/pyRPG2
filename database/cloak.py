
"""
class: CloakDatabase
"""

import enum

from constants import EquipmentType
from constants import ItemMaterial


SPRITEPATH = 'resources/sprites/icons/equipment/cloak1.png'


class CloakDatabase(enum.Enum):
    """..."""
    #                                                             val=prt**2+4
    cottoncloak = dict(nam="Cotton Cloak",                srt=1,  val=5,  shp=True,  wht=1, prt=1, col=0,   row=0,  mtr=ItemMaterial.ctn)
    leathercloak = dict(nam="Leather Cloak",              srt=2,  val=8,  shp=True,  wht=2, prt=2, col=32,  row=0,  mtr=ItemMaterial.ltr)
    #                                                             val=stl**2+9                 neppe materiale eigenlijk
    covercloak = dict(nam="Cover Cloak",                  srt=3,  val=10, shp=True,  wht=0, stl=1, col=0,   row=32, mtr=ItemMaterial.ctn)
    darkcloak = dict(nam="Dark Cloak",                    srt=5,  val=13, shp=True,  wht=0, stl=2, col=32,  row=32, mtr=ItemMaterial.ltr)
    disguisecloak = dict(nam="Disguise Cloak",            srt=7,  val=18, shp=True,  wht=0, stl=3, col=64,  row=32, mtr=ItemMaterial.brz)
    concealcloak = dict(nam="Conceal Cloak",              srt=9,  val=25, shp=True,  wht=0, stl=4, col=96,  row=32, mtr=ItemMaterial.irn)
    nightcloak = dict(nam="Night Cloak",                  srt=11, val=34, shp=True,  wht=0, stl=5, col=128, row=32, mtr=ItemMaterial.stl)
    stealthcloak = dict(nam="Stealth Cloak",              srt=13, val=45, shp=True,  wht=0, stl=6, col=160, row=32, mtr=ItemMaterial.slv)
    phantomcloak = dict(nam="Phantom Cloak",              srt=15, val=58, shp=False, wht=0, stl=7, col=192, row=32)
    invisibilitycloak = dict(nam="Invisibility Cloak",    srt=17, val=73, shp=False, wht=0, stl=8, col=224, row=32)

    silkcloak = dict(nam="Silk Cloak",                    srt=19, val=5,  shp=False, wht=0, thf=2, col=64,  row=0)


for clk in CloakDatabase:
    clk.value['typ'] = EquipmentType.clk
    clk.value['spr'] = SPRITEPATH
