
"""
class: GameEngine
"""

import pygame
import pygame.gfxdraw

import audio
import console
import data
import keys
import loadsave
import screens.menu.manager
import screens.overworld
import states

# todo, magic numbers overal opruimen

# todo, er gaat nog wat mis met sidestep als fps te hoog is, oorzaak onduidelijk.
FPS = 6000        # minimaal 15, anders kan hij door bomen lopen. maximaal 110, anders sidestep raar.

DEBUGFONT = 'courier'
DEBUGFONTSIZE = 11
DEBUGFONTCOLOR = pygame.Color("white")
DEBUGRECT = pygame.Rect(0, 0, 400, 600)
DEBUGRECTCOLOR = (32, 32, 32, 200)


class GameEngine(object):
    """
    De grafische weergave van het scherm. Handelt de states.
    """
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.statemachine = states.StateMachine()
        self.data = data.Data()
        self.audio = audio.Audio()

        self.running = False

        self.clock = pygame.time.Clock()
        self.playtime = 0.0
        self.dt = 0.0
        self.timer = 0.0

        self.menu_manager = screens.menu.manager.MenuManager(self)
        self.overworld = None   # todo, overworld moet self.gameplay(screen)? worden oid.

        self.debugfont = pygame.font.SysFont(DEBUGFONT, DEBUGFONTSIZE)
        self.currentstate = None
        self.key_input = None
        self.mouse_input = None

        self.loaded_save_game = None

        self.show_debug = False

    def main_loop(self):
        """
        Start de game loop.
        """
        self.running = True
        self.menu_manager.open_menu(states.MenuState.MainMenu)

        while self.running:
            self.dt = self.clock.tick(FPS)/1000.0       # limit the redraw speed to 60 frames per second
            self.playtime += self.dt

            self.currentstate = self.statemachine.peek()
            self.handle_states()
            self.handle_view()
            self.handle_audio()
            self.handle_multi_input()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_single_input(event)
            pygame.display.update()

    def handle_states(self):
        """
        Handelt de verschillende states af op verschillende voorwaarden.
        """
        if self.currentstate == states.GameState.Menu:
            self.menu_manager.loop()

        elif self.currentstate == states.GameState.Overworld:
            if self.overworld is None:
                self.overworld = screens.overworld.Overworld(self)
                if self.loaded_save_game:
                    self.load_saved_data()

    def handle_view(self):
        """
        Laat de weergave van de verschillende states zien.
        """
        if self.currentstate == states.GameState.Menu:
            self.menu_manager.handle_view(self.dt)
        elif self.currentstate == states.GameState.Overworld or \
                self.currentstate == states.GameState.PartyScreen:
            self.overworld.handle_view()

        self._show_debug()

    def handle_audio(self):
        """
        Geeft de juiste muziek en achtergrond geluiden weer.
        """
        audio_state_is_changed = self.statemachine.has_audio_state_changed()
        # self.audio.handle_music(self.currentstate, audio_state_is_changed)
        # self.audio.handle_bg_sounds(self.currentstate, audio_state_is_changed)

    def handle_multi_input(self):
        """
        Handelt de ingedrukt-houden muis en keyboard input af.
        Wordt op dit moment alleen maar gebruikt voor visuele oplichten van de buttons en character movement.
        """
        self.key_input = pygame.key.get_pressed()
        self.mouse_input = None
        if pygame.mouse.get_pressed()[0]:
            self.mouse_input = pygame.mouse.get_pos()

        if self.currentstate == states.GameState.Overworld or \
           self.currentstate == states.GameState.PartyScreen:
            self.overworld.handle_multi_input(self.key_input, self.mouse_input, self.dt)

    def handle_single_input(self, event):
        """
        Handelt de muis en keyboard input af.
        :param event: pygame.event.get()
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            console.mouse_down(event.pos, event.button)
        if event.type == pygame.KEYDOWN:
            console.keyboard_down(event.key, event.unicode)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.currentstate == states.GameState.Overworld or \
               self.currentstate == states.GameState.PartyScreen:
                self.overworld.handle_single_mouse_input(event)

        if event.type == pygame.MOUSEMOTION:
            if self.currentstate == states.GameState.PartyScreen:
                if self.overworld.partyscreen is not None:  # onverklaarbaar, anders kun je niet al muisbewegend, het
                    self.overworld.partyscreen.handle_single_mouse_motion(event)    # partyscreen verlaten.

        if event.type == pygame.KEYDOWN:
            if self.currentstate == states.GameState.Overworld or \
               self.currentstate == states.GameState.PartyScreen:
                self.overworld.handle_single_keyboard_input(event)

            if event.key == keys.DEBUG:
                self.show_debug ^= True                                             # simple boolean swith
            if event.key == keys.KILL:
                self._kill_game()                           # todo, deze, de key en de methode moeten uiteindelijk weg

        if self.currentstate == states.GameState.Menu:
            self.menu_manager.handle_single_input(event)

    def load_saved_data(self):
        """
        Laadt opgeslagen spel data.
        """
        loadsave.Dialog(self).load(self.loaded_save_game)
        self.loaded_save_game = None

    def delete_saved_data(self, savefile):
        """
        Verwijdert opgeslagen speldata.
        :param savefile: bestandsnaam die verwijdert moet worden
        """
        loadsave.Dialog(self).delete(savefile)

    @staticmethod
    def _kill_game():
        import sys
        pygame.quit()
        sys.exit()

    def _show_debug(self):
        if self.show_debug:
            text = (
                "FPS:               {:.2f}".format(self.clock.get_fps()),
                "dt:                {:.3f}".format(self.dt),
                "playtime:          {:.2f}".format(self.playtime),
                "clock:             {}".format(self.clock),
                "timer:             {}".format(self.timer),
                "",
                "currenstate:       {}".format(self.currentstate),
                "menu_cur_state:    {}".format(self.menu_manager.menu_currentstate),
                "menu_manager:      {}".format(self.menu_manager),
                "menu:              {}".format(self.menu_manager.menu),
                "overworld:         {}".format(self.overworld),
                "scr_capt:          {}".format(self.menu_manager.scr_capt),
                "cur_item:          {}".format(self.menu_manager.cur_item),
                "last_item:         {}".format(self.menu_manager.last_item),
                "mouse_input:       {}".format(self.mouse_input),
                "loaded_save_game   {}".format(self.loaded_save_game)
            )
            try:
                hero = self.overworld.window.hero
                text2 = (
                    "",
                    "partyscreen:       {}".format(self.overworld.partyscreen),
                    "",
                    "zoom:              {:.1f}".format(self.overworld.window.map1.map_layer.zoom),
                    "time_up:           {}".format(hero.time_up),
                    "time_down:         {}".format(hero.time_down),
                    "time_left:         {}".format(hero.time_left),
                    "time_right:        {}".format(hero.time_right),
                    "time_delay:        {}".format(hero.time_delay),
                    "last_direction:    {}".format(hero.last_direction),
                    "move_direction:    {}".format(hero.move_direction),
                    "movespeed:         {}".format(hero.movespeed),
                    "",
                    "old_position.x:    {}".format(hero.old_position[0]),
                    "old_position.y:    {}".format(hero.old_position[1]),
                    "",
                    "hero.rect.x:       {}".format(hero.rect.x),
                    "hero.rect.y:       {}".format(hero.rect.y),
                    "",
                    "true_position.x:   {}".format(hero.true_position[0]),
                    "true_position.y:   {}".format(hero.true_position[1]),
                    "",
                    "step_count:        {}".format(hero.step_count),
                    "step_animation:    {}".format(hero.step_animation)
                )
                text += text2
            except AttributeError:
                pass
            try:
                import screens.party.invclickbox
                text3 = (
                    "",
                    "max_box_height     {}".format(screens.party.invclickbox.MAXBOXHEIGHT),
                    "layer_height       {}".format(self.overworld.partyscreen.invclick_box.layer_height)
                )
                text += text3
            except AttributeError:
                pass
            text4 = (
                "",
                "StateStack:",
                ""
            )
            textb = []
            for state in self.statemachine.statestack:
                textb.append(str(state))
            textb.reverse()
            text4 += tuple(textb)
            text4 += (
                "",
                "Menu StateStack:",
                ""
            )
            textb = []
            for state in self.menu_manager.menu_statemachine.statestack:
                textb.append(str(state))
            textb.reverse()
            text4 += tuple(textb)
            text += text4

            pygame.gfxdraw.box(self.screen, DEBUGRECT, DEBUGRECTCOLOR)
            for count, line in enumerate(text):
                self.screen.blit(self.debugfont.render(line, True, DEBUGFONTCOLOR).convert_alpha(), (0, count * 10))
