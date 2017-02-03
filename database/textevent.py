
"""
class: TextEventDatabase
"""

import enum

HEROFACEPATH = 'resources/sprites/heroes/'
ALAGOS = HEROFACEPATH+"01f_alagos.png"


class TextEventDatabase(enum.Enum):
    """
    Er zijn meerdere messageboxen mogelijk als de verschillende teksten in meerdere lijsten staan.
    condition moet altijd True of een methode zijn, anders wordt hij niet uitgevoerd.
    """

    # noinspection PyMethodMayBeStatic
    def condition1(self, data):
        """
        Moet als aparte methode. Kon niet als lambda achter 'condition=' vanwege pickle save error.
        Het is eigenlijk een static, maar die is niet callable vanuit window, daarom geen static gemaakt.
        """
        return data.party.contains('luana')

    text1 = dict(condition=condition1,
                 text=[["hoi1"], ["hoi2"]],
                 face=[ALAGOS, HEROFACEPATH+"02f_luana.png"])
    text2 = dict(condition=True,
                 text=[["Woah! It's a hidden cave!"]],
                 face=[ALAGOS])
    text3 = dict(condition=True,
                 text=[["Kendall!"], ["Kendall!!"], ["Where are you?!"],
                       ["You're wife is looking for you!"], ["KENDALL!!"]],
                 face=[ALAGOS, ALAGOS, ALAGOS, ALAGOS, ALAGOS])
    text4 = dict(condition=True,
                 text=[["Where is he?"], ["He must be somewhere around here..."]],
                 face=[ALAGOS, ALAGOS])
