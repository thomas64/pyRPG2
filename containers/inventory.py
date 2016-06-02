
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
        self.MAX = 99

    def get_all_equipment_items_of_type(self, equipment_type):
        """
        Geeft uit de inventory alle equipment items van een bepaald type op de juiste volgorde terug.
        :param equipment_type: Enum EquipmentType, dus bijv. "sld" "Shield".
        :return: Een lijst met alleen de gewenste equipment items.
        """
        temp_list = []

        for equipment_item in sorted(self.values(), key=lambda xx: xx.SRT):
            if equipment_item.TYP == equipment_type:
                temp_list.append(equipment_item)

        return temp_list

    def contains(self, equipment_item):
        """
        Bekijkt of het item in de inventory zit.
        :param equipment_item: EquipmentItem Object
        """
        if equipment_item.RAW in self:
            return True
        return False

    def add(self, equipment_item, quantity=1, verbose=True):
        """
        Voeg equipment item toe aan de inventory.
        :param equipment_item: EquipmentItem Object
        :param quantity: integer
        :param verbose: als False meegegeven wordt, print dan niets in de console
        """
        if quantity < 1:
            console.error_quantity_less_than_one(quantity)
            raise ValueError
        if equipment_item.RAW in self:
            self[equipment_item.RAW].qty += quantity
            if self[equipment_item.RAW].qty > self.MAX:
                console.container_is_full(self.NAM)  # todo, hij geeft alleen nu nog maar mee, hij doet er nog niets aan
        else:
            # als hij nog niet in de inv dict zit, voeg hem toe.
            self[equipment_item.RAW] = equipment_item
            # equipment_item bestaat uit zichzelf al uit quantity = 1,
            # dus daarom, wanneer hij voor het eerst wordt toegevoegd: + qty - 1
            self[equipment_item.RAW].qty += (quantity - 1)
            if self[equipment_item.RAW].qty > self.MAX:
                console.container_is_full(self.NAM)  # todo, hij geeft alleen nu nog maar mee, hij doet er nog niets aan
        if verbose:
            console.add_item_in_container(quantity, equipment_item.NAM, self.NAM)

    def remove(self, equipment_item, quantity=1, verbose=True):
        """
        Verwijder equipment item uit de inventory.
        :param equipment_item: EquipmentItem Object
        :param quantity: integer
        :param verbose: als False meegegeven wordt, print dan niets in de console
        """
        if equipment_item.RAW not in self:
            console.error_no_equipment_item()
            raise AttributeError
        if quantity < 1:
            console.error_quantity_less_than_one(quantity)
            raise ValueError
        if self[equipment_item.RAW].qty > quantity:
            self[equipment_item.RAW].qty -= quantity
        elif self[equipment_item.RAW].qty == quantity:
            del self[equipment_item.RAW]
        else:
            console.error_quantity_not_enough()
            raise ValueError
        if verbose:
            console.remove_equipment_item(quantity, equipment_item.NAM, self.NAM)
