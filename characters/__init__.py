
"""
def: factory_all_heroes
"""

import characters.hero


def factory_all_heroes(heroes_enum):
    """
    Maak een dict van Hero Objecten uit de Enum database.
    :param heroes_enum: de enum class met alle hero data
    :return: de dict met Hero objecten
    """
    heroes_dict = dict()
    for hero_enum in heroes_enum:
        heroes_dict[hero_enum.name] = characters.hero.Hero(**hero_enum.value)
    return heroes_dict
