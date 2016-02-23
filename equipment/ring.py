
"""
class: RingsData
"""

import equipment.equipment

# todo, ringen afmaken

SPRITEPATH = ''


class RingsData(equipment.equipment.GearData):
    """
    Hier staan alle ringen uit het spel in als enum met een dict voor de waarden.
    """
    testring = dict(nam="Test Ring", val=100, shp=True,  wht=1, prt=1)

    @staticmethod
    def factory(ring):
        """
        Maak een object van een enum database item.
        :param ring: een bovenstaand enum item
        :return: een gearitem object met attributen uit de bovenstaande enum dict
        """
        if ring is None:
            return equipment.equipment.GearItem(equipment.equipment.GearType.ring, SPRITEPATH)
        return equipment.equipment.GearItem(equipment.equipment.GearType.ring, SPRITEPATH, **ring.value)
