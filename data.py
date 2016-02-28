
"""
class: Data
"""

import collections

import characters
import containers
import equipment


class Data(object):
    """
    Hier is alle gamedata.
    """
    def __init__(self):

        self.heroes = collections.OrderedDict()

        self.heroes['alagos'] = characters.HeroData.factory(characters.HeroData.alagos)
        self.heroes['luana'] = characters.HeroData.factory(characters.HeroData.luana)
        self.heroes['grindan'] = characters.HeroData.factory(characters.HeroData.grindan)
        self.heroes['rydalin'] = characters.HeroData.factory(characters.HeroData.rydalin)
        self.heroes['codrif'] = characters.HeroData.factory(characters.HeroData.codrif)
        self.heroes['galen'] = characters.HeroData.factory(characters.HeroData.galen)

        for hero in self.heroes.values():
            hero.calc_stats()
            hero.calc_skills()

        self.party = containers.Party()

        self.party.add(self.heroes['alagos'], verbose=False)
        self.party.add(self.heroes['alagos'])
        self.party.add(self.heroes['luana'])
        self.party.add(self.heroes['grindan'])
        self.party.add(self.heroes['rydalin'])
        self.party.add(self.heroes['luana'])
        self.party.add(self.heroes['galen'])
        self.party.add(self.heroes['codrif'])
        self.party.remove(self.heroes['alagos'])
        self.party.remove(self.heroes['luana'])
        self.party.add(self.heroes['grindan'])
        self.party.add(self.heroes['rydalin'])
        self.party.add(self.heroes['galen'])
        self.party.add(self.heroes['luana'])

        self.inventory = containers.Inventory()

        weapon1 = equipment.WeaponDatabase.factory('bronzeshortsword')
        weapon2 = equipment.WeaponDatabase.factory('bronzedagger')
        weapon3 = equipment.WeaponDatabase.factory('irondagger')
        weapon4 = equipment.WeaponDatabase.factory('silverdagger')
        weapon5 = equipment.WeaponDatabase.factory('steeldagger')
        boots1 = equipment.BootsDatabase.factory('ironboots')
        boots2 = equipment.BootsDatabase.factory('bootsofmotion')
        boots3 = equipment.BootsDatabase.factory('silenceboots')
        boots4 = equipment.BootsDatabase.factory('titaniumboots')
        shield1 = equipment.ShieldDatabase.factory('silverkite')
        shield2 = equipment.ShieldDatabase.factory('woodentarge')
        shield3 = equipment.ShieldDatabase.factory('bronzescutum')
        shield4 = equipment.ShieldDatabase.factory('ironheater')
        ring1 = equipment.RingDatabase.factory('testring')
        ring2 = equipment.RingDatabase.factory('testring2')

        self.inventory.add(weapon1, 48)
        self.inventory.add(weapon2, 20)
        self.inventory.add(weapon3, 22)
        self.inventory.add(weapon4, 23)
        self.inventory.add(weapon5, 24)
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
        self.inventory.add(ring1, 4)
        self.inventory.add(ring2, 6)

        # todo, hoe bepaal je of een ring aan de linker of rechter hand kan?

        self.heroes['alagos'].set_equipment_item(equipment.BootsDatabase.factory('ironboots'))
        self.heroes['alagos'].set_equipment_item(equipment.BootsDatabase.factory(None))
        self.heroes['alagos'].set_equipment_item(equipment.WeaponDatabase.factory('silverwarbow'))
