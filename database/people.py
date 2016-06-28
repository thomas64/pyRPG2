
"""
class: PeopleDatabase
"""

import enum

PATH = 'resources/sprites/npcs/'
FEXT = 'f.png'
SEXT = 's.png'
NAME = 'child_'


class PeopleDatabase(enum.Enum):
    """..."""

    person1 = dict(face=PATH+NAME+'01'+FEXT, sprite=PATH+NAME+'01'+SEXT, walking=True,
                   text=["Hi mister!"])
    person2 = dict(face=PATH+NAME+'01'+FEXT, sprite=PATH+NAME+'01'+SEXT, walking=False, quest='quest1')
