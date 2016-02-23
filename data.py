
"""
class: Data
"""

import collections

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
        self.heroes = collections.OrderedDict()

        self.heroes['alagos'] = characters.hero.HeroData.factory(characters.hero.HeroData.alagos)
        self.heroes['luana'] = characters.hero.HeroData.factory(characters.hero.HeroData.luana)
        self.heroes['grindan'] = characters.hero.HeroData.factory(characters.hero.HeroData.grindan)
        self.heroes['rydalin'] = characters.hero.HeroData.factory(characters.hero.HeroData.rydalin)
        self.heroes['codrif'] = characters.hero.HeroData.factory(characters.hero.HeroData.codrif)
        self.heroes['galen'] = characters.hero.HeroData.factory(characters.hero.HeroData.galen)

        for hero in self.heroes.values():
            hero.calc_stats()
            hero.calc_skills()

        self.party = containers.party.Party()
        self.party.add(self.heroes['alagos'], verbose=False)
        # self.party.add(self.heroes['alagos'])
        self.party.add(self.heroes['luana'])
        self.party.add(self.heroes['grindan'])
        self.party.add(self.heroes['rydalin'])
        # self.party.add(self.heroes['luana'])
        self.party.add(self.heroes['galen'])
        self.party.add(self.heroes['codrif'])
        # self.party.remove(self.heroes['alagos'])
        # self.party.remove(self.heroes['luana'])
        self.party.add(self.heroes['grindan'])
        self.party.add(self.heroes['rydalin'])
        self.party.add(self.heroes['galen'])

        self.inventory = containers.inventory.Inventory()

        piet1 = items.weapon.WeaponsData.factory(items.weapon.WeaponsData.bronzeshortsword)
        piet2 = items.shield.ShieldsData.factory(items.shield.ShieldsData.silverkite)
        piet3 = items.boots.BootsData.factory(items.boots.BootsData.ironboots)
        piet4 = items.boots.BootsData.factory(items.boots.BootsData.bootsofmotion)
        piet5 = items.boots.BootsData.factory(items.boots.BootsData.silenceboots)
        piet6 = items.boots.BootsData.factory(items.boots.BootsData.titaniumboots)
        piet7 = items.weapon.WeaponsData.factory(items.weapon.WeaponsData.bronzedagger)
        piet8 = items.shield.ShieldsData.factory(items.shield.ShieldsData.woodentarge)
        piet9 = items.shield.ShieldsData.factory(items.shield.ShieldsData.bronzescutum)
        piet10 = items.shield.ShieldsData.factory(items.shield.ShieldsData.ironheater)

        self.inventory.add(piet3, 48)
        self.inventory.add(piet1, 20)
        self.inventory.add(piet10, 25)
        self.inventory.add(piet5, 26)
        self.inventory.add(piet6, 27)
        self.inventory.add(piet7, 22)
        self.inventory.add(piet8, 23)
        self.inventory.add(piet9, 21)
        self.inventory.add(piet2, 9)
        self.inventory.add(piet4, 3)
        self.inventory.add(piet2, 0)
        self.inventory.add(piet2, -1)
        self.inventory.add(piet2, 1)

        # print(self.inventory)

        # for boot in items.shield.ShieldsData:
        #     print(boot[0])

        # quit()
