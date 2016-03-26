
"""
Pouchitems
"""

import collections


GOLDPATH = "resources/sprites/icons/pouch/gold.png"
HERBSPATH = "resources/sprites/icons/pouch/herbs.png"
SPICESPATH = "resources/sprites/icons/pouch/spices.png"

p = collections.OrderedDict()

p['gold'] = dict(nam="Gold",     srt=1, spr=GOLDPATH)
p['herbs'] = dict(nam="Herbs",   srt=2, spr=HERBSPATH)
p['spices'] = dict(nam="Spices", srt=3, spr=SPICESPATH)
