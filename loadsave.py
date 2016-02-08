"""
class: Dialog
"""

import os
import pickle

import wx

import console


SAVEPATH = 'savegame'


class Dialog(wx.App):
    """
    Twee wx dialog boxes om te saven en te laden. Maak bij voorbaat een pad aan.
    """
    def __init__(self, engine):
        self.engine = engine
        wx.App.__init__(self)
        if not os.path.exists(SAVEPATH):
            os.makedirs(SAVEPATH)

    def load(self):
        """
        Load dialog.
        """
        dialog = wx.FileDialog(None,
                               message='Load File',
                               defaultDir=SAVEPATH,
                               defaultFile='savefile.dat',
                               wildcard="Save Files (*.dat) |*.dat",
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dialog.ShowModal() == wx.ID_OK:
            filename = dialog.GetPath()
            try:
                console.load_gamedata()
                with open(filename, 'rb') as f:
                    (self.engine.data,
                     self.engine.overworld.window.hero.rect,
                     self.engine.overworld.window.hero.last_direction) = pickle.load(f)
            except pickle.UnpicklingError:
                console.corrupt_gamedata()
                filename = None
        else:
            filename = None
        dialog.Destroy()
        return filename

    def save(self):
        """
        Save dialog.
        """
        dialog = wx.FileDialog(None,
                               message='Save File',
                               defaultDir=SAVEPATH,
                               defaultFile='savefile.dat',
                               wildcard="Save Files (*.dat) |*.dat",
                               style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dialog.ShowModal() == wx.ID_OK:
            filename = dialog.GetPath()
            console.save_gamedata()
            with open(filename, 'wb') as f:
                pickle.dump([self.engine.data,
                             self.engine.overworld.window.hero.rect,
                             self.engine.overworld.window.hero.last_direction], f)
        else:
            filename = None
        dialog.Destroy()
        return filename
