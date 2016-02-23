
"""
class: Inventory
"""

import collections
import importlib

import console


class Inventory(dict):
    """
    Inventory container.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.NAM = "Inventory"

    def get_sorted_of_type(self, gear_type):
        """
        Geeft uit de inventory alle items van een bepaald type op de juiste volgorde terug.
        gear_type.value[1] en [2] zijn de values van de Enum GearType
        :param gear_type: Enum GearType
        :return: Een gesorteerde dict met alleen de gewenste items.
        """
        temp_dict = collections.OrderedDict()
        module_name = importlib.import_module(gear_type.value[1])
        items_data = getattr(module_name, gear_type.value[2])

        for item in items_data:
            if self.get(item[0]):
                temp_dict[item[0]] = self[item[0]]
        return temp_dict.values()

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
