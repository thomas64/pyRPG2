
"""
def: create_menu
"""


def create_menu(state_name, engine, title1=None, animation1=None, scr_capt=None, select=None):
    """
    Hier worden de verschillende eigenschappen van de verschillende menu's toegekend.
    :param state_name: Enum state name
    :param engine: self van GameEngine
    :param title1: menu Title Object, de 1 is voor anders is het shadow
    :param animation1: een dict van afbeeldingen, de 1 is voor anders is het shadow
    :param scr_capt: een afbeelding
    :param select: de voorgeslecteerde item
    """

    from components import ScreenCapture
    from constants import GameState

    from .animation import Animation
    from .title import Title
    from .display import Display
    from .mainmenu import MainMenu
    from .loadmenu import LoadMenu
    from .savemenu import SaveMenu
    from .settingsmenu import SettingsMenu
    from .pausemenu import PauseMenu

    content = None

    if state_name == GameState.MainMenu:
        content = MainMenu(engine)
        title1 = Title()
        animation1 = Animation()
        scr_capt = None
        if select is None:
            select = 0

    elif state_name == GameState.LoadMenu:
        content = LoadMenu(engine)
        title1 = Title(title=None, sub=GameState.LoadMenu.value)
        animation1 = None
        scr_capt = scr_capt
        if select is None:
            select = -1

    elif state_name == GameState.SaveMenu:
        content = SaveMenu(engine)
        title1 = Title(title=None, sub=GameState.SaveMenu.value)
        animation1 = None
        scr_capt = scr_capt
        if select is None:
            select = -1

    elif state_name == GameState.SettingsMenu:
        content = SettingsMenu(engine)
        title1 = title1
        animation1 = animation1
        scr_capt = scr_capt
        select = -1

    elif state_name == GameState.PauseMenu:
        content = PauseMenu(engine)
        title1 = None
        animation1 = None
        scr_capt = ScreenCapture()
        select = 0

    return Display(engine.audio, state_name, content, title1, animation1, scr_capt, select)
