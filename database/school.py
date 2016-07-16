
"""
class: SchoolDatabase
"""

import enum

from constants import SchoolType

PATH = 'resources/sprites/npcs/'
FEXT = 'f.png'
SEXT = 's.png'
SCHOOL1 = PATH+'woman50'


class SchoolDatabase(enum.Enum):
    """
    ...
    """

    school1 = dict(content=[SchoolType.elm, SchoolType.nmg],
                   face=SCHOOL1+FEXT, sprite=SCHOOL1+SEXT)
