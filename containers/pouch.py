
"""
class: Pouch
"""

import console
from pouchitems import PouchItem


# todo, nog niet tevreden, eigenlijk moeten de pouchitems een apart object zijn met een qty attr.
# en met een sprite icon attr, zodat plaatje kan weergegeven worden in messagebox bij openen van chest.

class Pouch(dict):
    """
    Pouch container.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.NAM = "Pouch"
        self.gold = 0
        self.goldmax = 999999
        self.herbs = 0
        self.herbsmax = 99
        self.spices = 0
        self.spicesmax = 99

    def add(self, pouch_item, quantity=1, verbose=True):
        """
        Voeg pouch item toe aan de pouch.
        :param pouch_item: Enum
        :param quantity: integer
        :param verbose: als False meegegeven wordt, print dan niets in de console
        """
        if quantity < 1:
            console.error_quantity_less_than_one(quantity)
            raise ValueError

        if pouch_item == PouchItem.Gold:
            self.gold += quantity
            if self.gold > self.goldmax:
                console.container_is_full(self.NAM)  # todo, hij geeft alleen nu nog maar mee, hij doet er nog niets aan

        elif pouch_item == PouchItem.Herbs:
            self.herbs += quantity
            if self.herbs > self.herbsmax:
                console.container_is_full(self.NAM)

        elif pouch_item == PouchItem.Spices:
            self.spices += quantity
            if self.spices > self.spicesmax:
                console.container_is_full(self.NAM)

        if verbose:
            console.add_item_in_container(quantity, pouch_item.name, self.NAM)

    def remove(self, pouch_item, quantity):
        """
        Verwijdert quantity uit de pouch. Als je iets koopt bijv.
        """
        if quantity < 1:
            console.error_quantity_less_than_one(quantity)
            raise ValueError

        if pouch_item == PouchItem.Gold:
            if self.gold < quantity:
                console.quantity_not_enough(pouch_item.name, quantity, self.gold)
                return False
            else:
                self.gold -= quantity
                return True

        elif pouch_item == PouchItem.Herbs:
            if self.herbs < quantity:
                console.quantity_not_enough(pouch_item.name, quantity, self.herbs)
                return False
            else:
                self.herbs -= quantity
                return True

        elif pouch_item == PouchItem.Spices:
            if self.spices < quantity:
                console.quantity_not_enough(pouch_item.name, quantity, self.spices)
                return False
            else:
                self.spices -= quantity
                return True
