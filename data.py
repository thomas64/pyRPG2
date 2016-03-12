
"""
class: Data
"""

import collections
import random

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
        self.party.add(self.heroes['alagos'], verbose=False)
        self.party.add(self.heroes['luana'], verbose=False)
        self.party.add(self.heroes['grindan'], verbose=False)
        self.party.add(self.heroes['rydalin'], verbose=False)
        self.party.add(self.heroes['luana'], verbose=False)
        self.party.add(self.heroes['galen'], verbose=False)
        self.party.add(self.heroes['codrif'], verbose=False)
        self.party.remove(self.heroes['alagos'], verbose=False)
        self.party.remove(self.heroes['luana'], verbose=False)
        self.party.add(self.heroes['grindan'], verbose=False)
        self.party.add(self.heroes['rydalin'], verbose=False)
        self.party.add(self.heroes['galen'], verbose=False)
        self.party.add(self.heroes['luana'], verbose=False)

        self.inventory = containers.Inventory()

        test_eqp = [
            equipment.WeaponDatabase.factory('bronzeshortsword'),
            equipment.WeaponDatabase.factory('bronzedagger'),
            equipment.WeaponDatabase.factory('irondagger'),
            equipment.WeaponDatabase.factory('silverdagger'),
            equipment.WeaponDatabase.factory('steeldagger'),
            equipment.BootsDatabase.factory('ironboots'),
            equipment.BootsDatabase.factory('bootsofmotion'),
            equipment.BootsDatabase.factory('silenceboots'),
            equipment.BootsDatabase.factory('titaniumboots'),
            equipment.ShieldDatabase.factory('silverkite'),
            equipment.ShieldDatabase.factory('woodentarge'),
            equipment.ShieldDatabase.factory('bronzescutum'),
            equipment.ShieldDatabase.factory('ironheater'),
            equipment.RingDatabase.factory('testring'),
            equipment.RingDatabase.factory('testring2'),
            equipment.AccessoryDatabase.factory('testaccessory'),
            equipment.AccessoryDatabase.factory('testaccessory2'),
            equipment.AmuletDatabase.factory('testamulet'),
            equipment.AmuletDatabase.factory('testamulet2'),
            equipment.ArmorDatabase.factory('lighttitaniumarmor'),
            equipment.BeltDatabase.factory('leatherbelt'),
            equipment.BeltDatabase.factory('testbelt2'),
            equipment.CloakDatabase.factory('cottoncloak'),
            equipment.GlovesDatabase.factory('leathergloves'),
            equipment.GlovesDatabase.factory('testgloves2'),
            equipment.HelmetDatabase.factory('leathercap'),
            equipment.HelmetDatabase.factory('bronzehelmet'),
            equipment.HelmetDatabase.factory('helmofknowledge'),
            equipment.HelmetDatabase.factory('helmofknowledge2'),
            equipment.HelmetDatabase.factory('helmofwisdom'),
            equipment.HelmetDatabase.factory('helmofwisdom2'),
            equipment.HelmetDatabase.factory('helmofcharisma'),
            equipment.HelmetDatabase.factory('helmofcharisma2'),
            equipment.HelmetDatabase.factory('helmofinsight'),
            equipment.HelmetDatabase.factory('helmofinsight2'),
            equipment.HelmetDatabase.factory('helmoftempests'),
            equipment.HelmetDatabase.factory('helmoftempests2'),
            equipment.HelmetDatabase.factory('wizardhat'),
            equipment.HelmetDatabase.factory('wizardhat2')
        ]

        for eqp in test_eqp:
            self.inventory.add(eqp, quantity=random.randint(1, 999), verbose=False)

        # todo, hoe bepaal je of een ring aan de linker of rechter hand kan?

        self.heroes['alagos'].set_equipment_item(equipment.BootsDatabase.factory('ironboots'))
        self.heroes['alagos'].set_equipment_item(equipment.BootsDatabase.factory(None))
        self.heroes['alagos'].set_equipment_item(equipment.WeaponDatabase.factory('silverwarbow'))
