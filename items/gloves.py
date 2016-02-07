
"""
class: GlovesData
"""

import items.gear

# todo, alle gloves afmaken


class GlovesData(items.gear.GearData):
    """
    Hier staan alle handschoenen uit het spel in als enum met een dict voor de waarden.
    """
    leathergloves = dict(name="Leather Gloves", value=100, shop=True,  weight=1, prt=1)

    @staticmethod
    def factory(gloves):
        """
        Maak een object van een enum database item.
        :param gloves: een bovenstaand enum item
        :return: een gearitem object met attributen uit de bovenstaande enum dict
        """
        return items.gear.GearItem(items.gear.GearType.gloves, **gloves.value)
