
"""
class: BraceletDatabase
"""

import collections

import console
import equipment

# todo, alle armbanden afmaken

SPRITEPATH = 'resources/sprites/icons/equipment/bracelet1.png'


class BraceletDatabase(collections.OrderedDict):
    """
    Zie accessory
    """
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

        self['testbracelet'] = dict(nam="Test Bracelet",    srt=1, val=100, shp=True, wht=1, prt=1, col=0, row=0)
        self['testbracelet2'] = dict(nam="Test Bracelet 2", srt=2, val=200, shp=True, wht=2, prt=2, col=0, row=0)

    def factory(self, key_name):
        """
        Zie accessory
        :param key_name:
        """
        if key_name is None:
            return equipment.EquipmentItem(equipment.EquipmentType.brc.value)
        try:
            bracelet = self[key_name]
            bracelet['spr'] = SPRITEPATH
            return equipment.EquipmentItem(equipment.EquipmentType.brc.value, **bracelet)
        except KeyError:
            console.equipment_item_name_not_in_database(key_name)
