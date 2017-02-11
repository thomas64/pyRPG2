
"""
class: LocationDatabase
"""

import aenum

from .chapter import ChapterDatabase
from .quest import QuestDatabase


class LocationDatabase(aenum.NoAliasEnum):
    """
    Hetzelfde als people database, alleen dan voor locaties. Plekken op de map waar je mee kan colliden.
    """

    location1 = dict(chapter=ChapterDatabase.chapter1)
    location2 = dict(quest=QuestDatabase.quest5)
