
"""
class: Display
"""

from components import MessageBox
from components import Parchment

from constants import EquipmentType as EqTy
from constants import GameState
from constants import SFX

from database import PouchItemDatabase

import inventoryitems

from .createbox import CreateBox
from .inventorybox import InventoryBox
from screens.shop.selector import Selector


SOURCETITLE1 = "Stamina {}: {}"


class Display(Parchment):
    """
    ...
    """
    def __init__(self, engine, hero):
        super().__init__(engine, "Create", "Invent.")

        self.subtype_list = [EqTy.wpn, EqTy.sld, EqTy.hlm, EqTy.arm, EqTy.clk, EqTy.glv, EqTy.blt, EqTy.bts]
        self.subtype = self.subtype_list[0]

        self.name = GameState.Shop

        self.main_title_pos_x = 1 / 16
        self.main_title_pos_y = 1 / 32
        self.source_title1 = SOURCETITLE1
        self.source_title1_pos_x = 1 / 16
        self.source_title1_pos_y = 70 / 100
        self.sub_title_pos_x = 5
        self.sub_title_pos_y1 = 15 / 100
        self.sub_title_pos_y2 = 17 / 100

        self.face_pos_x = 1 / 16
        self.face_pos_y = 3 / 16
        self.extra_face_size_x = 20
        self.extra_face_size_y = 0
        self.lines_next_to_face = 4
        self.small_line_height = 27

        self.leftbox_width = 20 / 100
        self.leftbox_height = 73 / 100
        self.leftbox_pos_x = 40 / 100
        self.leftbox_pos_y = 6 / 32
        self.rightbox_width = 26 / 100
        self.rightbox_height = 73 / 100
        self.rightbox_pos_x = 64 / 100
        self.rightbox_pos_y = 6 / 32
        self.infobox_width = 30 / 100
        self.infobox_height = 16 / 100
        self.infobox_pos_x = 1 / 16
        self.infobox_pos_y = 76 / 100

        self.selector_pos_x = 2 / 32
        self.selector_pos_y = 65 / 100
        self.selector_width = 36

        self.cur_hero = hero
        self._init_face_and_text(self.cur_hero.FAC, self.cur_hero.mec.welcome_text(self.cur_hero.NAM))
        self._init_selectors()
        self._init_boxes()
        self._init_buttons()

    def _init_selectors(self):
        for index, eqp_type in enumerate(self.subtype_list):
            self.selectors.add(Selector(self._set_x(self.selector_pos_x) + index * self.selector_width,
                                        self._set_y(self.selector_pos_y), eqp_type))

    def _init_boxes(self):
        self._init_infobox()
        self._init_createbox()
        self._init_inventorybox()

    def _init_createbox(self):
        width = self.screen.get_width() * self.leftbox_width
        height = self.screen.get_height() * self.leftbox_height

        if self.subtype == EqTy.wpn:
            from database.weapon import WeaponDatabase as DataBase
        elif self.subtype == EqTy.sld:
            from database.shield import ShieldDatabase as DataBase
        elif self.subtype == EqTy.hlm:
            from database.helmet import HelmetDatabase as DataBase
        elif self.subtype == EqTy.arm:
            from database.armor import ArmorDatabase as DataBase
        elif self.subtype == EqTy.clk:
            from database.cloak import CloakDatabase as DataBase
        elif self.subtype == EqTy.glv:
            from database.gloves import GlovesDatabase as DataBase
        elif self.subtype == EqTy.blt:
            from database.belt import BeltDatabase as DataBase
        elif self.subtype == EqTy.bts:
            from database.boots import BootsDatabase as DataBase
        else:
            raise AttributeError

        self.leftbox = CreateBox(self._set_x(self.leftbox_pos_x), self._set_y(self.leftbox_pos_y),
                                 int(width), int(height), DataBase)

    def _init_inventorybox(self):
        width = self.screen.get_width() * self.rightbox_width
        height = self.screen.get_height() * self.rightbox_height
        self.rightbox = InventoryBox(self._set_x(self.rightbox_pos_x), self._set_y(self.rightbox_pos_y),
                                     int(width), int(height),
                                     self.subtype, self.engine.data.party,
                                     self.engine.data.pouch, self.engine.data.inventory)

    def update(self, dt):
        """
        Update de selector border color.
        Update de gold quantity.
        :param dt: self.clock.tick(FPS)/1000.0
        """
        for selector in self.selectors:
            selector.update(self.subtype)
        self.main_title = self.cur_hero.mec.NAM
        self.source_title1 = SOURCETITLE1.format(self.cur_hero.NAM, self.cur_hero.sta.cur)

    def _handle_leftbox_click(self, event):
        create_click, selected_equipment = self.leftbox.mouse_click(event)
        if create_click:
            cloth = inventoryitems.factory_pouch_item(PouchItemDatabase.cloth)
            leather = inventoryitems.factory_pouch_item(PouchItemDatabase.leather)
            wood = inventoryitems.factory_pouch_item(PouchItemDatabase.wood)
            metals = inventoryitems.factory_pouch_item(PouchItemDatabase.metals)
            clt_qty = self.engine.data.pouch.get_quantity(cloth)
            ltr_qty = self.engine.data.pouch.get_quantity(leather)
            wod_qty = self.engine.data.pouch.get_quantity(wood)
            mtl_qty = self.engine.data.pouch.get_quantity(metals)

            if selected_equipment.CLT > clt_qty or \
               selected_equipment.LTR > ltr_qty or \
               selected_equipment.WOD > wod_qty or \
               selected_equipment.MTL > mtl_qty:
                text = ["You do not have the right components",
                        "to create that {}.".format(selected_equipment.NAM)]
                push_object = MessageBox(self.engine.gamestate, self.engine.audio, text, sound=SFX.menu_cancel)
                self.engine.gamestate.push(push_object)
                return True
            elif self.cur_hero.sta.cur < self.cur_hero.mec.STA_COST:
                text = ["{} does not have enough stamina".format(self.cur_hero.NAM),
                        "to create that {}.".format(selected_equipment.NAM)]
                push_object = MessageBox(self.engine.gamestate, self.engine.audio, text, sound=SFX.menu_cancel)
                self.engine.gamestate.push(push_object)
                return True
            elif 'pouch is full' is False:  # todo, moet 'pouch is vol' hier? of in pouch?
                self.engine.audio.play_sound(SFX.menu_cancel)
                return True

            self.engine.data.pouch.remove(cloth, selected_equipment.CLT, force=True)  # want kan ook 0 zijn.
            self.engine.data.pouch.remove(leather, selected_equipment.LTR, force=True)
            self.engine.data.pouch.remove(wood, selected_equipment.WOD, force=True)
            self.engine.data.pouch.remove(metals, selected_equipment.MTL, force=True)

            self.cur_hero.sta.cur -= self.cur_hero.mec.STA_COST

            # hoog het custom nummer op en zet die achter de .RAW zodat er meerdere customs in de inventory kunnen
            self.engine.data.custom_inventory_counter += 1
            selected_equipment.RAW += str(self.engine.data.custom_inventory_counter)

            # loop door alle attributen van selected_equipment heen
            # list(), zodat uit de iterate verwijderd kan worden
            for attr, value in list(vars(selected_equipment).items()):
                # als er een waarde van een attribute op 'X' vanuit de database staat,
                # dat betekent dat hij nog gevuld moet worden.
                if value == 'X':
                    # wat is de waarde van de gelijknamige attribute met 'MIN_' ervoor
                    min_value = getattr(selected_equipment, 'MIN_'+attr)
                    max_value = getattr(selected_equipment, 'MAX_'+attr)
                    # vraag bij de Mechanic Skill de berekende waarden op. en zet attribute op die waarde.
                    setattr(selected_equipment, attr, self.cur_hero.mec.get_eqp_itm_attr_value(min_value, max_value))
                    # en verwijder de overblijfselen
                    delattr(selected_equipment, 'MIN_'+attr)
                    delattr(selected_equipment, 'MAX_'+attr)

            text = ["{} successfully created.".format(selected_equipment.NAM)]
            self.engine.data.inventory.add_i(selected_equipment)
            push_object = MessageBox(self.engine.gamestate, self.engine.audio, text, sound=SFX.message)
            self.engine.gamestate.push(push_object)

            self._init_boxes()
            return True
        return False
