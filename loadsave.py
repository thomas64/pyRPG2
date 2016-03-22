
"""
class: Dialog
"""

import os
import pickle

import console

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
            console.load_gamedata()
            with open(filename, 'rb') as f:
                (self.engine.data,
                 self.engine.gamestate.peek().window.map1.name,
                 self.engine.gamestate.peek().window.map1.tmxpath,
                 self.engine.gamestate.peek().window.heroes[0].rect.topleft,
                 self.engine.gamestate.peek().window.heroes[0].last_direction) = pickle.load(f)
                self.engine.gamestate.peek().window.new_map(self.engine.gamestate.peek().window.map1.name,
                                                            self.engine.gamestate.peek().window.map1.tmxpath,
                                                            self.engine.gamestate.peek().window.heroes[0].rect.topleft,
                                                            self.engine.gamestate.peek().window.heroes[0].last_direction
                                                            )
        except (pickle.UnpicklingError, EOFError):
            console.corrupt_gamedata()

    def save(self, filename):
        """
        Save de voortgang naar een bestand.
        :param filename: het gekozen bestandsnaam uit de lijst of ingetypt.
        """
        console.save_gamedata()
        filename = os.path.join(SAVEPATH, filename)
        with open(filename, 'wb') as f:
            # deep_peek(-3) moet, omdat normaal peek() niet werkt, er zitten twee lagen erboven op de stack.
            pickle.dump([self.engine.data,
                         self.engine.gamestate.deep_peek(-3).window.map1.name,
                         self.engine.gamestate.deep_peek(-3).window.map1.tmxpath,
                         self.engine.gamestate.deep_peek(-3).window.heroes[0].rect.topleft,
                         self.engine.gamestate.deep_peek(-3).window.heroes[0].last_direction], f)

    @staticmethod
    def delete(filename):
        """
        Delete een opgeslagen spelbestand.
        :param filename: het gekozen bestandsnaam uit de lijst
        """
        console.delete_gamedata()
        filename = os.path.join(SAVEPATH, filename)
        os.remove(filename)
