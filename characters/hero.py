
"""
class: HeroData
"""

import enum

import characters.stats
import characters.skills
import items.weapon
import items.shield
import items.helmet
import items.amulet
import items.armor
import items.cloak
import items.gloves
import items.ring
import items.belt
import items.boots
import items.accessory


PATH = 'resources/sprites/heroes/'


class Hero(object):
    """
    Het Hero object. Alle Enum values worden ingeladen.
    """
    def __init__(self, **kwargs):
        self.NAM = kwargs['nam']
        self.RAW = self.NAM.strip().lower().replace(" ", "")
        self.SPR = kwargs['spr']
        self.FAC = kwargs['fac']

        self.lev = characters.stats.Level(kwargs['lev'])
        self.exp = characters.stats.Experience(kwargs['exp'])

        self.int = characters.stats.Intelligence(kwargs['int'])
        self.wil = characters.stats.Willpower(kwargs['wil'])
        self.dex = characters.stats.Dexterity(kwargs['dex'])
        self.agi = characters.stats.Agility(kwargs['agi'])
        self.edu = characters.stats.Endurance(kwargs['edu'])
        self.str = characters.stats.Strength(kwargs['str'])
        self.sta = characters.stats.Stamina(kwargs['sta'])

        self.alc = characters.skills.Alchemist(kwargs['alc'])
        self.dip = characters.skills.Diplomat(kwargs['dip'])
        self.hlr = characters.skills.Healer(kwargs['hlr'])
        self.lor = characters.skills.Loremaster(kwargs['lor'])
        self.mec = characters.skills.Mechanic(kwargs['mec'])
        self.mer = characters.skills.Merchant(kwargs['mer'])
        self.ran = characters.skills.Ranger(kwargs['ran'])
        self.stl = characters.skills.Stealth(kwargs['stl'])
        self.thf = characters.skills.Thief(kwargs['thf'])
        self.trb = characters.skills.Troubadour(kwargs['trb'])
        self.war = characters.skills.Warrior(kwargs['war'])
        self.wiz = characters.skills.Wizard(kwargs['wiz'])
        self.haf = characters.skills.Hafted(kwargs['haf'])
        self.mis = characters.skills.Missile(kwargs['mis'])
        self.pol = characters.skills.Pole(kwargs['pol'])
        self.shd = characters.skills.Shield(kwargs['shd'])
        self.swd = characters.skills.Sword(kwargs['swd'])
        self.thr = characters.skills.Thrown(kwargs['thr'])

        self.swd = items.weapon.WeaponsData.factory(kwargs['wpn'])
        self.sld = items.shield.ShieldsData.factory(kwargs['sld'])
        self.hlm = items.helmet.HelmetsData.factory(None)
        self.amu = items.amulet.AmuletsData.factory(None)
        self.arm = items.armor.ArmorsData.factory(kwargs['arm'])
        self.clk = items.cloak.CloakData.factory(None)
        self.glv = items.gloves.GlovesData.factory(None)
        self.lrg = items.ring.RingsData.factory(None)
        self.rrg = items.ring.RingsData.factory(None)
        self.blt = items.belt.BeltsData.factory(None)
        self.bts = items.boots.BootsData.factory(None)
        self.acy = items.accessory.AccessoriesData.factory(None)

    @property
    def cur_hp(self):
        """
        ...
        """
        return self.lev.cur + self.sta.cur + self.edu.cur

    @property
    def max_hp(self):
        """
        ...
        """
        return self.lev.qty + self.sta.qty + self.edu.qty


