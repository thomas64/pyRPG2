
"""
class: QuestItem
"""

import pygame

from constants import QuestState
from constants import QuestType
import equipment
import pouchitems

ICONSIZE = 32


# noinspection PyUnresolvedReferences
class QuestItem(object):
    """..."""
    def __init__(self, **kwargs):

        # elke nieuwe quest start bij met status onbekend.
        self.state = QuestState.Unknown

        for quest_value_key, quest_value_value in kwargs.items():
            setattr(self, quest_value_key, quest_value_value)       # zet de dict van kwargs om in attributen

    def get_text(self, confirm=None):
        """
        Geeft de juiste tekst terug op basis van de state van de quest.
        :param confirm: deze is standaard None, daar kijkt hij ook naar. Als parameter '0' wordt meegegeven, dan
        gebruikt hij de nulste uit de text van questdatabase, en dat is de confirmbox vraag.
        :return: bij 0 dus de confirmbox, maar anders de tekst die past bij de index van QuestState
        """
        if confirm is not None:
            return self.text[confirm]
        return self.text[self.state.value]

    def confirm_contact(self, data):
        """
        Bekijk in welke state de quest zit en doe daar een aanpassing op.
        :param data: self.engine.data
        :return: geeft standaard False terug, maar als hij compleet is, dan geeft hij True terug.
        """
        if self.state == QuestState.Unknown:
            self.state = QuestState.Running
            return self.is_complete(data)
        elif self.state == QuestState.Running:
            return self.is_complete(data)
        elif self.state == QuestState.Finished:
            self.state = QuestState.Rewarded
            return False
        elif self.state == QuestState.Rewarded:
            return False

    def is_complete(self, data):
        """
        Bekijkt of hij voldoet aan de condition van de quest.
        :param data: self.engine.data
        :return: Als alle conditions goed zijn geeft hij True terug.
        """

        if self.qtype == QuestType.ItemQuest:

            completed = []

            for key, value in self.condition.items():
                if key.startswith('eqp'):
                    completed.append(data.inventory.contains(value['nam'], value['qty']))
                elif key.startswith('itm'):
                    completed.append(data.pouch.contains(value['nam'], value['qty']))

            return all(completed)

    def fulfill(self, data):
        """
        Wordt aangeroepen als hij weet dat hij kàn voldoen. Je geeft de conditions, en krijgt de rewards.
        :param data: self.engine.data
        :return: geeft de text terug en de plaatjes voor een messagebox.
        """

        if self.qtype == QuestType.ItemQuest:

            for key, value in self.condition.items():
                if key.startswith('eqp'):
                    eqp_obj = equipment.factory_equipment_item(value['nam'])
                    data.inventory.remove_i(eqp_obj, value['qty'])
                elif key.startswith('itm'):
                    itm_obj = pouchitems.factory_pouch_item(value['nam'])
                    data.pouch.remove(itm_obj, value['qty'])

            # wat hieronder staat, lijkt erg op sparkly en chest in window. niet DRY!
            text = ["Received:"]
            image = []

            for key, value in self.reward.items():
                if key.startswith('eqp'):
                    eqp_obj = equipment.factory_equipment_item(value['nam'])
                    eqp_obj_spr = pygame.image.load(eqp_obj.SPR).subsurface(
                                                        eqp_obj.COL, eqp_obj.ROW, ICONSIZE, ICONSIZE).convert_alpha()
                    data.inventory.add_i(eqp_obj, value['qty'])
                    text.append("{} {}".format(value['qty'], eqp_obj.NAM))
                    image.append(eqp_obj_spr)

                elif key.startswith('itm'):
                    itm_obj = pouchitems.factory_pouch_item(value['nam'])
                    itm_obj_spr = pygame.image.load(itm_obj.SPR).convert_alpha()
                    data.pouch.add(itm_obj, value['qty'])
                    text.append("{} {}".format(value['qty'], itm_obj.NAM))
                    image.append(itm_obj_spr)

            # zet de state op Finished
            self.state = QuestState.Finished
            return text, image
