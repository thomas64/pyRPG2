
"""
class: Pouch
"""

import console
from . import Inventory


class Pouch(Inventory):
    """
    Pouch container.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.NAM = "Pouch"
        self.MAX = 999999

    def remove(self, pouch_item, quantity=1, verbose=True):
        """
        Verwijdert quantity uit de pouch. Als je iets koopt bijv.
        """
        if quantity < 1:
            console.error_quantity_less_than_one(quantity)
            raise ValueError

        if pouch_item.RAW not in self:
            console.quantity_not_enough(pouch_item.NAM, quantity, pouch_item.qty - 1)
            return False
        elif pouch_item.qty < quantity:
            console.quantity_not_enough(pouch_item.NAM, quantity, pouch_item.qty)
            return False
        elif pouch_item.qty == quantity and pouch_item.RAW != 'gold':   # goud is de enige uitzondering,
            del self[pouch_item.RAW]                                    # die moet in de pouch blijven, ook met 0.
            return True
        else:
            pouch_item.qty -= quantity
            return True
