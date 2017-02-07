
"""
def: main
"""

import os
import sys

import pygame

import engine

# todo, variabele resolutie maken
SCREENWIDTH = 1366
SCREENHEIGHT = 768  # 1366, 768  # 1920, 1080

TITLE = 'pyRPG2'
ICONPATH = 'resources\sprites\icons\skills\warrior.png'


def main():
    """
    Prepare our environment, create a display, and start the program.
    """
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()
    pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_icon(pygame.image.load(ICONPATH).convert_alpha())
    pygame.display.set_caption(TITLE)
    game = engine.GameEngine()
    game.on_enter()
    game.main_loop()
    # game.on_exit()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
