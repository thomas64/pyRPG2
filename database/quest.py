
"""
class: QuestDatabase
"""

import enum

from constants import QuestType
from .weapon import WeaponDatabase
from .pouchitem import PouchItemDatabase


class QuestDatabase(enum.Enum):
    """..."""

    quest1 = dict(qtype=QuestType.FetchItemWithRewardQuest,
                  condition=dict(itm1=dict(nam=PouchItemDatabase.herbs, qty=10)),
                  reward=dict(itm1=dict(nam=PouchItemDatabase.gold,     qty=2),
                              eqp1=dict(nam=WeaponDatabase.bronzedart,  qty=1)),
                  # deze teksten staan in QuestState volgorde.
                  text=([["Hi mister."], ["I need 10 herbs for my mommy.", "She's ill."],
                         ["Can you please help me find some?"]],
                        [["If you've got 10 herbs,", "please give them to me."]],
                        # de confirmbox tekst moet niet tussen dubbele blokhaken
                        ["Help the boy out and give him 10 herbs?", "", "Yes, ofcourse!", "No, these are my herbs."],
                        [["Thanks a lot for the herbs!", "Now my mom will be better soon."],
                         ["Instead of the herbs I found this here in the forest.",
                          "You can have it, for helping my mommy."]],
                        [["Hi mister."], ["It seems my mommy is all better now.", "Thanks to you!"]])
                  )
    quest2 = dict(qtype=QuestType.PersonMessageQuest,
                  reward=dict(itm1=dict(nam=PouchItemDatabase.gold,     qty=1)),
                  people=dict(person74='main',
                              person75='sub1'),
                  text=dict(person74=([["How are you?"], ["May I ask you something?"],
                                       ["I'm a bit shy.",
                                        "There is this girl that I like, but I'm afraid to tell her."],
                                       ["Would you tell her for me instead? Please?",
                                        "She is at the armor shop looking for a dress, and I won't",
                                        "dare to come near, so I went to this shop, I'm pathetic."]],
                                      [["Please do it for me. She is at the armor shop."]],
                                      [[" "]],
                                      [["Thank you for telling her!", "You can have this, for helping me out."]],
                                      [["Thanks again, I owe you big time!"]]),
                            person75=([["How are you?"]],
                                      [["How are you?"]],
                                      # de confirmbox tekst moet niet tussen dubbele blokhaken
                                      ["Bring the pathetic message over to her?", "",
                                       "Yes, everybody needs a chance.", "No, he has to grow up and be a man."],
                                      [["I... I didn't know that...", "Thank you for telling me."]],
                                      [["How are you?"], ["I'm also pretty shy myself."]])
                            )
                  )

    quest3 = dict(qtype=QuestType.FetchItemWithoutRewardQuest,
                  condition=dict(itm1=dict(nam=PouchItemDatabase.proofnote, qty=1)),
                  # geen reward, maar wel remove_temp_blockers() (standaard)
                  text=([["Halt! You may not enter Invernia Town!",
                          "Only if you can prove that you are not a monster."]],
                        [["Halt! You may not enter Invernia Town!",
                          "Only if you can prove that you are not a monster."]],
                        # de confirmbox tekst moet niet tussen dubbele blokhaken
                        ["Show him the 'Proof of not being a monster'?", "",
                         "Yes, I want to enter the town.", "No, he's stupid!"],
                        [["It seems you are not a monster. Continue."]],
                        [["Continue."]])
                  )

    quest4 = dict(qtype=QuestType.ReceiveItemQuest,
                  reward=dict(itm1=dict(nam=PouchItemDatabase.proofnote, qty=1)),
                  # meerdere textscheremen zoals bij notes.
                  text=([["It's so beautiful, I can watch this scenery for hours."],
                         ["    .       .       .       .       .       .       ."],
                         ["By the way, have you been bothered", "by that half ass soldier at our town?",
                          "He has taken it up on himself to prevent", "monsters for entering the town!"],
                         ["That may be noble, but he is not able", "to see the difference between a normal",
                          "person and an evil monster."], ["So he asks for proof?!?"],
                         ["I'll give you a 'Proof of not being a monster',",
                          "because you seem a normal person to me.", "*sigh*"]],
                        [[" "]], [[" "]], [[" "]],
                        [["It's so beautiful, I can watch this scenery for hours."],
                         ["    .       .       .       .       .       .       ."],
                         ["Did you 'prove' that you are not a monster?"]])
                  )
