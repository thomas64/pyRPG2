
"""
class: InnDatabase
"""

import enum


PATH = 'resources/sprites/npcs/'
PATHEXT = '_Inn.png'
FACE = 'f'
SPRITE = 's'


def welcome_text(price):
    """..."""
    return ["Good day sir, and welcome to my inn.",
            "For {} gold, you may rest here now".format(price),
            "and your health will be fully restored.",
            "",
            "Yes please.",
            "No thanks."]


def paid_text():
    """..."""
    return ["Thank you. Enjoy your stay."]


def fail_text():
    """..."""
    return ["I'm terribly sorry, but it seems you don't have enough gold.",
            "I can't give you a room, please come back another time."]


def deny_text():
    """..."""
    return ["I hope you'll visit us next time."]


class InnDatabase(enum.Enum):
    """..."""
    # het getal dat je meegeeft aan welcome() moet uiteraard hetzelfde zijn als die je meegeeft aan price=
    inn1 = dict(price=50, face=PATH+'01'+FACE+PATHEXT, sprite=PATH+'01'+SPRITE+PATHEXT,
                welcome=welcome_text(50), paid=paid_text(), fail=fail_text(), deny=deny_text())
