
"""
class: HeroData
"""

import enum

import characters.stats
import characters.skills
import console
import equipment


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
        self.stats_tuple = (self.int, self.wil, self.dex, self.agi, self.edu, self.str, self.sta)

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
        self.skills_tuple = (self.alc, self.dip, self.hlr, self.lor, self.mec, self.mer, self.ran, self.stl, self.thf,
                             self.trb, self.war, self.wiz, self.haf, self.mis, self.pol, self.shd, self.swd, self.thr)

        self.wpn = equipment.WeaponDatabase.factory(kwargs['wpn'])
        self.sld = equipment.ShieldDatabase.factory(kwargs['sld'])
        self.hlm = equipment.HelmetDatabase.factory(None)
        self.amu = equipment.AmuletDatabase.factory(None)
        self.arm = equipment.ArmorDatabase.factory(kwargs['arm'])
        self.clk = equipment.CloakDatabase.factory(None)
        self.glv = equipment.GlovesDatabase.factory(None)
        self.lrg = equipment.RingDatabase.factory(None)
        self.rrg = equipment.RingDatabase.factory(None)
        self.blt = equipment.BeltDatabase.factory(None)
        self.bts = equipment.BootsDatabase.factory(None)
        self.acy = equipment.AccessoryDatabase.factory(None)

    @property
    def equipment_tuple(self):
        """
        Deze tuple is apart van de andere tuples, omdat bij deze tuples ook echt de attributen kunnen veranderen.
        :return: een tuple met alle equipment
        """
        return (self.wpn, self.sld, self.hlm, self.amu, self.arm, self.clk,
                self.glv, self.lrg, self.rrg, self.blt, self.bts, self.acy)

    @property
    def cur_hp(self):
        """
        Current HP bestaat uit deze drie waarden.
        """
        return self.lev.cur + self.sta.cur + self.edu.cur

    @property
    def max_hp(self):
        """
        Maximum HP bestaat uit deze drie waarden.
        """
        return self.lev.qty + self.sta.qty + self.edu.qty

    @property
    def tot_wht(self):
        """
        Total Weight
        Loop door alle attributen van de hero heen en return een WHT waarde als hij die kan vinden, anders +0.
        :return: Tel die op en return de totale weight.
        """
        total = 0
        for equipment_item in self.equipment_tuple:
            total += equipment_item.get_value_of('WHT')
        return total

    @property
    def sta_mvp(self):
        """
        Stamina Movepoints
        :return: Iedereen krijgt 5 mvp + je variable stamina waarde / 10.
        """
        return 5 + round(self.sta.cur / 10)

    @property
    def tot_mvp(self):
        """
        Totale movepoints.
        :return: movepoints die je krijgt door je stamina min het gewicht dat je draagt.
        """
        total = self.sta_mvp - round(self.tot_wht / 2)
        if total < 1:
            return 1
        return total

    @property
    def dif_mvp(self):
        """
        Waarschijnlijk alleen voor visuele partyscreen weergave. Totale - stamina mvp
        """
        return self.tot_mvp - self.sta_mvp

    @property
    def prt(self):
        """
        Totale protection min shield protection
        :return: zie: def tot_wht()
        """
        total = 0
        for equipment_item in self.equipment_tuple:
            total += equipment_item.get_value_of('PRT')
        total -= self.sld_prt
        return total

    @property
    def sld_prt(self):
        """
        Alleen shield protection.
        """
        return self.sld.get_value_of('PRT')

    @property
    def tot_prt(self):
        """
        Totale protection, ook met shield.
        :return: zie: def tot_wht()
        """
        total = 0
        for equipment_item in self.equipment_tuple:
            total += equipment_item.get_value_of('PRT')
        return total

    @property
    def tot_des(self):
        """
        Totale Defense
        :return: zie: def tot_wht()
        """
        total = 0
        for equipment_item in self.equipment_tuple:
            total += equipment_item.get_value_of('DES')
        return total

    @property
    def tot_hit(self):
        """
        Totale BaseHit
        :return: zie: def tot_wht()
        """
        total = 0
        for equipment_item in self.equipment_tuple:
            total += equipment_item.get_value_of('HIT')
        return total

    @property
    def tot_dam(self):
        """
        Totale Damage
        :return: zie: def tot_wht()
        """
        total = 0
        for equipment_item in self.equipment_tuple:
            total += equipment_item.get_value_of('DAM')
        return total

    def get_equipped_item_of_type(self, equipment_type):
        """
        Geeft het item van het meegegeven Enum type wat de hero equipped heeft terug.
        :param equipment_type: Enum EquipmentType, dus bijv. ' sld = "Shield" '.
        :return: Als het geen empty is, geef dan het item. Anders None
        """
        # todo, Let op, bij ringen geeft hij er maar 1 terug. Denk ik, nog niet getest.
        # er moet een conversieslag komen oid. van rightring naar ring en andersom.
        for equipment_item in self.equipment_tuple:
            if equipment_item.TYP == equipment_type:
                if equipment_item.is_not_empty():
                    return equipment_item
        return None

    def set_equipment_item(self, new_equipment_item, verbose=True):
        """
        Nog niet zo netjes opgelost, naar wat ik denk. Hier wordt een nieuw equipment item aan de hero gegeven.
        :param new_equipment_item: Object van EquipmentItem
        :param verbose: geef console output if True
        """
        # ga door de waarden van alle attributen van hero heen.
        for key_eqp_item, value_eqp_item in self.__dict__.items():
            # als de attribute van type eqp_item is, (en dat weet hij omdat new_eqp_item ook van type eqp_item is)
            if isinstance(value_eqp_item, type(new_equipment_item)):
                # als de type van het equipment item overeenkomt met het type van de nieuwe equipment item
                if value_eqp_item.TYP == new_equipment_item.TYP:
                    # als de hero het equipment item mag/kan gebruiken:
                    if self.is_able_to_equip(new_equipment_item):
                        # stel de gekozen attribute bijv self.bts in op de nieuwe equipment
                        setattr(self, key_eqp_item, new_equipment_item)
                        self.calc_stats()
                        self.calc_skills()
                        if verbose:
                            if new_equipment_item.is_not_empty():
                                console.is_equipping(self.NAM, new_equipment_item.NAM)
                            else:
                                console.is_unequipping(self.NAM, value_eqp_item.NAM)

    def is_able_to_equip(self, new_equipment_item):
        """
        Hier bekijkt hij of hij het nieuwe equipment item wel mag/kan dragen.
        :param new_equipment_item: Object van EquipmentItem
        :return: False of True of hij mag/kan
        """
        if self.get_hero_weapon_skill_for_equipment_item(new_equipment_item) < 1:
            console.not_equipping_skill(self.NAM, new_equipment_item.NAM)
            return False
        if new_equipment_item.get_value_of('MIN_INT') > self.int.qty:
            console.not_equipping_min_int(self.NAM, new_equipment_item.NAM, new_equipment_item.MIN_INT)
            return False
        if new_equipment_item.get_value_of('MIN_STR') > self.str.qty:
            console.not_equipping_min_str(self.NAM, new_equipment_item.NAM, new_equipment_item.MIN_STR)
            return False
        return True

    def get_hero_weapon_skill_for_equipment_item(self, new_equipment_item):
        """
        Bekijkt welke SKL waarde het equipment item heeft, geef dan de bijbehorende qty van attribute van de hero terug.
        :param new_equipment_item: Object van EquipmentItem
        :return: of de qty waarde groter is dan 1, of anders 1
        """
        val = new_equipment_item.get_value_of('SKL')    # val is een Enum
        if val == equipment.WeaponType.swd:
            return self.swd.qty                         # return -1, 0 of iets groters dan dat
        elif val == equipment.WeaponType.haf:
            return self.haf.qty
        elif val == equipment.WeaponType.pol:
            return self.pol.qty
        elif val == equipment.WeaponType.mis:
            return self.mis.qty
        elif val == equipment.WeaponType.thr:
            return self.thr.qty
        elif val == equipment.WeaponType.shd:
            return self.shd.qty
        else:
            return 1

    def calc_stats(self):
        """
        Hier worden voor de 7 hero stats in alle equipment items gekeken en toegevoegd aan extra.
        En uiteindelijk ook aan total. Dit moet uitgevoerd worden aan het begin van het spel en
        wanneer een equipment item van een hero wordt verwisseld.
        Agility extra wordt op een andere manier gevuld voor een tweede keer, met weight. De eerste keer is
        soort van nutteloos.
        """
        for stat in self.stats_tuple:
            stat.ext = 0
            for equipment_item in self.equipment_tuple:
                stat.ext += equipment_item.get_value_of(stat.RAW)

        self.agi.ext = -round(self.tot_wht / 3)

        for stat in self.stats_tuple:
            stat.tot = stat.qty + stat.ext
            if stat.tot < 1:  # het origineel uit vb.net is < 0, klopt dat?
                stat.tot = 1

    def calc_skills(self):
        """
        Hetzelfde als calc_stats ongeveer, maar dan alles in een keer.
        Ga alle skills langs en ga daarmee alle equipment items langs en voeg die toe aan .ext.
        Ext en qty vormen samen totaal.
        """
        for skill in self.skills_tuple:
            skill.ext = 0
            for equipment_item in self.equipment_tuple:
                skill.ext += equipment_item.get_value_of(skill.RAW)
            skill.tot = skill.qty + skill.ext
            if skill.tot < 0 or skill.qty <= 0:
                skill.tot = 0
            # visueel aanpassen als het negatieve van de item groter is dan de skill van de hero
            if skill.ext < 0 and skill.ext < -skill.qty and skill.positive_quantity:
                skill.ext = -skill.qty


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

    # todo, alle hero data toevoegen

    alagos = dict(nam="Alagos", spr=PATH+"01s_Alagos.png", fac=PATH+"01f_Alagos.png",
                  lev=1, exp=500, int=18, wil=12, dex=15, agi=15, edu=15, str=15, sta=30,
                  alc=0, dip=0, hlr=0, lor=0, mec=0, mer=0, ran=0, stl=1, thf=0, trb=1, war=3, wiz=1,
                  haf=1, mis=3, pol=0, shd=3, swd=3, thr=0,
                  wpn='bronzeshortsword', sld='woodenbuckler', arm='lightleatherarmor')
    luana = dict(nam="Luana", spr=PATH+"02s_Luana.png", fac=PATH+"02f_Luana.png",
                 lev=1, exp=500, int=14, wil=10, dex=22, agi=20, edu=10, str=8, sta=20,
                 alc=0, dip=0, hlr=0, lor=0, mec=1, mer=0, ran=0, stl=3, thf=3, trb=0, war=0, wiz=0,
                 haf=-1, mis=-1, pol=0, shd=-1, swd=1, thr=2,
                 wpn='bronzedagger', sld=None, arm='lightleatherarmor')
    grindan = dict(nam="Grindan", spr=PATH+"03s_Grindan.png", fac=PATH+"03f_Grindan.png",
                   lev=8, exp=102000, int=10, wil=8, dex=25, agi=10, edu=20, str=20, sta=40,
                   alc=-1, dip=0, hlr=0, lor=0, mec=0, mer=0, ran=0, stl=1, thf=-1, trb=0, war=4, wiz=-1,
                   haf=0, mis=-1, pol=0, shd=2, swd=4, thr=2,
                   wpn='ironlongsword', sld='irontarge', arm='mediumbronzearmor')
    rydalin = dict(nam="Rydalin", spr=PATH+"04s_Rydalin.png", fac=PATH+"04f_Rydalin.png",
                   lev=3, exp=7000, int=22, wil=16, dex=20, agi=15, edu=16, str=10, sta=31,
                   alc=0, dip=0, hlr=0, lor=1, mec=0, mer=1, ran=0, stl=0, thf=0, trb=0, war=0, wiz=4,
                   haf=0, mis=-1, pol=3, shd=0, swd=3, thr=-1,
                   wpn='bronzestaff', sld=None, arm='mediumleatherarmor')
    codrif = dict(nam="Codrif", spr=PATH+"05s_Codrif.png", fac=PATH+"05f_Codrif.png",
                  lev=2, exp=2500, int=22, wil=18, dex=15, agi=12, edu=15, str=10, sta=20,
                  alc=3, dip=0, hlr=0, lor=2, mec=2, mer=0, ran=0, stl=0, thf=0, trb=0, war=0, wiz=2,
                  haf=-1, mis=-1, pol=0, shd=-1, swd=1, thr=1,
                  wpn='bronzedagger', sld=None, arm='lightleatherarmor')
    galen = dict(nam="Galen", spr=PATH+"06s_Galen.png", fac=PATH+"06f_Galen.png",
                 lev=4, exp=15000, int=15, wil=15, dex=18, agi=10, edu=20, str=25, sta=40,
                 alc=-1, dip=0, hlr=0, lor=0, mec=0, mer=0, ran=4, stl=3, thf=0, trb=0, war=5, wiz=-1,
                 haf=5, mis=3, pol=0, shd=3, swd=-1, thr=-1,
                 wpn='ironaxe', sld='irontarge', arm='mediumbronzearmor')
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
