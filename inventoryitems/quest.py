
"""
class: BaseQuestItem
class: FetchItemQuestItem
class: ReceiveItemQuestItem
class: FetchItemsPartlyQuestItem
class: PersonMessageQuest1Item
class: PersonMessageQuest2Item
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
    def __init__(self, qtype, condition, reward, text):
        self.state = QuestState.Unknown
        self.qtype = qtype
        self.condition = condition
        self.reward = reward
        self.text = text

    def show_message(self, gamestate, data, person_enum_val):
        """
        Geef een bericht en waneer mogelijk ook een confirmbox erachteraan.
        :param gamestate: self.engine.gamestate
        :param data: self.engine.data
        :param person_enum_val: een Enum .value uit de PeopleDatabase[x].value. het is een dict().
        :return: deze is voor het vullen van een quest_box in window. returnt een confirmbox indien nodig.
        """
        for i, text_part in enumerate(reversed(self._get_text())):
            push_object = MessageBox(text_part, face_image=person_enum_val['face'],
                                     last=(True if i == 0 and (not self._is_ready_to_fulfill(data) or
                                                               self.is_rewarded()) else False))
            gamestate.push(push_object)

        self._update_state(self._is_ready_to_fulfill(data))

        if self.state == QuestState.Ready:
            push_object = ConfirmBox(self._get_text(), callback=person_enum_val)
            gamestate.push(push_object)
            # plaats de confirmbox achter alle messageboxen
            gamestate.push_confirmbox_to_end()
            return push_object

        return None

    def decided(self, gamestate, data, audio, face_image, choice, yes, scr_capt, display_loot):
        """
        Deze wordt in de callback meegegeven bij het keuze moment in de confirmbox van de quest.
        :param gamestate: self.engine.gamestate
        :param data: self.engine.data
        :param audio: self.engine.audio
        :param face_image: PeopleDatabase[person_sprite.person_id].value['face']
        :param choice: confirmbox.cur_item
        :param yes: confirmbox.TOPINDEX
        :param scr_capt: hetzelfde schermafdruk die ook in de voorgaande confirmbox is gebruikt
        :param display_loot: methode uit Window() waar het overzicht gegeven wordt van wat je ontvangen hebt.
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
                push_object = MessageBox(text, spr_image=image, scr_capt=scr_capt, sound=SFX.reward, last=True)
                gamestate.push(push_object)

                # nog een bedank berichtje van de quest owner.
                for text_part in reversed(self._get_text()):
                    push_object = MessageBox(text_part, face_image=face_image, scr_capt=scr_capt)
                    gamestate.push(push_object)

            else:
                # als er geen directe reward is, maar er is wel een soort quest klaring.
                audio.play_sound(SFX.reward)

                # nog een bedank berichtje van de quest owner.
                amount_messages = len(self._get_text()) - 1
                for i, text_part in enumerate(reversed(self._get_text())):
                    push_object = MessageBox(text_part, face_image=face_image, scr_capt=scr_capt,
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

    def _get_text(self):
        """
        Geeft de juiste tekst terug op basis van de state van de quest.
        :return: de tekst die past bij de index van QuestState
        """
        return self.text[self.state.value]

    def is_running(self):
        """..."""
        if self.state == QuestState.Running:
            return True
        else:
            return False

    def is_rewarded(self):
        """
        Geeft terug of de state rewarded is.
        :return: true of false
        """
        if self.state == QuestState.Rewarded:
            return True
        else:
            return False

    def _is_ready_to_fulfill(self, data):
        """
        Deze moet overridden worden. Anders geeft hij altijd False.
        """
        return False

    def _fulfill(self, data):
        pass


class FetchItemQuestItem(BaseQuestItem):
    """
    Een persoon vraagt je om een of meerdere items. En bij het overdragen krijg je eventueel een beloning.
    """
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


class ReceiveItemQuestItem(BaseQuestItem):
    """
    Je praat met een persoon, en die geeft je op een voorwaarde wat.
    """
    def _is_ready_to_fulfill(self, data):
        """
        Bekijkt of hij voldoet aan de condition van de quest. 
        En dat doet hij soms vanaf het begin of als je ergens geweest bent altijd. 
        :param data: self.engine.data
        :return: Als alle conditions goed zijn geeft hij True terug.
        """
        return self.condition


class FetchItemsPartlyQuestItem(BaseQuestItem):
    """
    Een persoon vraagt je om meerdere items. En bij het gedeeltelijk overdragen krijg je eventueel een gedeelte 
    van de beloning. Bij een volledige overdraging van alle items krijg je de volledige beloning. 1x een overdraging.
    """
    def _is_ready_to_fulfill(self, data):
        """
        Bekijkt of hij voldoet aan de condition van de quest. En dat doet hij altijd. Want je mag ook niets inleveren.
        :param data: self.engine.data
        :return: Als alle conditions goed zijn geeft hij True terug.
        """
        return True

    def _fulfill(self, data):
        """
        Wordt aangeroepen als hij (gedeeltelijk) de items inlevert.
        :param data: self.engine.data
        """
        itemcounter = 0
        for key, value in self.condition.items():
            if key.startswith('eqp'):
                pass  # todo, dit is dus nog niet geimplementeerd. staat ook een notitie van bij quest6.

            elif key.startswith('itm'):
                itm_obj = inventoryitems.factory_pouch_item(value['nam'])
                itm_qty = data.pouch.get_quantity(itm_obj)          # de hoeveelheid die je bezit
                if itm_qty:                                         # als het aantal groter is dan 0
                    if itm_qty >= value['qty']:                     # als het item en aantal kloppen
                        data.pouch.remove(itm_obj, value['qty'])    # haal de gevraagde hoeveelheid weg
                        itemcounter += value['qty']                 # en doe het aantal bij de counter
                    elif itm_qty < value['qty']:                    # maar als minder is dan de gevraagde hoeveelheid
                        data.pouch.remove(itm_obj, itm_qty)         # haal dan alles wat je wel hebt weg
                        itemcounter += itm_qty                      # en doe het aantal bij de counter

        # todo, er mag nog alleen maar een reward van 'itm1' zijn. dat moet universeler uiteindelijk
        self.reward['itm1']['qty'] *= itemcounter                   # zet alles om naar de beloning


class PersonMessageQuest1Item(BaseQuestItem):
    """
    Een persoon vraagt of je wat wil zeggen tegen iemand. Als je dat doet krijg je eventueel een beloning.
    """
    def __init__(self, qtype, subquest, condition, reward, text):
        super().__init__(qtype, condition, reward, text)
        self.subquest = subquest

    def _is_ready_to_fulfill(self, data):
        """
        Als die andere quest (self.subquest) rewarded is, dus wanneer je de boodschap hebt doorgegeven.
        :param data: self.engine.data
        :return: Geef dan True terug als de andere quest succesvol is afgerond.
        """
        return data.logbook[self.subquest].is_rewarded()


class PersonMessageQuest2Item(BaseQuestItem):
    """
    De persoon aan wie je wat moet zeggen van PersonMessageQuest1Item. Kan ook een beloning krijgen.
    """
    def __init__(self, qtype, subquest, condition, reward, text):
        super().__init__(qtype, condition, reward, text)
        self.subquest = subquest

    def _is_ready_to_fulfill(self, data):
        """
        :param data: self.engine.data
        :return: Geeft True terug wanneer de andere quest (self.subquest) alleen al draait. En dat gebeurt al wanneer
         je hebt gepraat met die ander.
        """
        return data.logbook[self.subquest].is_running()
