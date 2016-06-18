
"""
class: SchoolDatabase
"""

import enum

from database import SchoolType

PATH = 'resources/sprites/npcs/'
PATHEXT = '_School.png'
FACE = 'f'
SPRITE = 's'


class SchoolDatabase(enum.Enum):
    """
    ...
    """

    school1 = dict(content=[SchoolType.elm, SchoolType.nmg],
                   face=PATH+'01'+FACE+PATHEXT, sprite=PATH+'01'+SPRITE+PATHEXT)
