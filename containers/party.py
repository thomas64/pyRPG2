
"""
class: Party
"""

import collections

import console


class Party(collections.OrderedDict):
    """
    Party container.
    """
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.NAM = "Party"
        self.MAX = 5

    def contains(self, hero_raw):
        """
        Bevat de party de opgegeven naam?
        :return: Ja of Nee
        """
        if hero_raw in self:
            return True
        return False

    def add(self, hero, verbose=True):
        """
        Voeg heroes toe aan de party.
        :param hero: Hero Object
        :param verbose: als False meegegeven wordt, print dan niets in de console
        """
        if hero.RAW in self:
            console.error_hero_double_join(hero.NAM, self.NAM)
            raise ValueError
        elif len(self) < self.MAX:
            self[hero.RAW] = hero
            if verbose:
                console.hero_join_party(hero.NAM, self.NAM)
            return True
        else:
            return False

    def remove(self, hero):
        """
        Haal heroes weg uit de party
        :param hero: Hero Object
        """
        if hero.RAW == 'alagos':
            console.error_leader_not_leave_party()
            raise AttributeError
        elif hero.RAW in self:
            del self[hero.RAW]
        else:
            console.error_hero_not_in_party(hero.NAM, self.NAM)
            raise AttributeError

    def get_highest_value_of_skill(self, attr):
        """
        Vraagt een hoogste attribute op van alle Party members en zijn/haar naam.
        :param attr: sting, het opgevraagde attribute, bijvoorbeeld 'thf'.
        :return: de hoogste waarde van het attribute en de bijbehorende hero naam.
        """
        skill_values = []
        hero_names = []
        for member in self.values():
            skill = getattr(member, attr)
            skill_values.append(skill.tot)
            hero_names.append(member.NAM)

        max_value = max(skill_values)
        max_index = skill_values.index(max(skill_values))
        max_hero = hero_names[max_index]

        return max_value, max_hero

    def get_sum_value_of_skill(self, attr):
        """
        Vraagt de opgetelde waarde van een attribute op van alle Party members
        :param attr: sting, het opgevraagde attribute, bijvoorbeeld 'mer'.
        :return: de opgetelde waarde van het attribute.
        """
        sum_skill_values = 0
        for member in self.values():
            skill = getattr(member, attr)
            sum_skill_values += skill.tot
        return sum_skill_values
