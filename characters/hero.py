
"""
class: Hero
"""

import characters.stats
import characters.skills
import characters.spells
from components import MessageBox
from constants import EquipmentType
from constants import SkillType
from constants import StatType
from constants import WeaponType
import containers
import inventoryitems


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
        self.exp = characters.stats.Experience(kwargs['lev'])   # initiele experience berekening

        self.int = characters.stats.Intelligence(kwargs[StatType.int.name])
        self.wil = characters.stats.Willpower(kwargs[StatType.wil.name])
        self.dex = characters.stats.Dexterity(kwargs[StatType.dex.name])
        self.agi = characters.stats.Agility(kwargs[StatType.agi.name])
        self.edu = characters.stats.Endurance(kwargs[StatType.edu.name])
        self.str = characters.stats.Strength(kwargs[StatType.str.name])
        self.sta = characters.stats.Stamina(kwargs[StatType.sta.name])
        self.stats_tuple = (self.int, self.wil, self.dex, self.agi, self.edu, self.str, self.sta)

        self.alc = characters.skills.Alchemist(kwargs[SkillType.alc.name])
        self.dip = characters.skills.Diplomat(kwargs[SkillType.dip.name])
        self.hlr = characters.skills.Healer(kwargs[SkillType.hlr.name])
        self.lor = characters.skills.Loremaster(kwargs[SkillType.lor.name])
        self.mec = characters.skills.Mechanic(kwargs[SkillType.mec.name])
        self.mer = characters.skills.Merchant(kwargs[SkillType.mer.name])
        self.ran = characters.skills.Ranger(kwargs[SkillType.ran.name])
        self.stl = characters.skills.Stealth(kwargs[SkillType.stl.name])
        self.thf = characters.skills.Thief(kwargs[SkillType.thf.name])
        self.trb = characters.skills.Troubadour(kwargs[SkillType.trb.name])
        self.war = characters.skills.Warrior(kwargs[SkillType.war.name])
        self.wiz = characters.skills.Wizard(kwargs[SkillType.wiz.name])
        self.haf = characters.skills.Hafted(kwargs[SkillType.haf.name])
        self.mis = characters.skills.Missile(kwargs[SkillType.mis.name])
        self.pol = characters.skills.Pole(kwargs[SkillType.pol.name])
        self.shd = characters.skills.Shield(kwargs[SkillType.shd.name])
        self.swd = characters.skills.Sword(kwargs[SkillType.swd.name])
        self.thr = characters.skills.Thrown(kwargs[SkillType.thr.name])
        self.skills_tuple = (self.alc, self.dip, self.hlr, self.lor, self.mec, self.mer, self.ran, self.stl, self.thf,
                             self.trb, self.war, self.wiz, self.haf, self.mis, self.pol, self.shd, self.swd, self.thr)

        self.wpn = inventoryitems.factory_empty_equipment_item(EquipmentType.wpn)
        self.sld = inventoryitems.factory_empty_equipment_item(EquipmentType.sld)
        self.hlm = inventoryitems.factory_empty_equipment_item(EquipmentType.hlm)
        self.amu = inventoryitems.factory_empty_equipment_item(EquipmentType.amu)
        self.arm = inventoryitems.factory_empty_equipment_item(EquipmentType.arm)
        self.clk = inventoryitems.factory_empty_equipment_item(EquipmentType.clk)
        self.brc = inventoryitems.factory_empty_equipment_item(EquipmentType.brc)
        self.glv = inventoryitems.factory_empty_equipment_item(EquipmentType.glv)
        self.rng = inventoryitems.factory_empty_equipment_item(EquipmentType.rng)
        self.blt = inventoryitems.factory_empty_equipment_item(EquipmentType.blt)
        self.bts = inventoryitems.factory_empty_equipment_item(EquipmentType.bts)
        self.acy = inventoryitems.factory_empty_equipment_item(EquipmentType.acy)

        # hier kan zeker None ingevuld worden omdat gamestate hierbij zeker weten niet zal pushen een messagebox.
        if kwargs[EquipmentType.wpn.name]:
            self.set_equipment_item(None, inventoryitems.EquipmentItem(**kwargs[EquipmentType.wpn.name].value))
        # kwargs['sld'] moet bestaan om de if te mogen doen.
        # maar de uitkomst moet niet None zijn om aan de voorwaarde te voldoen.
        if kwargs[EquipmentType.sld.name]:
            self.set_equipment_item(None, inventoryitems.EquipmentItem(**kwargs[EquipmentType.sld.name].value))
        if kwargs[EquipmentType.arm.name]:
            self.set_equipment_item(None, inventoryitems.EquipmentItem(**kwargs[EquipmentType.arm.name].value))

        self.scl = containers.School(kwargs['scl'])
        if kwargs.get('spl'):
            for spell_class_name, spell_quantity in kwargs['spl'].items():
                # noinspection PyPep8Naming
                ClassName = getattr(characters.spells, spell_class_name)
                new_spell = ClassName(spell_quantity)
                self.scl.add(new_spell, self.wiz.qty, force=True)

    @property
    def equipment_tuple(self):
        """
        Deze tuple is apart van de andere tuples, omdat bij deze tuples ook echt de attributen kunnen veranderen.
        :return: een tuple met alle equipment
        """
        return (self.wpn, self.sld, self.hlm, self.amu, self.arm, self.clk,
                self.brc, self.glv, self.rng, self.blt, self.bts, self.acy)

    @property
    def cur_hp(self):
        """
        Current HP bestaat uit deze drie waarden. Nieuw: vier waarden: edu kan ook in ext zitten.
        """
        # todo, bij deze cur_hp en ook bij max_hp testen of edu.ext wel goed gaat wanneer er damage en healing is bijv.
        return self.lev.cur + self.sta.cur + self.edu.cur + self.edu.ext

    @property
    def max_hp(self):
        """
        Maximum HP bestaat uit deze drie waarden. Nieuw: vier waarden:
        """
        return self.lev.qty + self.sta.qty + self.edu.qty + self.edu.ext

    @property
    def eqp_wht(self):
        """
        Total Weight
        Loop door alle attributen van de hero heen en return een WHT waarde als hij die kan vinden, anders +0.
        :return: Tel die op en return de totale weight.
        """
        total = 0
        for equipment_item in self.equipment_tuple:
            total += equipment_item.get_value_of(StatType.wht.name)
        return total

    @property
    def eqp_mvp(self):
        """
        Movepoints die van speciale items komen die speciaal movepoints geven.
        :return: Tel die op en return de total mvp
        """
        total = 0
        for equipment_item in self.equipment_tuple:
            total += equipment_item.get_value_of(StatType.mvp.name)
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
        :return: movepoints die je krijgt door je stamina min het gewicht dat je draagt, plus speciale items met mvp.
        """
        total = self.sta_mvp - round(self.eqp_wht / 2) + self.eqp_mvp
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
    def eqp_prt(self):
        """
        Totale protection min shield protection
        :return: zie: def eqp_wht()
        """
        total = 0
        for equipment_item in self.equipment_tuple:
            total += equipment_item.get_value_of(StatType.prt.name)
        total -= self.sld_prt
        return total

    @property
    def sld_prt(self):
        """
        Alleen shield protection.
        """
        return self.sld.get_value_of(StatType.prt.name)

    @property
    def tot_prt(self):
        """
        Totale protection, ook met shield.
        :return: zie: def eqp_wht()
        """
        return self.eqp_prt + self.sld_prt

    @property
    def sld_des(self):
        """
        Wat nu gecomment is, is aangepast. Geen total des maar sld des. Er hoeft helemaal geen total des te zijn?
        """
        # total = 0
        # for equipment_item in self.equipment_tuple:
        #     total += equipment_item.get_value_of('DES')
        # return total
        return self.sld.get_value_of(StatType.des.name)

    @property
    def eqp_hit(self):
        """
        Totale hit min weapon hit
        :return: zie: def eqp_wht()
        """
        total = 0
        for equipment_item in self.equipment_tuple:
            total += equipment_item.get_value_of(StatType.hit.name)
        total -= self.wpn_hit
        return total

    @property
    def wpn_hit(self):
        """
        Alleen weapon hit.
        """
        return self.wpn.get_value_of(StatType.hit.name)

    @property
    def war_hit(self):
        """
        Warrior bonus op wpn hit.
        """
        return self.war.bonus(self.wpn)

    @property
    def tot_hit(self):
        """
        Totale chance to hit: weapon hit + warrior bonus + ander equipment (bracelets)
        """
        return self.wpn_hit + self.war_hit + self.eqp_hit

    @property
    def sub_hit(self):
        """
        Waarschijnlijk alleen voor visuele partyscreen weergave.
        """
        return self.wpn_hit + self.war_hit

    @property
    def wpn_dam(self):
        """
        Wapen Damage
        :return: zie: def eqp_wht()
        """
        # total = 0
        # for equipment_item in self.equipment_tuple:
        #     total += equipment_item.get_value_of(StatType.dam.name)
        # return total
        return self.wpn.get_value_of(StatType.dam.name)

    def get_equipped_item_of_type(self, equipment_type):
        """
        Geeft het item van het meegegeven Enum type wat de hero equipped heeft terug.
        :param equipment_type: Enum EquipmentType, dus bijv. "sld" "Shield".
        :return: ook als het een 'empty' is, geef dan het item
        """
        # uitzondering gemaakt voor sellbox in shop. geef dan alleen maar een bepaald type weapon terug
        if isinstance(equipment_type, WeaponType):
            if self.wpn.get_value_of('SKL') == equipment_type:
                return self.wpn
        else:
            for equipment_item in self.equipment_tuple:
                if equipment_item.TYP == equipment_type:
                    return equipment_item

    def set_equipment_item(self, gamestate, new_equipment_item):
        """
        Nog niet zo netjes opgelost, naar wat ik denk. Hier wordt een nieuw equipment item aan de hero gegeven.
        :param gamestate: self.engine.gamestate uit partydisplay
        :param new_equipment_item: Object van EquipmentItem
        :return: is het equippen gelukt?
        """
        # ga door de waarden van alle attributen van hero heen.
        for key_eqp_item, value_eqp_item in self.__dict__.items():
            # als de attribute van type eqp_item is, (en dat weet hij omdat new_eqp_item ook van type eqp_item is)
            if isinstance(value_eqp_item, type(new_equipment_item)):
                # als de type van het equipment item overeenkomt met het type van de nieuwe equipment item
                if value_eqp_item.TYP == new_equipment_item.TYP:
                    # als de hero het equipment item mag/kan gebruiken:
                    if self.is_able_to_equip(gamestate, new_equipment_item):
                        # stel de gekozen attribute bijv self.bts in op de nieuwe equipment
                        setattr(self, key_eqp_item, new_equipment_item)
                        self.calc_stats()
                        self.calc_skills()
                        return True
        return False

    def is_able_to_equip(self, gamestate, new_equipment_item):
        """
        Hier bekijkt hij of hij het nieuwe equipment item wel mag/kan dragen.
        :param gamestate: self.engine.gamestate uit partydisplay
        :param new_equipment_item: Object van EquipmentItem
        :return: False of True of hij mag/kan
        """
        if not self.has_enough_weapon_skill_to_equip(new_equipment_item):
            text = ["{} doesn't have the skill to equip that {}.".format(
                                                        self.NAM, new_equipment_item.NAM)]
            push_object = MessageBox(gamestate, text)
            gamestate.push(push_object)
            return False
        if new_equipment_item.get_value_of('MIN_INT') > self.int.qty:
            text = ["{} needs {} {} to equip that {}.".format(self.NAM, new_equipment_item.MIN_INT,
                                                              StatType.int.value, new_equipment_item.NAM)]
            push_object = MessageBox(gamestate, text)
            gamestate.push(push_object)
            return False
        if new_equipment_item.get_value_of('MIN_WIL') > self.wil.qty:
            text = ["{} needs {} {} to equip that {}.".format(self.NAM, new_equipment_item.MIN_WIL,
                                                              StatType.wil.value, new_equipment_item.NAM)]
            push_object = MessageBox(gamestate, text)
            gamestate.push(push_object)
            return False
        if new_equipment_item.get_value_of('MIN_DEX') > self.dex.qty:
            text = ["{} needs {} {} to equip that {}.".format(self.NAM, new_equipment_item.MIN_DEX,
                                                              StatType.dex.value, new_equipment_item.NAM)]
            push_object = MessageBox(gamestate, text)
            gamestate.push(push_object)
            return False
        if new_equipment_item.get_value_of('MIN_STR') > self.str.qty:
            text = ["{} needs {} {} to equip that {}.".format(self.NAM, new_equipment_item.MIN_STR,
                                                              StatType.str.value, new_equipment_item.NAM)]
            push_object = MessageBox(gamestate, text)
            gamestate.push(push_object)
            return False
        if new_equipment_item.get_value_of('MIN_WIZ') > abs(self.wiz.qty):
            # die abs() is een hack, -1 wordt 1, en er zijn toch geen items met een min_wiz van 1.
            text = ["{} needs {} {} to equip that {}.".format(self.NAM, new_equipment_item.MIN_WIZ,
                                                              SkillType.wiz.value, new_equipment_item.NAM)]
            push_object = MessageBox(gamestate, text)
            gamestate.push(push_object)
            return False

        if (new_equipment_item.get_value_of('SKL') == WeaponType.mis and
                self.sld.is_not_empty()):
            text = ['{} can not use a bow when a shield is equipped.'.format(self.NAM)]
            push_object = MessageBox(gamestate, text)
            gamestate.push(push_object)
            return False
        elif (new_equipment_item.get_value_of('SKL') == WeaponType.shd and
                self.wpn.get_value_of('SKL') == WeaponType.mis):
            text = ['{} can not use a shield when a bow is equipped.'.format(self.NAM)]
            push_object = MessageBox(gamestate, text)
            gamestate.push(push_object)
            return False

        return True

    def has_enough_weapon_skill_to_equip(self, new_equipment_item):
        """
        Bekijkt welke SKL waarde het equipment item heeft, geef dan de bijbehorende qty van attribute van de hero terug.
        :param new_equipment_item: Object van EquipmentItem
        :return: Als het item geen skl waarde heeft, zoals bijv boots, return True.
        :return: als de qty waarde > 0 return True. Als de waarde 0 of -1 is return False.
        """
        wpn_skl = new_equipment_item.get_value_of('SKL')    # wpn_skl is een Enum van WeaponType
        if wpn_skl == 0:
            return True
        for wpn_typ in WeaponType:    # = Enum WeaponType
            if wpn_skl == wpn_typ:
                attr = getattr(self, wpn_typ.name)
                if attr.qty > 0:
                    return True
        return False

    def calc_stats(self):
        """
        Hier worden voor de 7 hero stats in alle equipment items gekeken en toegevoegd aan extra.
        Dit moet uitgevoerd worden aan het begin van het spel en wanneer een equipment item van
        een hero wordt verwisseld.
        Agility extra wordt op een andere manier gevuld voor een tweede keer, met weight.
        """
        for stat in self.stats_tuple:
            stat.ext = 0
            for equipment_item in self.equipment_tuple:
                stat.ext += equipment_item.get_value_of(stat.RAW)

        self.agi.ext += -round(self.eqp_wht / 3)

    def calc_skills(self):
        """
        Hetzelfde als calc_stats ongeveer, maar dan alles in een keer.
        Ga alle skills langs en ga daarmee alle equipment items langs en voeg die toe aan .ext.
        """
        for skill in self.skills_tuple:
            skill.ext = 0
            for equipment_item in self.equipment_tuple:
                skill.ext += equipment_item.get_value_of(skill.RAW)

            # visueel aanpassen als het negatieve van de item groter is dan de skill van de hero
            if skill.ext < 0 and skill.ext < -skill.qty and skill.positive_quantity():
                skill.ext = -skill.qty
