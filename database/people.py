
"""
class: PeopleDatabase
"""

import datetime
import enum

from .chapter import ChapterDatabase
from .quest import QuestDatabase


PATH = 'resources/sprites/npcs/'
FEXT = 'f.png'
SEXT = 's.png'

HEROFACEPATH = 'resources/sprites/heroes/'
ALAGOS = HEROFACEPATH+"01f_alagos.png"


class PeopleDatabase(enum.Enum):
    """
    Mogelijkheid om time1 en time2 op te nemen als een person op een specifiek tijdstip aanwezig moet zijn.
    Mogelijkheid om face alvast mee te geven, deze moet in een list. person80 is een voorbeeld.
    """

    # standard characters
    person1 = dict(name='boy01',         text=[["Hi mister."]])
    person2 = dict(name='boy02',         text=[["Hi mister."]])
    person3 = dict(name='girl01',        text=[["Hi mister."]])
    person4 = dict(name='girl02',        text=[["Hi mister."]])
    person5 = dict(name='youngman01',    text=[["How are you?"]])
    person6 = dict(name='youngman02',    text=[["How are you?"]])
    person7 = dict(name='youngwoman01',  text=[["How are you?"]])
    person8 = dict(name='youngwoman02',  text=[["How are you?"]])
    person9 = dict(name='man01',         text=[["How are you?"]])
    person10 = dict(name='man02',        text=[["How are you?"]])
    person11 = dict(name='woman01',      text=[["How are you?"]])
    person12 = dict(name='woman02',      text=[["How are you?"]])
    person13 = dict(name='oldman01',     text=[["How do you do?"]])
    person14 = dict(name='oldman02',     text=[["How do you do?"]])
    person15 = dict(name='oldwoman01',   text=[["How do you do?"]])
    person16 = dict(name='oldwoman02',   text=[["How do you do?"]])
    person17 = dict(name='animal01',     text=[["Meow"]],
                    # voorbeeld van time1 en time2
                    time1=datetime.datetime(2016, 10, 19, 2, 00),
                    time2=datetime.datetime(2099, 10, 19, 2, 15))
    person18 = dict(name='animal02',     text=[["Woof"]])
    person19 = dict(name='animal03',     text=[["Cluck"]])

    # ersin_forest_invernia
    person76 = dict(name='soldier01',    quest=QuestDatabase.quest3)
    person77 = dict(name='soldier01',    text=[["I'm terribly sorry sir, but I can",
                                               "not allow you to go any further."],
                                               ["It's dangerous to go alone."]])
    person80 = dict(name='soldier01',    chapter=ChapterDatabase.chapter1,
                                         text=[["Trespassing is not allowed!"],
                                               ["I'm sorry."]],
                    face=[PATH+'soldier01'+FEXT, ALAGOS])

    # ersin_forest_spring
    person82 = dict(name='animal02',     text=[["Woof"], [" . . . "], ["I mean, hello there."]])

    # ersin_forest_center
    person50 = dict(name='boy01',        quest=QuestDatabase.quest1)
    person81 = dict(name='girl02',       quest=QuestDatabase.quest5)
    person83 = dict(name='boy01',        quest=(QuestDatabase.quest6,   # een persoon kan meerdere quests achter
                                                QuestDatabase.quest5,   # elkaar hebben. op deze manier.
                                                QuestDatabase.quest1))

    # ersin_waterfall
    person51 = dict(name='man54',        quest=QuestDatabase.quest4)

    # invernia_town
    person52 = dict(name='boy01',        text=[["Hi mister!", "We're playing hide and seek.",
                                               "I'm seeking, where are they?"]])
    person53 = dict(name='girl01',       text=[["Aaw, I'm already caught."]])
    person54 = dict(name='girl02',       text=[["Psst, I'm hiding, please don't say anything."]])
    person55 = dict(name='boy02',        text=[["Teehee, he'll never find me here."]])
    # invernia_inn_1f
    person56 = dict(name='youngwoman01', text=[["Ouch! This tea is still to hot to drink."]])
    person57 = dict(name='youngman01',   text=[["The rooms are pretty cheap in this town.",
                                                "I've heard people tell of other places",
                                                "where they ask a lot more for a room."]])
    # invernia_inn_2f
    person58 = dict(name='youngwoman02', text=[["The food is so nice!"]])
    person59 = dict(name='youngman02',   text=[["She is so nice!"]])
    person60 = dict(name='woman52',      text=[["I wan't to go out, but my husband is always",
                                                "so busy with his work. I'm bored."]])
    person61 = dict(name='man50',        text=[["Argh, so much work to do."]])
    person62 = dict(name='maid01',       text=[["Sometimes these rooms are so dirty.",
                                               "What are people doing? Do they eat in bed?"]])
    # invernia_house_left
    person63 = dict(name='man01',        text=[["What are you doing inside our home?"]])
    person64 = dict(name='woman01',      text=[["What are you doing inside our home?"]])
    person65 = dict(name='boy01',        text=[["Are you here for mommy and daddy?"]])
    person66 = dict(name='girl01',       text=[["Are you here for mommy and daddy?"]])
    # invernia_house_right
    person67 = dict(name='man02',        text=[["What are you doing inside our home?"]])
    person68 = dict(name='woman02',      text=[["What are you doing inside our home?"]])
    person69 = dict(name='boy02',        text=[["Are you here for mommy and daddy?"]])
    person70 = dict(name='girl02',       text=[["Are you here for mommy and daddy?"]])
    # invernia_house_big_1f
    person71 = dict(name='priest01',     text=[["It's a busy life, taking care for all these orphans."]])
    person72 = dict(name='nun01',        text=[["It's a busy life, taking care for all these orphans."]])
    # invernia_house_big_2f
    person73 = dict(name='maid01',       text=[["These people are so sweet, taking care for all those children."]])
    # invernia_weapon_shop
    person74 = dict(name='youngman02',   quest=QuestDatabase.quest7)
    # invernia_armor_shop
    person75 = dict(name='youngwoman02', quest=QuestDatabase.quest8)
    # invernia_school
    person78 = dict(name='woman03',      text=[["The magic here is from another world!"]])

    @staticmethod
    def get_active_quest(quest_data, logbook):
        """
        Als een persoon meerdere quests heeft, dan zoekt hij naar de huidige quest.
        :param quest_data: person_enum_val['quest']. bijv QuestDatabase.quest2
        :param logbook: self.engine.data.logbook
        :return: het quest object uit de logbook
        """
        # meerdere quests
        if type(quest_data) == tuple:
            # loop dan door al zijn quests
            for index, quest in enumerate(quest_data):
                quest_key = quest.name
                the_quest = logbook[quest_key]
                # en als er nog eentje niet rewarded is, voer die dan uit.
                # OF als je bij de laatste quest bent, die mag je nog wel een keer uitvoeren.
                if not the_quest.is_rewarded() or index == len(quest_data) - 1:
                    return the_quest
        # of als de persoon 1 quest heeft
        else:
            quest_key = quest_data.name
            the_quest = logbook[quest_key]
            return the_quest


for person in PeopleDatabase:
    if not person.value.get('face'):  # als er nog geen face is stop ze in een list van faces.
        if person.value.get('text'):  # een quest heeft geen 'text'
            size = len(person.value['text'])
            person.value['face'] = [PATH+person.value['name']+FEXT] * size
        else:
            person.value['face'] = PATH + person.value['name'] + FEXT  # bij een quest.
    person.value['sprite'] = PATH+person.value['name']+SEXT
