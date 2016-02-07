
"""
class: HelmetsData
"""

import enum

import items.gear


class HelmetsData(enum.Enum):
    """
    Hier staan alle helmen uit het spel in als enum met een dict voor de waarden.
    """
    leathercap = dict(name="Leather Cap",                 value=100,   shop=True,  weight=1, prt=1)
    bronzehelmet = dict(name="Bronze Helmet",             value=1225,  shop=True,  weight=2, prt=2)
    ironhelmet = dict(name="Iron Helmet",                 value=3600,  shop=True,  weight=3, prt=3)
    steelhelmet = dict(name="Steel Helmet",               value=7225,  shop=True,  weight=4, prt=4)
    silverhelmet = dict(name="Silver Helmet",             value=12100, shop=True,  weight=5, prt=5)
    titaniumhelmet = dict(name="Titanium Helmet",         value=24300, shop=False, weight=1, prt=5)

    helmofknowledge = dict(name="Helm of Knowledge",      value=5500,  shop=True,  weight=2, prt=1, int=2)
    helmofknowledge2 = dict(name="Helm of Knowledge +",   value=6050,  shop=False, weight=3, prt=2, int=2)
    helmofwisdom = dict(name="Helm of Wisdom",            value=5500,  shop=True,  weight=2, prt=1, wil=2)
    helmofwisdom2 = dict(name="Helm of Wisdom +",         value=6050,  shop=False, weight=3, prt=2, wil=2)
    helmofcharisma = dict(name="Helm of Charisma",        value=6600,  shop=True,  weight=2, prt=1, dip=1)
    helmofcharisma2 = dict(name="Helm of Charisma +",     value=7260,  shop=False, weight=3, prt=2, dip=1)
    helmofinsight = dict(name="Helm of Insight",          value=7700,  shop=True,  weight=2, prt=1, lor=1)
    helmofinsight2 = dict(name="Helm of Insight +",       value=8470,  shop=False, weight=3, prt=2, lor=1)
    helmofcognizance = dict(name="Helm of Cognizance",    value=9900,  shop=True,  weight=2, prt=1, sci=1)
    helmofcognizance2 = dict(name="Helm of Cognizance +", value=10890, shop=False, weight=3, prt=2, sci=1)
    helmoftempests = dict(name="Helm of Tempests",        value=8800,  shop=True,  weight=2, prt=1, war=1)
    helmoftempests2 = dict(name="Helm of Tempests +",     value=9680,  shop=False, weight=3, prt=2, war=1)

    def __getitem__(self, item):        # als er iets wordt gevraagd wat niet kan aan een enum, zoals [0] of [1]
        if item == 0:                   # voor een OrderedDict (zoals ShieldsData) dan wordt deze uitgevoerd.
            return self.name            # hij returned dan een waarde die een enum wel kan, namelijk .name en .value
        elif item == 1:
            return self.value

    @staticmethod
    def factory(helmet):
        """
        Maak een object van een enum database item.
        :param helmet: een bovenstaand enum item
        :return: een gearitem object met attributen uit de bovenstaande enum dict
        """
        return items.gear.GearItem(items.gear.GearType.helmet, **helmet.value)


# for helmet in HelmetsData:
#     print(helmet[1]['name'])
#
# quit()
