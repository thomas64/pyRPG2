
"""
class: HelmetsData
"""

import equipment.equipment

# todo, wizard hat stats nog aanpassen, vooral betreffende protection en weight

SPRITEPATH = ''


class HelmetsData(equipment.equipment.GearData):
    """
    Hier staan alle helmen uit het spel in als enum met een dict voor de waarden.
    """
    leathercap = dict(nam="Leather Cap",               val=100,   shp=True,  wht=1, prt=1)
    bronzehelmet = dict(nam="Bronze Helmet",           val=1225,  shp=True,  wht=2, prt=2)
    ironhelmet = dict(nam="Iron Helmet",               val=3600,  shp=True,  wht=3, prt=3)
    steelhelmet = dict(nam="Steel Helmet",             val=7225,  shp=True,  wht=4, prt=4)
    silverhelmet = dict(nam="Silver Helmet",           val=12100, shp=True,  wht=5, prt=5)
    titaniumhelmet = dict(nam="Titanium Helmet",       val=24300, shp=False, wht=1, prt=5)

    helmofknowledge = dict(nam="Helm of Knowledge",    val=5500,  shp=True,  wht=2, prt=1, int=2)
    helmofknowledge2 = dict(nam="Helm of Knowledge +", val=6050,  shp=False, wht=3, prt=2, int=2)
    helmofwisdom = dict(nam="Helm of Wisdom",          val=5500,  shp=True,  wht=2, prt=1, wil=2)
    helmofwisdom2 = dict(nam="Helm of Wisdom +",       val=6050,  shp=False, wht=3, prt=2, wil=2)
    helmofcharisma = dict(nam="Helm of Charisma",      val=6600,  shp=True,  wht=2, prt=1, dip=1)
    helmofcharisma2 = dict(nam="Helm of Charisma +",   val=7260,  shp=False, wht=3, prt=2, dip=1)
    helmofinsight = dict(nam="Helm of Insight",        val=7700,  shp=True,  wht=2, prt=1, lor=1)
    helmofinsight2 = dict(nam="Helm of Insight +",     val=8470,  shp=False, wht=3, prt=2, lor=1)
    helmoftempests = dict(nam="Helm of Tempests",      val=8800,  shp=True,  wht=2, prt=1, war=1)
    helmoftempests2 = dict(nam="Helm of Tempests +",   val=9680,  shp=False, wht=3, prt=2, war=1)

    wizardhat = dict(nam="Wizard Hat",                 val=9900,  shp=True,  wht=2, prt=1, wiz=1)
    wizardhat2 = dict(nam="Wizard Hat +",              val=10890, shp=False, wht=3, prt=2, wiz=1)

    @staticmethod
    def factory(helmet):
        """
        Maak een object van een enum database item.
        :param helmet: een bovenstaand enum item
        :return: een gearitem object met attributen uit de bovenstaande enum dict
        """
        if helmet is None:
            return equipment.equipment.GearItem(equipment.equipment.GearType.helmet, SPRITEPATH)
        return equipment.equipment.GearItem(equipment.equipment.GearType.helmet, SPRITEPATH, **helmet.value)
