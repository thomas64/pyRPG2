
"""
class: Console
"""


class Console:
    """
    Alle print commando's van het spel.
    """

    @staticmethod
    def keyboard_down(event_key, event_unicode):
        """
        Engine.single_input()
        :param event_key: integer
        :param event_unicode: string
        """
        print("Keyboard, key={}, unicode={}".format(event_key, event_unicode))

    @staticmethod
    def mouse_down(event_pos, event_button):
        """
        Engine.single_input()
        :param event_pos: tuple
        :param event_button: integer
        """
        print("Mouse, pos={}, button={}".format(event_pos, event_button))

    @staticmethod
    def state_push(state):
        """
        StateMachine.push()
        :param state: Enum
        """
        print("Game pushed {} on stack.".format(state))

    @staticmethod
    def state_pop(state):
        """
        StateMachine.pop()
        :param state: Enum
        """
        print("Game popped {} off stack.".format(state))

    @staticmethod
    def state_clear():
        """
        StateMachine._clear()
        """
        print("Game cleared all states from stack.")

    @staticmethod
    def load_options():
        """
        Audio._load_cfg()
        Video._load_cfg()
        """
        print("Loading options file...")

    @staticmethod
    def write_options():
        """
        Audio.write_cfg()
        Video.write_cfg()
        """
        print("Writing options files...")

    @staticmethod
    def corrupt_options():
        """
        Video._load_cfg()
        Audio._load_cfg()
        """
        print("Corrupt options file.")

    @staticmethod
    def load_gamedata():
        """
        Dialog.load()
        """
        print("Loading gamedata...")

    @staticmethod
    def save_gamedata():
        """
        Dialog.save()
        """
        print("Saving gamedata...")

    @staticmethod
    def delete_gamedata():
        """
        Dialog.delete()
        """
        print("Deleting gamedata...")

    @staticmethod
    def corrupt_gamedata():
        """
        Dialog.load()
        """
        print("Corrupt gamedata.")

    @staticmethod
    def error_unknown_map_object():
        """
        Map()
        """
        print("Unknown Map Object.")

    @staticmethod
    def container_is_full(container_name):
        """
        Inventory.add_i()
        Pouch.add()
        :param container_name: string
        """
        print("{} is full.".format(container_name))

    @staticmethod
    def hero_join_party(hero_name, party_name):
        """
        Party.add()
        :param hero_name: string
        :param party_name: string
        """
        print("{} joined {}.".format(hero_name, party_name))

    @staticmethod
    def error_hero_double_join(hero_name, party_name):
        """
        Party.add()
        :param hero_name: string
        :param party_name: string
        """
        print("{} is already in {}.".format(hero_name, party_name))

    @staticmethod
    def error_hero_not_in_party(hero_name, party_name):
        """
        Party.remove()
        :param hero_name: string
        :param party_name: string
        """
        print("{} is not in {}.".format(hero_name, party_name))

    @staticmethod
    def error_leader_not_leave_party():
        """
        Party.remove()
        """
        print("The party leader cannot leave his own party!")

    @staticmethod
    def add_item_in_container(item_quantity, item_name, container_name):
        """
        Inventory.add_i()
        Pouch.add()
        :param item_quantity: integer
        :param item_name: string
        :param container_name: string
        """
        print("Put {} {} in {}.".format(item_quantity, item_name, container_name))

    @staticmethod
    def remove_item_from_container(item_quantity, item_name, container_name):
        """
        Inventory.remove_i()
        Pouch.remove()
        :param item_quantity: integer
        :param item_name: string
        :param container_name: string
        """
        print("Removed {} {} from {}.".format(item_quantity, item_name, container_name))

    @staticmethod
    def error_quantity_less_than_one(quantity):
        """
        Inventory.add_i()
        Inventory.remove_i()
        Pouch.add()
        Pouch.remove()
        :param quantity: integer
        """
        print("Quantity of {} is not possible.".format(quantity))

    @staticmethod
    def error_no_equipment_item():
        """
        Inventory.remove_i()
        """
        print("Equipment item not in container.")

    @staticmethod
    def error_quantity_not_enough():
        """
        Inventory.remove_i()
        """
        print("Item quantity not in container.")

    @staticmethod
    def quantity_not_enough(item_name, item_price, item_quantity):
        """
        Pouch.remove()
        """
        print("Not enough {}.".format(item_name))
        print("You need {} more {}.".format(item_price - item_quantity, item_name))

    @staticmethod
    def error_unknown_column_key():
        """
        ListBox.render()
        """
        print("Not 'icon', 'f_icon', or 'text'.")
