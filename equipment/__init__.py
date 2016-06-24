
"""
def: factory_empty_equipment_item
def: factory_equipment_item
"""

import console
import equipment.item
from database import wpn
from database import sld
from database import hlm
from database import amu
from database import arm
from database import clk
from database import brc
from database import glv
from database import rng
from database import blt
from database import bts
from database import acy

# todo, uit colornote app:
# - min int gebruiken voor items?
# - mvp aan items


def factory_empty_equipment_item(equipment_type):
    """
    Geeft een 'empty' EquipmentItem object terug op verzoek van een type.
    Met **, hij verwacht een dict.
    :param equipment_type: Enum EquipmentType, dus bijv. "sld" "Shield".
    """
    return equipment.item.EquipmentItem(**dict(typ=equipment_type))


def factory_equipment_item(equipment_item_key):
    """
    Geeft een EquipmentItem object terug op verzoek van een key.
    :param equipment_item_key: een sleutel uit de eqp items databases bijv "bronzeshortsword"
    """
    if equipment_item_key in wpn:
        return equipment.item.EquipmentItem(**wpn[equipment_item_key])
    elif equipment_item_key in sld:
        return equipment.item.EquipmentItem(**sld[equipment_item_key])
    elif equipment_item_key in hlm:
        return equipment.item.EquipmentItem(**hlm[equipment_item_key])
    elif equipment_item_key in amu:
        return equipment.item.EquipmentItem(**amu[equipment_item_key])
    elif equipment_item_key in arm:
        return equipment.item.EquipmentItem(**arm[equipment_item_key])
    elif equipment_item_key in clk:
        return equipment.item.EquipmentItem(**clk[equipment_item_key])
    elif equipment_item_key in brc:
        return equipment.item.EquipmentItem(**brc[equipment_item_key])
    elif equipment_item_key in glv:
        return equipment.item.EquipmentItem(**glv[equipment_item_key])
    elif equipment_item_key in rng:
        return equipment.item.EquipmentItem(**rng[equipment_item_key])
    elif equipment_item_key in blt:
        return equipment.item.EquipmentItem(**blt[equipment_item_key])
    elif equipment_item_key in bts:
        return equipment.item.EquipmentItem(**bts[equipment_item_key])
    elif equipment_item_key in acy:
        return equipment.item.EquipmentItem(**acy[equipment_item_key])
    else:
        console.error_item_name_not_in_database(equipment_item_key)
        raise KeyError
