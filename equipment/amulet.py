
"""
class: AmuletsData
"""

import equipment.equipment

# todo, alle amuletten afmaken

SPRITEPATH = ''


class AmuletsData(equipment.equipment.GearData):
    """
    Hier staan alle amuletten uit het spel in als enum met een dict voor de waarden.
    """
    testamulet = dict(nam="Test Amulet", val=100, shp=True,  wht=1, prt=1)

    @staticmethod
    def factory(amulet):
        """
        Maak een object van een enum database item.
        :param amulet: een bovenstaand enum item
        :return: een gearitem object met attributen uit de bovenstaande enum dict
        """
        if amulet is None:
            return equipment.equipment.GearItem(equipment.equipment.GearType.amulet, SPRITEPATH)
        return equipment.equipment.GearItem(equipment.equipment.GearType.amulet, SPRITEPATH, **amulet.value)
