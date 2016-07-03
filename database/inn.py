
"""
class: InnDatabase
"""

import enum


PATH = 'resources/sprites/npcs/'
FEXT = 'f.png'
SEXT = 's.png'
INN1 = PATH+'Inn_01'


class InnDatabase(enum.Enum):
    """..."""
    inn1 = dict(price=5, face=INN1+FEXT, sprite=INN1+SEXT)

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
