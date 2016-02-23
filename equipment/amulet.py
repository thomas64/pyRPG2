
"""
class: AmuletsData
"""

import equipment.gear

# todo, alle amuletten afmaken

SPRITEPATH = ''


class AmuletsData(equipment.gear.GearData):
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
            return equipment.gear.GearItem(equipment.gear.GearType.amulet, SPRITEPATH)
        return equipment.gear.GearItem(equipment.gear.GearType.amulet, SPRITEPATH, **amulet.value)
