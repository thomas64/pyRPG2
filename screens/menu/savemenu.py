
"""
class: SaveMenu
"""

from components import InputBox
from constants import GameState
from loadsave import Dialog as SaveDialog

from .loadmenu import LoadMenu
import screens.menu


class SaveMenu(LoadMenu):
    """
    Heeft LoadMenu als base class.
    """
    def on_select(self, menu_item, title, animation, scr_capt, index):
        """
        Wanneer op Back geklikt wordt, sluit.
        Wanneer op een item met '...' geklikt wordt, maak via de inputbox een nieuwe naam aan,
        converteer die, sla op, een herlaad het scherm.
        Wanneer er al een slot is, converteer de filename ervan, en sla die er overheen op.
        :param menu_item: zie BaseMenu
        :param title: zie BaseMenu
        :param animation: zie BaseMenu
        :param scr_capt: zie BaseMenu
        :param index: zie BaseMenu
        """
        filename = None
        if menu_item.text == "Back":
            self.on_quit()
        elif "..." in menu_item.text:
            new_name = InputBox(self.engine.audio).input_loop()
            if new_name:
                filename = str(index+1) + "_" + new_name + ".dat"
        else:
            filename = self._convert_to_filename(menu_item.text, index)

        if filename:
            SaveDialog.save(self.engine.data, filename)
            self._reload(scr_capt, index)

    def _reload(self, scr_capt, index):
        """
        Herlaad het scherm door de state te poppen en opnieuw te pushen.
        Dit kan alleen bij savemenu omdat savemenu dieper in de stack zit dan loadmenu bij het mainmenu.
        """
        self.engine.gamestate.pop()
        push_object = screens.menu.create_menu(GameState.SaveMenu, self.engine, scr_capt=scr_capt, select=index)
        self.engine.gamestate.push(push_object)
