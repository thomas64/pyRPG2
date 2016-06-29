
"""
def: factory_quest
"""


def factory_quest(logbook, quest_key):
    """
    Voeg een QuestItem object toe aan het logboek uit engine.
    :param logbook: self.engine.data.logbook
    :param quest_key: een string bijv 'quest3'
    """
    import console
    from .item import QuestItem
    from database import QuestDatabase

    # bestaat de key in de enum database?
    if quest_key in QuestDatabase.__members__:
        # als hij nog niet in het logboek staat, voeg hem toe
        if not logbook.get(quest_key):
            logbook[quest_key] = QuestItem(**QuestDatabase[quest_key].value)
        # en geef het QuestItem object weer terug
        return logbook[quest_key]
    else:
        console.error_item_name_not_in_database(quest_key)
        raise KeyError
