
"""
class: Pouch
"""

import console
from . import Inventory


class Pouch(dict):
    """
    Pouch container.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.NAM = "Pouch"
        self.MAX = 999999

    def get_all_pouch_items(self):
        """
        Geeft een gesorteerde lijst terug.
        """
        return sorted(self.values(), key=lambda xx: xx.SRT)

    # noinspection PyTypeChecker,PyCallByClass
    def add(self, pouch_item, quantity=1, verbose=True):
        """
        Hetzelfde als add van Inventory.
        """
        Inventory.add(self, pouch_item, quantity, verbose)

    def remove(self, pouch_item, cost):
        """
        Verwijdert quantity uit de pouch. Als je iets koopt bijv.
        """
        if cost < 1:
            console.error_quantity_less_than_one(cost)
            raise ValueError

        if pouch_item.RAW not in self:
            console.quantity_not_enough(pouch_item.NAM, cost, pouch_item.qty - 1)
            return False
        elif pouch_item.qty < cost:
            console.quantity_not_enough(pouch_item.NAM, cost, pouch_item.qty)
            return False
        elif pouch_item.qty == cost and pouch_item.RAW != 'gold':   # goud is de enige uitzondering,
            del self[pouch_item.RAW]                                # die moet in de pouch blijven, ook met 0.
            return True
        else:
            pouch_item.qty -= cost
            return True
