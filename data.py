
"""
class: Data
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
    Hier is alle gamedata.
    """
    def __init__(self):
        self.heroes = characters.hero.HeroData

        self.party = containers.party.Party()
        self.party.add(self.heroes.alagos, verbose=False)

        self.inventory = containers.inventory.Inventory()

        # piet1 = items.weapon.WeaponsData.factory(items.weapon.WeaponsData.bronzeshortsword)
        # piet2 = items.shield.ShieldsData.factory(items.shield.ShieldsData.silverkite)
        # piet3 = items.boots.BootsData.factory(items.boots.BootsData.ironboots)
        #
        # self.inventory.add(piet1, 20)
        # self.inventory.add(piet2, 9)
        # self.inventory.add(piet3, 48)
        # self.inventory.add(piet2, 0)
        # self.inventory.add(piet2, -1)
        # self.inventory.add(piet2, 1)
        #
        # print(self.inventory)
        # quit()
