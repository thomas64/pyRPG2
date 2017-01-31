
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

        # condition moet altijd True of een method/lambda zijn, anders wordt hij niet uitgevoerd.

        self['textevent1'] = dict(condition=lambda: self.data.party.contains('luana'),
                                  text=[["hoi1"], ["hoi2"]],
                                  face=[ALAGOS, HEROFACEPATH+"02f_luana.png"])
        self['textevent2'] = dict(condition=True,
                                  text=[["Woah! It's a hidden cave!"]],
                                  face=[ALAGOS])
