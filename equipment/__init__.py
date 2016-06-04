
"""
def: factory_empty_equipment_item
def: factory_equipment_item
"""

import console
import equipment.item
import database.weapon
import database.shield
import database.helmet
import database.amulet
import database.armor
import database.cloak
import database.bracelet
import database.gloves
import database.ring
import database.belt
import database.boots
import database.accessory

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
    if equipment_item_key in database.weapon.wpn:
        return equipment.item.EquipmentItem(**database.weapon.wpn[equipment_item_key])
    elif equipment_item_key in database.shield.sld:
        return equipment.item.EquipmentItem(**database.shield.sld[equipment_item_key])
    elif equipment_item_key in database.helmet.hlm:
        return equipment.item.EquipmentItem(**database.helmet.hlm[equipment_item_key])
    elif equipment_item_key in database.amulet.amu:
        return equipment.item.EquipmentItem(**database.amulet.amu[equipment_item_key])
    elif equipment_item_key in database.armor.arm:
        return equipment.item.EquipmentItem(**database.armor.arm[equipment_item_key])
    elif equipment_item_key in database.cloak.clk:
        return equipment.item.EquipmentItem(**database.cloak.clk[equipment_item_key])
    elif equipment_item_key in database.bracelet.brc:
        return equipment.item.EquipmentItem(**database.bracelet.brc[equipment_item_key])
    elif equipment_item_key in database.gloves.glv:
        return equipment.item.EquipmentItem(**database.gloves.glv[equipment_item_key])
    elif equipment_item_key in database.ring.rng:
        return equipment.item.EquipmentItem(**database.ring.rng[equipment_item_key])
    elif equipment_item_key in database.belt.blt:
        return equipment.item.EquipmentItem(**database.belt.blt[equipment_item_key])
    elif equipment_item_key in database.boots.bts:
        return equipment.item.EquipmentItem(**database.boots.bts[equipment_item_key])
    elif equipment_item_key in database.accessory.acy:
        return equipment.item.EquipmentItem(**database.accessory.acy[equipment_item_key])
    else:
        console.error_item_name_not_in_database(equipment_item_key)
        raise KeyError
