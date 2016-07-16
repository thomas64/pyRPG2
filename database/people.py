
"""
class: PeopleDatabase
"""

import enum

from .quest import QuestDatabase


PATH = 'resources/sprites/npcs/'
FEXT = 'f.png'
SEXT = 's.png'


class PeopleDatabase(enum.Enum):
    """..."""

    # standard characters
    person1 = dict(name='boy01',         text=["Hi mister."])
    person2 = dict(name='boy02',         text=["Hi mister."])
    person3 = dict(name='girl01',        text=["Hi mister."])
    person4 = dict(name='girl02',        text=["Hi mister."])
    person5 = dict(name='youngman01',    text=["How are you?"])
    person6 = dict(name='youngman02',    text=["How are you?"])
    person7 = dict(name='youngwoman01',  text=["How are you?"])
    person8 = dict(name='youngwoman02',  text=["How are you?"])
    person9 = dict(name='man01',         text=["How are you?"])
    person10 = dict(name='man02',        text=["How are you?"])
    person11 = dict(name='woman01',      text=["How are you?"])
    person12 = dict(name='woman02',      text=["How are you?"])
    person13 = dict(name='oldman01',     text=["How do you do?"])
    person14 = dict(name='oldman02',     text=["How do you do?"])
    person15 = dict(name='oldwoman01',   text=["How do you do?"])
    person16 = dict(name='oldwoman02',   text=["How do you do?"])
    person17 = dict(name='animal01',     face=False, text=["Meow"])
    person18 = dict(name='animal02',     face=False, text=["Bow wow"])
    person19 = dict(name='animal03',     face=False, text=["Cluck cluck"])

    # invernia_forest_center
    person50 = dict(name='boy01',        quest=QuestDatabase.quest1)
    # invernia_forest_waterfall
    person51 = dict(name='man54',        text=["It's so beautiful, I can watch this scenery for hours."])

    # invernia_town
    person52 = dict(name='boy01',        text=["Hi mister!", "We're playing hide and seek.",
                                               "I'm seeking, where are they?"])
    person53 = dict(name='girl01',       text=["Aaw, I'm already caugth."])
    person54 = dict(name='girl02',       text=["Psst, I'm hiding, please don't say anything."])
    person55 = dict(name='boy02',        text=["Teehee, he'll never find me here."])

    # invernia_inn_1f
    person56 = dict(name='youngwoman01', text=["Ouch! This tea is still to hot to drink."])
    person57 = dict(name='youngman01',   text=["The rooms are pretty cheap in this town.",
                                               "I've heard people tell of other places",
                                               "where they ask a lot more for a room."])
    # invernia_inn_2f
    person58 = dict(name='youngwoman02', text=["The food is so nice!"])
    person59 = dict(name='youngman02',   text=["She is so nice!"])
    person60 = dict(name='woman52',      text=["I wan't to go out, but my husband is always",
                                               "so busy with his work. I'm bored."])
    person61 = dict(name='man50',        text=["Argh, so much work to do."])
    person62 = dict(name='woman53',      text=["Sometimes these rooms are so dirty.",
                                               "What are people doing? Do they eat in bed?"])


for person in PeopleDatabase:
    if not person.value['name'].startswith('animal'):
        person.value['face'] = PATH+person.value['name']+FEXT
    person.value['sprite'] = PATH+person.value['name']+SEXT
