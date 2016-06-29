
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

    if equipment_item_key in WeaponDatabase.__members__:
        return EquipmentItem(**WeaponDatabase[equipment_item_key].value)
    elif equipment_item_key in ShieldDatabase.__members__:
        return EquipmentItem(**ShieldDatabase[equipment_item_key].value)
    elif equipment_item_key in HelmetDatabase.__members__:
        return EquipmentItem(**HelmetDatabase[equipment_item_key].value)
    elif equipment_item_key in AmuletDatabase.__members__:
        return EquipmentItem(**AmuletDatabase[equipment_item_key].value)
    elif equipment_item_key in ArmorDatabase.__members__:
        return EquipmentItem(**ArmorDatabase[equipment_item_key].value)
    elif equipment_item_key in CloakDatabase.__members__:
        return EquipmentItem(**CloakDatabase[equipment_item_key].value)
    elif equipment_item_key in BraceletDatabase.__members__:
        return EquipmentItem(**BraceletDatabase[equipment_item_key].value)
    elif equipment_item_key in GlovesDatabase.__members__:
        return EquipmentItem(**GlovesDatabase[equipment_item_key].value)
    elif equipment_item_key in RingDatabase.__members__:
        return EquipmentItem(**RingDatabase[equipment_item_key].value)
    elif equipment_item_key in BeltDatabase.__members__:
        return EquipmentItem(**BeltDatabase[equipment_item_key].value)
    elif equipment_item_key in BootsDatabase.__members__:
        return EquipmentItem(**BootsDatabase[equipment_item_key].value)
    elif equipment_item_key in AccessoryDatabase.__members__:
        return EquipmentItem(**AccessoryDatabase[equipment_item_key].value)
    else:
        console.error_item_name_not_in_database(equipment_item_key)
        raise KeyError
