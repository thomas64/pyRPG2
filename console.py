
"""
Alle print commando's van het spel.
"""


def keyboard_down(event_key, event_unicode):
    """
    Engine.single_input()
    :param event_key: integer
    :param event_unicode: string
    """
    print("Keyboard, key={}, unicode={}".format(event_key, event_unicode))


def mouse_down(event_pos, event_button):
    """
    Engine.single_input()
    :param event_pos: tuple
    :param event_button: integer
    """
    print("Mouse, pos={}, button={}".format(event_pos, event_button))


def state_push(state):
    """
    StateMachine.push()
    :param state: Enum
    """
    print("Game pushed {} on stack.".format(state))


def state_pop(state):
    """
    StateMachine.pop()
    :param state: Enum
    """
    print("Game popped {} off stack.".format(state))


def state_clear():
    """
    StateMachine._clear()
    """
    print("Game cleared all states from stack.")


def load_options():
    """
    Audio._load_cfg()
    Video._load_cfg()
    """
    print("Loading options file...")


def write_options():
    """
    Audio.write_cfg()
    Video.write_cfg()
    """
    print("Writing options files...")


def corrupt_options():
    """
    Video._load_cfg()
    Audio._load_cfg()
    """
    print("Corrupt options file.")


def load_gamedata():
    """
    Dialog.load()
    """
    print("Loading gamedata...")


def save_gamedata():
    """
    Dialog.save()
    """
    print("Saving gamedata...")


def delete_gamedata():
    """
    Dialog.delete()
    """
    print("Deleting gamedata...")


def corrupt_gamedata():
    """
    Dialog.load()
    """
    print("Corrupt gamedata.")


def container_is_full(container_name):
    """
    Party.add()
    Inventory.add()
    Pouch.add()
    :param container_name: string
    """
    print("{} is full.".format(container_name))


def hero_join_party(hero_name, party_name):
    """
    Party.add()
    :param hero_name: string
    :param party_name: string
    """
    print("{} joined {}.".format(hero_name, party_name))


def error_hero_double_join(hero_name, party_name):
    """
    Party.add()
    :param hero_name: string
    :param party_name: string
    """
    print("{} is already in {}.".format(hero_name, party_name))


def error_hero_not_in_party(hero_name, party_name):
    """
    Party.remove()
    :param hero_name: string
    :param party_name: string
    """
    print("{} is not in {}.".format(hero_name, party_name))


def error_leader_not_leave_party():
    """
    Party.remove()
    """
    print("The party leader cannot leave his own party!")


def add_item_in_container(item_quantity, item_name, container_name):
    """
    Inventory.add()
    Pouch.add()
    :param item_quantity: integer
    :param item_name: string
    :param container_name: string
    """
    print("Put {} {} in {}.".format(item_quantity, item_name, container_name))


def remove_item_from_container(item_quantity, item_name, container_name):
    """
    Inventory.remove()
    Pouch.remove()
    :param item_quantity: integer
    :param item_name: string
    :param container_name: string
    """
    print("Removed {} {} from {}.".format(item_quantity, item_name, container_name))


def error_quantity_less_than_one(quantity):
    """
    Inventory.add()
    Inventory.remove()
    Pouch.add()
    Pouch.remove()
    :param quantity: integer
    """
    print("Quantity of {} is not possible.".format(quantity))


def error_no_equipment_item():
    """
    Inventory.remove()
    """
    print("Equipment item not in container.")


def error_quantity_not_enough():
    """
    Inventory.remove()
    """
    print("Item quantity not in container.")


def quantity_not_enough(item_name, item_price, item_quantity):
    """
    Pouch.remove()
    """
    print("Not enough {}.".format(item_name))
    print("You need {} more {}.".format(item_price - item_quantity, item_name))


def error_item_name_not_in_database(item_name):
    """
    equipment.factory()
    pouchitems.factory()
    :param item_name: string
    """
    print("Cannot find {} in database.".format(item_name))
