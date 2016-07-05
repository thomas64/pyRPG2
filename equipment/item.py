
"""
class: EquipmentItem
"""

import enum

from constants import SkillType
from constants import StatType


class EquipmentItem(object):
    """
    Een EquipmentItem object met attributen als de waarden van de extra's die het item heeft zoals THF.
    """
    def __init__(self, **kwargs):
        self.qty = 1

        for eqp_value_key, eqp_value_value in kwargs.items():
            setattr(self, eqp_value_key.upper(), eqp_value_value)       # zet de dict van kwargs om in attributen

        try:
            # noinspection PyUnresolvedReferences
            self.RAW = self.NAM.strip().lower().replace(" ", "")        # als er een NAM is, geef hem een RAW
        except AttributeError:
            pass
        try:
            # noinspection PyUnresolvedReferences
            del self.SHP                                        # deze is niet nodig wanneer het een object geworden is.
        except AttributeError:
            pass

    # noinspection PyUnresolvedReferences
    def display(self):
        """
        Deze is voor weergave. Voeg de gevonden attributen op volgorde samen.
        :return: een lijst van de geselecteerde attributen
        """
        #               attr[0]             attr[1]
        attrs = [(self.TYP.value,      'nam'),
                 ('Skill',             'skl'),
                 ('Min. Intelligence', 'min_int'),
                 ('Min. Dexterity',    'min_dex'),
                 ('Min. Strength',     'min_str')]
        # voeg ook alle stats en skills in deze lijst toe.
        for stat in StatType:
            attrs.append((stat.value,  stat.name))
        for skill in SkillType:
            attrs.append((skill.value, skill.name))

        # nu alle mogelijkheden geladen zijn, ga dan aan de slag met diegene die van toepassing zijn
        attr_list = []

        for attr in attrs:
            value_of_attr = self.get_value_of(attr[1])
            # uitzondering, 'wht' altijd gewoon weergeven
            if attr[0] == StatType.wht.value:
                # deze uitzondering geldt niet voor weapons en shields.
                if not isinstance(self.get_value_of('skl'), enum.Enum):  # niet wanneer 'skl' een waarde heeft
                    attr_list.append((attr[0], str(value_of_attr)))
            elif value_of_attr:
                if isinstance(value_of_attr, enum.Enum):    # uitzondering alleen voor 'skl'
                    value_of_attr = value_of_attr.value
                elif attr[0] == StatType.hit.value:         # uitzondering alleen voor 'hit'
                    value_of_attr = str(value_of_attr)+"%"
                attr_list.append((attr[0], str(value_of_attr)))

        return attr_list

    def get_value_of(self, attr):
        """
        Vraagt een attribute op van een EquipmentItem. De RAW van bijv een skill is in lower zoals 'alc', maar de
        'alc' van een EquipmentItem is self.ALC, vandaar de upper().
        :param attr: sting, het opgevraagde attribute
        :return: de waarde van het attribute, en zo niet bestaand, nul.
        """
        return getattr(self, attr.upper(), 0)

    def is_not_empty(self):
        """
        Bekijkt of de EquipmentItem een 'empty' is, door te checken op attribute NAM.
        :return: True wanneer de NAM bestaat, want hij is niet empty. Anders False, want hij ís empty.
        """
        if hasattr(self, 'NAM'):
            return True
        return False
