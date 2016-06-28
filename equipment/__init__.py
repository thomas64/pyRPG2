
"""
def: factory_empty_equipment_item
def: factory_equipment_item
"""

# todo, uit colornote app:
# - min int gebruiken voor items?
# - mvp aan items


def factory_empty_equipment_item(equipment_type):
    """
    Geeft een 'empty' EquipmentItem object terug op verzoek van een type.
    Met **, hij verwacht een dict.
    :param equipment_type: Enum EquipmentType, dus bijv. "sld" "Shield".
    """
    from .item import EquipmentItem
    return EquipmentItem(**dict(typ=equipment_type))


def factory_equipment_item(equipment_item_key):
    """
    Geeft een EquipmentItem object terug op verzoek van een key.
    :param equipment_item_key: een sleutel uit de eqp items databases bijv "bronzeshortsword"
    """
    import console
    from database import WeaponDatabase
    from database import ShieldDatabase
    from database import HelmetDatabase
    from database import AmuletDatabase
    from database import ArmorDatabase
    from database import CloakDatabase
    from database import BraceletDatabase
    from database import GlovesDatabase
    from database import RingDatabase
    from database import BeltDatabase
    from database import BootsDatabase
    from database import AccessoryDatabase
    from .item import EquipmentItem

    if equipment_item_key in WeaponDatabase:
        return EquipmentItem(**WeaponDatabase[equipment_item_key])
    elif equipment_item_key in ShieldDatabase:
        return EquipmentItem(**ShieldDatabase[equipment_item_key])
    elif equipment_item_key in HelmetDatabase:
        return EquipmentItem(**HelmetDatabase[equipment_item_key])
    elif equipment_item_key in AmuletDatabase:
        return EquipmentItem(**AmuletDatabase[equipment_item_key])
    elif equipment_item_key in ArmorDatabase:
        return EquipmentItem(**ArmorDatabase[equipment_item_key])
    elif equipment_item_key in CloakDatabase:
        return EquipmentItem(**CloakDatabase[equipment_item_key])
    elif equipment_item_key in BraceletDatabase:
        return EquipmentItem(**BraceletDatabase[equipment_item_key])
    elif equipment_item_key in GlovesDatabase:
        return EquipmentItem(**GlovesDatabase[equipment_item_key])
    elif equipment_item_key in RingDatabase:
        return EquipmentItem(**RingDatabase[equipment_item_key])
    elif equipment_item_key in BeltDatabase:
        return EquipmentItem(**BeltDatabase[equipment_item_key])
    elif equipment_item_key in BootsDatabase:
        return EquipmentItem(**BootsDatabase[equipment_item_key])
    elif equipment_item_key in AccessoryDatabase:
        return EquipmentItem(**AccessoryDatabase[equipment_item_key])
    else:
        console.error_item_name_not_in_database(equipment_item_key)
        raise KeyError
