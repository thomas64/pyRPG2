
"""
class: EquipmentItem
"""


class EquipmentItem(object):
    """
    Een EquipmentItem object met attributen als de waarden van de extra's die het item heeft zoals THF.
    """
    def __init__(self, equipment_type, **kwargs):
        self.TYP = equipment_type                                       # Enum van EquipmentType.value
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

    def display(self):
        """
        Deze is voor weergave. Voeg de gevonden attributen op volgorde samen.
        :return: een lijst van de geselecteerde attributen
        """
        name_tuple = (self.TYP, 'Skill', 'Min. Intelligence', 'Min. Strength', 'Weight', 'Movepoints',
                      'Protection', 'Defense', 'Base Hit', 'Damage',
                      'Intelligence', 'Willpower', 'Dexterity',
                      'Diplomat', 'Loremaster', 'Ranger', 'Stealth', 'Thief', 'Warrior', 'Wizard')

        attr_tuple = ('nam', 'skl', 'min_int', 'min_str', 'wht', 'mvp',
                      'prt', 'des', 'hit', 'dam',
                      'int', 'wil', 'dex',
                      'dip', 'lor', 'ran', 'stl', 'thf', 'war', 'wiz')

        attr_list = []

        for index, attr in enumerate(attr_tuple):
            value_of_attr = self.get_value_of(attr)
            if value_of_attr:
                attr_list.append((str(name_tuple[index]), str(value_of_attr)))

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
