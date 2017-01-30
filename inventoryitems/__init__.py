
"""
def: factory_empty_equipment_item
"""

# todo, uit colornote app:
# - min int gebruiken voor items?
# - mvp aan items

from .quest import FetchItemQuestItem
from .quest import PersonMessageQuestItem
from .quest import ReceiveItemQuestItem


def factory_empty_equipment_item(equipment_type):
    """
    Geeft een 'empty' EquipmentItem object terug op verzoek van een type.
    Met **, hij verwacht een dict.
    :param equipment_type: Enum EquipmentType, dus bijv. "sld" "Shield".
    """
    from .equipment import EquipmentItem

    return EquipmentItem(**dict(typ=equipment_type))


def factory_equipment_item(enum):
    """
    :param enum: Enum waarde uit een van de equipment databases.
    :return: een object op basis van het item uit de enum database.
    """
    from .equipment import EquipmentItem

    return EquipmentItem(**enum.value)


def factory_pouch_item(enum):
    """
    :param enum: Enum waarde uit de PouchItemDatabase
    :return: een object op basis van het item uit de database
    """
    from database.pouchitem import PouchItemDatabase

    from .pouch import PouchItem
    from .pouch import HealingPotion
    from .pouch import CuringPotion
    from .pouch import StaminaPotion
    from .pouch import RestorePotion

    # de check moet op de name. door de shop kan het namelijk ook vanuit een andere enum komen, maar de naam
    # zal in ieder geval hetzelfde zijn. dus daar kan de check op.
    if enum.name == PouchItemDatabase.hlg_pot.name:
        return HealingPotion(**enum.value)
    elif enum.name == PouchItemDatabase.cur_pot.name:
        return CuringPotion(**enum.value)
    elif enum.name == PouchItemDatabase.sta_pot.name:
        return StaminaPotion(**enum.value)
    elif enum.name == PouchItemDatabase.res_pot.name:
        return RestorePotion(**enum.value)
    else:
        return PouchItem(**enum.value)
