
"""
...
"""

import enum

# todo, de juiste imports, denk aan de volgorde


class MenuItems(enum.Enum):
    """
    ...
    """
    MainMenu = 1
    LoadMenu = 2
    OptionsMenu = 3


def create_menu(choice, engine, select=None):
    """
    ...
    :param choice:
    :param engine:
    :param select:
    """
    if choice == MenuItems.MainMenu:
        content = screens.menu.mainmenu.MainMenu(engine)
        title = True
        animation = True
        scr_capt = None
        select = 0

    elif choice == MenuItems.LoadMenu:
        content = screens.menu.loadmenu.LoadMenu(engine)
        title = False
        animation = False
        scr_capt = None
        if select is None:
            select = -1

    elif choice == MenuItems.OptionsMenu:
        content = screens.menu.optionsmenu.OptionsMenu(engine)
        title = True
        animation = True
        scr_capt = None
        select = -1

    # noinspection PyUnboundLocalVariable
    return Display(engine.screen, engine.audio, content, title, animation, scr_capt, select)
