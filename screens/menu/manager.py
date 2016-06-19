
"""
def: create_menu
"""

from components import ScreenCapture
import screens.menu.animation
import screens.menu.display
import screens.menu.mainmenu
import screens.menu.loadmenu
import screens.menu.savemenu
import screens.menu.optionsmenu
import screens.menu.pausemenu
import screens.menu.title
import statemachine

# todo, fade out mogelijk maken voor LoadMenu vanuit MainMenu? in bijv on_enter met for i, transp.


def create_menu(state_name, engine, title=None, animation=None, scr_capt=None, select=None):
    """
    Hier worden de verschillende eigenschappen van de verschillende menu's toegekend.
    :param state_name: Enum state name
    :param engine: self van GameEngine
    :param title: menu Title Object
    :param animation: een dict van afbeeldingen
    :param scr_capt: een afbeelding
    :param select: de voorgeslecteerde item
    """
    content = None

    if state_name == statemachine.States.MainMenu:
        content = screens.menu.mainmenu.MainMenu(engine)
        title = screens.menu.title.Title()
        animation = screens.menu.animation.Animation()
        scr_capt = None
        if select is None:
            select = 0

    elif state_name == statemachine.States.LoadMenu:
        content = screens.menu.loadmenu.LoadMenu(engine)
        title = screens.menu.title.Title(title=None, sub=statemachine.States.LoadMenu.value)
        animation = None
        if scr_capt is None:
            scr_capt = None
        if select is None:
            select = -1

    elif state_name == statemachine.States.SaveMenu:
        content = screens.menu.savemenu.SaveMenu(engine)
        title = screens.menu.title.Title(title=None, sub=statemachine.States.SaveMenu.value)
        animation = None
        if scr_capt is None:
            scr_capt = None
        if select is None:
            select = -1

    elif state_name == statemachine.States.OptionsMenu:
        content = screens.menu.optionsmenu.OptionsMenu(engine)
        if title is None:
            title = None
        if animation is None:
            animation = None
        if scr_capt is None:
            scr_capt = None
        select = -1

    elif state_name == statemachine.States.PauseMenu:
        content = screens.menu.pausemenu.PauseMenu(engine)
        title = None
        animation = None
        scr_capt = ScreenCapture()
        select = 0

    return screens.menu.display.Display(engine.audio, state_name,
                                        content, title, animation, scr_capt, select)
