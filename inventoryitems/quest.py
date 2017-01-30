
"""
class: BaseQuestItem
class: FetchItemQuestItem
class: PersonMessageQuestItem
"""

from components import ConfirmBox
from components import MessageBox
from constants import QuestState
from constants import SFX

import inventoryitems


class BaseQuestItem(object):
    """
    Abstracte base class voor quests.
    """
    def __init__(self, qtype, reward, text):
        self.state = QuestState.Unknown
        self.qtype = qtype
        self.reward = reward
        self.text = text

    def _get_text(self, *args):
        """
        Geeft de juiste tekst terug op basis van de state van de quest.
        :return: de tekst die past bij de index van QuestState
        """
        return self.text[self.state.value]

    def is_rewarded(self):
        """
        Geeft terug of de state rewarded is.
        :return: true of false
        """
        if self.state == QuestState.Rewarded:
            return True
        else:
            return False


class FetchItemQuestItem(BaseQuestItem):
    """
    Een persoon vraagt je om een of meerdere items. En bij het overdragen krijg je eventueel een beloning.
    """
    def __init__(self, qtype, condition, reward, text):
        super().__init__(qtype, reward, text)
        self.condition = condition

    def show_message(self, gamestate, data, audio, face_image, person_id, display_loot):
        """
        Geef een bericht en waneer mogelijk ook een confirmbox erachteraan.
        :param gamestate: self.engine.gamestate
        :param data: self.engine.data
        :param audio: self.engine.audio
        :param face_image: PeopleDatabase[person_sprite.person_id].value['face']
        :param person_id: Voor deze niet nodig, maar wel voor PersonMessageQuestItem.
        :param display_loot: Voor deze niet nodig, maar wel voor PersonMessageQuestItem.
        :return: deze is voor het vullen van een quest_box in window. returnt een confirmbox indien nodig.
        """
        for i, text_part in enumerate(reversed(self._get_text())):
            push_object = MessageBox(gamestate, audio, text_part, face_image,
                                     last=(True if i == 0 and (not self._is_ready_to_fulfill(data) or
                                                               self.state == QuestState.Rewarded) else False))
            gamestate.push(push_object)

        self._update_state(self._is_ready_to_fulfill(data))

        if self.state == QuestState.Ready:
            push_object = ConfirmBox(gamestate, audio, self._get_text(), callback=self.decided)
            gamestate.push(push_object)
            # plaats de confirmbox achter alle messageboxen
            gamestate.push_confirmbox_to_end()
            return push_object

        return None

    def decided(self, gamestate, data, audio, face_image, choice, yes, scr_capt, person_id, display_loot):
        """
        Deze wordt in de callback meegegeven bij het keuze moment in de confirmbox van de quest.
        :param gamestate: self.engine.gamestate
        :param data: self.engine.data
        :param audio: self.engine.audio
        :param face_image: PeopleDatabase[person_sprite.person_id].value['face']
        :param choice: confirmbox.cur_item
        :param yes: confirmbox.TOPINDEX
        :param scr_capt: hetzelfde schermafdruk die ook in de voorgaande confirmbox is gebruikt
        :param person_id: Voor deze niet nodig, maar wel voor PersonMessageQuestItem.
        :param display_loot: methode uit window waar het overzicht gegeven wordt van wat je ontvangen hebt.
        """
        if choice == yes:
            # ga naar Finished
            self._update_state(is_fulfilled=True)
            # hij kan voldoen, komt daarom met text en plaatjes terug, om dat weer te kunnen geven.
            self._fulfill(data)

            if self.reward:
                text = ["Received:"]
                image = []
                text, image = display_loot(self.reward, text, image)
                push_object = MessageBox(gamestate, audio, text, spr_image=image, scr_capt=scr_capt,
                                         sound=SFX.reward, last=True)
                gamestate.push(push_object)

                # nog een bedank berichtje van de quest owner.
                for text_part in reversed(self._get_text()):
                    push_object = MessageBox(gamestate, audio, text_part, face_image=face_image, scr_capt=scr_capt)
                    gamestate.push(push_object)

            else:
                # als er geen directe reward is, maar er is wel een soort quest klaring.
                audio.play_sound(SFX.reward)

                # nog een bedank berichtje van de quest owner.
                amount_messages = len(self._get_text()) - 1
                for i, text_part in enumerate(reversed(self._get_text())):
                    push_object = MessageBox(gamestate, audio, text_part, face_image=face_image, scr_capt=scr_capt,
                                             sound=(None if i == amount_messages else SFX.message),
                                             last=(True if i == 0 else False))
                    gamestate.push(push_object)

            # ga naar Rewarded
            self._update_state(got_rewarded=True)

        else:
            # bij 'nee' dan word je state weer een stapje omlaag gezet.
            audio.play_sound(SFX.done)
            if self.state == QuestState.Ready:
                self.state = QuestState.Running

    def _update_state(self, is_ready_to_fulfill=False, is_fulfilled=False, got_rewarded=False):
        """
        Bekijk in welke state de quest zit en doe daar een aanpassing op.
        :param is_ready_to_fulfill: kan door de gelijknamige methode True meegegeven worden, is van running naar ready.
        :param is_fulfilled: kan eventueel True meegegeven worden, is voor van Ready naar Finished.
        :param got_rewarded: kan eventueel True meegegeven worden, is voor van Finished naar Rewarded.
        """
        if self.state == QuestState.Unknown:
            self.state = QuestState.Running

        # geen elif hier, dan kan hij namelijk eventueel direct al gebruik maken van bovenstaande state wijziging.
        if self.state == QuestState.Running:
            if is_ready_to_fulfill:
                self.state = QuestState.Ready

        elif self.state == QuestState.Ready:
            if is_fulfilled:
                self.state = QuestState.Finished

        elif self.state == QuestState.Finished:
            if got_rewarded:
                self.state = QuestState.Rewarded

        elif self.state == QuestState.Rewarded:
            pass

    def _is_ready_to_fulfill(self, data):
        """
        Bekijkt of hij voldoet aan de condition van de quest.
        :param data: self.engine.data
        :return: Als alle conditions goed zijn geeft hij True terug.
        """

        all_items = []

        for key, value in self.condition.items():
            if key.startswith('eqp'):
                eqp_obj = inventoryitems.factory_equipment_item(value['nam'])
                all_items.append(data.inventory.contains(eqp_obj, value['qty']))
            elif key.startswith('itm'):
                itm_obj = inventoryitems.factory_pouch_item(value['nam'])
                all_items.append(data.pouch.contains(itm_obj, value['qty']))

        return all(all_items)

    def _fulfill(self, data):
        """
        Wordt aangeroepen als hij weet dat hij kàn voldoen. Je geeft de conditions.
        :param data: self.engine.data
        """

        for key, value in self.condition.items():
            if key.startswith('eqp'):
                eqp_obj = inventoryitems.factory_equipment_item(value['nam'])
                data.inventory.remove_i(eqp_obj, value['qty'])
            elif key.startswith('itm'):
                itm_obj = inventoryitems.factory_pouch_item(value['nam'])
                data.pouch.remove(itm_obj, value['qty'])


