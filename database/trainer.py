
"""
class: TrainerDatabase
"""

import enum

from constants import SkillType

PATH = 'resources/sprites/npcs/'
FEXT = 'f.png'
SEXT = 's.png'
TRAINER1 = PATH+'man51'
TRAINER2 = PATH+'teacher01'
TRAINER3 = PATH+'captain01'


class TrainerDatabase(enum.Enum):
    """
    ...
    """

    trainer1 = dict(content=[SkillType.war.name, SkillType.haf.name, SkillType.mis.name, SkillType.pol.name,
                             SkillType.shd.name, SkillType.swd.name, SkillType.thr.name],
                    face=TRAINER1+FEXT, sprite=TRAINER1+SEXT)
    trainer2 = dict(content=[SkillType.alc.name, SkillType.dip.name, SkillType.hlr.name, SkillType.lor.name,
                             SkillType.wiz.name],
                    face=TRAINER2+FEXT, sprite=TRAINER2+SEXT)
    trainer3 = dict(content=[SkillType.mec.name, SkillType.mer.name, SkillType.ran.name, SkillType.stl.name,
                             SkillType.thf.name, SkillType.trb.name],
                    face=TRAINER3+FEXT, sprite=TRAINER3+SEXT)

    @staticmethod
    def welcome_text():
        """..."""
        return ("Good day sir. Welcome to my academy.",
                "In the 'Train' box are all the skills that",
                "I can train you in. And in the 'Known'",
                "box are all the skills you already have been trained in.",
                "Click once on a selected item to train a skill.",
                "You can scroll through the lists with your mouse-",
                "wheel if the list is longer than what you can see.",
                "Below here, all your party members are shown.",
                "Click on it to select someone else to be taught.")
