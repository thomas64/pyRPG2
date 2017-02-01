
"""
class: MoveEventDatabase
"""

from constants import Direction
from constants import PersonState


class MoveEventDatabase(dict):
    """
    Condition wordt op False gezet bij het eenmalig uitvoeren van de event.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self['move1'] = dict(condition=True,
                             movement=[                               # seconden
                                 [PersonState.Resting, Direction.South, 1],
                                 [PersonState.Resting, Direction.North, 0.5],
                                 [PersonState.Resting, Direction.West,  0.5],
                                 [PersonState.Resting, Direction.East,  0.5],
                                 [PersonState.Resting, Direction.West,  0.5],
                                 [PersonState.Resting, Direction.East,  0.5],
                                 [PersonState.Resting, Direction.South, 0.5],
                                 [PersonState.Moving,  Direction.South, 0.8],
                                 [PersonState.Moving,  Direction.West,  2.2],
                                 [PersonState.Moving,  Direction.South, 1.2],
                                 [PersonState.Moving,  Direction.West,  2.9],
                                 [PersonState.Resting, Direction.West,  1],
                                 [PersonState.Resting, Direction.East,  0.5],
                                 [PersonState.Resting, Direction.North, 0.5],
                                 [PersonState.Resting, Direction.South, 0.5],
                                 [PersonState.Resting, Direction.East,  0.5],
                                 [PersonState.Resting, Direction.West,  0.5],
                                 [PersonState.Resting, Direction.North, 0.5],
                                 [PersonState.Resting, Direction.South, 0.5],
                                ]
                             )
        self['move2'] = dict(condition=True,
                             movement=[
                                 [PersonState.Resting, Direction.South, 1],
                                 [PersonState.Resting, Direction.West,  0.5],
                                 [PersonState.Resting, Direction.East,  0.5],
                                 [PersonState.Resting, Direction.South, 0.5],
                                 [PersonState.Moving,  Direction.South, 0.6],
                                ]
                             )
