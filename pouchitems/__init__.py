
"""
def: factory_pouch_items
"""

import console
from database import pch_itm
import pouchitems.item


def factory_pouch_item(pouch_item_key):
    """
    Geeft een PouchItem object terug op verzoek van een key.
    :param pouch_item_key: een sleutel uit de pouch items databases bijv "herbs"
    """
    if pouch_item_key in pch_itm:
        return pouchitems.item.PouchItem(**pch_itm[pouch_item_key])
    else:
        console.error_item_name_not_in_database(pouch_item_key)
        raise KeyError
