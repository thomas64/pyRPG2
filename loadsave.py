
"""
class: Dialog
"""

import os
import pickle

import wx


class Dialog(wx.App):
    """
    Twee wx dialog boxes om te saven en te laden. Maak bij voorbaat een pad aan.
    """
    def __init__(self):
        wx.App.__init__(self)
        if not os.path.exists('savegame'):
            os.makedirs('savegame')

    @staticmethod
    def load(game):
        """
        Load dialog.
        :param game: self van game.py
        """
        dialog = wx.FileDialog(None,
                               message='Load File',
                               defaultDir='savegame',
                               defaultFile='savefile.dat',
                               wildcard="Save Files (*.dat) |*.dat",
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dialog.ShowModal() == wx.ID_OK:
            filename = dialog.GetPath()
            try:
                print("Loading gamedata...")
                with open(filename, 'rb') as f:
                    game.overworld.hero.rect, game.overworld.hero.last_direction = pickle.load(f)
            except pickle.UnpicklingError:
                print('Corrupt gamedata.')
                filename = None
        else:
            filename = None
        dialog.Destroy()
        return filename

    @staticmethod
    def save(game):
        """
        Save dialog.
        :param game: self van game.py
        """
        dialog = wx.FileDialog(None,
                               message='Save File',
                               defaultDir='savegame',
                               defaultFile='savefile.dat',
                               wildcard="Save Files (*.dat) |*.dat",
                               style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dialog.ShowModal() == wx.ID_OK:
            filename = dialog.GetPath()
            print("Saving gamedata...")
            with open(filename, 'wb') as f:
                pickle.dump([game.overworld.hero.rect, game.overworld.hero.last_direction], f)
        else:
            filename = None
        dialog.Destroy()
        return filename
