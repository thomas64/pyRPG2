
"""
Ring
"""

import collections

from constants import EquipmentType


# todo, alle ringen afmaken

SPRITEPATH = 'resources/sprites/icons/equipment/ring1.png'

rng = collections.OrderedDict()

rng['testring'] = dict(nam="Test Ring",    srt=1, val=100, shp=True, wht=1, prt=1, col=0, row=0)
rng['testring2'] = dict(nam="Test Ring 2", srt=2, val=200, shp=True, wht=2, prt=2, col=0, row=0)

for value in rng.values():
    value['typ'] = EquipmentType.rng
    value['spr'] = SPRITEPATH
