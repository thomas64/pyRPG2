
"""
class: HeroDatabase
"""

import enum

PATH = 'resources/sprites/heroes/'


class HeroDatabase(enum.Enum):
    """
    Alle heroes uit het spel als Enum met een dict voor de waarden.
    """
    # todo, alle hero data toevoegen

    alagos = dict(nam="Alagos", spr=PATH+"01s_Alagos.png", fac=PATH+"01f_Alagos.png",
                  lev=1, exp=500, int=18, wil=12, dex=15, agi=15, edu=15, str=15, sta=30,
                  alc=0, dip=0, hlr=0, lor=0, mec=0, mer=0, ran=0, stl=1, thf=0, trb=1, war=3, wiz=1,
                  haf=1, mis=3, pol=0, shd=3, swd=3, thr=0,
                  wpn='bronzeshortsword', sld='woodenbuckler', arm='lightleatherarmor')
    luana = dict(nam="Luana", spr=PATH+"02s_Luana.png", fac=PATH+"02f_Luana.png",
                 lev=1, exp=500, int=14, wil=10, dex=22, agi=20, edu=10, str=8, sta=20,
                 alc=0, dip=0, hlr=0, lor=0, mec=1, mer=0, ran=0, stl=3, thf=3, trb=0, war=0, wiz=0,
                 haf=-1, mis=-1, pol=0, shd=-1, swd=1, thr=2,
                 wpn='bronzedagger', sld=None, arm='lightleatherarmor')
    grindan = dict(nam="Grindan", spr=PATH+"03s_Grindan.png", fac=PATH+"03f_Grindan.png",
                   lev=8, exp=102000, int=10, wil=8, dex=25, agi=10, edu=20, str=20, sta=40,
                   alc=-1, dip=0, hlr=0, lor=0, mec=0, mer=0, ran=0, stl=1, thf=-1, trb=0, war=4, wiz=-1,
                   haf=0, mis=-1, pol=0, shd=2, swd=4, thr=2,
                   wpn='ironlongsword', sld='irontarge', arm='mediumbronzearmor')
    rydalin = dict(nam="Rydalin", spr=PATH+"04s_Rydalin.png", fac=PATH+"04f_Rydalin.png",
                   lev=3, exp=7000, int=22, wil=16, dex=20, agi=15, edu=16, str=10, sta=31,
                   alc=0, dip=0, hlr=0, lor=1, mec=0, mer=1, ran=0, stl=0, thf=0, trb=0, war=0, wiz=4,
                   haf=0, mis=-1, pol=3, shd=0, swd=3, thr=-1,
                   wpn='bronzestaff', sld=None, arm='mediumleatherarmor')
    codrif = dict(nam="Codrif", spr=PATH+"05s_Codrif.png", fac=PATH+"05f_Codrif.png",
                  lev=2, exp=2500, int=22, wil=18, dex=15, agi=12, edu=15, str=10, sta=20,
                  alc=3, dip=0, hlr=0, lor=2, mec=2, mer=0, ran=0, stl=0, thf=0, trb=0, war=0, wiz=2,
                  haf=-1, mis=-1, pol=0, shd=-1, swd=1, thr=1,
                  wpn='bronzedagger', sld=None, arm='lightleatherarmor')
    galen = dict(nam="Galen", spr=PATH+"06s_Galen.png", fac=PATH+"06f_Galen.png",
                 lev=4, exp=15000, int=15, wil=15, dex=18, agi=10, edu=20, str=25, sta=40,
                 alc=-1, dip=0, hlr=0, lor=0, mec=0, mer=0, ran=4, stl=3, thf=0, trb=0, war=5, wiz=-1,
                 haf=5, mis=3, pol=0, shd=3, swd=-1, thr=-1,
                 wpn='ironaxe', sld='irontarge', arm='mediumbronzearmor')
    raiko = dict(nam="Raiko", spr=PATH+"07s_Raiko.png", fac=PATH+"07f_Raiko.png",
                 lev=12, exp=325000, int=6, wil=11, dex=14, agi=8, edu=30, str=30, sta=60,
                 alc=-1, dip=0, hlr=0, lor=-1, mec=0, mer=0, ran=0, stl=1, thf=-1, trb=-1, war=6, wiz=-1,
                 haf=0, mis=-1, pol=6, shd=4, swd=6, thr=-1,
                 wpn='ironbroadsword', sld='ironkite', arm='heavyironarmor')
    # name = dict(nam="", spr=PATH+"0s_.png", fac=PATH+"0f_.png",
    #              lev=, exp=, int=, wil=, dex=, agi=, edu=, str=, sta=,
    #              alc=0, dip=0, hlr=0, lor=0, mec=0, mer=0, ran=0, stl=0, thf=0, trb=0, war=0, wiz=0,
    #              haf=0, mis=0, pol=0, shd=0, swd=0, thr=0,
    #              wpn=items.weapon.WeaponsData.empty, sld=items.shield.ShieldsData.empty,
    #              arm=items.armor.ArmorsData.empty)
    # name = dict(nam="", spr=PATH+"0s_.png", fac=PATH+"0f_.png",
    #              lev=, exp=, int=, wil=, dex=, agi=, edu=, str=, sta=,
    #              alc=0, dip=0, hlr=0, lor=0, mec=0, mer=0, ran=0, stl=0, thf=0, trb=0, war=0, wiz=0,
    #              haf=0, mis=0, pol=0, shd=0, swd=0, thr=0,
    #              wpn=items.weapon.WeaponsData.empty, sld=items.shield.ShieldsData.empty,
    #              arm=items.armor.ArmorsData.empty)
    # name = dict(nam="", spr=PATH+"0s_.png", fac=PATH+"0f_.png",
    #              lev=, exp=, int=, wil=, dex=, agi=, edu=, str=, sta=,
    #              alc=0, dip=0, hlr=0, lor=0, mec=0, mer=0, ran=0, stl=0, thf=0, trb=0, war=0, wiz=0,
    #              haf=0, mis=0, pol=0, shd=0, swd=0, thr=0,
    #              wpn=items.weapon.WeaponsData.empty, sld=items.shield.ShieldsData.empty,
    #              arm=items.armor.ArmorsData.empty)
    # name = dict(nam="", spr=PATH+"0s_.png", fac=PATH+"0f_.png",
    #              lev=, exp=, int=, wil=, dex=, agi=, edu=, str=, sta=,
    #              alc=0, dip=0, hlr=0, lor=0, mec=0, mer=0, ran=0, stl=0, thf=0, trb=0, war=0, wiz=0,
    #              haf=0, mis=0, pol=0, shd=0, swd=0, thr=0,
    #              wpn=items.weapon.WeaponsData.empty, sld=items.shield.ShieldsData.empty,
    #              arm=items.armor.ArmorsData.empty)
    # name = dict(nam="", spr=PATH+"0s_.png", fac=PATH+"0f_.png",
    #              lev=, exp=, int=, wil=, dex=, agi=, edu=, str=, sta=,
    #              alc=0, dip=0, hlr=0, lor=0, mec=0, mer=0, ran=0, stl=0, thf=0, trb=0, war=0, wiz=0,
    #              haf=0, mis=0, pol=0, shd=0, swd=0, thr=0,
    #              wpn=items.weapon.WeaponsData.empty, sld=items.shield.ShieldsData.empty,
    #              arm=items.armor.ArmorsData.empty)
    # name = dict(nam="", spr=PATH+"0s_.png", fac=PATH+"0f_.png",
    #              lev=, exp=, int=, wil=, dex=, agi=, edu=, str=, sta=,
    #              alc=0, dip=0, hlr=0, lor=0, mec=0, mer=0, ran=0, stl=0, thf=0, trb=0, war=0, wiz=0,
    #              haf=0, mis=0, pol=0, shd=0, swd=0, thr=0,
    #              wpn=items.weapon.WeaponsData.empty, sld=items.shield.ShieldsData.empty,
    #              arm=items.armor.ArmorsData.empty)
    # name = dict(nam="", spr=PATH+"0s_.png", fac=PATH+"0f_.png",
    #              lev=, exp=, int=, wil=, dex=, agi=, edu=, str=, sta=,
    #              alc=0, dip=0, hlr=0, lor=0, mec=0, mer=0, ran=0, stl=0, thf=0, trb=0, war=0, wiz=0,
    #              haf=0, mis=0, pol=0, shd=0, swd=0, thr=0,
    #              wpn=items.weapon.WeaponsData.empty, sld=items.shield.ShieldsData.empty,
    #              arm=items.armor.ArmorsData.empty)

    @staticmethod
    def opening(hero_raw):
        """
        ...
        :param hero_raw:
        """
        if hero_raw == 'galen':
            return ["Good day young man.",
                    "It has been a while since I've seen battle,",
                    "but in my younger days my reputation was",
                    "fearsome. I even saved the King's life once...",
                    "But enough about that.",
                    "I need to be in Dalenok Town and I would like",
                    "to join you when you are ready to go to there.",
                    "My axe will be of service to you.",
                    "",
                    "I would definitely need your axe and reputation.",
                    "I don't want to go to Dalenok Town."]
