
"""
class: Dialog
"""

import os
import pickle

from console import Console

SAVEPATH = 'savegame'


class Dialog:
    """
    Deze heet nog Dialog omdat dit ooit een TKinter Dialog was.
    """

    @staticmethod
    def load(filename):
        """
        Laad een opgeslagen spelbestand.
        :param filename: het gekozen bestandsnaam uit de lijst
        """
        filename = os.path.join(SAVEPATH, filename)
        try:
            Console.load_gamedata()
            with open(filename, 'rb') as f:
                data = pickle.load(f)
            return data
        except (pickle.UnpicklingError, EOFError, AttributeError):
            Console.corrupt_gamedata()

    @staticmethod
    def save(data, filename):
        """
        Save de voortgang naar een bestand. Maak bij voorbaat een pad aan.
        :param data: self.engine.data
        :param filename: het gekozen bestandsnaam uit de lijst of ingetypt.
        """
        if not os.path.exists(SAVEPATH):
            os.makedirs(SAVEPATH)

        Console.save_gamedata()
        filename = os.path.join(SAVEPATH, filename)
        with open(filename, 'wb') as f:
            pickle.dump(data, f)

    @staticmethod
    def delete(filename):
        """
        Delete een opgeslagen spelbestand.
        :param filename: het gekozen bestandsnaam uit de lijst
        """
        Console.delete_gamedata()
        filename = os.path.join(SAVEPATH, filename)
        os.remove(filename)
