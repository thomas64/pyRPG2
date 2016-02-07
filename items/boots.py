
"""
class: BootsData
"""

import items.gear

# todo, prijzen nog bepalen


class BootsData(items.gear.GearData):
    """
    Hier staan alle laarzen uit het spel in als enum met een dict voor de waarden.
    """
    leatherboots = dict(name="Leather Boots",         value=100,  shop=True,  weight=1, prt=1)
    bronzeboots = dict(name="Bronze Boots",           value=200,  shop=True,  weight=2, prt=2)
    ironboots = dict(name="Iron Boots",               value=400,  shop=True,  weight=3, prt=3)
    steelboots = dict(name="Steel Boots",             value=800,  shop=True,  weight=4, prt=4)
    silverboots = dict(name="Silver Boots",           value=1600, shop=True,  weight=5, prt=5)
    titaniumboots = dict(name="Titanium Boots",       value=3200, shop=False, weight=1, prt=5)

    bootsofmotion = dict(name="Boots of Motion",      value=1000, shop=True,  weight=2, prt=1, mvp=1)
    bootsofmotion2 = dict(name="Boots of Motion +",   value=1100, shop=False, weight=3, prt=2, mvp=1)
    bootsofspeed = dict(name="Boots of Speed",        value=2000, shop=True,  weight=2, prt=1, mvp=2)
    bootsofspeed2 = dict(name="Boots of Speed +",     value=2200, shop=False, weight=3, prt=2, mvp=2)
    woodsmansboots = dict(name="Woodsman's Boots",    value=1000, shop=True,  weight=2, prt=1, ran=1)
    woodsmansboots2 = dict(name="Woodsman's Boots +", value=1100, shop=False, weight=3, prt=2, ran=1)
    silenceboots = dict(name="Silence Boots",         value=1000, shop=True,  weight=2, prt=1, stl=1)
    silenceboots2 = dict(name="Silence Boots +",      value=1100, shop=False, weight=3, prt=2, stl=1)

    @staticmethod
    def factory(boots):
        """
        Maak een object van een enum database item.
        :param boots: een bovenstaand enum item
        :return: een gearitem object met attributen uit de bovenstaande enum dict
        """
        return items.gear.GearItem(items.gear.GearType.boots, **boots.value)
