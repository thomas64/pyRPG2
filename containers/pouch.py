
"""
class: Pouch
"""

import console


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

    def add(self, pouch_item, quantity=1, verbose=True):
        """
        Voeg equipment item toe aan de inventory.
        :param pouch_item: PouchItem Object
        :param quantity: integer
        :param verbose: als False meegegeven wordt, print dan niets in de console
        """
        if quantity < 1:
            console.error_quantity_less_than_one(quantity)
            raise ValueError
        if pouch_item.RAW in self:
            self[pouch_item.RAW].qty += quantity
            if self[pouch_item.RAW].qty > self.MAX:
                console.container_is_full(self.NAM)  # todo, hij geeft alleen nu nog maar mee, hij doet er nog niets aan
        else:
            # als hij nog niet in de inv dict zit, voeg hem toe.
            self[pouch_item.RAW] = pouch_item
            # equipment_item bestaat uit zichzelf al uit quantity = 1,
            # dus daarom, wanneer hij voor het eerst wordt toegevoegd: + qty - 1
            self[pouch_item.RAW].qty += (quantity - 1)
            if self[pouch_item.RAW].qty > self.MAX:
                console.container_is_full(self.NAM)  # todo, hij geeft alleen nu nog maar mee, hij doet er nog niets aan
        if verbose:
            console.add_item_in_container(quantity, pouch_item.NAM, self.NAM)

    def remove(self, pouch_item, cost, verbose=True):
        """
        Verwijdert quantity uit de pouch. Als je iets koopt bijv.
        """
        if cost < 1:
            console.error_quantity_less_than_one(cost)
            raise ValueError

        if pouch_item.RAW not in self:
            console.quantity_not_enough(pouch_item.NAM, cost, 0)
            return False
        elif self[pouch_item.RAW].qty < cost:
            console.quantity_not_enough(pouch_item.NAM, cost, self[pouch_item.RAW].qty)
            return False
        elif self[pouch_item.RAW].qty == cost and pouch_item.RAW != 'gold':   # goud is de enige uitzondering,
            del self[pouch_item.RAW]                                # die moet in de pouch blijven, ook met 0.
            return True
        else:
            self[pouch_item.RAW].qty -= cost
            if verbose:
                console.remove_item_from_container(cost, pouch_item.NAM, self.NAM)
            return True
