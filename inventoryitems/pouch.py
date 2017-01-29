
"""
class: PouchItem
"""


class PouchItem(object):
    """
    Maak een PouchItem object vanuit de pouchitem database.
    """
    def __init__(self, **kwargs):
        self.qty = 1

        for eqp_value_key, eqp_value_value in kwargs.items():
            setattr(self, eqp_value_key.upper(), eqp_value_value)  # zet de dict van kwargs om in attributen

        self.RAW = self.NAM.strip().lower().replace(" ", "")  # als er een NAM is, geef hem een RAW

    def show_info(self):
        """
        show_info is polymorph met EquipmentItem()
        :return:
        """
        return self.DESC

    def use(self, *args):
        """
        Voornamelijk methode voor overervende children, maar als er in de CLICK een plaatje staat, beeld die
        dan af met een MessageBox.
        """
        if hasattr(self, 'CLICK'):
            return True, self.CLICK
        else:
            return None, None

    def is_sellable(self):
        """
        Als een PouchItem geen .VAL waarde heeft is hij niet verkoopbaar in winkels.
        :return: True of False
        """
        if hasattr(self, 'VAL'):
            return True
        return False

    def is_resource(self):
        """
        Als de value waarde 1 is, dan is het een resource.
        :return:
        """
        if hasattr(self, 'VAL'):
            if self.VAL == 1:
                return True
        return False


class HealingPotion(PouchItem):
    """
    ...
    """
    def use(self, hero):
        """
        Dezelfde methode, maar nu gevuld met iets.
        """
        if hero.cur_hp < hero.max_hp:
            healpoints = round(hero.max_hp / self.HP)
            hero.recover_part_hp(healpoints)
            text = ["{} used a {}.".format(hero.NAM, self.NAM)]
            return True, text
        else:
            text = ["A {} cannot be used right now.".format(self.NAM)]
            return False, text


class CuringPotion(HealingPotion):
    """
    Is een child van HealingPotion, alleen self.HP is anders.
    Hoeft dus niet eens een child te zijn, maar voor de duidelijkheid in de class name is het wel handig.
    """


class StaminaPotion(PouchItem):
    """..."""
    def use(self, hero):
        """..."""
        if hero.sta.cur < hero.sta.qty:
            hero.recover_full_stamina()
            text = ["{} used a {}.".format(hero.NAM, self.NAM)]
            return True, text
        else:
            text = ["A {} cannot be used right now.".format(self.NAM)]
            return False, text


class RestorePotion(PouchItem):
    """..."""
    def use(self, hero):
        """..."""
        if hero.cur_hp < hero.max_hp:
            hero.recover_full_hp()
            text = ["{} used a {}.".format(hero.NAM, self.NAM)]
            return True, text
        else:
            text = ["A {} cannot be used right now.".format(self.NAM)]
            return False, text
