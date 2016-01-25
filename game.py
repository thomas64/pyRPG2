
"""
class: GameEngine
"""

import pygame

import gamemenu
import music
import overworld
import statemachine

FPS = 60

DEBUGFONT = 'courier'
DEBUGFONTSIZE = 11
DEBUGFONTCOLOR = pygame.Color("white")


class GameEngine(object):
    """
    De grafische weergave van het scherm.
    """
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.state = statemachine.StateMachine()
        self.music = music.Music()

        self.mainmenu = None
        self.pausemenu = None
        self.overworld = None

        self.running = False

        self.clock = pygame.time.Clock()
        self.playtime = 0.0
        self.dt = 0.0
        self.timer = 0.0

        self.debugfont = pygame.font.SysFont(DEBUGFONT, DEBUGFONTSIZE)
        self.key_input = None
        self.scr_capt = None

        self.show_debug = True

    def main_loop(self):
        """
        Start de game loop.
        """
        self.running = True
        self.state.push(statemachine.State.MainMenu)
        self.mainmenu = gamemenu.GameMenu(self.screen, gamemenu.MainMenuItem, True)

        while self.running:
            self.dt = self.clock.tick(FPS)/1000.0       # limit the redraw speed to 60 frames per second
            self.playtime += self.dt

            currentstate = self.state.peek()
            self.handle_view(currentstate)
            self.handle_music(currentstate)
            self.handle_multi_input(currentstate)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_single_input(event, currentstate)
            pygame.display.flip()

    def handle_view(self, currentstate):
        """
        Laat de weergave van de verschillende states zien.
        :param currentstate: bovenste state van de stack
        """
        if currentstate == statemachine.State.MainMenu:
            self.mainmenu.handle_view(None)                 # geen achtergrond
        elif currentstate == statemachine.State.PauseMenu:
            self.pausemenu.handle_view(self.scr_capt)       # achtergrond, screen capture
        elif currentstate == statemachine.State.OverWorld:
            self.overworld.handle_view()

        """
        Geeft debug informatie weer linksboven in het scherm.
        """
        if self.show_debug:
            text = ("FPS:              {:.2f}".format(self.clock.get_fps()),
                    "dt:               {:.2f}".format(self.dt),
                    "playtime:         {:.2f}".format(self.playtime),
                    )
            for count, line in enumerate(text):
                self.screen.blit(self.debugfont.render(line, True, DEBUGFONTCOLOR), (0, count * 10))

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
        if event.type == pygame.KEYDOWN:
            print("Keyboard, key={}, unicode={}".format(event.key, event.unicode))

            if currentstate == statemachine.State.MainMenu:
                menu_choice = self.mainmenu.handle_input(event)
                if menu_choice == gamemenu.MainMenuItem.ExitGame:
                    self.running = False
                elif menu_choice == gamemenu.MainMenuItem.NewGame:
                    self.state.pop(currentstate)
                    self.state.push(statemachine.State.OverWorld)
                    self.overworld = overworld.OverWorld(self.screen)
                elif menu_choice == gamemenu.MainMenuItem.LoadGame:
                    pass

            elif currentstate == statemachine.State.PauseMenu:
                menu_choice = self.pausemenu.handle_input(event)
                if event.key == pygame.K_ESCAPE:
                    self.state.pop(currentstate)
                elif menu_choice == gamemenu.PauseMenuItem.ContinueGame:
                    self.state.pop(currentstate)
                elif menu_choice == gamemenu.PauseMenuItem.MainMenu:
                    self.state.clear()
                    self.overworld = None
                    self.state.push(statemachine.State.MainMenu)
                elif menu_choice == gamemenu.PauseMenuItem.SaveGame:
                    pass

            elif currentstate == statemachine.State.OverWorld:
                if event.key == pygame.K_ESCAPE:
                    data = pygame.image.tostring(self.screen, 'RGBA')       # maak een screen capture
                    self.scr_capt = pygame.image.frombuffer(data, self.screen.get_size(), 'RGBA')
                    self.state.push(statemachine.State.PauseMenu)
                    self.pausemenu = gamemenu.GameMenu(self.screen, gamemenu.PauseMenuItem, False)
