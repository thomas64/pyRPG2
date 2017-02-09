
"""
class: LoadMenu
"""

import datetime
import os

from components import LoadScreen
from components import Transition
from constants import SFX
from loadsave import Dialog as LoadDialog

from .basemenu import BaseMenu


SAVEPATH = 'savegame'
MAXSLOTS = 5


class LoadMenu(BaseMenu):
    """
    Hier worden alle bestanden van de savegame dir in een list gezet
    en weergegeven in de inside dict.
    """
    def __init__(self, engine):
        super().__init__(engine)

        number_of_slots = []

        # maak het aantal list entries aan. en een tijdelijke lijst met alle '#_' prefixes.
        for index in range(0, MAXSLOTS):
            self.content.append("Slot {}:  ...".format(index+1))
            number_of_slots.append(str(index+1)+"_")

        # loop door de savegame dir heen en sla alle bestanden op in 'files'.
        files = []
        for (dirpath, dirnames, filenames) in os.walk(SAVEPATH):
            files.extend(filenames)
            break

        # loop door alle files heen.
        for file in files:
            # loop door alle prefixes heen.
            for index, start in enumerate(number_of_slots):
                # als een gevonden bestand start met een prefix en eindigd op .dat
                if file.startswith(start) and file.endswith(".dat"):
                    # haal dan de prefix en .dat weg en vervang dat door visuele text weergave
                    visual = file.replace(start, "Slot "+str(index+1)+":  ").replace(".dat", "")
                    timestamp = os.path.getmtime(os.path.join(SAVEPATH, file))
                    timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                    # voeg ook de timestamp toe en zet het in de list overheen bij de juiste slot
                    self.content[index] = "{} [{}]".format(visual, timestamp)

        self.content.append('Back')

    def on_select(self, menu_item, title, animation, scr_capt, index):
        """
        Zie BaseMenu. Wanneer geen 'Back' of '...' in de text. Change de state naar Overworld,
        converteer de gelecteerde tekst naar filename, laad die in over de Overworld Data.
        :param menu_item: zie BaseMenu
        :param title: zie BaseMenu
        :param animation: zie BaseMenu
        :param scr_capt: zie BaseMenu
        :param index: zie BaseMenu
        """
        if menu_item.text == "Back":
            self.on_quit()
        elif "..." in menu_item.text:
            self.engine.audio.stop_sound(SFX.menu_select)
            self.engine.audio.play_sound(SFX.menu_error)
        else:
            filename = self._convert_to_filename(menu_item.text, index)
            data = LoadDialog.load(filename)
            # als de data niet corrupt is.
            if data:
                self.engine.data = data
                # als er na de reeks gamestates niets meer op stack ligt, komt overworld er in.
                self.engine.gamestate.change(Transition())
                self.engine.gamestate.push(LoadScreen())
                self.engine.gamestate.push(Transition())
                self.engine.force_bg_music = True
            else:
                self.engine.audio.stop_sound(SFX.menu_select)
                self.engine.audio.play_sound(SFX.menu_error)

    def on_delete(self, menu_item, scr_capt, index):
        """
        Zie BaseMenu. Als er delete wordt gedrukt op niet de Back knop. Herlaad het hele object.
        :param menu_item: zie BaseMenu
        :param scr_capt: zie BaseMenu
        :param index: zie BaseMenu
        """
        if menu_item.text == "Back":
            self.engine.audio.stop_sound(SFX.menu_select)
            self.engine.audio.play_sound(SFX.menu_error)
        elif "..." in menu_item.text:
            self.engine.audio.stop_sound(SFX.menu_select)
            self.engine.audio.play_sound(SFX.menu_error)
        else:
            filename = self._convert_to_filename(menu_item.text, index)
            LoadDialog.delete(filename)
            # er is niet voor _reload() gekozen omdat bij het poppen de muziek van mainmenu omhoog kwam.
            # bij savemenu is dat geen probleem omdat die dieper in het menu ligt.
            menu_item.clear_save_slot(self.engine.screen, index+1)

    @staticmethod
    def _convert_to_filename(menu_text, index):
        """
        Haal tekst ervoor weg en maak daar #_ van. Haal de hele datum erachter weg. Zet .dat erachter.
        """
        filename = menu_text.replace("Slot "+str(index+1)+":  ", str(index+1)+"_")
        filename = filename[:-22]
        filename += ".dat"
        return filename
