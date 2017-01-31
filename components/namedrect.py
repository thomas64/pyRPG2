
"""
class: NamedRect
"""


class NamedRect(object):
    """
    De naam van de rect en de rect zelf.
    """
    def __init__(self, name, rect, opt=None):
        """
        :param opt: optioneel, om iets extra's mee te kunnen geven. text_event gebruikt het voor zwarte achtergrond.
        """
        self.name = name
        self.rect = rect
        self.opt = opt
