
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
    StateMachine.clear()
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


def hero_leave_party(hero_name, party_name):
    """
    Party.remove()
    :param hero_name: string
    :param party_name: string
    """
    print("{} left {}.".format(hero_name, party_name))


def error_hero_not_in_party(hero_name, party_name):
    """
    Party.remove()
    :param hero_name: string
    :param party_name: string
    """
    print("{} is not in {}.".format(hero_name, party_name))


def leader_not_leave_party():
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


def remove_equipment_item(equipment_item_quantity, equipment_item_name, inventory_name):
    """
    Inventory.remove()
    :param equipment_item_quantity: integer
    :param equipment_item_name: string
    :param inventory_name: string
    """
    print("Removed {} {} from {}.".format(equipment_item_quantity, equipment_item_name, inventory_name))


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


def error_equipment_item_name_not_in_database(equipment_item_name):
    """
    EquipmentDatabase.factory()
    :param equipment_item_name: string
    """
    print("Cannot find {} in database.".format(equipment_item_name))


def is_equipping(hero_name, equipment_item_name):
    """
    Hero.set_equipment_item()
    :param hero_name: string
    :param equipment_item_name: string
    """
    print("{} is equipping {}.".format(hero_name, equipment_item_name))


def is_unequipping(hero_name, equipment_item_name):
    """
    Hero.set_equipment_item()
    :param hero_name: string
    :param equipment_item_name: string
    """
    print("{} is unequipping {}.".format(hero_name, equipment_item_name))


def not_equipping_skill(hero_name, equipment_item_name):
    """
    Hero.is_able_to_equip()
    :param hero_name: string
    :param equipment_item_name: string
    """
    print("{} doesn't have the skill to equip that {}.".format(hero_name, equipment_item_name))


def not_equipping_min_int(hero_name, equipment_item_name, min_int_of_eqp_item):
    """
    Hero.is_able_to_equip()
    :param hero_name: string
    :param equipment_item_name: string
    :param min_int_of_eqp_item: integer
    """
    print("{} needs {} intelligence to equip that {}.".format(hero_name, min_int_of_eqp_item, equipment_item_name))


def not_equipping_min_str(hero_name, equipment_item_name, min_str_of_eqp_item):
    """
    Hero.is_able_to_equip()
    :param hero_name: string
    :param equipment_item_name: string
    :param min_str_of_eqp_item: integer
    """
    print("{} needs {} strength to equip that {}.".format(hero_name, min_str_of_eqp_item, equipment_item_name))
