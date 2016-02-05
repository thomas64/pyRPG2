
"""
class: NecklacesData
"""

import enum

import items.gear

# todo, alle necklaces afmaken


class NecklacesData(enum.Enum):
    """
    Hier staan alle halskettingen uit het spel in als enum met een dict voor de waarden.
    """
    emptynecklace = dict(name="Empty Necklace", value=0,   shop=False, weight=0)

    testnecklace = dict(name="Test Necklace",   value=100, shop=True,  weight=1, prt=1)

    @staticmethod
    def factory(necklace):
        """
        Maak een object van een enum database item.
        :param necklace: een bovenstaand enum item
        :return: een gearitem object met attributen uit de bovenstaande enum dict
        """
        return items.gear.GearItem(items.gear.GearType.necklace, **necklace.value)
