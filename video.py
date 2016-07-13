
"""
class: Video
"""

import os
import pickle

import pygame

from console import Console

OPTIONSPATH = 'options'
OPTIONSFILE = os.path.join(OPTIONSPATH, 'video.cfg')


class Video(object):
    """
    Video instellingen.
    """
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.fullscreen = False
        self._load_cfg()

        if self.fullscreen:
            pygame.display.set_mode((self.screen.get_size()),
                                    pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
        else:
            pygame.display.set_mode(self.screen.get_size())

    def _load_cfg(self):
        """
        Laad settings uit config bestand.
        """
        if not os.path.exists(OPTIONSPATH):
            os.makedirs(OPTIONSPATH)

        try:
            with open(OPTIONSFILE, 'rb') as f:
                self.fullscreen = pickle.load(f)
            Console.load_options()
        except (pickle.UnpicklingError, FileNotFoundError, EOFError):
            Console.corrupt_options()
            self.fullscreen = False
            self.write_cfg()

    def write_cfg(self):
        """
        Schrijf settings naar config bestand.
        """
        with open(OPTIONSFILE, 'wb') as f:
            pickle.dump(self.fullscreen, f)
        Console.write_options()

    def flip_fullscreen(self):
        """
        Zet fullscreen aan als het uit staat en vice versa.
        """
        if self.fullscreen:
            pygame.display.set_mode(self.screen.get_size())
        else:
            pygame.display.set_mode((self.screen.get_size()),
                                    pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
        self.fullscreen ^= True
