
"""
class: State
class: Statemachine
"""

import enum


class State(enum.Enum):
    """
    State machine constants for the StateMachine class below
    """
    MainMenu = 1
    OptionsMenu = 2
    PauseMenu = 3
    OverWorld = 4


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
            return None     # empty stack

    def pop(self, state):
        """
        Returns the current state and remove it from the stack.
        Returns None if the stack is empty.
        :param state: print the name of the popped state
        """
        try:
            print("Game popped {}".format(state))
            self.statestack.pop()
            return len(self.statestack) > 0
        except IndexError:
            return None     # empty stack

    def push(self, state):
        """
        :param state: Push a new state onto the stack.
        :return: Returns the pushed value.
        """
        print("Game pushed {}".format(state))
        self.statestack.append(state)
        return state

    def clear(self):
        """
        Clear the whole stack.
        """
        print("Game cleared all states.")
        self.statestack = []
