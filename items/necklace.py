
"""
class: NecklacesData
"""

import items.gear

# todo, alle necklaces afmaken


class NecklacesData(items.gear.GearData):
    """
    Hier staan alle halskettingen uit het spel in als enum met een dict voor de waarden.
    """
    testnecklace = dict(nam="Test Necklace",   val=100, shp=True,  wht=1, prt=1)

    @staticmethod
    def factory(necklace):
        """
        Maak een object van een enum database item.
        :param necklace: een bovenstaand enum item
        :return: een gearitem object met attributen uit de bovenstaande enum dict
        """
        return items.gear.GearItem(items.gear.GearType.necklace, **necklace.value)
