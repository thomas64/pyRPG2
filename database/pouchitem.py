
"""
class: PouchItemDatabase
"""

import enum
import os

POUCHPATH = "resources/sprites/icons/pouch"

GOLDIMG = os.path.join(POUCHPATH, "gold.png")
HERBIMG = os.path.join(POUCHPATH, "herbs.png")
SPICEIMG = os.path.join(POUCHPATH, "spices.png")
GEMSTONEIMG = os.path.join(POUCHPATH, "gemstones.png")
NOTEPIMG = os.path.join(POUCHPATH, "note.png")


class PouchItemDatabase(enum.Enum):
    """..."""
    gold = dict(nam="Gold",                 srt=1, spr=GOLDIMG)
    herbs = dict(nam="Herbs",               srt=2, spr=HERBIMG)
    spices = dict(nam="Spices",             srt=3, spr=SPICEIMG)
    gemstones = dict(nam="Gemstones",       srt=4, spr=GEMSTONEIMG)
    proofnote = dict(nam="Proofnote",       srt=5, spr=NOTEPIMG)
