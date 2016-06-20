
"""
class: ShopDatabase
"""

import enum

from database import EquipmentType
from database import WeaponType
from database import ItemMaterial


PATH = 'resources/sprites/npcs/Shop_'
FACE = 'f.png'
SPRITE = 's.png'


class ShopDatabase(enum.Enum):
    """
    ...
    """

    shop1 = dict(content=[WeaponType.swd, WeaponType.haf, WeaponType.pol, WeaponType.mis, WeaponType.thr],
                 material=[ItemMaterial.brz],
                 face=PATH+'01'+FACE,
                 sprite=PATH+'01'+SPRITE)
    shop2 = dict(content=[EquipmentType.arm, EquipmentType.sld, EquipmentType.hlm],
                 material=[ItemMaterial.wdn, ItemMaterial.ltr],
                 face=PATH+'02'+FACE,
                 sprite=PATH+'02'+SPRITE)
