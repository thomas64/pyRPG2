
"""
def: factory_empty_equipment_item
"""

# todo, uit colornote app:
# - min int gebruiken voor items?
# - mvp aan items

from .equipment import EquipmentItem
from .pouch import PouchItem
from .quest import FetchItemQuestItem
from .quest import PersonMessageQuestItem


def factory_empty_equipment_item(equipment_type):
    """
    Geeft een 'empty' EquipmentItem object terug op verzoek van een type.
    Met **, hij verwacht een dict.
    :param equipment_type: Enum EquipmentType, dus bijv. "sld" "Shield".
    """
    return EquipmentItem(**dict(typ=equipment_type))
