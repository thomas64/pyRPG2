
"""
class: SchoolDatabase
"""

import enum

from constants import SchoolType

PATH = 'resources/sprites/npcs/School_'
FACE = 'f.png'
SPRITE = 's.png'


class SchoolDatabase(enum.Enum):
    """
    ...
    """

    school1 = dict(content=[SchoolType.elm, SchoolType.nmg],
                   face=PATH+'01'+FACE, sprite=PATH+'01'+SPRITE)
