
"""
def: factory_pouch_items
"""

import console
import pouchitems.item
import database.pouchitem


def factory_pouch_item(pouch_item_key):
    """
    Geeft een PouchItem object terug op verzoek van een key.
    :param pouch_item_key: een sleutel uit de pouch items databases bijv "herbs"
    """
    if pouch_item_key in database.pouchitem.p:
        return pouchitems.item.PouchItem(**database.pouchitem.p[pouch_item_key])
    else:
        console.error_item_name_not_in_database(pouch_item_key)
        raise KeyError
