
"""
Belt
"""

import collections

from . import EquipmentType


# todo, alle gordels afmaken

SPRITEPATH = 'resources/sprites/icons/equipment/belt1.png'

b = collections.OrderedDict()

b['leatherbelt'] = dict(nam="Leather Belt", srt=1, val=100, shp=True, wht=1, prt=1, col=0, row=0)
b['testbelt2'] = dict(nam="Test Belt 2",    srt=2, val=200, shp=True, wht=2, prt=2, col=0, row=0)

for value in b.values():
    value['typ'] = EquipmentType.blt
    value['spr'] = SPRITEPATH
