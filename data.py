
"""
...
"""


import collections

import characters.hero
import characters.party


class Data(object):
    """
    ...
    """
    def __init__(self):
        self.heroes = collections.OrderedDict()

        self.heroes['alagos'] = characters.hero.HeroData.factory(characters.hero.HeroData.alagos)
        self.heroes['luana'] = characters.hero.HeroData.factory(characters.hero.HeroData.luana)
        self.heroes['grindan'] = characters.hero.HeroData.factory(characters.hero.HeroData.grindan)
        self.heroes['rydalin'] = characters.hero.HeroData.factory(characters.hero.HeroData.rydalin)
        self.heroes['codrif'] = characters.hero.HeroData.factory(characters.hero.HeroData.codrif)
        self.heroes['galen'] = characters.hero.HeroData.factory(characters.hero.HeroData.galen)

        self.party = characters.party.Party()

        self.party.add(self.heroes['alagos'], verbose=False)
