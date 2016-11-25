
"""
class: Portal
"""


class Portal(object):
    """
    Een portal knoopt 2 maps aan elkaar.
    Hij krijgt een van en een naar naam mee. Hij laadt dan de naarmap en zoekt daarin naar de naam van de vanmap.
    Wanneer gevonden, dan wordt dat object de startpositie van de naarmap.
    """
    def __init__(self, from_name, from_rect, to_name, to_nr, direction=None):
        self.from_name = from_name
        self.rect = from_rect
        self.to_name = to_name
        self.to_nr = to_nr          # dit is obj.type. is een getal. correspondeert met hetzelfde andere getal.
        self.direction = direction  # deze wordt alleen gebruikt door Portal als start_pos
