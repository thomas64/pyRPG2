
"""
class: AmuletDatabase
"""

import collections

import console
import equipment

# todo, alle amuletten afmaken

SPRITEPATH = ''


class AmuletDatabase(collections.OrderedDict):
    """
    Zie accessory
    """
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

        self['testamulet'] = dict(nam="Test Amulet",    srt=1, val=100, shp=True, wht=1, prt=1)
        self['testamulet2'] = dict(nam="Test Amulet 2", srt=2, val=200, shp=True, wht=2, prt=2)

    def factory(self, key_name):
        """
        Zie accessory
        :param key_name:
        """
        if key_name is None:
            return equipment.EquipmentItem(equipment.EquipmentType.amu)
        try:
            amulet = self[key_name]
            amulet['spr'] = SPRITEPATH
            return equipment.EquipmentItem(equipment.EquipmentType.amu, **amulet)
        except KeyError:
            console.equipment_item_name_not_in_database(key_name)
