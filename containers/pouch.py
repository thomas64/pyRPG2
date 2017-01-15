
"""
class: Pouch
"""

from console import Console

from .inventory import Inventory


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

    def get_all_resource_items(self):
        """
        Geeft een gesorteerde lijst terug met alleen resources.
        :return:
        """
        sorted_list = sorted(self.values(), key=lambda xx: xx.SRT)
        return [item for item in sorted_list if item.is_resource()]

    def get_quantity(self, pouch_item):
        """
        Geeft het aantal terug van het gevraagde pouch item object.
        :param pouch_item: object
        :return: het aantal of als het item niet bestaat return 0
        """
        if pouch_item.RAW in self:
            return self[pouch_item.RAW].qty
        return 0

    def contains(self, pouch_item, quantity):
        """
        Bekijkt of het item en de quantity in de pouch zitten.
        :param pouch_item: object
        :param quantity: integer
        """
        if pouch_item.RAW in self:
            if self[pouch_item.RAW].qty >= quantity:
                return True
        return False

    # noinspection PyTypeChecker,PyCallByClass
    def add(self, pouch_item, quantity=1, verbose=True):
        """
        Hetzelfde als add van Inventory.
        """
        Inventory.add_i(self, pouch_item, quantity, verbose)

    def remove(self, pouch_item, cost, verbose=True, force=False):
        """
        Verwijdert quantity uit de pouch. Als je iets koopt bijv.
        :param pouch_item:
        :param cost:
        :param verbose:
        :param force: als hij er 0 uit de pouch moet nemen vanwege polymorph, dan zou hij crashen, gebruik force
        om qty 0 uit de pouch te nemen.
        """
        if cost < 1 and force is False:
            Console.error_quantity_less_than_one(cost)
            raise ValueError

        if pouch_item.RAW not in self:
            Console.quantity_not_enough(pouch_item.NAM, cost, 0)
            return False
        elif self[pouch_item.RAW].qty < cost:
            Console.quantity_not_enough(pouch_item.NAM, cost, self[pouch_item.RAW].qty)
            return False
        elif self[pouch_item.RAW].qty == cost and pouch_item.RAW != 'gold':   # goud is de enige uitzondering,
            del self[pouch_item.RAW]                                # die moet in de pouch blijven, ook met 0.
            return True
        else:
            self[pouch_item.RAW].qty -= cost
            if verbose:
                Console.remove_item_from_container(cost, pouch_item.NAM, self.NAM)
            return True
