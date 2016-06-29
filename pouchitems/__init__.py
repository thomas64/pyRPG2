
"""
def: factory_pouch_items
"""


def factory_pouch_item(pouch_item_key):
    """
    Geeft een PouchItem object terug op verzoek van een key.
    :param pouch_item_key: een sleutel uit de pouch items databases bijv "herbs"
    """
    import console
    from database import PouchItemDatabase
    from .item import PouchItem

    if pouch_item_key in PouchItemDatabase.__members__:
        return PouchItem(**PouchItemDatabase[pouch_item_key].value)
    else:
        console.error_item_name_not_in_database(pouch_item_key)
        raise KeyError
