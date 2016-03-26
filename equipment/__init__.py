
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
    if equipment_item_key in database.weapon.w:
        return equipment.item.EquipmentItem(**database.weapon.w[equipment_item_key])
    elif equipment_item_key in database.shield.s:
        return equipment.item.EquipmentItem(**database.shield.s[equipment_item_key])
    elif equipment_item_key in database.helmet.h:
        return equipment.item.EquipmentItem(**database.helmet.h[equipment_item_key])
    elif equipment_item_key in database.amulet.a:
        return equipment.item.EquipmentItem(**database.amulet.a[equipment_item_key])
    elif equipment_item_key in database.armor.a:
        return equipment.item.EquipmentItem(**database.armor.a[equipment_item_key])
    elif equipment_item_key in database.cloak.c:
        return equipment.item.EquipmentItem(**database.cloak.c[equipment_item_key])
    elif equipment_item_key in database.bracelet.b:
        return equipment.item.EquipmentItem(**database.bracelet.b[equipment_item_key])
    elif equipment_item_key in database.gloves.g:
        return equipment.item.EquipmentItem(**database.gloves.g[equipment_item_key])
    elif equipment_item_key in database.ring.r:
        return equipment.item.EquipmentItem(**database.ring.r[equipment_item_key])
    elif equipment_item_key in database.belt.b:
        return equipment.item.EquipmentItem(**database.belt.b[equipment_item_key])
    elif equipment_item_key in database.boots.b:
        return equipment.item.EquipmentItem(**database.boots.b[equipment_item_key])
    elif equipment_item_key in database.accessory.a:
        return equipment.item.EquipmentItem(**database.accessory.a[equipment_item_key])
    else:
        console.error_item_name_not_in_database(equipment_item_key)
        raise KeyError
