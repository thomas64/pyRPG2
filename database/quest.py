
"""
class: QuestDatabase
"""

import enum

from constants import QuestType


class QuestDatabase(enum.Enum):
    """..."""

    quest1 = dict(qtype=QuestType.ItemQuest,
                  condition=dict(itm1=dict(nam='herbs',   qty=5)),
                  reward=dict(itm1=dict(nam='gold',       qty=2),
                              eqp1=dict(nam='bronzedart', qty=1)),
                  # de nulste moet de confirmbox zijn.
                  # de anderen zijn in QuestState volgorde.
                  text=(["Help the boy out and give him 5 herbs?", "", "Yes, ofcourse!", "No, these are my herbs."],
                        ["Hi mister,", "I need 5 herbs for my mommy. She's ill.", "Can you please help me find some?"],
                        ["If you've got 5 herbs, please give them to me."],
                        ["Thanks a lot for the herbs! Now my mom will be better soon.",
                         "Instead of the herbs I found this here in the forest.",
                         "You can have it, for helping my mommy."],
                        ["Hi mister,", "It seems my mommy is all better now.", "Thanks to you!"])
                  )
    quest2 = dict()
