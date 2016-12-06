
"""
def: factory_empty_equipment_item
"""

# todo, uit colornote app:
# - min int gebruiken voor items?
# - mvp aan items

from .equipment import EquipmentItem
from .quest import FetchItemQuestItem
from .quest import PersonMessageQuestItem
from .quest import ReceiveItemQuestItem


def factory_empty_equipment_item(equipment_type):
    """
    Geeft een 'empty' EquipmentItem object terug op verzoek van een type.
    Met **, hij verwacht een dict.
    :param equipment_type: Enum EquipmentType, dus bijv. "sld" "Shield".
    """
    return EquipmentItem(**dict(typ=equipment_type))


def factory_pouch_item(enum):
    """
    :param enum: Enum waarde uit de PouchItemDatabase
    :return: een object op basis van het item uit de database
    """
    from database.pouchitem import PouchItemDatabase

    from .pouch import PouchItem
    from .pouch import HealingPotion

    # de check moet op de name. door de shop kan het namelijk ook vanuit een andere enum komen, maar de naam
    # zal in ieder geval hetzelfde zijn. dus daar kan de check op.
    if enum.name == PouchItemDatabase.hlg_pot.name:
        return HealingPotion(**enum.value)
    else:
        return PouchItem(**enum.value)
