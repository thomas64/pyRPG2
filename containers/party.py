
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
        :param character: HeroData Enum
        :param verbose: als False meegegeven wordt, print dan niets in de console
        """
        if character in self.values():
            console.character_double_join(character.value.NAM, self.NAM)
        elif len(self) < self.MAX:
            self[character.name] = character
            if verbose:
                console.character_join_party(character.value.NAM, self.NAM)
        else:
            console.character_full_party(self.NAM)

    def remove(self, character):
        """
        Haal heroes weg uit de party
        :param character: HeroData Enum
        """
        if character.name == 'alagos':
            console.leader_not_leave_party()
        elif character in self.values():
            console.character_leave_party(character.value.NAM, self.NAM)
            del self[character.name]
        else:
            console.character_not_in_party(character.value.NAM, self.NAM)
