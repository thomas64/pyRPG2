
"""
class: Script
"""

import characters
import database.treasurechest


class Script(object):
    """
    Alle momenten van het spel
    """
    def __init__(self, engine):
        self.engine = engine

    def new_game(self):
        """
        Wat te doen bij het starten van een nieuw spel.
        """
        # Vul de heroes database met alle heroes die er in het spel bestaan.
        self.engine.data.heroes['alagos'] = characters.HeroData.factory(characters.HeroData.alagos)
        self.engine.data.heroes['luana'] = characters.HeroData.factory(characters.HeroData.luana)
        self.engine.data.heroes['grindan'] = characters.HeroData.factory(characters.HeroData.grindan)
        self.engine.data.heroes['rydalin'] = characters.HeroData.factory(characters.HeroData.rydalin)
        self.engine.data.heroes['codrif'] = characters.HeroData.factory(characters.HeroData.codrif)
        self.engine.data.heroes['galen'] = characters.HeroData.factory(characters.HeroData.galen)

        for hero in self.engine.data.heroes.values():
            hero.calc_stats()
            hero.calc_skills()

        self.engine.data.treasure_chests = database.treasurechest.TreasureChestDatabase()

        # Vul de party aan met de eerste hero
        self.engine.data.party.add(self.engine.data.heroes['alagos'], verbose=False)
        # De hieronder zijn om te testen
        self.engine.data.party.add(self.engine.data.heroes['galen'], verbose=False)
        self.engine.data.party.add(self.engine.data.heroes['luana'], verbose=False)
        self.engine.data.party.add(self.engine.data.heroes['grindan'], verbose=False)
        self.engine.data.party.add(self.engine.data.heroes['rydalin'], verbose=False)
        self.engine.data.party.add(self.engine.data.heroes['codrif'], verbose=False)

        return

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
            equipment.BraceletDatabase.factory('testbracelet'),
            equipment.BraceletDatabase.factory('testbracelet2'),
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
