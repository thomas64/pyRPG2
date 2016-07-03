
"""
class: ShopDatabase
"""

import enum

from constants import EquipmentType
from constants import WeaponType
from constants import ItemMaterial


PATH = 'resources/sprites/npcs/'
FEXT = 'f.png'
SEXT = 's.png'
SHOP1 = PATH+'Man_01'
SHOP2 = PATH+'Man_02'


class ShopDatabase(enum.Enum):
    """
    ...
    """

    shop1 = dict(content=[WeaponType.swd, WeaponType.haf, WeaponType.pol, WeaponType.mis, WeaponType.thr],
                 material=[ItemMaterial.brz],
                 face=SHOP1+FEXT, sprite=SHOP1+SEXT)
    shop2 = dict(content=[EquipmentType.arm, EquipmentType.sld, EquipmentType.hlm],
                 material=[ItemMaterial.wdn, ItemMaterial.ltr],
                 face=SHOP2+FEXT, sprite=SHOP2+SEXT)
