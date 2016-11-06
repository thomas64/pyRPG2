
"""
class: TrainerDatabase
"""

import enum

from constants import SkillType

PATH = 'resources/sprites/npcs/'
FEXT = 'f.png'
SEXT = 's.png'
TRAINER1 = PATH+'man51'


class TrainerDatabase(enum.Enum):
    """
    ...
    """

    trainer1 = dict(content=[SkillType.mec, SkillType.ran, SkillType.war],
                    face=TRAINER1+FEXT, sprite=TRAINER1+SEXT)

    @staticmethod
    def welcome_text():
        """..."""
        return ("Good day sir, and welcome to my XXXXXX.",
                "In the 'Known' box are all the skills you",
                "already have learned.  And in the",
                "'Learn' box are all the skills that I can teach.",
                "Click once on a selected item to learn a skill.",
                "You can scroll through the lists with your mouse-",
                "wheel if the list is longer than what you can see.",
                "Below here, all your party members are shown.",
                "Click on it to select someone else to be taught.")
