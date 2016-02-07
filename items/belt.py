
"""
class: BeltsData
"""

import items.gear

# todo, alle belts afmaken


class BeltsData(items.gear.GearData):
    """
    Hier staan alle gordels uit het spel in als enum met een dict voor de waarden.
    """
    leatherbelt = dict(name="Leather Belt", value=100, shop=True,  weight=1, prt=1)

    @staticmethod
    def factory(belt):
        """
        Maak een object van een enum database item.
        :param belt: een bovenstaand enum item
        :return: een gearitem object met attributen uit de bovenstaande enum dict
        """
        return items.gear.GearItem(items.gear.GearType.belt, **belt.value)
