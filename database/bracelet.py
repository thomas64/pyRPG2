
"""
Bracelet
"""

import collections

from . import EquipmentType


# todo, alle armbanden afmaken

SPRITEPATH = 'resources/sprites/icons/equipment/bracelet1.png'

b = collections.OrderedDict()

b['testbracelet'] = dict(nam="Test Bracelet",    srt=1, val=100, shp=True, wht=1, prt=1, col=0, row=0)
b['testbracelet2'] = dict(nam="Test Bracelet 2", srt=2, val=200, shp=True, wht=2, prt=2, col=0, row=0)

for value in b.values():
    value['typ'] = EquipmentType.brc
    value['spr'] = SPRITEPATH
