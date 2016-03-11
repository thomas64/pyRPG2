
"""
class: Video
"""

import os
import pickle

import pygame

import console

OPTIONSPATH = 'options'
OPTIONSFILE = os.path.join(OPTIONSPATH, 'video.cfg')


class Video(object):
    """
    Video instellingen.
    """
    def __init__(self, engine):
        self.engine = engine
        self.fullscreen = False
        self._load_cfg()

        if self.fullscreen:
            pygame.display.set_mode((self.engine.screen.get_size()),
                                    pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
        else:
            pygame.display.set_mode(self.engine.screen.get_size())

    def _load_cfg(self):
        """
        Laad settings uit config bestand.
        """
        if not os.path.exists(OPTIONSPATH):
            os.makedirs(OPTIONSPATH)

        try:
            with open(OPTIONSFILE, 'rb') as f:
                self.fullscreen = pickle.load(f)
        except (pickle.UnpicklingError, FileNotFoundError, EOFError):
            console.corrupt_options()
            self.fullscreen = False
            self.write_cfg()

    def write_cfg(self):
        """
        Schrijf settings naar config bestand.
        """
        with open(OPTIONSFILE, 'wb') as f:
            pickle.dump(self.fullscreen, f)

    def flip_fullscreen(self):
        """
        Zet fullscreen aan als het uit staat en vice versa.
        """
        if self.fullscreen:
            pygame.display.set_mode(self.engine.screen.get_size())
        else:
            pygame.display.set_mode((self.engine.screen.get_size()),
                                    pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
        self.fullscreen ^= True
