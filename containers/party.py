
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

    def add(self, character, verbose=True):
        """
        Voeg heroes toe aan de party.
        :param character: HeroData Object
        :param verbose: als False meegegeven wordt, print dan niets in de console
        """
        if character.RAW in self:
            console.character_double_join(character.NAM, self.NAM)
        elif len(self) < self.MAX:
            self[character.RAW] = character
            if verbose:
                console.character_join_party(character.NAM, self.NAM)
        else:
            console.character_full_party(self.NAM)

    def remove(self, character):
        """
        Haal heroes weg uit de party
        :param character: HeroData Object
        """
        if character.RAW == 'alagos':
            console.leader_not_leave_party()
        elif character.RAW in self:
            console.character_leave_party(character.NAM, self.NAM)
            del self[character.RAW]
        else:
            console.character_not_in_party(character.NAM, self.NAM)
