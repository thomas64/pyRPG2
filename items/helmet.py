
"""
class: HelmetsData
class: Helmet
"""

import enum


class HelmetsData(enum.Enum):
    """
    Hier staan alle helmen uit het spel in als enum met een dict voor de waarden.
    """
    emptyhelmet = dict(name="Empty Helmet",               value=0,     shop=False, weight=0, prt=0)

    leathercap = dict(name="Leather Cap",                 value=100,   shop=True,  weight=1, prt=1)
    bronzehelmet = dict(name="Bronze Helmet",             value=1225,  shop=True,  weight=2, prt=2)
    ironhelmet = dict(name="Iron Helmet",                 value=3600,  shop=True,  weight=3, prt=3)
    steelhelmet = dict(name="Steel Helmet",               value=7225,  shop=True,  weight=4, prt=4)
    silverhelmet = dict(name="Silver Helmet",             value=12100, shop=True,  weight=5, prt=5)
    titaniumhelmet = dict(name="Titanium Helmet",         value=24300, shop=False, weight=1, prt=5)

    helmofknowledge = dict(name="Helm of Knowledge",      value=5500,  shop=True,  weight=2, prt=1, intell=2)
    helmofknowledge2 = dict(name="Helm of Knowledge +",   value=6050,  shop=False, weight=3, prt=2, intell=2)
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

    # ik wil bij de regel "if 'intell' not in helmet" niet helmet.value hoeven te gebruiken.
    def __contains__(self, dict_key):               # dict_key is intell of wil of war etc
        return dict_key in self.value               # self.value is de dict achter het = teken

    # dit is voor bijvoorbeeld "HelmetsData.emptyhelmet['name']" te kunnen doen.
    def __getitem__(self, dict_key):
        return self.value[dict_key]                 # self.value is de dict achter het = teken

    def __setitem__(self, dict_key, new_value):     # dict_key is intell of wil of war etc
        self.value[dict_key] = new_value

    @staticmethod
    def add_missing_values():
        """
        De items die bepaalde waarden nog niet hebben worden hier aangevuld.
        """
        for helmet in HelmetsData:
            if 'intell' not in helmet:
                helmet['intell'] = None
            if 'wil' not in helmet:
                helmet['wil'] = None
            if 'dip' not in helmet:
                helmet['dip'] = None
            if 'lor' not in helmet:
                helmet['lor'] = None
            if 'sci' not in helmet:
                helmet['sci'] = None
            if 'war' not in helmet:
                helmet['war'] = None

    @staticmethod
    def factory(helmet):
        """
        ...
        :param helmet:
        :return:
        """
        return Helmet(helmet['name'],
                      helmet['value'],
                      helmet['shop'],
                      helmet['weight'],
                      helmet['prt'],
                      helmet['intell'],
                      helmet['wil'],
                      helmet['dip'],
                      helmet['lor'],
                      helmet['sci'],
                      helmet['war'])

HelmetsData.add_missing_values()


class Helmet(gear):
    """
    ...
    """
    def __init__(self, name, value, shop, weight, prt, intell, wil, dip, lor, sci, war):
        super().__init__(name, value, shop)
        self.WEIGHT = weight
        self.PRT = prt
        self.INT = intell
        self.WIL = wil
        self.DIP = dip
        self.LOR = lor
        self.SCI = sci
        self.WAR = war


piet = HelmetsData.factory(HelmetsData.ironhelmet)
a = 1