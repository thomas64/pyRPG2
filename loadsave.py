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
    def __init__(self):
        wx.App.__init__(self)
        if not os.path.exists(SAVEPATH):
            os.makedirs(SAVEPATH)

    @staticmethod
    def load(engine):
        """
        Load dialog.
        :param engine: self van engine.py
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
                    (engine.data,
                     engine.overworld.window.hero.rect,
                     engine.overworld.window.hero.last_direction) = pickle.load(f)
            except pickle.UnpicklingError:
                console.corrupt_gamedata()
                filename = None
        else:
            filename = None
        dialog.Destroy()
        return filename

    @staticmethod
    def save(engine):
        """
        Save dialog.
        :param engine: self van engine.py
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
                pickle.dump([engine.data,
                             engine.overworld.window.hero.rect,
                             engine.overworld.window.hero.last_direction], f)
        else:
            filename = None
        dialog.Destroy()
        return filename
