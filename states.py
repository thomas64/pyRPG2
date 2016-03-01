
"""
class: GameState
class: Statemachine
"""

import enum

import console


class GameState(enum.Enum):
    """
    State machine constants for the StateMachine class
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
        self.audio_state_is_changed = False

    def has_audio_state_changed(self):
        """
        Als er een state veranderd is, zet hem dan weer onveranderd en geef True terug. Anders gewoon False.
        :return: True of False
        """
        if self.audio_state_is_changed:
            self.audio_state_is_changed ^= True
            return True
        else:
            return False

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
            console.state_pop(state)
            self.statestack.pop()
            if state != GameState.OptionsMenu:      # bij optionsmenu niet, omdat het geluid moet doorlopen.
                self.audio_state_is_changed = True
            return len(self.statestack) > 0
        except IndexError:
            return None     # empty stack

    def push(self, state):
        """
        :param state: Push a new state onto the stack.
        :return: Returns the pushed value.
        """
        console.state_push(state)
        self.statestack.append(state)
        if state != GameState.OptionsMenu:
            self.audio_state_is_changed = True
        return state

    def change(self, state):
        """
        Clear the whole stack. And pushes one.
        :param state: Push a new state onto the stack.
        """
        console.state_change()
        self.statestack = []
        self.push(state)
