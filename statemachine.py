
"""
class: StateMachine
"""

import collections
import enum

import console


class States(enum.Enum):
    """
    Alle states uit het spel.
    """
    MainMenu = 1
    LoadMenu = "Load Game"
    SaveMenu = "Save Game"
    OptionsMenu = 4
    PauseMenu = 5

    Overworld = 6
    Battle = 7
    Conversation = 8
    PartyScreen = 9
    MessageBox = 10
    Shop = 11


class StateMachine(object):
    """
    Manages a stack based state machine.
    peek(), pop() and push() perform as traditionally expected.
    peeking and popping an empty stack returns None.
    """
    def __init__(self):
        self.statestack = collections.deque()
        self.prev_state = None

    def peek(self):
        """
        Returns the current state without altering the stack.
        Returns None if the stack is empty.
        """
        try:
            return self.statestack[-1]      # [-1] is om de laatste in een list te krijgen
        except IndexError:
            return None                     # empty stack

    def deep_peek(self, stackindex=-2):
        """
        Kijk in de op een na bovenste laag van de stack.
        :param stackindex: -1 is de bovenste, -2 is de op een na bovenste, -3 etc.
        """
        try:
            return self.statestack[stackindex]
        except IndexError:
            return None

    def pop(self):
        """
        Returns the current state and remove it from the stack.
        Returns None if the stack is empty.
        """
        try:
            self.prev_state = self.peek().name
            self.peek().on_exit()
            # bij messagebox geen console output
            if self.peek().name != States.MessageBox:
                console.state_pop(self.peek().name)
            del self.statestack[-1]
            self.peek().on_enter()
            self.prev_state = None
            return len(self.statestack) > 0
        except IndexError:
            return None                     # empty stack

    def push(self, state):
        """
        :param state: Push a new state onto the stack.
        :return: Returns the pushed value.
        """
        try:
            self.prev_state = self.peek().name
            self.peek().on_exit()
        except AttributeError:
            pass                            # doe niet on_exit() bij lege stack
        # bij messagebox geen console output
        if state.name != States.MessageBox:
            console.state_push(state.name)
        self.statestack.append(state)
        self.peek().on_enter()
        self.prev_state = None
        return state

    def _clear(self):
        """
        Clear the whole stack.
        """
        self.peek().on_exit()
        console.state_clear()
        self.statestack = []
        self.prev_state = None

    def change(self, state):
        """
        Clear the whole stack. And pushes one.
        :param state: Push a new state onto the stack.
        """
        self._clear()
        self.push(state)

    def swap(self):
        """
        Als de laatste 2 op de stack een messagebox zijn, draai ze dan om.
        """
        if self.statestack[-1].name == States.MessageBox and self.statestack[-2].name == States.MessageBox:
            self.statestack[-1], self.statestack[-2] = self.statestack[-2], self.statestack[-1]
