
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


class HeroData(enum.Enum):
    """
    ...
    """
    alagos = dict(nam="Alagos", spr=PATH+"01s_Alagos.png", fac=PATH+"01f_Alagos.png",
                  lev=1, exp=500, int=18, wil=12, dex=15, agi=15, edu=15, str=15, sta=30,
                  alc=0, dip=0, hlr=0, lor=0, mec=0, mer=0, ran=0, stl=1, thf=0, trb=1, war=3, wiz=1,
                  haf=1, mis=3, pol=0, shd=3, swd=3, thr=0,
                  wpn=items.weapon.WeaponsData.bronzeshortsword,
                  sld=items.shield.ShieldsData.woodenbuckler,
                  hlm=items.helmet.HelmetsData.empty,
                  amu=items.amulet.AmuletsData.empty,
                  arm=items.armor.ArmorsData.lightleatherarmor,
                  clk=items.cloak.CloakData.empty,
                  glv=items.gloves.GlovesData.empty,
                  lrg=items.ring.RingsData.empty,
                  rrg=items.ring.RingsData.empty,
                  blt=items.belt.BeltsData.empty,
                  bts=items.boots.BootsData.empty,
                  acy=items.accessory.AccessoriesData.empty)

    @staticmethod
    def factory(hero):
        """
        Maak een object van een enum database item.
        :param hero: een bovenstaand enum item
        :return: een gearitem object met attributen uit de bovenstaande enum dict
        """
        return Hero(**hero.value)


class Hero(object):
    """
    ...
    """
    def __init__(self, **kwargs):
        self.NAM = kwargs['nam']
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
        self.hlm = items.helmet.HelmetsData.factory(kwargs['hlm'])
        self.amu = items.amulet.AmuletsData.factory(kwargs['amu'])
        self.arm = items.armor.ArmorsData.factory(kwargs['arm'])
        self.clk = items.cloak.CloakData.factory(kwargs['clk'])
        self.glv = items.gloves.GlovesData.factory(kwargs['glv'])
        self.lrg = items.ring.RingsData.factory(kwargs['lrg'])
        self.rrg = items.ring.RingsData.factory(kwargs['rrg'])
        self.blt = items.belt.BeltsData.factory(kwargs['blt'])
        self.bts = items.boots.BootsData.factory(kwargs['bts'])
        self.acy = items.accessory.AccessoriesData.factory(kwargs['acy'])


# piet = HeroData.factory(HeroData.alagos)
# print(piet.NAM)
# print(piet.sld.NAM)
# print(piet.arm.TYP)
# print(piet.acy.NAM)
# quit()
