
"""
class: InnDatabase
"""

import enum


PATH = 'resources/sprites/npcs/Inn_'
FACE = 'f.png'
SPRITE = 's.png'


class InnDatabase(enum.Enum):
    """..."""
    # het getal dat je meegeeft aan welcome() moet uiteraard hetzelfde zijn als die je meegeeft aan price=
    inn1 = dict(price=5, face=PATH+'01'+FACE, sprite=PATH+'01'+SPRITE)

    @classmethod
    def welcome_text(cls, price):
        """..."""
        return ["Good day sir, and welcome to my inn.",
                "For {} gold, you may rest here now".format(price),
                "and your health will be fully restored.",
                "",
                "Yes please.",
                "No thanks."]

    @classmethod
    def paid_text(cls):
        """..."""
        return ["Thank you. Enjoy your stay."]

    @classmethod
    def fail_text(cls):
        """..."""
        return ["I'm terribly sorry, but it seems you don't have enough gold.",
                "I can't give you a room, please come back another time."]

    @classmethod
    def deny_text(cls):
        """..."""
        return ["I hope you'll visit us next time."]
