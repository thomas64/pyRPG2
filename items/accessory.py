
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
    testaccessory = dict(name="Test Accessory",   value=100, shop=True,  weight=1, prt=1)

    def __getitem__(self, item):        # als er iets wordt gevraagd wat niet kan aan een enum, zoals [0] of [1]
        if item == 0:                   # voor een OrderedDict (zoals ShieldsData) dan wordt deze uitgevoerd.
            return self.name            # hij returned dan een waarde die een enum wel kan, namelijk .name en .value
        elif item == 1:
            return self.value

    @staticmethod
    def factory(accessory):
        """
        Maak een object van een enum database item.
        :param accessory: een bovenstaand enum item
        :return: een gearitem object met attributen uit de bovenstaande enum dict
        """
        return items.gear.GearItem(items.gear.GearType.accessory, **accessory.value)
