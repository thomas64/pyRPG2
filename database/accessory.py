
"""
class: AccessoryDatabase
"""

import collections

import console
import equipment

# todo, alle accessoires afmaken
# todo, alle sprites van alle equipment items

SPRITEPATH = 'resources/sprites/icons/equipment/accessory1.png'


class AccessoryDatabase(collections.OrderedDict):
    """
    Hier staan alle accessoires uit het spel in als OrderedDict met een dict voor de waarden.
    """
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

        self['testaccessory'] = dict(nam="Test Accessory",    srt=1, val=100, shp=True, wht=1, prt=1, col=0, row=0)
        self['testaccessory2'] = dict(nam="Test Accessory 2", srt=2, val=200, shp=True, wht=2, prt=2, col=0, row=0)

    def factory(self, key_name):
        """
        Maakt een object van een van de items uit bovenstaande dict database.
        Geef ook een Enum EquipmentType mee.
        Wanneer een accessory wordt gemaakt die None meekrijgt, maak dan een leeg object aan. Dit is volgens mij
        alleen bij het unequippen van een item.
        :param key_name: de key van een bovenstaande dicts
        :return: een EquipmentItem object met attributen uit de bovenstaande ordered dict
        """
        if key_name is None:
            return equipment.EquipmentItem(equipment.EquipmentType.acy)
        try:
            accessory = self[key_name]
            accessory['spr'] = SPRITEPATH
            return equipment.EquipmentItem(equipment.EquipmentType.acy, **accessory)
        except KeyError:
            console.error_equipment_item_name_not_in_database(key_name)
            raise KeyError
