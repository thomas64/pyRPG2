
"""
dict: ShopDatabase
"""

from database import EquipmentType
from database import WeaponType


ShopDatabase = dict()

ShopDatabase['shop1'] = dict(content=[EquipmentType.arm])
ShopDatabase['shop2'] = dict(content=[WeaponType.swd, WeaponType.haf, WeaponType.pol])
