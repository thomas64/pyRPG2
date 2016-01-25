
"""..."""

import os
import sys

import pygame

import game

SCREENWIDTH = 1600
SCREENHEIGHT = 800  # 1600, 800  # 1920, 1080


def main():
    """
    Prepare our environment, create a display, and start the program.
    """
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()
    pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), pygame.NOFRAME)  # | pygame.FULLSCREEN)
    game.GameEngine().main_loop()
    # exit
    game.GameEngine().music.current.fadeout(1000)
    pygame.time.delay(1000)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
