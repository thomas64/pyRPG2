
"""
class: GlovesDatabase
"""

import collections

import console
import equipment

# todo, alle handschoenen afmaken

SPRITEPATH = 'resources/sprites/icons/equipment/gloves1.png'


class GlovesDatabase(collections.OrderedDict):
    """
    Zie accessory
    """
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

        self['leathergloves'] = dict(nam="Leather Gloves", srt=1, val=100, shp=True, wht=1, prt=1, col=0, row=0)
        self['testgloves2'] = dict(nam="Test Gloves 2",    srt=2, val=200, shp=True, wht=2, prt=2, col=0, row=0)

    def factory(self, key_name):
        """
        Zie accessory
        :param key_name:
        """
        if key_name is None:
            return equipment.EquipmentItem(equipment.EquipmentType.glv.value)
        try:
            gloves = self[key_name]
            gloves['spr'] = SPRITEPATH
            return equipment.EquipmentItem(equipment.EquipmentType.glv.value, **gloves)
        except KeyError:
            console.equipment_item_name_not_in_database(key_name)
