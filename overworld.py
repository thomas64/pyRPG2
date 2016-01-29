
"""
class: OverWorld
"""

import pygame

import character
import map
import sprites


WINDOWWIDTH = 800
WINDOWHEIGHT = 600
WINDOWPOS = 100, 100

BACKGROUNDCOLOR = pygame.Color("black")
GRIDCOLOR = pygame.Color("gray38")
WINDOWCOLOR = pygame.Color("gray12")
HEROCOLOR = pygame.Color("blue")
TREECOLOR = pygame.Color("yellow")

# todo, mooiere map maken met variatie in het gras
OVERWORLDPATH = 'resources/maps/start_forest.tmx'
PLAYERLAYER = 1
GRIDLAYER = 6
CBOXLAYER = 7
GRIDSIZE = 32

# todo, laden van pad van sprite moet nog anders
HEROPATH = 'resources/sprites/heroes/01_Alagos.png'
HEROPOS = 640, 768


class OverWorld(object):
    """
    Overworld layout.
    """
    def __init__(self, screen, audio):
        self.screen = screen
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(BACKGROUNDCOLOR)
        self.background = self.background.convert()
        self.window = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
        self.window.fill(WINDOWCOLOR)
        self.window = self.window.convert()

        self.audio = audio

        self.map1 = map.Map(OVERWORLDPATH, WINDOWWIDTH, WINDOWHEIGHT, PLAYERLAYER)
        self.group = self.map1.view

        self.hero = character.Hero(HEROPATH, HEROPOS, self.audio)
        self.group.add(self.hero)

        self.grid_sprite = None
        self.cbox_sprites = []

    def handle_view(self):
        """
        Update locaties -> teken de achtergrond -> centreer op de hero -> teken de window.
        """
        if len(self.cbox_sprites) > 0:                                  # de eerste die aan cbox_sprites bij F11 is
            self.cbox_sprites[0].update(self.hero.rect)                 # toegevoegd is de hero.rect, vandaar [0]

        self.screen.blit(self.background, (0, 0))
        self.group.center(self.hero.rect.center)
        self.group.draw(self.window)
        self.screen.blit(self.window, WINDOWPOS)

    def handle_multi_input(self, key_input, dt):
        """
        Handel de input af voor snelheid en richting. Check daarna op collision.
        :param key_input: pygame.key.get_pressed()
        :param dt: self.clock.tick(FPS)/1000.0
        """
        self.hero.speed(key_input)
        self.hero.direction(key_input, dt)
        # todo, moet dit niet naar de hero class?
        self.hero.check_obstacle(self.map1.obstacle_rects, self.map1.low_obst_rects,
                                 None, self.map1.width, self.map1.height, dt)

    def handle_single_input(self, event):
        """
        Handelt keyevents af.
        :param event: pygame.event.get() uit screen.py
        """
        if event.key == pygame.K_F10:
            if self.grid_sprite is None:
                self.grid_sprite = sprites.GridSprite(self.map1.width, self.map1.height, GRIDCOLOR, GRIDSIZE, GRIDLAYER)
                self.group.add(self.grid_sprite)
            else:
                self.group.remove(self.grid_sprite)
                self.grid_sprite = None

        elif event.key == pygame.K_F11:
            if len(self.cbox_sprites) == 0:                             # als de lijst leeg is.
                self.cbox_sprites.append(sprites.ColorBoxSprite(self.hero.rect, HEROCOLOR, CBOXLAYER))
                for rect in self.map1.tree_rects:
                    self.cbox_sprites.append(sprites.ColorBoxSprite(rect, TREECOLOR, CBOXLAYER))
                self.group.add(self.cbox_sprites)
            else:
                self.group.remove(self.cbox_sprites)
                self.cbox_sprites = []
