
"""
class: Data
"""

import collections

import characters.hero
import containers.party
import containers.inventory
import equipment


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

        weapon1 = equipment.WeaponDatabase.factory('bronzeshortsword')
        weapon2 = equipment.WeaponDatabase.factory('bronzedagger')
        boots1 = equipment.BootsDatabase.factory('ironboots')
        boots2 = equipment.BootsDatabase.factory('bootsofmotion')
        boots3 = equipment.BootsDatabase.factory('silenceboots')
        boots4 = equipment.BootsDatabase.factory('titaniumboots')
        shield1 = equipment.ShieldDatabase.factory('silverkite')
        shield2 = equipment.ShieldDatabase.factory('woodentarge')
        shield3 = equipment.ShieldDatabase.factory('bronzescutum')
        shield4 = equipment.ShieldDatabase.factory('ironheater')

        self.inventory.add(weapon1, 48)
        self.inventory.add(weapon2, 20)
        self.inventory.add(boots1, 25)
        self.inventory.add(boots2, 26)
        self.inventory.add(boots3, 27)
        self.inventory.add(boots4, 22)
        self.inventory.add(shield1, 23)
        self.inventory.add(shield2, 21)
        self.inventory.add(shield3, 9)
        self.inventory.add(shield4, 3)
        self.inventory.add(shield4, 0)
        self.inventory.add(shield4, -1)
        self.inventory.add(shield4, 1)

        # print(self.inventory)

        # for boot in items.shield.ShieldsData:
        #     print(boot[0])

        # quit()
