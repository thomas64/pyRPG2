
"""
class: BeltsData
"""

import equipment.gear

# todo, alle belts afmaken

SPRITEPATH = ''


class BeltsData(equipment.gear.GearData):
    """
    Hier staan alle gordels uit het spel in als enum met een dict voor de waarden.
    """
    leatherbelt = dict(nam="Leather Belt", val=100, shp=True,  wht=1, prt=1)

    @staticmethod
    def factory(belt):
        """
        Maak een object van een enum database item.
        :param belt: een bovenstaand enum item
        :return: een gearitem object met attributen uit de bovenstaande enum dict
        """
        if belt is None:
            return equipment.gear.GearItem(equipment.gear.GearType.belt, SPRITEPATH)
        return equipment.gear.GearItem(equipment.gear.GearType.belt, SPRITEPATH, **belt.value)
