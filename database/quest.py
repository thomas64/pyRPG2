
"""
class: QuestDatabase
"""

import pouchitems


class QuestDatabase(dict):
    """..."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self['quest1'] = dict(condition=dict(itm1=dict(nam='herbs',   qty=3)),
                              reward=dict(itm1=dict(nam='gold',       qty=2),
                                          eqp1=dict(nam='bronzedart', qty=1))
                              )
        self['quest2'] = dict()

        for value in self.values():
            value['text'] = self.text
            value['is_complete'] = self.is_complete
            value['started'] = False
            value['complete'] = False
            value['finished'] = False
            value['rewarded'] = False

    def text(self, quest_raw):
        """..."""
        if not self[quest_raw]['started']:
            if quest_raw == 'quest1':
                return ["I want 4 herbs."]
        elif self[quest_raw]['started'] and not self[quest_raw]['complete']:
            if quest_raw == 'quest1':
                return ["Don't forget, 4 herbs."]
        elif self[quest_raw]['started'] and self[quest_raw]['complete'] and not self[quest_raw]['finished']:
            if quest_raw == 'quest1':
                return ["Give 4 herbs?",
                        "",
                        "Yes",
                        "No"]
        elif self[quest_raw]['started'] and self[quest_raw]['complete'] and self[quest_raw]['finished'] and not self[quest_raw]['rewarded']:
            if quest_raw == 'quest1':
                return ["Thanks a lot for the herbs!"]
        elif self[quest_raw]['started'] and self[quest_raw]['complete'] and self[quest_raw]['finished'] and self[quest_raw]['rewarded']:
            if quest_raw == 'quest1':
                return ["I'll never forget."]

    def is_complete(self, quest_raw, data):
        """..."""
        if not self[quest_raw]['complete']:
            if quest_raw == 'quest1':
                item = pouchitems.factory_pouch_item(self[quest_raw]['condition']['itm1']['nam'])
                qty = self[quest_raw]['condition']['itm1']['qty']
                if data.pouch.remove(item, qty):
                    self[quest_raw]['complete'] = True
                    return True
