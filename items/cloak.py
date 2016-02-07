
"""
class: CloaksData
"""

import items.gear


class CloakData(items.gear.GearData):
    """
    Hier staan alle mantels uit het spel in als enum met een dict voor de waarden.
    """
    empty = dict()

    leathercloak = dict(nam="Leather Cloak",              val=100,   shp=True,  wht=1, prt=1)
    battlecloak = dict(nam="Battle Cloak",                val=1000,  shp=True,  wht=2, prt=2)

    covercloak = dict(nam="Cover Cloak",                  val=100,   shp=True,  wht=1, stl=1)
    covercloak2 = dict(nam="Cover Cloak +",               val=110,   shp=False, wht=2, stl=1, prt=1)
    darkcloak = dict(nam="Dark Cloak",                    val=300,   shp=True,  wht=1, stl=2)
    darkcloak2 = dict(nam="Dark Cloak +",                 val=330,   shp=False, wht=2, stl=2, prt=1)
    disguisecloak = dict(nam="Disguise Cloak",            val=700,   shp=True,  wht=1, stl=3)
    disguisecloak2 = dict(nam="Disguise Cloak +",         val=770,   shp=False, wht=2, stl=3, prt=1)
    concealcloak = dict(nam="Conceal Cloak",              val=1500,  shp=True,  wht=1, stl=4)
    concealcloak2 = dict(nam="Conceal Cloak +",           val=1650,  shp=False, wht=2, stl=4, prt=1)
    nightcloak = dict(nam="Night Cloak",                  val=3100,  shp=True,  wht=1, stl=5)
    nightcloak2 = dict(nam="Night Cloak +",               val=3410,  shp=False, wht=2, stl=5, prt=1)
    stealthcloak = dict(nam="Stealth Cloak",              val=6300,  shp=True,  wht=1, stl=6)
    stealthcloak2 = dict(nam="Stealth Cloak +",           val=6930,  shp=False, wht=2, stl=6, prt=1)
    phantomcloak = dict(nam="Phantom Cloak",              val=12700, shp=True,  wht=1, stl=7)
    phantomcloak2 = dict(nam="Phantom Cloak +",           val=13970, shp=False, wht=2, stl=7, prt=1)
    invisibilitycloak = dict(nam="Invisibility Cloak",    val=25500, shp=True,  wht=1, stl=8)
    invisibilitycloak2 = dict(nam="Invisibility Cloak +", val=28050, shp=False, wht=2, stl=8, prt=1)

    silkcloak = dict(nam="Silk Cloak",                    val=2500,  shp=True,  wht=1, thf=1)
    silkcloak2 = dict(nam="Silk Cloak +",                 val=2750,  shp=False, wht=2, thf=1, prt=1)
    thievescloak = dict(nam="Thieves Cloak",              val=5000,  shp=True,  wht=1, thf=2)
    thievescloak2 = dict(nam="Thieves Cloak +",           val=5500,  shp=False, wht=2, thf=2, prt=1)

    @staticmethod
    def factory(cloak):
        """
        Maak een object van een enum database item.
        :param cloak: een bovenstaand enum item
        :return: een gearitem object met attributen uit de bovenstaande enum dict
        """
        return items.gear.GearItem(items.gear.GearType.cloak, **cloak.value)
