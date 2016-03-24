
"""
class: RingDatabase
"""

import collections

import console
import equipment

# todo, alle ringen afmaken

SPRITEPATH = 'resources/sprites/icons/equipment/ring1.png'


class RingDatabase(collections.OrderedDict):
    """
    Zie accessory
    """
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

        self['testring'] = dict(nam="Test Ring",    srt=1, val=100, shp=True, wht=1, prt=1, col=0, row=0)
        self['testring2'] = dict(nam="Test Ring 2", srt=2, val=200, shp=True, wht=2, prt=2, col=0, row=0)

    def factory(self, key_name):
        """
        Zie accessory
        :param key_name:
        """
        if key_name is None:
            return equipment.EquipmentItem(equipment.EquipmentType.rng)
        try:
            ring = self[key_name]
            ring['spr'] = SPRITEPATH
            return equipment.EquipmentItem(equipment.EquipmentType.rng, **ring)
        except KeyError:
            console.error_equipment_item_name_not_in_database(key_name)
            raise KeyError