class PersonMessageQuestItem(BaseQuestItem):
    """
    Een persoon vraagt je om wat te zeggen tegen een ander. Na te voldoen krijg je van de eerste weer een beloning.
    """
    def __init__(self, qtype, people, reward, text):
        super().__init__(qtype, reward, text)
        self.people = people

    def _message_is_last(self, i, person_id):
        """
        Kijkt of een message een 'done' geluid geeft of dat er nog eentje na komt.
        :param i: index van enumerate
        :param person_id: om te bepalen of het een main of een sub is.
        :return: False onder bepaalde voorwaarden, anders True
        """
        if i == 0:
            if self.state == QuestState.Running and self.people[person_id] != 'main':
                return False
            if self.state == QuestState.Finished and self.people[person_id] == 'main':
                return False
            return True
        return False

    def show_message(self, gamestate, data, audio, face_image, person_id, display_loot):
        """
        Geeft een bericht en waneer mogelijk ook een confirmbox erachteraan.
        :param gamestate: self.engine.gamestate
        :param data: self.engine.data
        :param audio: self.engine.audio
        :param face_image: PeopleDatabase[person_sprite.person_id].value['face']
        :param person_id: Nodig voor identificatie en voor weergeven tekst van de juiste persoon.
        :param display_loot: methode uit window waar het overzicht gegeven wordt van wat je ontvangen hebt.
        :return: deze is voor het vullen van een quest_box in window. returnt een confirmbox indien nodig.
        """
        # let op dat de volgorde volledig omgedraaid is.
        if self.state == QuestState.Finished:
            if self.people[person_id] == 'main':
                text = ["Received:"]
                image = []
                text, image = display_loot(self.reward, text, image)
                push_object = MessageBox(gamestate, audio, text, spr_image=image, sound=SFX.reward, last=True)
                gamestate.push(push_object)

        for i, text_part in enumerate(reversed(self._get_text(person_id))):
            push_object = MessageBox(gamestate, audio, text_part, face_image, last=self._message_is_last(i, person_id))
            gamestate.push(push_object)

        self._update_state(person_id)

        if self.state == QuestState.Ready:
            push_object = ConfirmBox(gamestate, audio, self._get_text(person_id), callback=self.decided)
            gamestate.push(push_object)
            # plaats de confirmbox achter alle messageboxen
            gamestate.push_confirmbox_to_end()
            return push_object

        return None

    def decided(self, gamestate, data, audio, face_image, choice, yes, scr_capt, person_id, display_loot):
        """
        Deze wordt in de callback meegegeven bij het keuze moment in de confirmbox van de quest.
        :param gamestate: self.engine.gamestate
        :param data: self.engine.data
        :param audio: self.engine.audio
        :param face_image: PeopleDatabase[person_sprite.person_id].value['face']
        :param choice: confirmbox.cur_item
        :param yes: confirmbox.TOPINDEX
        :param scr_capt: hetzelfde schermafdruk die ook in de voorgaande confirmbox is gebruikt
        :param person_id: Nodig voor identificatie en voor weergeven tekst van de juiste persoon.
        :param display_loot: Voor deze niet nodig, maar wel voor FetchItemQuestItem.
        """
        if choice == yes:
            # ga naar Finished
            self._update_state(person_id, is_fulfilled=True)

            amount_messages = len(self._get_text(person_id)) - 1
            for i, text_part in enumerate(reversed(self._get_text(person_id))):
                push_object = MessageBox(gamestate, audio, text_part, face_image=face_image, scr_capt=scr_capt,
                                         sound=(SFX.reward if i == amount_messages else SFX.message),
                                         last=(True if i == 0 else False))
                gamestate.push(push_object)

        else:
            # bij 'nee' dan wordt je state weer een stapje omlaag gezet.
            audio.play_sound(SFX.done)
            if self.state == QuestState.Ready:
                self.state = QuestState.Running

    def _get_text(self, person_id):
        """
        Geeft de juiste tekst terug op basis van de state van de quest en van de person_id.
        :return: de tekst die past bij de index van QuestState
        """
        return self.text[person_id][self.state.value]

    def _update_state(self, person_id, is_fulfilled=False):
        """
        Bekijk in welke state de quest zit en doe daar een aanpassing op.
        :param person_id: is hij 'main' of 'sub'?
        :param is_fulfilled: kan eventueel True meegegeven worden, is voor van Ready naar Finished.
        """
        if self.state == QuestState.Unknown:
            if self.people[person_id] == 'main':
                self.state = QuestState.Running

        elif self.state == QuestState.Running:
            if self.people[person_id] != 'main':
                self.state = QuestState.Ready

        elif self.state == QuestState.Ready:
            if self.people[person_id] != 'main':
                if is_fulfilled:
                    self.state = QuestState.Finished

        elif self.state == QuestState.Finished:
            if self.people[person_id] == 'main':
                self.state = QuestState.Rewarded

        elif self.state == QuestState.Rewarded:
            pass


