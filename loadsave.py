
"""
class: Dialog
"""

import os
import pickle

from console import Console

SAVEPATH = 'savegame'


class Dialog(object):
    """
    Deze heet nog Dialog omdat dit ooit een TKinter Dialog was.
    Maak bij voorbaat een pad aan.
    """
    def __init__(self, engine):
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
            Console.load_gamedata()
            with open(filename, 'rb') as f:
                self.engine.data = pickle.load(f)
        except (pickle.UnpicklingError, EOFError):
            Console.corrupt_gamedata()

    def save(self, filename):
        """
        Save de voortgang naar een bestand.
        :param filename: het gekozen bestandsnaam uit de lijst of ingetypt.
        """
        Console.save_gamedata()
        filename = os.path.join(SAVEPATH, filename)
        with open(filename, 'wb') as f:
            pickle.dump(self.engine.data, f)

    @staticmethod
    def delete(filename):
        """
        Delete een opgeslagen spelbestand.
        :param filename: het gekozen bestandsnaam uit de lijst
        """
        Console.delete_gamedata()
        filename = os.path.join(SAVEPATH, filename)
        os.remove(filename)