class HeroData(enum.Enum):
    """
    Alle heroes uit het spel als Enum met een dict voor de waarden.
    """
    @staticmethod
    def factory(hero):
        """
        Maak een object van een enum database item.
        :param hero: een onderstaand enum item
        :return: een hero object met attributen uit de onderstaanstaande enum dict
        """
        return Hero(**hero.value)

    alagos = dict(nam="Alagos", spr=PATH+"01s_Alagos.png", fac=PATH+"01f_Alagos.png",
                  lev=1, exp=500, int=18, wil=12, dex=15, agi=15, edu=15, str=15, sta=30,
                  alc=0, dip=0, hlr=0, lor=0, mec=0, mer=0, ran=0, stl=1, thf=0, trb=1, war=3, wiz=1,
                  haf=1, mis=3, pol=0, shd=3, swd=3, thr=0,
                  wpn=items.weapon.WeaponsData.bronzeshortsword, sld=items.shield.ShieldsData.woodenbuckler,
                  arm=items.armor.ArmorsData.lightleatherarmor)
    luana = dict(nam="Luana", spr=PATH+"02s_Luana.png", fac=PATH+"02f_Luana.png",
                 lev=1, exp=500, int=14, wil=10, dex=22, agi=20, edu=10, str=8, sta=20,
                 alc=0, dip=0, hlr=0, lor=0, mec=1, mer=0, ran=0, stl=3, thf=3, trb=0, war=0, wiz=0,
                 haf=-1, mis=-1, pol=0, shd=-1, swd=1, thr=2,
                 wpn=items.weapon.WeaponsData.bronzedagger, sld=None,
                 arm=items.armor.ArmorsData.lightleatherarmor)
    grindan = dict(nam="Grindan", spr=PATH+"03s_Grindan.png", fac=PATH+"03f_Grindan.png",
                   lev=8, exp=102000, int=10, wil=8, dex=25, agi=10, edu=20, str=20, sta=40,
                   alc=-1, dip=0, hlr=0, lor=0, mec=0, mer=0, ran=0, stl=1, thf=-1, trb=0, war=4, wiz=-1,
                   haf=0, mis=-1, pol=0, shd=2, swd=4, thr=2,
                   wpn=items.weapon.WeaponsData.ironlongsword, sld=items.shield.ShieldsData.irontarge,
                   arm=items.armor.ArmorsData.mediumbronzearmor)
    rydalin = dict(nam="Rydalin", spr=PATH+"04s_Rydalin.png", fac=PATH+"04f_Rydalin.png",
                   lev=3, exp=7000, int=22, wil=16, dex=20, agi=15, edu=16, str=10, sta=31,
                   alc=0, dip=0, hlr=0, lor=1, mec=0, mer=1, ran=0, stl=0, thf=0, trb=0, war=0, wiz=4,
                   haf=0, mis=-1, pol=3, shd=0, swd=3, thr=-1,
                   wpn=items.weapon.WeaponsData.bronzestaff, sld=None,
                   arm=items.armor.ArmorsData.mediumleatherarmor)
    codrif = dict(nam="Codrif", spr=PATH+"05s_Codrif.png", fac=PATH+"05f_Codrif.png",
                  lev=2, exp=2500, int=22, wil=18, dex=15, agi=12, edu=15, str=10, sta=20,
                  alc=3, dip=0, hlr=0, lor=2, mec=2, mer=0, ran=0, stl=0, thf=0, trb=0, war=0, wiz=2,
                  haf=-1, mis=-1, pol=0, shd=-1, swd=1, thr=1,
                  wpn=items.weapon.WeaponsData.bronzedagger, sld=None,
                  arm=items.armor.ArmorsData.lightleatherarmor)
    galen = dict(nam="Galen", spr=PATH+"06s_Galen.png", fac=PATH+"06f_Galen.png",
                 lev=4, exp=15000, int=15, wil=15, dex=18, agi=10, edu=20, str=25, sta=40,
                 alc=-1, dip=0, hlr=0, lor=0, mec=0, mer=0, ran=4, stl=3, thf=0, trb=0, war=5, wiz=-1,
                 haf=5, mis=3, pol=0, shd=3, swd=-1, thr=-1,
                 wpn=items.weapon.WeaponsData.ironaxe, sld=items.shield.ShieldsData.irontarge,
                 arm=items.armor.ArmorsData.mediumbronzearmor)
    # name = dict(nam="", spr=PATH+"0s_.png", fac=PATH+"0f_.png",
    #              lev=, exp=, int=, wil=, dex=, agi=, edu=, str=, sta=,
    #              alc=0, dip=0, hlr=0, lor=0, mec=0, mer=0, ran=0, stl=0, thf=0, trb=0, war=0, wiz=0,
    #              haf=0, mis=0, pol=0, shd=0, swd=0, thr=0,
    #              wpn=items.weapon.WeaponsData.empty, sld=items.shield.ShieldsData.empty,
    #              arm=items.armor.ArmorsData.empty)
    # name = dict(nam="", spr=PATH+"0s_.png", fac=PATH+"0f_.png",
    #              lev=, exp=, int=, wil=, dex=, agi=, edu=, str=, sta=,
    #              alc=0, dip=0, hlr=0, lor=0, mec=0, mer=0, ran=0, stl=0, thf=0, trb=0, war=0, wiz=0,
    #              haf=0, mis=0, pol=0, shd=0, swd=0, thr=0,
    #              wpn=items.weapon.WeaponsData.empty, sld=items.shield.ShieldsData.empty,
    #              arm=items.armor.ArmorsData.empty)
    # name = dict(nam="", spr=PATH+"0s_.png", fac=PATH+"0f_.png",
    #              lev=, exp=, int=, wil=, dex=, agi=, edu=, str=, sta=,
    #              alc=0, dip=0, hlr=0, lor=0, mec=0, mer=0, ran=0, stl=0, thf=0, trb=0, war=0, wiz=0,
    #              haf=0, mis=0, pol=0, shd=0, swd=0, thr=0,
    #              wpn=items.weapon.WeaponsData.empty, sld=items.shield.ShieldsData.empty,
    #              arm=items.armor.ArmorsData.empty)
    # name = dict(nam="", spr=PATH+"0s_.png", fac=PATH+"0f_.png",
    #              lev=, exp=, int=, wil=, dex=, agi=, edu=, str=, sta=,
    #              alc=0, dip=0, hlr=0, lor=0, mec=0, mer=0, ran=0, stl=0, thf=0, trb=0, war=0, wiz=0,
    #              haf=0, mis=0, pol=0, shd=0, swd=0, thr=0,
    #              wpn=items.weapon.WeaponsData.empty, sld=items.shield.ShieldsData.empty,
    #              arm=items.armor.ArmorsData.empty)
    # name = dict(nam="", spr=PATH+"0s_.png", fac=PATH+"0f_.png",
    #              lev=, exp=, int=, wil=, dex=, agi=, edu=, str=, sta=,
    #              alc=0, dip=0, hlr=0, lor=0, mec=0, mer=0, ran=0, stl=0, thf=0, trb=0, war=0, wiz=0,
    #              haf=0, mis=0, pol=0, shd=0, swd=0, thr=0,
    #              wpn=items.weapon.WeaponsData.empty, sld=items.shield.ShieldsData.empty,
    #              arm=items.armor.ArmorsData.empty)
    # name = dict(nam="", spr=PATH+"0s_.png", fac=PATH+"0f_.png",
    #              lev=, exp=, int=, wil=, dex=, agi=, edu=, str=, sta=,
    #              alc=0, dip=0, hlr=0, lor=0, mec=0, mer=0, ran=0, stl=0, thf=0, trb=0, war=0, wiz=0,
    #              haf=0, mis=0, pol=0, shd=0, swd=0, thr=0,
    #              wpn=items.weapon.WeaponsData.empty, sld=items.shield.ShieldsData.empty,
    #              arm=items.armor.ArmorsData.empty)
    # name = dict(nam="", spr=PATH+"0s_.png", fac=PATH+"0f_.png",
    #              lev=, exp=, int=, wil=, dex=, agi=, edu=, str=, sta=,
    #              alc=0, dip=0, hlr=0, lor=0, mec=0, mer=0, ran=0, stl=0, thf=0, trb=0, war=0, wiz=0,
    #              haf=0, mis=0, pol=0, shd=0, swd=0, thr=0,
    #              wpn=items.weapon.WeaponsData.empty, sld=items.shield.ShieldsData.empty,
    #              arm=items.armor.ArmorsData.empty)
    # name = dict(nam="", spr=PATH+"0s_.png", fac=PATH+"0f_.png",
    #              lev=, exp=, int=, wil=, dex=, agi=, edu=, str=, sta=,
    #              alc=0, dip=0, hlr=0, lor=0, mec=0, mer=0, ran=0, stl=0, thf=0, trb=0, war=0, wiz=0,
    #              haf=0, mis=0, pol=0, shd=0, swd=0, thr=0,
    #              wpn=items.weapon.WeaponsData.empty, sld=items.shield.ShieldsData.empty,
    #              arm=items.armor.ArmorsData.empty)
