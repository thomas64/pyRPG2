"""
class: Dialog
"""

import os
import pickle
import tkinter
import tkinter.filedialog

import console

SAVEPATH = 'savegame'

# todo, ipv tkinter, iets met pygame maken. zodat hij in fullscreen kan blijven


class Dialog(object):
    """
    Twee tk dialog boxes om te saven en te laden. Maak bij voorbaat een pad aan.
    """
    def __init__(self, engine):
        self.root = tkinter.Tk()
        self.root.withdraw()        # dat er verder geen venster zichtbaar is
        # dit maakt hem ongeveer op het midden van het scherm. als ik dat niet doe, dan schiet de save dialog
        # soms naar achter vreemd genoeg.
        self.root.geometry('0x0+{}+{}'.format(engine.screen.get_width() // 3, engine.screen.get_height() // 3))

        self.engine = engine
        if not os.path.exists(SAVEPATH):
            os.makedirs(SAVEPATH)

    def load(self, filename):
        """
        Laad een opgeslagen spelbestand.
        :param filename: het gekozen bestandsnaam uit de lijst
        """
        filename = os.path.join(SAVEPATH, filename)
        try:
            console.load_gamedata()
            with open(filename, 'rb') as f:
                (self.engine.data,
                 self.engine.gamestate.peek().window.heroes[0].rect.topleft,
                 self.engine.gamestate.peek().window.heroes[0].last_direction) = pickle.load(f)
                self.engine.gamestate.peek().window.align()  # zet andere chars achter de hero
        except (pickle.UnpicklingError, EOFError):
            console.corrupt_gamedata()
            filename = None
        return filename

    def save(self):
        """
        Save dialog.
        """
        filename = tkinter.filedialog.asksaveasfilename(title='Save File',
                                                        initialdir=SAVEPATH,
                                                        initialfile='savefile.dat',
                                                        filetypes=[('Save Files', '*.dat')]
                                                        )
        if filename:
            console.save_gamedata()
            with open(filename, 'wb') as f:
                pickle.dump([self.engine.data,
                             self.engine.gamestate.peek().window.heroes[0].rect.topleft,
                             self.engine.gamestate.peek().window.heroes[0].last_direction], f)
        else:
            filename = None
        self.root.destroy()
        return filename

    @staticmethod
    def delete(filename):
        """
        Delete een opgeslagen spelbestand.
        :param filename: het gekozen bestandsnaam uit de lijst
        """
        console.delete_gamedata()
        filename = os.path.join(SAVEPATH, filename)
        os.remove(filename)
