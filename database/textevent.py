
"""
class: TextEventDatabase
"""

HEROFACEPATH = 'resources/sprites/heroes/'
ALAGOS = HEROFACEPATH+"01f_alagos.png"


class TextEventDatabase(dict):
    """
    Er zijn meerdere messageboxen mogelijk als de verschillende teksten in meerdere lijsten staan.
    """
    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)

        self.data = data

        # condition moet altijd True of een methode zijn, anders wordt hij niet uitgevoerd.

        self['text1'] = dict(condition=self.condition1,
                             text=[["hoi1"], ["hoi2"]],
                             face=[ALAGOS, HEROFACEPATH+"02f_luana.png"])
        self['text2'] = dict(condition=True,
                             text=[["Woah! It's a hidden cave!"]],
                             face=[ALAGOS])
        self['text3'] = dict(condition=True,
                             text=[["Kendall!"], ["Kendall!!"], ["Where are you?!"],
                                   ["You're wife is looking for you!"], ["KENDALL!!"]],
                             face=[ALAGOS, ALAGOS, ALAGOS, ALAGOS, ALAGOS])
        self['text4'] = dict(condition=True,
                             text=[["Where is he?"], ["He must be somewhere around here..."]],
                             face=[ALAGOS, ALAGOS])

    def condition1(self):
        """
        Moet als aparte methode. Kon niet als lambda achter 'condition=' vanwege pickle save error.
        """
        return self.data.party.contains('luana')
