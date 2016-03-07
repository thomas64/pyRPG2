
"""
...
"""

import enum

import pygame

import screens.menu.animation
import screens.menu.display
import screens.menu.mainmenu
import screens.menu.loadmenu
import screens.menu.optionsmenu
import screens.menu.pausemenu
import screens.menu.title

# todo, muziek later in laten komen?
# todo, on exit en enter gebruiken?


class MenuItems(enum.Enum):
    """
    ...
    """
    MainMenu = 1
    LoadMenu = 2
    OptionsMenu = 3
    PauseMenu = 4


def create_menu(choice, engine, title=None, animation=None, scr_capt=None, select=None):
    """
    ...
    :param choice:
    :param engine:
    :param title:
    :param animation:
    :param scr_capt:
    :param select:
    """
    if choice == MenuItems.MainMenu:
        content = screens.menu.mainmenu.MainMenu(engine)
        title = screens.menu.title.Title()
        animation = screens.menu.animation.Animation()
        scr_capt = None
        if select is None:
            select = 0

    elif choice == MenuItems.LoadMenu:
        content = screens.menu.loadmenu.LoadMenu(engine)
        title = None
        animation = None
        if scr_capt is None:
            scr_capt = None
        if select is None:
            select = -1

    elif choice == MenuItems.OptionsMenu:
        content = screens.menu.optionsmenu.OptionsMenu(engine)
        if title is None:
            title = None
        if animation is None:
            animation = None
        if scr_capt is None:
            scr_capt = None
        select = -1

    elif choice == MenuItems.PauseMenu:
        content = screens.menu.pausemenu.PauseMenu(engine)
        title = None
        animation = None
        scr_data = pygame.image.tostring(engine.screen, 'RGBA')    # maak een screen capture
        scr_capt = pygame.image.frombuffer(scr_data, engine.screen.get_size(), 'RGBA').convert()
        select = 0

    return screens.menu.display.Display(engine.screen, engine.audio, content, title, animation, scr_capt, select)
