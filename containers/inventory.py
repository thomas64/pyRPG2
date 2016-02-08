
"""
class: Inventory
"""

import collections

import console


class Inventory(collections.OrderedDict):
    """
    Inventory container.
    """
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.NAM = "Inventory"

    def add(self, gear, quantity=1, verbose=True):
        """
        Voeg gear toe aan de inventory.
        :param gear: GearData Object
        :param quantity: integer
        :param verbose: als False meegegeven wordt, print dan niets in de console
        """
        if quantity < 1:
            console.quantity_less_than_one()
            return
        if gear.RAW in self:
            self[gear.RAW].qty += quantity
        else:
            self[gear.RAW] = gear                       # gear bestaat uit zichzelf al uit quantity = 1
            self[gear.RAW].qty += (quantity - 1)        # dus daarom, wanneer hij voor het eerst wordt toegevoegd: - 1
        if verbose:
            console.add_item(quantity, gear.NAM, self.NAM)
