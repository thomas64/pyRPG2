
"""
class: InnDatabase
"""

import enum


PATH = 'resources/sprites/npcs/'
FEXT = 'f.png'
SEXT = 's.png'
INN1 = PATH+'Woman_01'


class InnDatabase(enum.Enum):
    """..."""
    inn1 = dict(price=5, face=INN1+FEXT, sprite=INN1+SEXT)

    @staticmethod
    def welcome_text(price):
        """..."""
        return ["Good day sir, and welcome to my inn.",
                "For {} gold, you may rest here now".format(price),
                "and your health will be fully restored.",
                "",
                "Yes please.",
                "No thanks."]

    @staticmethod
    def paid_text():
        """..."""
        return ["Thank you. Enjoy your stay."]

    @staticmethod
    def fail_text():
        """..."""
        return ["I'm terribly sorry, but it seems you don't have enough gold.",
                "I can't give you a room, please come back another time."]

    @staticmethod
    def deny_text():
        """..."""
        return ["I hope you'll visit us next time."]
