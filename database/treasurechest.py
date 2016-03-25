
"""
TreasureChest
"""

t = dict()

# start_forest
t['chest1'] = dict(content=dict(eqp1=dict(nam='bronzeshortsword', qty=1),
                                eqp2=dict(nam='leathercap',       qty=1)))

# self['chest1'] = dict(content=dict(gold=100,
#                                    herbs=3,
#                                    eqp1=dict(typ='wpn', nam='bronzeshortsword', qty=1),
#                                    eqp2=dict(typ='hlm', nam='leathercap',       qty=1)))

for value in t.values():
    value['opened'] = 0
