
"""
class: HeroData
"""

import enum


PATH = 'resources/sprites/heroes/'


class HeroData(enum.Enum):
    """
    ...
    """
    alagos = dict(name="Alagos", sprite=PATH+"01s_Alagos.png", face=PATH+"01f_Alagos.png",
                  lev=1, txp=500, int=18, wil=12, dex=15, agi=15, edu=15, str=15, sta=30,
                  chm=0, dip=0, lor=0, mec=0, med=0, mer=0, ran=0, sci=1, stl=1, thf=0, trb=1, war=3,
                  haf=1, mis=3, pol=0, shd=3, swd=3, thr=0,
                  wpn=None, sld=None, hlm=None, nlc=None, arm=None, clk=None,
                  glv=None, lrg=None, rrg=None, blt=None, bts=None, acy=None)
    # ringen nog, en None vervangen door de enums
