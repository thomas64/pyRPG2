
"""
class: PeopleDatabase
"""

import enum

PATH = 'resources/sprites/npcs/'
FEXT = 'f.png'
SEXT = 's.png'
NAME = 'child_'


class PeopleDatabase(enum.Enum):
    """
    ...
    """

    person1 = dict(face=PATH+NAME+'01'+FEXT, sprite=PATH+NAME+'01'+SEXT, walking=True)
    person2 = dict(face=PATH+NAME+'01'+FEXT, sprite=PATH+NAME+'01'+SEXT, walking=False)
