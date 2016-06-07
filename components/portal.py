
"""
class: Portal
"""

import pytmx

MAPSPATH = 'resources/maps/'
STARTPOS = "start_pos"


class Portal(object):
    """
    Een portal knoopt 2 maps aan elkaar.
    Hij krijgt een van en een naar naam mee. Hij laadt dan de naarmap en zoekt daarin naar de naam van de vanmap.
    Wanneer gevonden, dan wordt dat object de startpositie van de naarmap.
    """
    def __init__(self, from_name, from_rect, to_name, to_nr):
        self.from_name = from_name
        self.rect = from_rect
        self.to_name = to_name
        self.to_nr = to_nr
        self.to_pos = self._load_position()

    def _load_position(self):
        """
        to_nr kan gebruikt worden als er 2 locaties aan elkaar verbonden zijn met meerdere verbindingen.
        Dan kan de .Type in een .tmx file met dezelfde cijfers in portal en start_pos aan elkaar verbonden worden.
        """
        temp_tmx_data = pytmx.load_pygame(MAPSPATH+self.to_name+".tmx")
        for obj in temp_tmx_data.get_layer_by_name(STARTPOS):
            if obj.name == self.from_name:
                if obj.type == self.to_nr:
                    return obj.x, obj.y
