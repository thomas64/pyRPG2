
"""
class: NoteDatabase
"""

import enum

PATH = 'resources/images/'


class NoteDatabase(enum.Enum):
    """
    Er zijn meerdere messageboxen mogelijk als de verschillende teksten in meerdere lijsten staan.
    Single plaatjes zijn ook mogelijk, maar dan moet het een string zijn.
    """
    # invernia_inn_1f
    note1 = [["You shouldn't read other people's mail."]]
    note2 = [["The cup seems to be empty."]]
    # invernia_inn_2f
    note3 = PATH+'landkaart.jpg'
    # invernia_guild
    note4 = [["You found a secret book."],
             ["But there are no pages..."]]
    # ersin_forest
    note5 = [["I'm out admiring the scenery.",
             "I'll be back..."]]
