
"""
class: Window
"""

import collections

import pygame

import audio as sfx
import components.messagebox
import components.sprites
import equipment
import keys
import pouchitems
import screens.unit
import screens.direction
import screens.map

BACKGROUNDCOLOR = pygame.Color("gray12")
GRIDCOLOR = pygame.Color("gray36")
HEROCOLOR = pygame.Color("blue")
HIGHBLOCKERCOLOR = pygame.Color("yellow")
LOWBLOCKERCOLOR = pygame.Color("purple")

ZOOMSPEED = .1
MAXZOOM = 3.1
DEFZOOM = 1.0
MINZOOM = .5

OVERWORLDPATH = 'resources/maps/'
OVERWORLDNAME = 'start_forest'
STARTPOSITION = 'start_game'    # dit is de naam van de startpositie object in de tmx map
STARTDIRECTION = screens.direction.Direction.South
PLAYERLAYER = 3
GRIDLAYER = 8
CBOXLAYER = 9
GRIDSIZE = 32
ICONSIZE = 32

NEWMAPTIMEOUT = 0.1  # minimale keyblock. Zonder deze timer kun je op de movement keys drukken terwijl de map laadt.


class Window(object):
    """
    De window met de kaart en hero's.
    """
    def __init__(self, width, height, engine):
        self.width = width
        self.height = height
        self.engine = engine
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(BACKGROUNDCOLOR)
        self.surface = self.surface.convert()

        self.map1 = None
        self.prev_map_name = None
        self.group = None
        self.grid_sprite = None
        self.cbox_sprites = None
        self.party_sprites = None
        self.party = None
        self.maxlen = None
        self.leader_history = None

        self.new_map(OVERWORLDNAME, OVERWORLDPATH + OVERWORLDNAME + '.tmx', STARTPOSITION, STARTDIRECTION)

    def new_map(self, map_name, map_path, startposition, startdirection):
        """
        Maak een nieuwe map aan met de hero's in het veld.
        :param map_name: naam van de map
        :param map_path: het pad van de tmx
        :param startposition: de positie van party_sprites[0] als naam van een tmx start_pos object layer
        :param startdirection: welke kant kijkt party_sprites[0] op
        """
        self.map1 = screens.map.Map(map_name, map_path, self.width, self.height, PLAYERLAYER)
        self.group = self.map1.view
        self.grid_sprite = None
        self.cbox_sprites = []

        start_pos = startposition           # voor loadsave moet het point zijn ipv een naam
        for pos in self.map1.start_pos:     # kijk in de start_pos list van de map
            if pos.name == startposition:   # van alle start_possen, welke komt overeen met waar de hero vandaan komt
                start_pos = (pos.x, pos.y)  # zet dan de x,y waarde op dié start_pos

        self.party_sprites = []
        self.party = list(self.engine.data.party.values())
        for hero in self.party:
            self.party_sprites.append(screens.unit.Unit(hero.SPR, start_pos, startdirection, self.engine.audio))
        self.party_sprites.reverse()               # voeg de party_sprites in juiste volgorde toe
        self.group.add(self.party_sprites)         # maar als sprites moeten ze precies andersom staan
        self.party_sprites.reverse()               # want daar wil je party_sprites[0] bovenop weergegeven hebben

        self.maxlen = ((len(self.party)-1)*GRIDSIZE)+1              # bereken de lengte van het deck
        self.leader_history = collections.deque(maxlen=self.maxlen)   # maak een lege deck aan
        self.align()

        # voeg alle objecten toe van uit de map
        self.group.add(self.map1.objects)

        self.engine.audio.set_bg_music(self.engine.gamestate.peek().name)
        self.engine.audio.set_bg_sounds(self.engine.gamestate.peek().name)

        # want deze is alleen nodig voor de audio, dus nadien weghalen
        self.prev_map_name = None

    def align(self):
        """
        Positioneer de party achter de hero. Vul de geschiedenis vol met de huidige positie data.
        """
        for unit in self.party_sprites:
            unit.rect.topleft = list(self.party_sprites[0].rect.topleft)
            unit.last_direction = self.party_sprites[0].last_direction
        for _ in range(0, self.maxlen):
            self.leader_history.append(self.party_sprites[0].get_history_data())

    def single_input(self, event):
        """
        Handelt de muis en keyboard input af.
        :param event: pygame.event.get()
        """
        if event.type == pygame.KEYDOWN:

            if event.key == keys.ALIGN:
                self.party_sprites[0].align_to_grid(GRIDSIZE)
                self.align()

            elif event.key in keys.SELECT:
                self.check_chests()

            elif event.key == keys.GRID:
                if self.grid_sprite is None:
                    self.grid_sprite = components.sprites.Grid(self.map1.width, self.map1.height,
                                                               GRIDCOLOR, GRIDSIZE, GRIDLAYER)
                    self.group.add(self.grid_sprite)
                else:
                    self.group.remove(self.grid_sprite)
                    self.grid_sprite = None

            elif event.key == keys.CBOX:
                if len(self.cbox_sprites) == 0:                             # als de lijst leeg is.
                    for unit in self.party_sprites:
                        self.cbox_sprites.append(components.sprites.ColorBox(unit.rect, HEROCOLOR, CBOXLAYER))
                    for rect in self.map1.high_blocker_rects:
                        self.cbox_sprites.append(components.sprites.ColorBox(rect, HIGHBLOCKERCOLOR, CBOXLAYER))
                    for rect in self.map1.low_blocker_rects:
                        self.cbox_sprites.append(components.sprites.ColorBox(rect, LOWBLOCKERCOLOR, CBOXLAYER))
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

        self.party_sprites[0].speed(key_input)
        self.party_sprites[0].direction(key_input, dt)
        # todo, moet dit niet naar de unit class?
        self.party_sprites[0].check_blocker(self.map1.high_blocker_rects, self.map1.low_blocker_rects,
                                            None, self.map1.width, self.map1.height, dt)

        self.leader_trail(dt)

    def update(self, dt):
        """
        Is de hero tegen een portal aangelopen. Update locaties (indien F11). Centreer op de hero.
        :param dt: self.clock.tick(FPS)/1000.0
        """
        self.check_sounds()
        self.check_portals()

        # misschien gaat dit een probleem geven wanneer ingame de party grootte wordt gewijzigd.
        # dan heeft bijv een boom een unit.rect.topleft oid.
        if len(self.cbox_sprites) > 0:
            for index, unit in enumerate(self.party_sprites):  # dit kan om dat de eerste paar die aan cbox_sprites bij
                self.cbox_sprites[index].rect.topleft = unit.rect.topleft  # F11 zijn toegevoegd zijn de unit.rects

        if self.map1.width >= self.width and \
           self.map1.height >= self.height:
            self.group.center(self.party_sprites[0].rect.center)

    def render(self):
        """
        Render de plaatjes van de objecten.
        Teken de window inhoud.
        """
        for obj in self.map1.objects:
            # todo, hij doet dit nu bij alle objecten in de lijst, ook de niet chests. moet nog uitgesplit worden
            # of voorwaarde scheppen als het een class van treasurechest is oid.
            chest_data = self.engine.data.treasure_chests[obj.chest_id]
            obj.render(chest_data['opened'])

        self.group.draw(self.surface)

    def leader_trail(self, dt):
        """
        Als 1 van de 4 pijltoetsen gedrukt wordt en de zich ook daadwerkelijk verplaatst.
        Vul de history van de leader dan aan met allemaal data uit een methode van Unit.
        :param dt: self.clock.tick(FPS)/1000.0
        """
        # todo, voetstappen van party te weinig, ligt aan omdat 2e deel van _clip nooit aangeroepen wordt.
        if self.party_sprites[0].is_moving() and \
                (self.party_sprites[0].rect.x != self.leader_history[-1][0] or   # bekijk de laatste uit de deque
                 self.party_sprites[0].rect.y != self.leader_history[-1][1]):

            self.leader_history.append(self.party_sprites[0].get_history_data())

            # de index loopt op van 0, 1, 2, 3.
            # de i loopt af van 4, 3, 2, 1.
            for index, i in enumerate(range(len(self.party)-1, 0, -1)):
                self.party_sprites[i].rect.x = self.leader_history[index * GRIDSIZE][0]
                self.party_sprites[i].rect.y = self.leader_history[index * GRIDSIZE][1]
                self.party_sprites[i].last_direction = self.leader_history[index * GRIDSIZE][2]
                self.party_sprites[i].move_direction = self.leader_history[index * GRIDSIZE][3]
                self.party_sprites[i].movespeed = self.leader_history[index * GRIDSIZE][4]
                self.party_sprites[i].animate(dt, make_sound=False)

    def check_sounds(self):
        """
        Bekijk op de kaart met welke sound de voeten colliden.
        Zet die naam van het object van de kaart als audio.footstep.
        """
        if len(self.party_sprites[0].feet.collidelistall(self.map1.sounds)) == 1:
            sound_nr = self.party_sprites[0].feet.collidelist(self.map1.sounds)
            name = self.map1.sounds[sound_nr].name
            self.engine.audio.footstep = name

    def check_portals(self):
        """
        Bekijk of hij collide met een portal.
        Zo ja, haal dan de van en naar data uit de portal.
        Hij gebruikt de van naam voor de startpositie in de nieuwe map.
        """
        if len(self.party_sprites[0].rect.collidelistall(self.map1.portals)) == 1:
            self.engine.timer = NEWMAPTIMEOUT
            portal_nr = self.party_sprites[0].rect.collidelist(self.map1.portals)
            self.prev_map_name = self.map1.portals[portal_nr].from_name
            to_name = self.map1.portals[portal_nr].to_name
            to_map_path = OVERWORLDPATH+to_name+'.tmx'
            self.new_map(to_name, to_map_path, self.prev_map_name, self.party_sprites[0].last_direction)

    def check_chests(self):
        """
        Bekijk of collide met een chest.
        """
        if self.party_sprites[0].last_direction == screens.direction.Direction.North:
            if len(self.party_sprites[0].rect.collidelistall(self.map1.objects)) == 1:
                object_nr = self.party_sprites[0].rect.collidelist(self.map1.objects)
                chest_sprite = self.map1.objects[object_nr]
                chest_data = self.engine.data.treasure_chests[chest_sprite.chest_id]
                if chest_data['content']:
                    chest_data['opened'] = 1
                    text = ["Found:"]
                    image = []
                    for key, value in chest_data['content'].items():
                        if key.startswith('eqp'):
                            equipment_item = equipment.factory_equipment_item(value['nam'])
                            equipment_item_spr = pygame.image.load(equipment_item.SPR).subsurface(
                                equipment_item.COL, equipment_item.ROW, ICONSIZE, ICONSIZE).convert_alpha()
                            self.engine.data.inventory.add(equipment_item, quantity=value['qty'])
                            text.append("{} {}".format(str(value['qty']), str(equipment_item.NAM)))
                            image.append(equipment_item_spr)
                        elif key.startswith('itm'):
                            pouch_item = pouchitems.factory_pouch_item(value['nam'])
                            pouch_item_spr = pygame.image.load(pouch_item.SPR).convert_alpha()
                            self.engine.data.pouch.add(pouch_item, quantity=value['qty'])
                            text.append("{} {}".format(str(value['qty']), str(pouch_item.NAM)))
                            image.append(pouch_item_spr)
                    self.engine.audio.play_sound(sfx.CHEST)
                    chest_data['content'] = dict()
                    push_object = components.messagebox.MessageBox(self.engine.gamestate, text, image)
                    self.engine.gamestate.push(push_object)
