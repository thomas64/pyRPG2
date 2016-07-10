
"""
class: AccessoryDatabase
"""

import enum

from constants import EquipmentType


SPRITEPATH = 'resources/sprites/icons/equipment/accessory1.png'


class AccessoryDatabase(enum.Enum):
    """..."""
    rope = dict(nam="Rope",                     srt=1, val=35, shp=True,  wht=1, min_dex=21, thf=2, col=0,   row=0)
    smithshammer = dict(nam="Smith's Hammer",   srt=2, val=40, shp=True,  wht=2, min_str=23, mec=2, col=0,   row=32)
    chemset = dict(nam="Chemset",               srt=3, val=60, shp=True,  wht=1, min_int=22, alc=2, col=128, row=0)
    medkit = dict(nam="Medkit",                 srt=4, val=50, shp=True,  wht=1, min_int=20, hlr=2, col=96,  row=0)
    hornofkynon = dict(nam="Horn of Kynon",     srt=5, val=40, shp=False, wht=1, min_int=20, trb=3, col=32,  row=0)
    harpofigone = dict(nam="Harp of Igone",     srt=6, val=80, shp=False, wht=1, min_int=24, trb=6, col=64,  row=0)
    spellbook = dict(nam="Spellbook",           srt=7, val=80, shp=True,  wht=1, min_int=26, wiz=2, col=32,  row=32)
    # todo, alle spells +1 oid?
    wizardswand = dict(nam="Wizard's Wand",     srt=8, val=80, shp=True,  wht=1, min_wiz=9,         col=64,  row=32)

for acy in AccessoryDatabase:
    acy.value['typ'] = EquipmentType.acy
    acy.value['spr'] = SPRITEPATH
