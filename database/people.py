
"""
class: PeopleDatabase
"""

import enum

from .quest import QuestDatabase


PATH = 'resources/sprites/npcs/'
FEXT = 'f.png'
SEXT = 's.png'
CHILD1 = PATH+'Child_01'
CHILD2 = PATH+'Child_02'
CHILD3 = PATH+'Child_03'
CHILD4 = PATH+'Child_04'
WOMAN3 = PATH+'Woman_03'
MAN5 = PATH+'Man_05'


class PeopleDatabase(enum.Enum):
    """..."""

    # invernia_forest_center
    person1 = dict(face=CHILD1+FEXT, sprite=CHILD1+SEXT,
                   quest=QuestDatabase.quest1)
    # invernia_town
    person2 = dict(face=CHILD1+FEXT, sprite=CHILD1+SEXT,
                   text=["Hi mister!", "We're playing hide and seek.", "I'm seeking, where are they?"])
    person3 = dict(face=CHILD2+FEXT, sprite=CHILD2+SEXT,
                   text=["Aaw, I'm already caugth."])
    person4 = dict(face=CHILD3+FEXT, sprite=CHILD3+SEXT,
                   text=["Psst, I'm hiding, please don't say anything."])
    person5 = dict(face=CHILD4+FEXT, sprite=CHILD4+SEXT,
                   text=["Teehee, he'll never find me here."])
    # invernia_inn_1f
    person6 = dict(face=WOMAN3+FEXT, sprite=WOMAN3+SEXT,
                   text=["Ouch! This tea is still to hot to drink."])
    person7 = dict(face=MAN5+FEXT, sprite=MAN5+SEXT,
                   text=["The rooms are pretty cheap in this town.",
                         "I've heard people tell of other places where they ask a lot more for a room."])
