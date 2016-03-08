
"""
class: StateMachine
"""

import enum

import console


class States(enum.Enum):
    """
    Alle states uit het spel.
    """
    MainMenu = 1
    LoadMenu = 2
    SaveMenu = 3
    OptionsMenu = 4
    PauseMenu = 5

    Overworld = 6
    Battle = 7
    Conversation = 8
    PartyScreen = 9


class StateMachine(object):
    """
    Manages a stack based state machine.
    peek(), pop() and push() perform as traditionally expected.
    peeking and popping an empty stack returns None.
    """
    def __init__(self):
        self.statestack = []

    def peek(self):
        """
        Returns the current state without altering the stack.
        Returns None if the stack is empty.
        """
        try:
            return self.statestack[-1]      # [-1] is om de laatste in een list te krijgen
        except IndexError:
            return None                     # empty stack

    def pop(self):
        """
        Returns the current state and remove it from the stack.
        Returns None if the stack is empty.
        """
        try:
            console.state_pop()
            self.statestack.pop()
            return len(self.statestack) > 0
        except IndexError:
            return None                     # empty stack

    def push(self, state):
        """
        :param state: Push a new state onto the stack.
        :return: Returns the pushed value.
        """
        console.state_push(state)
        try:
            self.peek().on_exit()
        except AttributeError:
            pass                            # doe niet on_exit() bij lege stack
        self.statestack.append(state)
        self.peek().on_enter()
        return state

    def clear(self):
        """
        Clear the whole stack.
        """
        self.peek().on_exit()
        console.state_clear()
        self.statestack = []

    def change(self, state):
        """
        Clear the whole stack. And pushes one.
        :param state: Push a new state onto the stack.
        """
        self.clear()
        self.push(state)
