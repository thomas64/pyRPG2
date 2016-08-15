
"""
class: Logbook
"""

from constants import QuestType
from inventoryitems import FetchItemQuestItem
from inventoryitems import PersonMessageQuestItem


class Logbook(dict):
    """..."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.NAM = "Logbook"

    def add_quest(self, quest_key, quest_value):
        """
        Voegt op basis van de gevonden key en value (uit de quest database de juiste quest toe.
        :param quest_key: bijv quest1
        :param quest_value: condition, reward en text
        :return: het quest object
        """
        if not self.get(quest_key):
            if quest_value['qtype'] == QuestType.FetchItemQuest:
                self[quest_key] = FetchItemQuestItem(quest_value['qtype'],
                                                     quest_value['condition'],
                                                     quest_value['reward'],
                                                     quest_value['text'])
            elif quest_value['qtype'] == QuestType.PersonMessageQuest:
                self[quest_key] = PersonMessageQuestItem(quest_value['qtype'],
                                                         quest_value['people'],
                                                         quest_value['reward'],
                                                         quest_value['text'])
        return self[quest_key]
