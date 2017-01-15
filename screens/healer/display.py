
"""
class: Display
"""

from components import MessageBox
from components import Parchment

from constants import GameState
from constants import HealingType
from constants import SFX

from .herobox import HeroBox
from .pouchbox import PouchBox
from .selector import Selector


SOURCETITLE1 = "Stamina {}: {}"


class Display(Parchment):
    """
    ...
    """
    def __init__(self, engine, hero, party):
        super().__init__(engine, "Party", "Pouch")

        self.subtype_list = [HealingType.hands, HealingType.herbs]
        self.subtype = self.subtype_list[0]

        self.name = GameState.Shop

        self.main_title_pos_x = 1 / 16
        self.main_title_pos_y = 1 / 32
        self.source_title1 = SOURCETITLE1
        self.source_title1_pos_x = 1 / 16
        self.source_title1_pos_y = 70 / 100
        self.source_title2 = self.subtype.value
        self.source_title2_pos_x = 1 / 16
        self.source_title2_pos_y = 65 / 100
        self.sub_title_pos_x = 5
        self.sub_title_pos_y1 = 15 / 100
        self.sub_title_pos_y2 = 17 / 100

        self.face_pos_x = 1 / 16
        self.face_pos_y = 3 / 16
        self.extra_face_size_x = 20
        self.extra_face_size_y = 0
        self.lines_next_to_face = 4
        self.small_line_height = 27

        self.leftbox_width = 25 / 100
        self.leftbox_height = 73 / 100
        self.leftbox_pos_x = 40 / 100
        self.leftbox_pos_y = 6 / 32
        self.rightbox_width = 15 / 100
        self.rightbox_height = 73 / 100
        self.rightbox_pos_x = 70 / 100
        self.rightbox_pos_y = 6 / 32
        self.infobox_width = 30 / 100
        self.infobox_height = 16 / 100
        self.infobox_pos_x = 1 / 16
        self.infobox_pos_y = 76 / 100

        self.selector_pos_x = 2 / 32
        self.selector_pos_y = 60 / 100
        self.selector_width = 36

        self.cur_hero = hero
        self.party = party
        self._init_face_and_text(self.cur_hero.FAC, ["TODO"])
        self._init_selectors()
        self._init_boxes()
        self._init_buttons()

    def _init_selectors(self):
        for index, healing_type in enumerate(self.subtype_list):
            self.selectors.add(Selector(self._set_x(self.selector_pos_x) + index * self.selector_width,
                                        self._set_y(self.selector_pos_y), healing_type))

    def _init_boxes(self):
        self._init_infobox()
        self._init_herobox()
        self._init_pouchbox()

    def _init_herobox(self):
        width = self.screen.get_width() * self.leftbox_width
        height = self.screen.get_height() * self.leftbox_height
        self.leftbox = HeroBox(self._set_x(self.leftbox_pos_x), self._set_y(self.leftbox_pos_y),
                               int(width), int(height), self.engine.data.party, self.cur_hero)

    def _init_pouchbox(self):
        width = self.screen.get_width() * self.rightbox_width
        height = self.screen.get_height() * self.rightbox_height
        self.rightbox = PouchBox(self._set_x(self.rightbox_pos_x), self._set_y(self.rightbox_pos_y),
                                 int(width), int(height), self.engine.data.pouch)

    def update(self, dt):
        """
        :param dt: self.clock.tick(FPS)/1000.0
        """
        for selector in self.selectors:
            selector.update(self.subtype)
        self.main_title = self.cur_hero.hlr.NAM
        self.source_title1 = SOURCETITLE1.format(self.cur_hero.NAM, str(self.cur_hero.sta.cur))
        self.source_title2 = self.subtype.value

    def _handle_leftbox_click(self, event):
        # todo
        pass
