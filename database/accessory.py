
"""
class: AccessoryDatabase
"""

import enum

from constants import EquipmentType

# todo, alle accessoires afmaken
# todo, alle sprites van alle equipment items

SPRITEPATH = 'resources/sprites/icons/equipment/accessory1.png'


class AccessoryDatabase(enum.Enum):
    """..."""
    testaccessory = dict(nam="Test Accessory",    srt=1, val=100, shp=True, wht=1, prt=1, col=0, row=0)
    testaccessory2 = dict(nam="Test Accessory 2", srt=2, val=200, shp=True, wht=2, prt=2, col=0, row=0)


for acy in AccessoryDatabase:
    acy.value['typ'] = EquipmentType.acy
    acy.value['spr'] = SPRITEPATH
