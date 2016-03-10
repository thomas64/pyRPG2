
"""
class: Window
"""

import collections

import pygame

import keys
import screens.character
import screens.map
import screens.sprites

BACKGROUNDCOLOR = pygame.Color("gray12")
GRIDCOLOR = pygame.Color("gray36")
HEROCOLOR = pygame.Color("blue")
TREECOLOR = pygame.Color("yellow")
WATERCOLOR = pygame.Color("purple")

ZOOMSPEED = .1
MAXZOOM = 3.1
DEFZOOM = 1.0
MINZOOM = .5

# todo, mooiere map maken met variatie in het gras
OVERWORLDPATH = 'resources/maps/start_forest.tmx'
PLAYERLAYER = 3
GRIDLAYER = 8
CBOXLAYER = 9
GRIDSIZE = 32


class Window(object):
    """
    De window met de kaart en hero's.
    """
    def __init__(self, width, height, engine):
        self.engine = engine
        self.surface = pygame.Surface((width, height))
        self.surface.fill(BACKGROUNDCOLOR)
        self.surface = self.surface.convert()

        self.map1 = screens.map.Map(OVERWORLDPATH, width, height, PLAYERLAYER)
        self.group = self.map1.view

        self.heroes = []
        self.party = list(self.engine.data.party.values())
        for hero in self.party:
            self.heroes.append(screens.character.Hero(hero.SPR, self.map1.start_pos.topleft, self.engine.audio))
        self.heroes.reverse()           # voeg de heroes in juiste volgorde toe
        self.group.add(self.heroes)     # maar als sprites moeten ze precies andersom staan
        self.heroes.reverse()           # want daar wil je heroes[0] bovenop weergegeven hebben

        self.grid_sprite = None
        self.cbox_sprites = []

        self.maxlen = ((len(self.party)-1)*GRIDSIZE)+1
        self.hero_history = collections.deque(maxlen=self.maxlen)
        self.align()

    def align(self):
        """
        Zet de hero in het grid. Positioneer de party achter hem. Vul de geschiedenis met lege data.
        """
        self.heroes[0].align_to_grid(GRIDSIZE)
        for hero in self.heroes:
            hero.rect.topleft = list(self.heroes[0].rect.topleft)
            hero.last_direction = self.heroes[0].last_direction
        for _ in range(0, self.maxlen):
            self.hero_history.append(self.heroes[0].get_history_data())

    def single_input(self, event):
        """
        Handelt de muis en keyboard input af.
        :param event: pygame.event.get()
        """
        if event.type == pygame.KEYDOWN:

            if event.key == keys.ALIGN:
                self.align()

            elif event.key == keys.GRID:
                if self.grid_sprite is None:
                    self.grid_sprite = screens.sprites.GridSprite(self.map1.width, self.map1.height,
                                                                  GRIDCOLOR, GRIDSIZE, GRIDLAYER)
                    self.group.add(self.grid_sprite)
                else:
                    self.group.remove(self.grid_sprite)
                    self.grid_sprite = None

            elif event.key == keys.CBOX:
                if len(self.cbox_sprites) == 0:                             # als de lijst leeg is.
                    for hero in self.heroes:
                        self.cbox_sprites.append(screens.sprites.ColorBoxSprite(hero.rect, HEROCOLOR, CBOXLAYER))
                    for rect in self.map1.tree_rects:
                        self.cbox_sprites.append(screens.sprites.ColorBoxSprite(rect, TREECOLOR, CBOXLAYER))
                    for rect in self.map1.water_rects:
                        self.cbox_sprites.append(screens.sprites.ColorBoxSprite(rect, WATERCOLOR, CBOXLAYER))
                    self.group.add(self.cbox_sprites)
                else:
                    self.group.remove(self.cbox_sprites)
                    self.cbox_sprites = []

    def multi_input(self, key_input, mouse_pos, dt):
        """
        Plus en min voor zoomen.
        Handel daarde de input af voor snelheid en richting. Check daarna op collision.
        :param key_input: pygame.key.get_pressed()
        :param mouse_pos: pygame.mouse.get_pos()
        :param dt: self.clock.tick(FPS)/1000.0
        """
        if key_input[keys.ZOOMPLUS[0]] or key_input[keys.ZOOMPLUS[1]]:
            value = self.map1.map_layer.zoom + ZOOMSPEED
            if value < MAXZOOM:
                self.map1.map_layer.zoom = value
        elif key_input[keys.ZOOMMIN[0]] or key_input[keys.ZOOMMIN[1]]:
            value = self.map1.map_layer.zoom - ZOOMSPEED
            if value > MINZOOM:
                self.map1.map_layer.zoom = value
        elif key_input[keys.ZOOMRESET[0]] or key_input[keys.ZOOMRESET[1]]:
            self.map1.map_layer.zoom = DEFZOOM

        self.heroes[0].speed(key_input)
        self.heroes[0].direction(key_input, dt)
        # todo, moet dit niet naar de hero class?
        self.heroes[0].check_obstacle(self.map1.obstacle_rects, self.map1.low_obst_rects,
                                      None, self.map1.width, self.map1.height, dt)

        self.hero_trail(key_input, dt)

    # noinspection PyMethodMayBeStatic
    def update(self, dt):
        """
        Update de waarden van de bovenste state.
        :param dt: self.clock.tick(FPS)/1000.0
        """
        pass

    def render(self):
        """
        Update locaties (indien F11) -> centreer op de hero -> teken de window inhoud.
        """
        # misschien gaat dit een probleem geven wanneer ingame de party grootte wordt gewijzigd.
        # dan heeft bijv een boom een hero.rect.topleft oid.
        if len(self.cbox_sprites) > 0:
            for index, hero in enumerate(self.heroes):  # dit kan om dat de eerste paar die aan cbox_sprites bij F11
                self.cbox_sprites[index].rect.topleft = hero.rect.topleft  # zijn toegevoegd zijn de hero.rects

        self.group.center(self.heroes[0].rect.center)
        self.group.draw(self.surface)

    def hero_trail(self, key_input, dt):
        """
        Als 1 van de 4 pijltoetsen gedrukt wordt en de zich ook daadwerkelijk verplaatst.
        Vul de history van de hero dan aan met allemaal data uit een methode van character.
        :param key_input: pygame.key.get_pressed()
        :param dt: self.clock.tick(FPS)/1000.0
        """
        if (key_input[keys.UP] or key_input[keys.DOWN] or
            key_input[keys.LEFT] or key_input[keys.RIGHT]) and \
                (self.heroes[0].rect.x != self.hero_history[-1][0] or   # bekijk de laatste uit de deque
                 self.heroes[0].rect.y != self.hero_history[-1][1]):

            self.hero_history.append(self.heroes[0].get_history_data())

            # de index loopt op van 0, 1, 2, 3.
            # de i loopt af van 4, 3, 2, 1.
            for index, i in enumerate(range(len(self.party)-1, 0, -1)):
                self.heroes[i].rect.x = self.hero_history[index*GRIDSIZE][0]
                self.heroes[i].rect.y = self.hero_history[index*GRIDSIZE][1]
                self.heroes[i].last_direction = self.hero_history[index*GRIDSIZE][2]
                self.heroes[i].move_direction = self.hero_history[index*GRIDSIZE][3]
                self.heroes[i].movespeed = self.hero_history[index*GRIDSIZE][4]
                self.heroes[i].animate(dt, make_sound=False)
