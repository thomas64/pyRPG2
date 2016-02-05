
"""
class: CloaksData
"""

import enum

import items.gear


class CloakData(enum.Enum):
    """
    Hier staan alle mantels uit het spel in als enum met een dict voor de waarden.
    """
    emptycloak = dict(name="Empty Cloak",                  value=0,     shop=False, weight=0)

    leathercloak = dict(name="Leather Cloak",              value=100,   shop=True,  weight=1, prt=1)
    battlecloak = dict(name="Battle Cloak",                value=1000,  shop=True,  weight=2, prt=2)

    covercloak = dict(name="Cover Cloak",                  value=100,   shop=True,  weight=1, stl=1)
    covercloak2 = dict(name="Cover Cloak +",               value=110,   shop=False, weight=2, stl=1, prt=1)
    darkcloak = dict(name="Dark Cloak",                    value=300,   shop=True,  weight=1, stl=2)
    darkcloak2 = dict(name="Dark Cloak +",                 value=330,   shop=False, weight=2, stl=2, prt=1)
    disguisecloak = dict(name="Disguise Cloak",            value=700,   shop=True,  weight=1, stl=3)
    disguisecloak2 = dict(name="Disguise Cloak +",         value=770,   shop=False, weight=2, stl=3, prt=1)
    concealcloak = dict(name="Conceal Cloak",              value=1500,  shop=True,  weight=1, stl=4)
    concealcloak2 = dict(name="Conceal Cloak +",           value=1650,  shop=False, weight=2, stl=4, prt=1)
    nightcloak = dict(name="Night Cloak",                  value=3100,  shop=True,  weight=1, stl=5)
    nightcloak2 = dict(name="Night Cloak +",               value=3410,  shop=False, weight=2, stl=5, prt=1)
    stealthcloak = dict(name="Stealth Cloak",              value=6300,  shop=True,  weight=1, stl=6)
    stealthcloak2 = dict(name="Stealth Cloak +",           value=6930,  shop=False, weight=2, stl=6, prt=1)
    phantomcloak = dict(name="Phantom Cloak",              value=12700, shop=True,  weight=1, stl=7)
    phantomcloak2 = dict(name="Phantom Cloak +",           value=13970, shop=False, weight=2, stl=7, prt=1)
    invisibilitycloak = dict(name="Invisibility Cloak",    value=25500, shop=True,  weight=1, stl=8)
    invisibilitycloak2 = dict(name="Invisibility Cloak +", value=28050, shop=False, weight=2, stl=8, prt=1)

    silkcloak = dict(name="Silk Cloak",                    value=2500,  shop=True,  weight=1, thf=1)
    silkcloak2 = dict(name="Silk Cloak +",                 value=2750,  shop=False, weight=2, thf=1, prt=1)
    thievescloak = dict(name="Thieves Cloak",              value=5000,  shop=True,  weight=1, thf=2)
    thievescloak2 = dict(name="Thieves Cloak +",           value=5500,  shop=False, weight=2, thf=2, prt=1)

    @staticmethod
    def factory(cloak):
        """
        Maak een object van een enum database item.
        :param cloak: een bovenstaand enum item
        :return: een gearitem object met attributen uit de bovenstaande enum dict
        """
        return items.gear.GearItem(items.gear.GearType.cloak, **cloak.value)
