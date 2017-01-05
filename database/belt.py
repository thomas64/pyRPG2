
"""
class: BeltDatabase
"""

import enum

from constants import EquipmentType
from constants import ItemMaterial


SPRITEPATH = 'resources/sprites/icons/equipment/belt1.png'


class BeltDatabase(enum.Enum):
    """..."""
    # idee? belts zijn voornamelijk voor bedoeld voor agi te uppen?
    #                                                  val=prt**2+3
    custombelt = dict(nam="Custom Belt",        srt=1, val=1, shp=False, wht=0, prt=0, agi=0,  col=0,   row=32,
                      cus=True, clt=2, ltr=2, wod=0, mtl=0,
                      desc="The Weight of a custom made Belt may vary between 0-2, Protection between 0-2 and "
                           "Agility between 0-3. Creating a Custom Belt requires 2 Cloth and 2 Leather.")

    cottonbelt = dict(nam="Cotton Belt",        srt=2, val=4, shp=True,  wht=0,        agi=1,  col=0,   row=0,  mtr=ItemMaterial.ctn)
    leatherbelt = dict(nam="Leather Belt",      srt=3, val=7, shp=True,  wht=1, prt=1, agi=2,  col=32,  row=0,  mtr=ItemMaterial.ltr)

    comfortbelt = dict(nam="Comfort Belt",      srt=6, val=4, shp=False, wht=0,        agi=3,  col=64,  row=0)
    # todo, deze maakt dat het wisselen van een item tijdens battle geen end_of_turn wordt
    utilitybelt = dict(nam="Utility Belt",      srt=7, val=4, shp=False, wht=1,        dex=-1, col=96,  row=0)
    woodsmansbelt = dict(nam="Woodsman's Belt", srt=8, val=4, shp=False, wht=1, prt=1, ran=1,  col=128, row=0)

for blt in BeltDatabase:
    blt.value['typ'] = EquipmentType.blt
    blt.value['spr'] = SPRITEPATH
