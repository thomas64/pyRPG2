
"""
class: GameEngine
"""

import pygame

import gamemenu
import music
import overworld
import sound
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
        self.sound = sound.Sound()

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

        self.show_debug = False

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
        def show_debug():
            """
            Geeft debug informatie weer linksboven in het scherm.
            """
            if self.show_debug:
                # hero = self.overworld.hero
                text = ("FPS:              {:.2f}".format(self.clock.get_fps()),
                        "dt:               {:.3f}".format(self.dt),
                        "playtime:         {:.2f}".format(self.playtime),
                        # "time_up:          {}".format(hero.time_up),
                        # "time_down:        {}".format(hero.time_down),
                        # "time_left:        {}".format(hero.time_left),
                        # "time_right:       {}".format(hero.time_right),
                        # "time_delay:       {}".format(hero.time_delay),
                        # "last_direction:   {}".format(hero.last_direction),
                        # "move_direction:   {}".format(hero.move_direction),
                        # "movespeed:        {}".format(hero.movespeed),
                        # "old_position.x:   {}".format(hero.old_position[0]),
                        # "old_position.y:   {}".format(hero.old_position[1]),
                        # "new_position.x:   {}".format(hero.rect.x),
                        # "new_position.y:   {}".format(hero.rect.y),
                        # "true_position.x:  {}".format(hero.true_position[0]),
                        # "true_position.y:  {}".format(hero.true_position[1]),
                        # "step_count:       {}".format(hero.step_count),
                        # "step_animation:   {}".format(hero.step_animation),
                        )
                for count, line in enumerate(text):
                    self.screen.blit(self.debugfont.render(line, True, DEBUGFONTCOLOR), (0, count * 10))

        if currentstate == statemachine.State.MainMenu:
            self.mainmenu.handle_view(None)                 # geen achtergrond
            show_debug()
        elif currentstate == statemachine.State.PauseMenu:
            self.pausemenu.handle_view(self.scr_capt)       # achtergrond, screen capture
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
            self.overworld.handle_multi_input(self.key_input, self.dt)

    def handle_single_input(self, event, currentstate):
        """
        Handelt de muis en keyboard input af.
        :param event: pygame.event.get()
        :param currentstate: bovenste state van de stack
        """
        if event.type == pygame.KEYDOWN:
            print("Keyboard, key={}, unicode={}".format(event.key, event.unicode))

            if currentstate == statemachine.State.MainMenu:
                menu_choice = self.mainmenu.handle_single_input(event)
                if event.key == pygame.K_F12:
                    self.show_debug ^= True             # simple boolean swith
                elif menu_choice == gamemenu.MainMenuItem.ExitGame:
                    self.running = False
                elif menu_choice == gamemenu.MainMenuItem.NewGame:
                    self.state.pop(currentstate)
                    self.state.push(statemachine.State.OverWorld)
                    self.overworld = overworld.OverWorld(self.screen)
                elif menu_choice == gamemenu.MainMenuItem.LoadGame:
                    # todo, loadgame
                    pass

            elif currentstate == statemachine.State.PauseMenu:
                menu_choice = self.pausemenu.handle_single_input(event)
                if event.key == pygame.K_ESCAPE:
                    self.state.pop(currentstate)
                elif menu_choice == gamemenu.PauseMenuItem.ContinueGame:
                    self.state.pop(currentstate)
                elif menu_choice == gamemenu.PauseMenuItem.MainMenu:
                    self.state.clear()
                    self.overworld = None
                    self.state.push(statemachine.State.MainMenu)
                elif menu_choice == gamemenu.PauseMenuItem.SaveGame:
                    # todo, savegame
                    pass

            elif currentstate == statemachine.State.OverWorld:
                self.overworld.handle_single_input(event)
                if event.key == pygame.K_ESCAPE:
                    self.sound.select.play()
                    data = pygame.image.tostring(self.screen, 'RGBA')       # maak een screen capture
                    self.scr_capt = pygame.image.frombuffer(data, self.screen.get_size(), 'RGBA')
                    self.state.push(statemachine.State.PauseMenu)
                    self.pausemenu = gamemenu.GameMenu(self.screen, gamemenu.PauseMenuItem, False)
                if event.key == pygame.K_BACKSPACE:                         # todo, deze moet uiteindelijk weg
                    import sys
                    sys.exit()
