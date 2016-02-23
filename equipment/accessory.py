
"""
class: AccessoryDatabase
"""

import collections

import equipment.equipment as eqp

# todo, alle accessoires afmaken

SPRITEPATH = ''


class AccessoryDatabase(collections.OrderedDict):
    """
    Hier staan alle accessoires uit het spel in als OrderedDict met een dict voor de waarden.
    """
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

        self['testaccessory'] = dict(nam="Test Accessory",    srt=1, val=100, shp=True, wht=1, prt=1)
        self['testaccessory2'] = dict(nam="Test Accessory 2", srt=2, val=200, shp=True, wht=2, prt=2)

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
            return eqp.EquipmentItem(eqp.EquipmentType.acy)
        accessory = self[key_name]
        accessory['spr'] = SPRITEPATH
        return eqp.EquipmentItem(eqp.EquipmentType.acy, **accessory)
