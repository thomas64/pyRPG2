
"""
class: PouchItemDatabase
"""

import enum

GOLDPATH = "resources/sprites/icons/pouch/gold.png"
HERBSPATH = "resources/sprites/icons/pouch/herbs.png"
SPICESPATH = "resources/sprites/icons/pouch/spices.png"


class PouchItemDatabase(enum.Enum):
    """..."""
    gold = dict(nam="Gold",     srt=1, spr=GOLDPATH)
    herbs = dict(nam="Herbs",   srt=2, spr=HERBSPATH)
    spices = dict(nam="Spices", srt=3, spr=SPICESPATH)
