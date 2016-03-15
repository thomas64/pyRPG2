
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
        else:
            console.container_is_full(self.NAM)

    def remove(self, hero, verbose=True):
        """
        Haal heroes weg uit de party
        :param hero: Hero Object
        :param verbose: als False meegegeven wordt, print dan niets in de console
        """
        if hero.RAW == 'alagos':
            console.leader_not_leave_party()
        elif hero.RAW in self:
            del self[hero.RAW]
            if verbose:
                console.hero_leave_party(hero.NAM, self.NAM)
        else:
            console.error_hero_not_in_party(hero.NAM, self.NAM)
            raise AttributeError
