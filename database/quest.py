
"""
class: QuestDatabase
"""

import enum

from constants import QuestType


class QuestDatabase(enum.Enum):
    """..."""

    quest1 = dict(qtype=QuestType.ItemQuest,
                  condition=dict(itm1=dict(nam='herbs',   qty=3)),
                  reward=dict(itm1=dict(nam='gold',       qty=2),
                              eqp1=dict(nam='bronzedart', qty=1)),
                  text=(["I want 3 herbs."],
                        ["Don't forget, 3 herbs."],
                        ["Give 3 herbs?", "", "Yes", "No"],
                        ["Thanks a lot for the herbs!"],
                        ["I'll never forget."])
                  )
    quest2 = dict()
