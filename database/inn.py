
"""
class: InnDatabase
"""

import enum


PATH = 'resources/sprites/npcs/'
PATHEXT = '_Inn.png'
FACE = 'f'
SPRITE = 's'


def text(price):
    """
    ...
    :param price:
    :return:
    """
    return ["Good day sir, and welcome to my inn.",
            "For {} gold, you may rest here now".format(price),
            "and your health will be fully restored.",
            "",
            "Yes please.",
            "No thanks."]


class InnDatabase(enum.Enum):
    """
    ...
    """
    # het getal dat je meegeeft aan text() moet uiteraard hetzelfde zijn als die je meegeeft aan price=
    inn1 = dict(price=50, face=PATH+'01'+FACE+PATHEXT, sprite=PATH+'01'+SPRITE+PATHEXT, text=text(50))
