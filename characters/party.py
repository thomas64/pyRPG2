
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
        :param character: hero object
        :param verbose: als False meegegeven wordt, print dan niets in de console
        """
        if character in self.values():
            console.Output.character_double_join(character.NAM, self.NAM)
        elif len(self) < self.MAX:
            self[character.RAW] = character
            if verbose:
                console.Output.character_join_party(character.NAM, self.NAM)
        else:
            console.Output.character_full_party(self.NAM)

    def remove(self, character):
        """
        Haal heroes weg uit de party
        :param character: hero object
        """
        if character.RAW == 'alagos':
            console.Output.leader_not_leave_party()
        elif character in self.values():
            console.Output.character_leave_party(character.NAM, self.NAM)
            del self[character.RAW]
        else:
            console.Output.character_not_in_party(character.NAM, self.NAM)
