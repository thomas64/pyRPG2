
"""
class: RingsData
"""

import items.gear

# todo, ringen afmaken


class RingsData(items.gear.GearData):
    """
    Hier staan alle ringen uit het spel in als enum met een dict voor de waarden.
    """
    testring = dict(name="Test Ring",   value=100, shop=True,  weight=1, prt=1)

    @staticmethod
    def factory(ring):
        """
        Maak een object van een enum database item.
        :param ring: een bovenstaand enum item
        :return: een gearitem object met attributen uit de bovenstaande enum dict
        """
        return items.gear.GearItem(items.gear.GearType.ring, **ring.value)
