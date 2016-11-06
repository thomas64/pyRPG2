
"""
class: Display
"""

import pygame

from components import Button
from components import ConfirmBox
from components import MessageBox
from components import Transition
from constants import GameState
from constants import Keys
from constants import SFX
from database import TrainerDatabase
from database import PouchItemDatabase
from inventoryitems import PouchItem

from screens.school.display import Display as SchoolDisplay
from screens.shop.infobox import InfoBox
# from .knownbox import KnownBox
# from .learnbox import LearnBox
# from .selector import Selector


class Display(SchoolDisplay):
    """
    ...
    """
    def __init__(self, engine, skilltype_list, face):
        super().__init__(engine, skilltype_list, face)
