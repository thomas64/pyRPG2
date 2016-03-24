
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
