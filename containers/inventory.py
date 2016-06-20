
"""
class: Inventory
"""

import console
from database import WeaponType


class Inventory(list):
    """
    Inventory container.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.NAM = "Inventory"
        self.MAX = 5

    def get_all_equipment_items_of_type(self, equipment_type):
        """
        Geeft uit de inventory alle equipment items van een bepaald type op de juiste volgorde terug.
        :param equipment_type: Enum EquipmentType, dus bijv. "sld" "Shield".
        :return: Een lijst met alleen de gewenste equipment items.
        """
        temp_list = []

        for equipment_item in sorted(self, key=lambda xx: xx.SRT):
            # uitzondering gemaakt voor sellbox in shop. geef dan alleen maar een bepaald type weapon terug
            if isinstance(equipment_type, WeaponType):
                if equipment_item.get_value_of('SKL'):
                    if equipment_item.SKL == equipment_type:
                        temp_list.append(equipment_item)
            else:
                if equipment_item.TYP == equipment_type:
                    temp_list.append(equipment_item)

        return temp_list

    def add_i(self, equipment_item, verbose=True):
        """
        Voeg equipment item toe aan de inventory.
        :param equipment_item: EquipmentItem Object
        :param verbose: als False meegegeven wordt, print dan niets in de console
        """
        if len(self)-1 < self.MAX:
            self.append(equipment_item)
            if verbose:
                console.add_item_in_container(1, equipment_item.NAM, self.NAM)
            return True
        else:
            console.container_is_full(self.NAM)
            return False

    def remove_i(self, equipment_item, verbose=True):
        """
        Verwijder equipment item uit de inventory.
        :param equipment_item: EquipmentItem Object
        :param verbose: als False meegegeven wordt, print dan niets in de console
        """
        if equipment_item not in self:
            console.error_no_equipment_item()
            raise AttributeError
        self.remove(equipment_item)
        if verbose:
            console.remove_item_from_container(1, equipment_item.NAM, self.NAM)
