
"""
class: PauseMenu
"""


class PauseMenu(MenuItem):
    """
    De pausemenu items.
    """
    def __init__(self, engine):
        super().__init__(engine)

        self.inside['ContinueGame'] = 'Continue'
        self.inside['LoadGame'] = 'Load Game'
        self.inside['SaveGame'] = 'Save Game'
        self.inside['Options'] = 'Options'
        self.inside['MainMenu'] = 'Main Menu'
