
"""
class: ShopDatabase
"""

import enum

from database import EquipmentType
from database import WeaponType


PATH = 'resources/sprites/npcs/'
PATHEXT = '_Shop.png'
FACE = 'f'
SPRITE = 's'


class ShopDatabase(enum.Enum):
    """
    ...
    """

    shop1 = dict(content=[WeaponType.swd, WeaponType.haf, WeaponType.pol],
                 face=PATH+'01'+FACE+PATHEXT,
                 sprite=PATH+'01'+SPRITE+PATHEXT)
    shop2 = dict(content=[EquipmentType.arm],
                 face=PATH+'02'+FACE+PATHEXT,
                 sprite=PATH+'02'+SPRITE+PATHEXT)
