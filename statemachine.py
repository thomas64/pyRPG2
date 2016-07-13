
"""
class: StateMachine
"""

import collections

import console
from constants import GameState


class StateMachine(object):
    """
    Manages a stack based state machine.
    peek(), pop() and push() perform as traditionally expected.
    peeking and popping an empty stack returns None.
    """
    def __init__(self):
        self.statestack = collections.deque()
        self.prev_state = None
        self.new_state = False

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
            # bij messagebox en fade geen console output
            if self.peek().name != GameState.MessageBox and \
               self.peek().name != GameState.FadeBlack:
                console.state_pop(self.peek().name)
            del self.statestack[-1]
            self.peek().on_enter()
            self.prev_state = None
            self.new_state = True
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
        # bij messagebox fade geen console output
        if state.name != GameState.MessageBox and \
           state.name != GameState.FadeBlack:
            console.state_push(state.name)
        self.statestack.append(state)
        self.peek().on_enter()
        self.prev_state = None
        self.new_state = True
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
        X (Als de laatste 2 op de stack een messagebox zijn, draai ze dan om.) X
        Nee, draai ze gewoon om, ongeacht de voorwaarde.
        """
        # if self.statestack[-1].name == GameState.MessageBox and self.statestack[-2].name == GameState.MessageBox:
        self.statestack[-1], self.statestack[-2] = self.statestack[-2], self.statestack[-1]

        """
        Interessant om later misschien eens (ongeveer) te gebruiken. Deze draait een gedeelte van de list om.
        def reverse_sublist(lst,start,end):
            sublist=lst[start:end]
            sublist.reverse()
            lst[start:end]=sublist
            print(lst)
        """
