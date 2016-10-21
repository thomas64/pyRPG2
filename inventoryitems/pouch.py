
"""
class: PouchItem
"""


class PouchItem(object):
    """
    Maak een PouchItem object vanuit de pouchitem database.
    """
    def __init__(self, **kwargs):
        self.qty = 1

        for eqp_value_key, eqp_value_value in kwargs.items():
            setattr(self, eqp_value_key.upper(), eqp_value_value)  # zet de dict van kwargs om in attributen

        self.RAW = self.NAM.strip().lower().replace(" ", "")  # als er een NAM is, geef hem een RAW
