
"""
class: PeopleDatabase
"""

import enum


PATH = 'resources/sprites/npcs/'
FEXT = 'f.png'
SEXT = 's.png'
CHILD1 = PATH+'Child_01'
CHILD2 = PATH+'Child_02'
CHILD3 = PATH+'Child_03'
CHILD4 = PATH+'Child_04'


class PeopleDatabase(enum.Enum):
    """..."""

    person1 = dict(face=CHILD1+FEXT, sprite=CHILD1+SEXT,
                   quest='quest1')
    person2 = dict(face=CHILD1+FEXT, sprite=CHILD1+SEXT,
                   text=["Hi mister!", "We're playing hide and seek.", "I'm seeking, where are they?"])
    person3 = dict(face=CHILD2+FEXT, sprite=CHILD2+SEXT,
                   text=["Aaw, I'm already caugth."])
    person4 = dict(face=CHILD3+FEXT, sprite=CHILD3+SEXT,
                   text=["Psst, I'm hiding, please don't say anything."])
    person5 = dict(face=CHILD4+FEXT, sprite=CHILD4+SEXT,
                   text=["Teehee, he'll never find me here."])
