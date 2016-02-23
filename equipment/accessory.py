
"""
class: AccessoryDataBase
"""

import equipment.gear

# todo, accessoires afmaken

SPRITEPATH = ''


class AccessoryDatabase(equipment.gear.GearData):
    """
    Hier staan alle accessoires uit het spel in als OrderedDict met een dict voor de waarden.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.inside['testaccessory'] = dict(nam="Test Accessory", srt=1, val=100, shp=True, wht=1, prt=1)

    @staticmethod
    def factory(accessory):
        """
        Maak een object van een van de items uit de inside dict database.
        Geef ook een Enum GearType mee.
        Wanneer een accessory wordt gemaakt die None meekrijgt, maak dan een leeg object aan. Dit is volgens mij
        alleen bij het unequippen van een item.
        :param accessory: een bovenstaand item
        :return: een gearitem object met attributen uit de bovenstaande ordered dict
        """
        if accessory is None:
            return equipment.gear.GearItem(equipment.gear.GearType.acy)
        accessory['spr'] = SPRITEPATH
        return equipment.gear.GearItem(equipment.gear.GearType.acy, **accessory)
