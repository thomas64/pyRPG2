
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
    person2 = dict(face=PATH+NAME+'01'+FEXT, sprite=PATH+NAME+'01'+SEXT, walking=False, quest='quest1')

    @classmethod
    def opening(cls, people_key):
        """..."""
        if people_key == cls.person1.name:
            return ["Hi mister!"]
        elif people_key == cls.person2.name:
            return ["Hi mister!"]
