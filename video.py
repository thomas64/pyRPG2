
"""
class: Video
"""

import os
import pickle

import pygame

from console import Console

SETTINGSPATH = 'settings'
SETTINGSFILE = os.path.join(SETTINGSPATH, 'video.cfg')


class Video(object):
    """
    Video instellingen.
    """
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.fullscreen = False
        self.window_frame = True
        self._load_cfg()

        if self.fullscreen:
            pygame.display.set_mode((self.screen.get_size()),
                                    pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
        else:
            if self.window_frame:
                pygame.display.set_mode(self.screen.get_size())
            else:
                pygame.display.set_mode((self.screen.get_size()), pygame.NOFRAME)

    def _load_cfg(self):
        """
        Laad settings uit config bestand.
        """
        if not os.path.exists(SETTINGSPATH):
            os.makedirs(SETTINGSPATH)

        try:
            with open(SETTINGSFILE, 'rb') as f:
                self.fullscreen, self.window_frame = pickle.load(f)
            Console.load_settings()
        except (pickle.UnpicklingError, FileNotFoundError, EOFError, TypeError):
            Console.corrupt_settings()
            self.fullscreen = False
            self.window_frame = True
            self.write_cfg()

    def write_cfg(self):
        """
        Schrijf settings naar config bestand.
        """
        with open(SETTINGSFILE, 'wb') as f:
            pickle.dump([self.fullscreen, self.window_frame], f)
        Console.write_settings()

    def flip_fullscreen(self):
        """
        Zet fullscreen aan als het uit staat en vice versa.
        """
        if self.fullscreen:
            if self.window_frame:
                pygame.display.set_mode(self.screen.get_size())
            else:
                pygame.display.set_mode((self.screen.get_size()), pygame.NOFRAME)
        else:
            pygame.display.set_mode((self.screen.get_size()),
                                    pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
        self.fullscreen ^= True

    def flip_window_frame(self):
        """..."""
        if not self.fullscreen:
            if self.window_frame:
                pygame.display.set_mode((self.screen.get_size()), pygame.NOFRAME)
            else:
                pygame.display.set_mode(self.screen.get_size())

        self.window_frame ^= True
