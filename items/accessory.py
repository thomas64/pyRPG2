
"""
class: AccessoriesData
"""

import enum

import items.gear

# todo, accessoires afmaken


class AccessoriesData(enum.Enum):
    """
    Hier staan alle accessoires uit het spel in als enum met een dict voor de waarden.
    """
    emptyaccessory = dict(name="Empty Accessory", value=0,   shop=False, weight=0)

    testaccessory = dict(name="Test Accessory",   value=100, shop=True,  weight=1, prt=1)

    @staticmethod
    def factory(accessory):
        """
        Maak een object van een enum database item.
        :param accessory: een bovenstaand enum item
        :return: een gearitem object met attributen uit de bovenstaande enum dict
        """
        return items.gear.GearItem(items.gear.GearType.accessory, **accessory.value)
