
"""
class: PeopleDatabase
"""

import enum

PATH = 'resources/sprites/npcs/'
FEXT = 'f.png'
SEXT = 's.png'
CHILD01 = PATH+'child_01'
CHILD02 = PATH+'child_02'
CHILD03 = PATH+'child_03'
CHILD04 = PATH+'child_04'


class PeopleDatabase(enum.Enum):
    """..."""

    person001 = dict(face=CHILD01+FEXT, sprite=CHILD01+SEXT,
                     quest='quest1')
    person002 = dict(face=CHILD01+FEXT, sprite=CHILD01+SEXT,
                     text=["Hi mister!", "We're playing hide and seek.", "I'm seeking, where are they?"])
    person003 = dict(face=CHILD02+FEXT, sprite=CHILD02+SEXT,
                     text=["Aaw, I'm already caugth."])
    person004 = dict(face=CHILD03+FEXT, sprite=CHILD03+SEXT,
                     text=["Psst, I'm hiding, please don't say anything."])
    person005 = dict(face=CHILD04+FEXT, sprite=CHILD04+SEXT,
                     text=["Teehee, he'll never me here."])