class ReceiveItemQuestItem(BaseQuestItem):
    """
    Je praat met een persoon, en die geeft je gelijk wat.
    """
    def __init__(self, qtype, reward, text):
        super().__init__(qtype, reward, text)

    def show_message(self, gamestate, data, audio, face_image, person_id, display_loot):
        """
        Geeft een bericht net zoals notes verdeeld over meerdere schermen, met een inverse loop.
        :param gamestate: self.engine.gamestate
        :param data: self.engine.data
        :param audio: self.engine.audio
        :param face_image: PeopleDatabase[person_sprite.person_id].value['face']
        :param person_id: Voor deze niet nodig, maar wel voor PersonMessageQuestItem.
        :param display_loot: methode uit window waar het overzicht gegeven wordt van wat je ontvangen hebt.
        :return: deze is voor deze quest altijd None.
        """

        # let op dat de volgorde volledig omgedraaid is.
        if self.state != QuestState.Rewarded:
            text = ["Received:"]
            image = []
            text, image = display_loot(self.reward, text, image)
            push_object = MessageBox(gamestate, audio, text, spr_image=image, sound=SFX.reward, last=True)
            gamestate.push(push_object)

        for i, text_part in enumerate(reversed(self._get_text())):
            push_object = MessageBox(gamestate, audio, text_part, face_image,
                                     last=(True if i == 0 and self.state == QuestState.Rewarded else False))
            gamestate.push(push_object)

        self._update_state()

        return None

    def _update_state(self):
        """
        Zet de state gelijk naar rewarded, vanaf welke state dan ook.
        """
        self.state = QuestState.Rewarded
