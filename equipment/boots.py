
"""
class: BootsData
"""

import equipment.equipment

# todo, prijzen nog bepalen

SPRITEPATH = ''


class BootsData(equipment.equipment.GearData):
    """
    Hier staan alle laarzen uit het spel in als enum met een dict voor de waarden.
    """
    leatherboots = dict(nam="Leather Boots",         val=100,  shp=True,  wht=1, prt=1)
    bronzeboots = dict(nam="Bronze Boots",           val=200,  shp=True,  wht=2, prt=2)
    ironboots = dict(nam="Iron Boots",               val=400,  shp=True,  wht=3, prt=3)
    steelboots = dict(nam="Steel Boots",             val=800,  shp=True,  wht=4, prt=4)
    silverboots = dict(nam="Silver Boots",           val=1600, shp=True,  wht=5, prt=5)
    titaniumboots = dict(nam="Titanium Boots",       val=3200, shp=False, wht=1, prt=5)

    bootsofmotion = dict(nam="Boots of Motion",      val=1000, shp=True,  wht=2, prt=1, mvp=1)
    bootsofmotion2 = dict(nam="Boots of Motion +",   val=1100, shp=False, wht=3, prt=2, mvp=1)
    bootsofspeed = dict(nam="Boots of Speed",        val=2000, shp=True,  wht=2, prt=1, mvp=2)
    bootsofspeed2 = dict(nam="Boots of Speed +",     val=2200, shp=False, wht=3, prt=2, mvp=2)
    woodsmansboots = dict(nam="Woodsman's Boots",    val=1000, shp=True,  wht=2, prt=1, ran=1)
    woodsmansboots2 = dict(nam="Woodsman's Boots +", val=1100, shp=False, wht=3, prt=2, ran=1)
    silenceboots = dict(nam="Silence Boots",         val=1000, shp=True,  wht=2, prt=1, stl=1)
    silenceboots2 = dict(nam="Silence Boots +",      val=1100, shp=False, wht=3, prt=2, stl=1)

    @staticmethod
    def factory(boots):
        """
        Maak een object van een enum database item.
        :param boots: een bovenstaand enum item
        :return: een gearitem object met attributen uit de bovenstaande enum dict
        """
        if boots is None:
            return equipment.equipment.GearItem(equipment.equipment.GearType.boots, SPRITEPATH)
        return equipment.equipment.GearItem(equipment.equipment.GearType.boots, SPRITEPATH, **boots.value)
