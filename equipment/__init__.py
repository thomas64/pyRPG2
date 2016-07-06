
"""
def: factory_empty_equipment_item
"""

# todo, uit colornote app:
# - min int gebruiken voor items?
# - mvp aan items

from .item import EquipmentItem


def factory_empty_equipment_item(equipment_type):
    """
    Geeft een 'empty' EquipmentItem object terug op verzoek van een type.
    Met **, hij verwacht een dict.
    :param equipment_type: Enum EquipmentType, dus bijv. "sld" "Shield".
    """
    return EquipmentItem(**dict(typ=equipment_type))
