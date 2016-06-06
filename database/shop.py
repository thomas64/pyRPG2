
"""
dict: ShopDatabase
"""

from database import EquipmentType
from database import WeaponType


PATH = 'resources/sprites/npcs/'
PATHEXT = '_Shop.png'
FACE = 'f'
SPRITE = 's'


ShopDatabase = dict()

ShopDatabase['shop1'] = dict(content=[WeaponType.swd, WeaponType.haf, WeaponType.pol],
                             face=PATH+'01'+FACE+PATHEXT,
                             sprite=PATH+'01'+SPRITE+PATHEXT)
ShopDatabase['shop2'] = dict(content=[EquipmentType.arm],
                             face=PATH+'02'+FACE+PATHEXT,
                             sprite=PATH+'02'+SPRITE+PATHEXT)
