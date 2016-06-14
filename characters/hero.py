
"""
class: Hero
"""

import characters.stats
import characters.skills
import components
import database
import equipment


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

        self.wpn = equipment.factory_empty_equipment_item(database.EquipmentType.wpn)
        self.sld = equipment.factory_empty_equipment_item(database.EquipmentType.sld)
        self.hlm = equipment.factory_empty_equipment_item(database.EquipmentType.hlm)
        self.amu = equipment.factory_empty_equipment_item(database.EquipmentType.amu)
        self.arm = equipment.factory_empty_equipment_item(database.EquipmentType.arm)
        self.clk = equipment.factory_empty_equipment_item(database.EquipmentType.clk)
        self.brc = equipment.factory_empty_equipment_item(database.EquipmentType.brc)
        self.glv = equipment.factory_empty_equipment_item(database.EquipmentType.glv)
        self.rng = equipment.factory_empty_equipment_item(database.EquipmentType.rng)
        self.blt = equipment.factory_empty_equipment_item(database.EquipmentType.blt)
        self.bts = equipment.factory_empty_equipment_item(database.EquipmentType.bts)
        self.acy = equipment.factory_empty_equipment_item(database.EquipmentType.acy)

        # hier kan zeker None ingevuld worden omdat gamestate hierbij zeker weten niet zal pushen een messagebox.
        if kwargs['wpn']:
            self.set_equipment_item(None, equipment.factory_equipment_item(kwargs['wpn']))
        if kwargs['sld']:
            self.set_equipment_item(None, equipment.factory_equipment_item(kwargs['sld']))
        if kwargs['arm']:
            self.set_equipment_item(None, equipment.factory_equipment_item(kwargs['arm']))

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
    def sld_des(self):
        """
        Wat nu gecomment is, is aangepast. Geen total des maar sld des. Er hoeft helemaal geen total des te zijn?
        """
        # total = 0
        # for equipment_item in self.equipment_tuple:
        #     total += equipment_item.get_value_of('DES')
        # return total
        return self.sld.get_value_of('DES')

    @property
    def wpn_hit(self):
        """
        Wat nu gecomment is, is aangepast. Geen total hit maar wpn hit. Er hoeft helemaal geen total hit te zijn?
        """
        # total = 0
        # for equipment_item in self.equipment_tuple:
        #     total += equipment_item.get_value_of('HIT')
        # return total
        return self.wpn.get_value_of('HIT')

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
        :param equipment_type: Enum EquipmentType, dus bijv. "sld" "Shield".
        :return: ook als het een 'empty' is, geef dan het item
        """
        # uitzondering gemaakt voor sellbox in shop. geef dan alleen maar een bepaald type weapon terug
        if isinstance(equipment_type, database.WeaponType):
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
            push_object = components.MessageBox(gamestate, text)
            gamestate.push(push_object)
            return False
        if new_equipment_item.get_value_of('MIN_INT') > self.int.qty:
            text = ["{} needs {} intelligence to equip that {}.".format(
                                                        self.NAM, new_equipment_item.MIN_INT, new_equipment_item.NAM)]
            push_object = components.MessageBox(gamestate, text)
            gamestate.push(push_object)
            return False
        if new_equipment_item.get_value_of('MIN_STR') > self.str.qty:
            text = ["{} needs {} strength to equip that {}.".format(
                                                        self.NAM, new_equipment_item.MIN_STR, new_equipment_item.NAM)]
            push_object = components.MessageBox(gamestate, text)
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
        for wpn_typ in database.WeaponType:    # = Enum WeaponType
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
        Agility extra wordt op een andere manier gevuld voor een tweede keer, met weight. De eerste keer is
        soort van nutteloos.
        """
        for stat in self.stats_tuple:
            stat.ext = 0
            for equipment_item in self.equipment_tuple:
                stat.ext += equipment_item.get_value_of(stat.RAW)

        self.agi.ext = -round(self.tot_wht / 3)

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
