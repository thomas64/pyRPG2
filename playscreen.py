
"""
class: PlayScreen
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


# todo, een window klasse maken voor de inhoud van de window
class PlayScreen(object):
    """
    Playscreen layout.
    """
    def __init__(self, screen, audio):
        self.screen = screen
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(BACKGROUNDCOLOR)
        self.background = self.background.convert()
        self.window = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
        self.window.fill(WINDOWCOLOR)
        self.window = self.window.convert()

        self.map1 = map.Map(OVERWORLDPATH, WINDOWWIDTH, WINDOWHEIGHT, PLAYERLAYER)
        self.group = self.map1.view

        self.hero = character.Hero(HEROPATH, HEROPOS, audio)
        self.group.add(self.hero)

        self.buttons = None
        self._init_buttons()
        self.key_input = pygame.key.get_pressed()

        self.grid_sprite = None
        self.cbox_sprites = []

    def _init_buttons(self):
        """
        Maak de knoppen aan en zet ze in een lijst.
        Plaats ook de bijbehorende keys in een lijst.
        """
        bg_width = self.background.get_width()
        bg_height = self.background.get_height()

        # todo, afhankelijk van situatie, buttons niet weergeven
        # button_view = sprites.ButtonSprite((bg_width-200,   bg_height-300), "V",     pygame.K_v)
        button_up = sprites.ButtonSprite((bg_width-150,     bg_height-300), "Up",    pygame.K_UP)
        button_down = sprites.ButtonSprite((bg_width-150,   bg_height-250), "Down",  pygame.K_DOWN)
        button_left = sprites.ButtonSprite((bg_width-200,   bg_height-250), "Left",  pygame.K_LEFT)
        button_right = sprites.ButtonSprite((bg_width-100,  bg_height-250), "Right", pygame.K_RIGHT)
        # button_cancel = sprites.ButtonSprite((bg_width-100, bg_height-200), "C",     pygame.K_c)

        # self.buttons = [button_view, button_up, button_down, button_left, button_right, button_cancel]
        self.buttons = [button_up, button_down, button_left, button_right]

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

        for button in self.buttons:
            button.draw(self.screen, self.key_input)

    def handle_multi_input(self, key_input, mouse_pos, dt):
        """
        Handel de input af voor snelheid en richting. Check daarna op collision.
        :param key_input: pygame.key.get_pressed()
        :param mouse_pos: pygame.mouse.get_pos()
        :param dt: self.clock.tick(FPS)/1000.0
        """
        self.key_input = key_input

        if mouse_pos is not None:
            for button in self.buttons:
                if button.rect.collidepoint(mouse_pos):
                    self.key_input = list(self.key_input)
                    self.key_input[button.key] = 1

        self.hero.speed(self.key_input)
        self.hero.direction(self.key_input, dt)
        # todo, moet dit niet naar de hero class?
        self.hero.check_obstacle(self.map1.obstacle_rects, self.map1.low_obst_rects,
                                 None, self.map1.width, self.map1.height, dt)

    def handle_single_input(self, event):
        """
        Handelt keyevents af.
        :param event: pygame.event.get() uit playscreen.py
        """
        if event.key == pygame.K_SPACE:
            self.hero.align_to_grid(GRIDSIZE)

        elif event.key == pygame.K_F10:
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
