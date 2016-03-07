
"""
class: GameEngine
"""

import pygame
import pygame.gfxdraw

import audio
import console
import data
import keys
import screens.menu.manager
import states

# todo, magic numbers overal opruimen

# todo, er gaat nog wat mis met sidestep als fps te hoog is, oorzaak onduidelijk.
# minimaal 15, anders kan hij door bomen lopen. maximaal 110, anders sidestep raar.
FPS = 6000

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
        self.data = data.Data()
        self.audio = audio.Audio()

        self.running = False

        self.clock = pygame.time.Clock()
        self.playtime = 0.0
        self.dt = 0.0
        self.timer = 0.0

        self.gamestate = states.StateMachine()

        self.debugfont = pygame.font.SysFont(DEBUGFONT, DEBUGFONTSIZE)
        self.key_input = None
        self.mouse_input = None

        self.show_debug = False

    def main_loop(self):
        """
        Start de game loop.
        """
        self.running = True
        push_object = screens.menu.manager.create_menu(screens.menu.manager.MenuItems.MainMenu, self)
        self.gamestate.push(push_object)

        while self.running:
            # limit the redraw speed to 60 frames per second
            self.dt = self.clock.tick(FPS)/1000.0
            self.playtime += self.dt

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.single_input(event)
            self.multi_input()
            self.update()
            self.render()
            pygame.display.update()

    def single_input(self, event):
        """
        Handelt de muis en keyboard input af.
        :param event: pygame.event.get()
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            console.mouse_down(event.pos, event.button)
        if event.type == pygame.KEYDOWN:
            console.keyboard_down(event.key, event.unicode)

            if event.key == keys.DEBUG:
                # simple boolean swith
                self.show_debug ^= True
            if event.key == keys.KILL:
                # todo, deze, de key en de methode moeten uiteindelijk weg
                self._kill_game()

        self.gamestate.peek().single_input(event)

    def multi_input(self):
        """
        Handelt de ingedrukt-houden muis en keyboard input af.
        Wordt op dit moment alleen maar gebruikt voor visuele oplichten van de buttons en character movement.
        """
        self.key_input = pygame.key.get_pressed()
        self.mouse_input = None
        if pygame.mouse.get_pressed()[0]:
            self.mouse_input = pygame.mouse.get_pos()

        self.gamestate.peek().multi_input(self.key_input, self.mouse_input, self.dt)

    def update(self):
        """
        Update de waarden van de bovenste state.
        """
        self.gamestate.peek().update(self.dt)

    def render(self):
        """
        Laat de weergave van de bovenste states zien.
        En de debugscherm.
        """
        self.gamestate.peek().render()
        self._show_debug()

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
                "timer:             {}".format(self.timer),
                "",
                "mouse_input:       {}".format(self.mouse_input),
                ""
            )
            try:
                text2 = (
                    "menu_name:         {}".format(self.gamestate.peek().name),
                    "cur_item:          {}".format(self.gamestate.peek().cur_item),
                    "scr_capt:          {}".format(self.gamestate.peek().scr_capt)
                )
                text += text2
            except AttributeError:
                pass
            try:
                hero = self.gamestate.peek().window.hero
                text2 = (
                    "zoom:              {:.1f}".format(self.gamestate.peek().window.map1.map_layer.zoom),
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
                text2 = (
                    "",
                    "max_box_height     {}".format(screens.party.invclickbox.MAXBOXHEIGHT),
                    "layer_height       {}".format(self.gamestate.peek().invclick_box.layer_height)
                )
                text += text2
            except AttributeError:
                pass
            text2 = (
                "",
                "StateStack:",
                ""
            )
            textb = []
            for state in self.gamestate.statestack:
                textb.append(str(state))
            textb.reverse()
            text2 += tuple(textb)
            text += text2

            pygame.gfxdraw.box(self.screen, DEBUGRECT, DEBUGRECTCOLOR)
            for count, line in enumerate(text):
                self.screen.blit(self.debugfont.render(line, True, DEBUGFONTCOLOR).convert_alpha(), (0, count * 10))
