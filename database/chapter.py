
"""
class: ChapterDatabase
"""

import aenum


class ChapterDatabase(aenum.NoAliasEnum):
    """
    Als je over een plekje loopt met een chapter# naam, dan gaat de condition op True en
    dan kunnen er personen verschijnen. De personen worden aan een chapter gekoppeld in de people database.
    """

    chapter1 = dict(condition=False)
