
"""
...
"""

import characters.hero
import items.weapon
import items.shield
import items.helmet
import items.amulet
import items.armor
import items.cloak
import items.gloves
import items.ring
import items.belt
import items.boots
import items.accessory
import containers.party
import containers.inventory


class Data(object):
    """
    ...
    """
    def __init__(self):
        self.heroes = characters.hero.HeroData

        self.party = containers.party.Party()
        self.party.add(self.heroes.alagos, verbose=False)

        # todo, poging tot gear zijn nog geen objecten in inventory.
        # ze worden pas een object wanneer een hero de gear equiped.
        # ook kijken of de de ordereddict kan converteren naar een enum.
        # de quantity is ook nog een probleem.
        self.inventory = containers.inventory.Inventory()
        self.inventory.add(items.boots.BootsData.ironboots, 48)
        self.inventory.add(items.weapon.WeaponsData.bronzeshortsword, 20)
        self.inventory.add(items.shield.ShieldsData.silverkit, 9)

        print(self.inventory)
