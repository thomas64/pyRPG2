
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

    trainer1 = dict(content=[SkillType.war.name, SkillType.haf.name, SkillType.swd.name, SkillType.pol.name,
                             SkillType.shd.name],
                    face=TRAINER1+FEXT, sprite=TRAINER1+SEXT)

    @staticmethod
    def welcome_text():
        """..."""
        return ("Good day sir. Welcome to my academy.",
                "In the 'Known' box are all the skills you",
                "already have learned.  And in the",
                "'Learn' box are all the skills that I can teach.",
                "Click once on a selected item to learn a skill.",
                "You can scroll through the lists with your mouse-",
                "wheel if the list is longer than what you can see.",
                "Below here, all your party members are shown.",
                "Click on it to select someone else to be taught.")
