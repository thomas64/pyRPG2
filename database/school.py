
"""
class: SchoolDatabase
"""

import enum

from constants import SchoolType

PATH = 'resources/sprites/npcs/'
FEXT = 'f.png'
SEXT = 's.png'
SCHOOL1 = PATH+'gypsy01'


class SchoolDatabase(enum.Enum):
    """
    ...
    """

    school1 = dict(content=[SchoolType.ntl, SchoolType.elm, SchoolType.nmg, SchoolType.ncy, SchoolType.str],
                   face=SCHOOL1+FEXT, sprite=SCHOOL1+SEXT)

    @staticmethod
    def welcome_text():
        """..."""
        return ("Good day sir, and welcome to my school.",
                "In the 'Known' box are all the spells you",
                "already have learned.  And in the",
                "'Learn' box are all the spells that I can teach.",
                "Click once on a selected item to learn a spell.",
                "You can scroll through the lists with your mouse-",
                "wheel if the list is longer than what you can see.",
                "Below here, all your party members are shown.",
                "Click on it to select someone else to be taught.")
