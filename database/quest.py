
"""
class: QuestDatabase
"""


class QuestDatabase(dict):
    """
    ...
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self['quest1'] = dict(first=self.first('quest1'), second=self.second('quest1'),
                              condition=dict(),
                              reward=dict(itm1=dict(nam='gold',       qty=2),
                                          eqp1=dict(nam='bronzedart', qty=1))
                              )
        self['quest2'] = dict()

        for value in self.values():
            value['started'] = False
            value['finished'] = False

    def first(self, quest_raw):
        """"..."""
        pass

    def second(self, quest_raw):
        """..."""
        pass
