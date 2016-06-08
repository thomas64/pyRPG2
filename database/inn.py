
"""
class: InnDatabase
"""

import enum


PATH = 'resources/sprites/npcs/'
PATHEXT = '_Inn.png'
FACE = 'f'
SPRITE = 's'


class InnDatabase(enum.Enum):
    """
    ...
    """

    inn1 = dict(price=50, face=PATH+'01'+FACE+PATHEXT, sprite=PATH+'01'+SPRITE+PATHEXT)
