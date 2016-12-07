
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

    def use(self, hero):
        """
        Lege methode voor overervende children.
        """
        return None, None


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

            hero.edu.cur += healpoints
            if hero.edu.cur > hero.edu.qty:
                healpoints = hero.edu.cur - hero.edu.qty
                hero.edu.cur = hero.edu.qty

                hero.sta.cur += healpoints
                if hero.sta.cur > hero.sta.qty:
                    healpoints = hero.sta.cur - hero.sta.qty
                    hero.sta.cur = hero.sta.qty

                    hero.lev.cur += healpoints
                    if hero.lev.cur > hero.lev.qty:
                        # healpoints = 0
                        hero.lev.cur = hero.lev.qty

            text = ["{} used a {}.".format(hero.NAM, self.NAM)]
            return True, text
        else:
            text = ["A {} cannot be used right now.".format(self.NAM)]
            return False, text
