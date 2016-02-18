
"""
class: GameEngine
"""

import pygame
import pygame.gfxdraw

import audio
import console
import data
import screens.menu.content
import screens.menu.display
import screens.loadsave
import screens.overworld
import states

# todo, magic numbers overal opruimen

# todo, er gaat nog wat mis met sidestep als fps te hoog is, oorzaak onduidelijk.
FPS = 60        # minimaal 15, anders kan hij door bomen lopen. maximaal 110, anders sidestep raar.

DEBUGKEY = pygame.K_F12
DEBUGFONT = 'courier'
DEBUGFONTSIZE = 11
DEBUGFONTCOLOR = pygame.Color("white")
DEBUGRECT = (0, 0, 600, 400)
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

        self.mainmenu = None
        self.pausemenu = None
        self.optionsmenu = None
        self.overworld = None

        self.debugfont = pygame.font.SysFont(DEBUGFONT, DEBUGFONTSIZE)
        self.currentstate = None
        self.key_input = None
        self.mouse_input = None
        self.scr_capt = None

        self.show_debug = False

    def main_loop(self):
        """
        Start de game loop.
        """
        self.running = True
        self._show_main_menu()

        while self.running:
            self.dt = self.clock.tick(FPS)/1000.0       # limit the redraw speed to 60 frames per second
            self.playtime += self.dt

            self.currentstate = self.statemachine.peek()
            self.handle_view()
            self.handle_multi_input()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_single_input(event)
            pygame.display.flip()

    def handle_view(self):
        """
        Laat de weergave van de verschillende states zien.
        """
        def _show_debug():
            if self.show_debug:
                text = (
                    "FPS:               {:.2f}".format(self.clock.get_fps()),
                    "dt:                {:.3f}".format(self.dt),
                    "playtime:          {:.2f}".format(self.playtime),
                    "",
                    "currenstate:       {}".format(self.currentstate),
                    "mainmenu:          {}".format(self.mainmenu),
                    "pausemenu:         {}".format(self.pausemenu),
                    "optionsmenu:       {}".format(self.optionsmenu),
                    "overworld:         {}".format(self.overworld),
                    "scr_capt:          {}".format(self.scr_capt),
                    "mouse_input:       {}".format(self.mouse_input)
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
                pygame.gfxdraw.box(self.screen, pygame.Rect(DEBUGRECT), DEBUGRECTCOLOR)
                for count, line in enumerate(text):
                    self.screen.blit(self.debugfont.render(line, True, DEBUGFONTCOLOR), (0, count * 10))

        if self.currentstate == states.GameState.MainMenu:
            self.mainmenu.handle_view()                         # geen achtergrond
        elif self.currentstate == states.GameState.OptionsMenu:
            self.optionsmenu.handle_view()
        elif self.currentstate == states.GameState.PauseMenu:
            self.pausemenu.handle_view(self.scr_capt)           # achtergrond, screen capture
        elif self.currentstate == states.GameState.Overworld or \
                self.currentstate == states.GameState.PartyScreen:
            self.overworld.handle_view()

        _show_debug()

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

            if self.currentstate == states.GameState.Overworld or \
               self.currentstate == states.GameState.PartyScreen:
                self.overworld.handle_single_mouse_input(event)

        if event.type == pygame.MOUSEMOTION:
            if self.currentstate == states.GameState.PartyScreen:
                if self.overworld.partyscreen is not None:  # onverklaarbaar, anders kun je niet al muisbewegend, het
                    self.overworld.partyscreen.handle_single_mouse_motion(event)  # partyscreen verlaten.

        if event.type == pygame.KEYDOWN:
            console.keyboard_down(event.key, event.unicode)

            if self.currentstate == states.GameState.Overworld or \
               self.currentstate == states.GameState.PartyScreen:
                self.overworld.handle_single_keyboard_input(event)

            if event.key == DEBUGKEY:
                self.show_debug ^= True                                     # simple boolean swith
            if event.key == pygame.K_BACKSPACE:
                self._kill_game()                           # todo, deze en de methode moeten uiteindelijk weg
            if event.key == pygame.K_ESCAPE:
                if self.currentstate == states.GameState.MainMenu:          # eerst de keys op het toetsenbord
                    self._main_menu_select_exit_game(with_esc=True)
                    return                                                  # returns, want anders zitten ze
                elif self.currentstate == states.GameState.OptionsMenu:     # de menu's in de weg
                    self._options_menu_select_back(with_esc=True)
                    return
                elif self.currentstate == states.GameState.PauseMenu:
                    self._pause_menu_select_continue(with_esc=True)
                    return
                elif self.currentstate == states.GameState.Overworld:
                    self._show_pause_menu()
                    return

        self._handle_menu_input(event)                                      # dan de menu's

    def _handle_menu_input(self, full_event):

        if self.currentstate == states.GameState.MainMenu:
            menu_keys = screens.menu.content.MainMenu()
            menu_choice = self.mainmenu.handle_single_input(full_event)
            if menu_choice == menu_keys.NewGame:
                self._main_menu_select_new_game()
            elif menu_choice == menu_keys.LoadGame:
                self._main_menu_select_load_game()
            elif menu_choice == menu_keys.Options:
                self._main_menu_select_options()
            elif menu_choice == menu_keys.ExitGame:
                self._main_menu_select_exit_game()
            return

        elif self.currentstate == states.GameState.OptionsMenu:
            menu_keys = screens.menu.content.OptionsMenu()
            menu_choice = self.optionsmenu.handle_single_input(full_event)
            if menu_choice == menu_keys.Music:                             # .Music geeft de key "Music"
                self._options_menu_select_music()
            elif menu_choice == menu_keys.Sound:
                self._options_menu_select_sound()
            elif menu_choice == menu_keys.Back:
                self._options_menu_select_back()
            return

        elif self.currentstate == states.GameState.PauseMenu:
            menu_keys = screens.menu.content.PauseMenu()
            menu_choice = self.pausemenu.handle_single_input(full_event)
            if menu_choice == menu_keys.ContinueGame:
                self._pause_menu_select_continue()
            elif menu_choice == menu_keys.SaveGame:
                self._pause_menu_select_save_game()
            elif menu_choice == menu_keys.MainMenu:
                self._pause_menu_select_main_menu()
            return

    def _show_main_menu(self):
        self.pausemenu = None
        self.scr_capt = None
        self.overworld = None
        self.statemachine.clear()
        self.statemachine.push(states.GameState.MainMenu)
        menu_items = screens.menu.content.MainMenu()
        self.mainmenu = screens.menu.display.Display(self.screen, self.audio, menu_items, True)
        self.audio.play_music(self.audio.mainmenu)

    def _main_menu_select_new_game(self):
        self.mainmenu = None
        self.statemachine.pop(self.currentstate)
        self.statemachine.push(states.GameState.Overworld)
        self.overworld = screens.overworld.Overworld(self)
        self.audio.play_music(self.audio.overworld)

    def _main_menu_select_load_game(self):
        dialog = screens.loadsave.Dialog(self)
        self.overworld = screens.overworld.Overworld(self)                      # laad de overworld alvast
        if dialog.load() is None:
            self.overworld = None                                               # toch niet
        else:                                                                   # geef dan data mee aan de overworld
            self.audio.play_sound(self.audio.select)
            self.mainmenu = None
            self.statemachine.pop(self.currentstate)
            self.statemachine.push(states.GameState.Overworld)
            self.audio.play_music(self.audio.overworld)
        pygame.event.clear()

    def _main_menu_select_options(self):
        self._show_options_menu()

    def _main_menu_select_exit_game(self, with_esc=False):
        if with_esc:
            self.audio.play_sound(self.audio.select)
        self.audio.fade_music()
        self.running = False

    def _show_options_menu(self):
        self.statemachine.push(states.GameState.OptionsMenu)
        menu_items = screens.menu.content.OptionsMenu(self.audio.music, self.audio.sound)  # hier worden de weergave van
        self.optionsmenu = screens.menu.display.Display(self.screen, self.audio, menu_items, True)    # options gekozen

    def _options_menu_select_music(self):
        settingview = self.optionsmenu.menu_texts[self.optionsmenu.cur_item]        # hier wordt de weergave
        if self.audio.music == 1:
            settingview.text = settingview.text.replace("On", "Off")                # later aangepast
            self.audio.music = 0                                                    # en de instelling zelf aangepast
            self.audio.stop_music()
        else:
            settingview.text = settingview.text.replace("Off", "On")
            self.audio.music = 1
            self.audio.play_music(self.audio.mainmenu)
        self.audio.write_cfg()                                                      # en weggeschreven

    def _options_menu_select_sound(self):
        settingview = self.optionsmenu.menu_texts[self.optionsmenu.cur_item]
        if self.audio.sound == 1:
            self.audio.stop_sound(self.audio.select)    # vanwege de enter knop in menu's speelt hij dit geluid af
            settingview.text = settingview.text.replace("On", "Off")    # stop hem daarom alsnog.
            self.audio.sound = 0
        else:
            settingview.text = settingview.text.replace("Off", "On")
            self.audio.sound = 1
            self.audio.play_sound(self.audio.select)    # en speel weer een geluid af omdat er geluid is.
        self.audio.write_cfg()

    def _options_menu_select_back(self, with_esc=False):
        if with_esc:
            self.audio.play_sound(self.audio.select)
        self.statemachine.pop(self.currentstate)
        self.optionsmenu = None

    def _show_pause_menu(self):
        self.audio.play_sound(self.audio.select)
        self.audio.fade_music()
        scr_data = pygame.image.tostring(self.screen, 'RGBA')   # maak een screen capture
        self.scr_capt = pygame.image.frombuffer(scr_data, self.screen.get_size(), 'RGBA')
        self.statemachine.push(states.GameState.PauseMenu)
        menu_items = screens.menu.content.PauseMenu()
        self.pausemenu = screens.menu.display.Display(self.screen, self.audio, menu_items, False)

    def _pause_menu_select_continue(self, with_esc=False):
        if with_esc:
            self.audio.play_sound(self.audio.select)            # omdat escape in menu standaard geen geluid geeft
        self.statemachine.pop(self.currentstate)
        self.pausemenu = None
        self.scr_capt = None
        self.audio.play_music(self.audio.overworld)

    def _pause_menu_select_save_game(self):
        dialog = screens.loadsave.Dialog(self)
        if dialog.save():
            self.audio.play_sound(self.audio.select)
        pygame.event.clear()                                    # anders stapelen de geluiden zich op

    def _pause_menu_select_main_menu(self):
        self._show_main_menu()

    @staticmethod
    def _kill_game():
        import sys
        pygame.quit()
        sys.exit()
