
"""
class: QuestItem
"""

import pygame

from constants import QuestState
from constants import QuestType
from .equipment import EquipmentItem
from .pouch import PouchItem

ICONSIZE = 32


class QuestItem(object):
    """..."""
    def __init__(self, **kwargs):

        # elke nieuwe quest start bij met status onbekend.
        self.state = QuestState.Unknown
        self.qtype = None
        self.condition = None
        self.reward = None
        self.text = None
        self.subtext = None

        for quest_value_key, quest_value_value in kwargs.items():
            setattr(self, quest_value_key, quest_value_value)       # zet de dict van kwargs om in attributen

    def get_text(self):
        """
        Geeft de juiste tekst terug op basis van de state van de quest.
        :return: de tekst die past bij de index van QuestState
        """
        return self.text[self.state.value]

    def get_subtext(self):
        """
        Soortgelijk aan get_text() maar dan voor subtext.
        """
        return self.subtext[self.state.value]

    def update_state(self, data, got_reward=False, talk_to_sub=False):
        """
        Bekijk in welke state de quest zit en doe daar een aanpassing op.
        :param data: self.engine.data of None
        :param got_reward: kan eventueel True meegegeven worden, is voor van Finished naar Rewarded.
        :param talk_to_sub: wanneer de subquester aangesproken wordt
        """
        if self.qtype == QuestType.ItemQuest:
            if self.state == QuestState.Unknown:
                self.state = QuestState.Running
            # geen elif hier, dan kan hij namelijk eventueel direct al gebruik maken van bovenstaande state wijziging.
            if self.state == QuestState.Running:
                if self.is_ready_to_fulfill(data):
                    self.state = QuestState.Ready
            elif self.state == QuestState.Ready:
                self.state = QuestState.Finished
            elif self.state == QuestState.Finished:
                if got_reward:
                    self.state = QuestState.Rewarded
            elif self.state == QuestState.Rewarded:
                pass

        elif self.qtype == QuestType.PersonQuest:
            if self.state == QuestState.Unknown:
                if not talk_to_sub:
                    self.state = QuestState.Running
            elif self.state == QuestState.Running:
                if talk_to_sub:
                    self.state = QuestState.Ready
            elif self.state == QuestState.Ready:
                self.state = QuestState.Finished
            elif self.state == QuestState.Finished:
                if got_reward:
                    self.state = QuestState.Rewarded
            elif self.state == QuestState.Rewarded:
                pass

    def downdate_state(self):
        """
        Bij het selecteren van Nee bij de vraag, breng de state weer naar Running.
        """
        if self.state == QuestState.Ready:
            self.state = QuestState.Running

    def is_ready_to_fulfill(self, data):
        """
        Bekijkt of hij voldoet aan de condition van de quest.
        :param data: self.engine.data
        :return: Als alle conditions goed zijn geeft hij True terug.
        """

        if self.qtype == QuestType.ItemQuest:

            all_items = []

            for key, value in self.condition.items():
                if key.startswith('eqp'):
                    eqp_obj = EquipmentItem(**value['nam'].value)
                    all_items.append(data.inventory.contains(eqp_obj, value['qty']))
                elif key.startswith('itm'):
                    itm_obj = PouchItem(**value['nam'].value)
                    all_items.append(data.pouch.contains(itm_obj, value['qty']))

            return all(all_items)

    def is_ready_to_finish(self):
        """
        Bekijkt of de state op Ready staat.
        :return: boolean True or False
        """
        if self.state == QuestState.Ready:
            return True

    def reward_after_confirm(self):
        """
        Bekijkt of de state op Finished staat.
        :return: boolean True or False
        """
        if self.qtype == QuestType.ItemQuest:
            if self.state == QuestState.Finished:
                return True

    def reward_after_message(self):
        """..."""
        if self.qtype == QuestType.PersonQuest:
            if self.state == QuestState.Finished:
                return True

    # noinspection PyUnresolvedReferences
    def fulfill(self, data):
        """
        Wordt aangeroepen als hij weet dat hij kàn voldoen. Je geeft de conditions, en krijgt de rewards.
        :param data: self.engine.data
        :return: geeft de text terug en de plaatjes voor een messagebox.
        """

        if self.qtype == QuestType.ItemQuest:

            for key, value in self.condition.items():
                if key.startswith('eqp'):
                    eqp_obj = EquipmentItem(**value['nam'].value)
                    data.inventory.remove_i(eqp_obj, value['qty'])
                elif key.startswith('itm'):
                    itm_obj = PouchItem(**value['nam'].value)
                    data.pouch.remove(itm_obj, value['qty'])

        # wat hieronder staat, lijkt erg op sparkly en chest in window. niet DRY!
        text = ["Received:"]
        image = []

        for key, value in self.reward.items():
            if key.startswith('eqp'):
                eqp_obj = EquipmentItem(**value['nam'].value)
                eqp_obj_spr = pygame.image.load(eqp_obj.SPR).subsurface(
                                                    eqp_obj.COL, eqp_obj.ROW, ICONSIZE, ICONSIZE).convert_alpha()
                data.inventory.add_i(eqp_obj, value['qty'])
                text.append("{} {}".format(value['qty'], eqp_obj.NAM))
                image.append(eqp_obj_spr)

            elif key.startswith('itm'):
                itm_obj = PouchItem(**value['nam'].value)
                itm_obj_spr = pygame.image.load(itm_obj.SPR).convert_alpha()
                data.pouch.add(itm_obj, value['qty'])
                text.append("{} {}".format(value['qty'], itm_obj.NAM))
                image.append(itm_obj_spr)

        return text, image
