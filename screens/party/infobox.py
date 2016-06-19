
"""
class: InfoBox
"""

from components import TextBox


class InfoBox(TextBox):
    """
    Waar in het partyscreen alle omschrijvingen worden weergegeven.
    """
    def __init__(self, position, width, height):
        super().__init__(position, width, height)
