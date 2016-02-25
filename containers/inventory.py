
"""
class: Inventory
"""

import console


class Inventory(dict):
    """
    Inventory container.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.NAM = "Inventory"

    def get_sorted_of_type(self, equipment_type):
        """
        Geeft uit de inventory alle equipment items van een bepaald type op de juiste volgorde terug.
        :param equipment_type: Enum EquipmentType
        :return: Een lijst met alleen de gewenste equipment items.
        """
        temp_list = []

        for equipment_item in sorted(self.values(), key=lambda xx: xx.SRT):
            if equipment_item.TYP == equipment_type:
                temp_list.append(equipment_item)

        return temp_list

    def add(self, equipment_item, quantity=1, verbose=True):
        """
        Voeg equipment item toe aan de inventory.
        :param equipment_item: EquipmentItem Object
        :param quantity: integer
        :param verbose: als False meegegeven wordt, print dan niets in de console
        """
        if quantity < 1:
            console.quantity_less_than_one()
            return
        if equipment_item.RAW in self:
            self[equipment_item.RAW].qty += quantity
        else:
            # equipment_item bestaat uit zichzelf al uit quantity = 1
            self[equipment_item.RAW] = equipment_item
            # dus daarom, wanneer hij voor het eerst wordt toegevoegd: + qty - 1
            self[equipment_item.RAW].qty += (quantity - 1)
        if verbose:
            console.add_equipment_item(quantity, equipment_item.NAM, self.NAM)
