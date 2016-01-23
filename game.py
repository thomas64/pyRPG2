
"""
class: GameEngine
"""

import os
import time

import pygame

import mainmenu
import statemachine

SCREENWIDTH = 1600
SCREENHEIGHT = 800  # 1600, 800  # 1920, 1080

FPS = 60

MENUMUSIC = os.path.join('resources/sounds', 'mainmenu_music.ogg')


class GameEngine(object):
    """
    De grafische weergave van het scherm.
    """
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))  # , pygame.NOFRAME | pygame.FULLSCREEN)

        self.state = statemachine.StateMachine()
        self.mainmenu = mainmenu.MainMenu(self.screen)

        self.running = False

        self.clock = pygame.time.Clock()
        self.playtime = 0
        self.milliseconds = 0
        self.timer = 0

    def run(self):
        """
        Start de game loop.
        """
        self.running = True
        self.state.push(statemachine.State.MainMenu)
        pygame.mixer.music.load(MENUMUSIC)
        pygame.mixer.music.play(-1)

        while self.running:
            self.milliseconds = self.clock.tick(FPS)        # limit the redraw speed to 60 frames per second
            self.playtime += self.milliseconds / 1000

            currentstate = self.state.peek()
            self.handle_view(currentstate)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_single_input(event, currentstate)

            pygame.display.set_caption("FPS: {:.2f}, time: {:.2f} seconds".format(self.clock.get_fps(), self.playtime))
            pygame.display.flip()

        pygame.quit()

    def handle_view(self, currentstate):
        """
        Laat de weergave van de verschillende states zien.
        :param currentstate: bovenste state van de stack
        """
        if currentstate == statemachine.State.MainMenu:
            self.mainmenu.handle_view()

    def handle_single_input(self, event, currentstate):
        """
        Handelt de muis en keyboard input af.
        :param event: pygame.event.get()
        :param currentstate: bovenste state van de stack
        """
        if currentstate == statemachine.State.MainMenu:
            if self.mainmenu.handle_input(event) == mainmenu.MenuItem.ExitGame:
                pygame.mixer.music.fadeout(1000)
                time.sleep(1)
                self.running = False
