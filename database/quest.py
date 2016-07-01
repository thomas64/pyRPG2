
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
                  # de nulste moet de confirmbox zijn.
                  # de anderen zijn in QuestState volgorde.
                  text=(["Give 3 herbs?", "", "Yes", "No"],
                        ["I want 3 herbs."],
                        ["Don't forget, 3 herbs."],
                        ["Thanks a lot for the herbs!", "Here is your reward."],
                        ["I'll never forget."])
                  )
    quest2 = dict()
