
"""
class: GlovesData
"""

import equipment.equipment

# todo, alle gloves afmaken

SPRITEPATH = ''


class GlovesData(equipment.equipment.GearData):
    """
    Hier staan alle handschoenen uit het spel in als enum met een dict voor de waarden.
    """
    leathergloves = dict(nam="Leather Gloves", val=100, shp=True,  wht=1, prt=1)

    @staticmethod
    def factory(gloves):
        """
        Maak een object van een enum database item.
        :param gloves: een bovenstaand enum item
        :return: een gearitem object met attributen uit de bovenstaande enum dict
        """
        if gloves is None:
            return equipment.equipment.GearItem(equipment.equipment.GearType.gloves, SPRITEPATH)
        return equipment.equipment.GearItem(equipment.equipment.GearType.gloves, SPRITEPATH, **gloves.value)
