
"""
class: ShopDatabase
"""

import enum

from constants import EquipmentType
from constants import WeaponType
from constants import ItemMaterial

from .pouchitem import PouchItemDatabase as PiDb


PATH = 'resources/sprites/npcs/'
FEXT = 'f.png'
SEXT = 's.png'
SHOP1 = PATH+'man01'
SHOP2 = PATH+'man50'
SHOP3 = PATH+'man52'
SHOP4 = PATH+'woman51'


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
    shop3 = dict(content=[EquipmentType.clk, EquipmentType.blt, EquipmentType.bts, EquipmentType.glv],
                 material=[ItemMaterial.ctn, ItemMaterial.ltr],
                 face=SHOP3+FEXT, sprite=SHOP3+SEXT)
    shop4 = dict(content=[EquipmentType.amu, EquipmentType.rng, EquipmentType.brc, EquipmentType.acy,
                          (EquipmentType.itm, [PiDb.herbs, PiDb.healing_potions])],
                 face=SHOP4+FEXT, sprite=SHOP4+SEXT)

    @staticmethod
    def welcome_text():
        """..."""
        return ("Good day sir, and welcome to my shop.",
                "In the 'Buy' box you can find all what",
                "my shop has to offer.  And in the 'Sell'",
                "box your own inventory is shown.",
                "Click once on a selected item to buy or to sell.",
                "You can scroll through the lists with your mouse-",
                "wheel if the list is longer than what you can see.",
                "Below here, you see one or multiple icons.",
                "They represent different sections of my shop.",
                "Click on it to enter one of those sections.")
