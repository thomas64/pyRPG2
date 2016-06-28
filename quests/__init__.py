
"""
def: factory_quest
"""


def factory_quest(quest_data, quest_key):
    """
    Voeg een QuestItem object toe aan de quests data uit engine.
    :param quest_data: self.engine.data.quests
    :param quest_key: een string bijv 'quest3'
    """
    import console
    from .item import QuestItem
    from database import QuestDatabase

    # bestaat de key in de enum database?
    if quest_key in QuestDatabase.__members__:
        if not quest_data.get(quest_key):
            quest_data[quest_key] = QuestItem(**QuestDatabase[quest_key].value)
    else:
        console.error_item_name_not_in_database(quest_key)
        raise KeyError
