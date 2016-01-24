
"""
class: GameEngine
"""

import os
import time

import pygame

import mainmenu
import music
import overworld
import statemachine

SCREENWIDTH = 1600
SCREENHEIGHT = 800  # 1600, 800  # 1920, 1080

FPS = 60


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
        self.music = music.Music()

        # todo, moeten deze niet pas geladen worden wanneer ze echt nodig zijn?
        self.mainmenu = mainmenu.MainMenu(self.screen)
        self.overworld = overworld.OverWorld(self.screen)

        self.running = False

        self.clock = pygame.time.Clock()
        self.playtime = 0
        self.milliseconds = 0
        self.timer = 0

        self.key_input = None

    def run(self):
        """
        Start de game loop.
        """
        self.running = True
        self.state.push(statemachine.State.MainMenu)

        while self.running:
            self.milliseconds = self.clock.tick(FPS)        # limit the redraw speed to 60 frames per second
            self.playtime += self.milliseconds / 1000

            currentstate = self.state.peek()
            self.handle_view(currentstate)
            self.handle_music(currentstate)
            self.handle_multi_input(currentstate)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_single_input(event, currentstate)

            pygame.display.set_caption("FPS: {:.2f}, time: {:.2f} seconds".format(self.clock.get_fps(), self.playtime))
            pygame.display.flip()

        self.music.current.fadeout(1000)
        time.sleep(1)
        pygame.quit()

    def handle_view(self, currentstate):
        """
        Laat de weergave van de verschillende states zien.
        :param currentstate: bovenste state van de stack
        """
        if currentstate == statemachine.State.MainMenu:
            self.mainmenu.handle_view()
        elif currentstate == statemachine.State.OverWorld:
            self.overworld.handle_view()

    def handle_music(self, currentstate):
        """
        Handelt het spelen van muziek af.
        :param currentstate: bovenste state van de stack
        """
        self.music.play(currentstate)

    def handle_multi_input(self, currentstate):
        """
        Handelt de ingedrukt-houden muis en keyboard input af.
        :param currentstate: bovenste state van de stack
        """
        self.key_input = pygame.key.get_pressed()

        if currentstate == statemachine.State.OverWorld:
            self.overworld.handle_multi_input(self.key_input)

    def handle_single_input(self, event, currentstate):
        """
        Handelt de muis en keyboard input af.
        :param event: pygame.event.get()
        :param currentstate: bovenste state van de stack
        """
        if currentstate == statemachine.State.MainMenu:
            menu_choice = self.mainmenu.handle_input(event)
            if menu_choice == mainmenu.MenuItem.ExitGame:
                self.running = False
            elif menu_choice == mainmenu.MenuItem.NewGame:
                self.state.pop(currentstate)
                self.state.push(statemachine.State.OverWorld)
            elif menu_choice == mainmenu.MenuItem.LoadGame:
                pass
