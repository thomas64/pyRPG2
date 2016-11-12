
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


class ShopDatabase(enum.Enum):
    """
    ...
    """

    shop1 = dict(content=[WeaponType.swd, WeaponType.haf, WeaponType.pol, WeaponType.mis, WeaponType.thr],
                 material=[ItemMaterial.brz],
                 name='man01')
    shop2 = dict(content=[EquipmentType.arm, EquipmentType.sld, EquipmentType.hlm],
                 material=[ItemMaterial.wdn, ItemMaterial.ltr],
                 name='man50')
    shop3 = dict(content=[EquipmentType.clk, EquipmentType.blt, EquipmentType.bts, EquipmentType.glv],
                 material=[ItemMaterial.ctn, ItemMaterial.ltr],
                 name='man52')
    shop4 = dict(content=[EquipmentType.amu, EquipmentType.rng, EquipmentType.brc],
                 name='youngwoman04')
    shop5 = dict(content=[EquipmentType.acy, (EquipmentType.itm,
                                              [itm for itm in PiDb if itm.value.get('val')])],
                                              # [PiDb.herbs, PiDb.spices, PiDb.hlg_pot, PiDb.ant_pot, PiDb.fir_flk])],
                 name='youngwoman03')

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

for shop in ShopDatabase:
    shop.value['face'] = PATH+shop.value['name']+FEXT
    shop.value['sprite'] = PATH+shop.value['name']+SEXT
