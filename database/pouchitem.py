
"""
Pouchitems
"""

import collections


GOLDPATH = "resources/sprites/icons/pouch/gold.png"
HERBSPATH = "resources/sprites/icons/pouch/herbs.png"
SPICESPATH = "resources/sprites/icons/pouch/spices.png"

pch_itm = collections.OrderedDict()

pch_itm['gold'] = dict(nam="Gold",     srt=1, spr=GOLDPATH)
pch_itm['herbs'] = dict(nam="Herbs",   srt=2, spr=HERBSPATH)
pch_itm['spices'] = dict(nam="Spices", srt=3, spr=SPICESPATH)
