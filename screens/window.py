
"""
class: Window
"""

import collections

import pygame

import audio as sfx
import components.map
import components.messagebox
import components.sprites
import equipment
import keys
import pouchitems
import screens.direction
import screens.shop.display
import screens.unit

BACKGROUNDCOLOR = pygame.Color("gray12")
GRIDCOLOR = pygame.Color("gray36")
HEROCOLOR = pygame.Color("blue")
HIGHBLOCKERCOLOR = pygame.Color("yellow")
LOWBLOCKERCOLOR = pygame.Color("purple")

ZOOMSPEED = .1
MAXZOOM = 3.1
DEFZOOM = 1.0
MINZOOM = .5

GRIDLAYER = 8
CBOXLAYER = 9
GRIDSIZE = 32
ICONSIZE = 32

NEWMAPTIMEOUT = 0.1  # minimale keyblock. Zonder deze timer kun je op de movement keys drukken terwijl de map laadt.


class Window(object):
    """
    De window met de kaart en hero's.
    """
    def __init__(self, engine):
        self.engine = engine

        self.prev_map_name = None
        self.group = None
        self.grid_sprite = None
        self.cbox_sprites = None
        self.party_sprites = None
        self.party = None
        self.maxlen = None
        self.leader_history = None

        self.load_map()

        self.width = self.engine.current_map.window_width
        self.height = self.engine.current_map.window_height
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(BACKGROUNDCOLOR)
        self.surface = self.surface.convert()

    def load_map(self):
        """
        Maak een nieuwe map aan met de hero's in het veld.
        """
        self.group = self.engine.current_map.view
        self.grid_sprite = None
        self.cbox_sprites = []

        start_pos = self.engine.data.map_pos               # normaliter is start_pos een point, behalve bij het start
        start_dir = self.engine.data.map_dir               # van het spel, dan is het een string.
        if type(start_pos) is str:                         # maw, als start_pos = 'start_game'
            for pos in self.engine.current_map.start_pos:  # kijk in de start_pos list van de map
                if pos.name == start_pos:                  # van alle start_possen, welke komt overeen met 'start_game'
                    start_pos = pos.x, pos.y               # zet dan de x,y waarde op dié start_pos
                    break

        self.party_sprites = []
        self.party = list(self.engine.data.party.values())
        for hero in self.party:
            self.party_sprites.append(screens.unit.Unit(hero.SPR, start_pos, start_dir, self.engine.audio))
        self.party_sprites.reverse()               # voeg de party_sprites in juiste volgorde toe
        self.group.add(self.party_sprites)         # maar als sprites moeten ze precies andersom staan
        self.party_sprites.reverse()               # want daar wil je party_sprites[0] bovenop weergegeven hebben

        self.maxlen = ((len(self.party)-1)*GRIDSIZE)+1                  # bereken de lengte van het deck
        self.leader_history = collections.deque(maxlen=self.maxlen)     # maak een lege deck aan
        self.align()

        # voeg alle objecten toe van uit de map
        self.group.add(self.engine.current_map.chests)
        self.group.add(self.engine.current_map.sparkly)

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
        for _ in range(self.maxlen):
            self.leader_history.appendleft(self.party_sprites[0].get_history_data())

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
                self.check_sparklies(self.get_check_rect())

            elif event.key == keys.GRID:
                if self.grid_sprite is None:
                    self.grid_sprite = components.sprites.Grid(self.engine.current_map.width,
                                                               self.engine.current_map.height,
                                                               GRIDCOLOR, GRIDSIZE, GRIDLAYER)
                    self.group.add(self.grid_sprite)
                else:
                    self.group.remove(self.grid_sprite)
                    self.grid_sprite = None

            elif event.key == keys.CBOX:
                if len(self.cbox_sprites) == 0:                             # als de lijst leeg is.
                    for unit in self.party_sprites:
                        self.cbox_sprites.append(components.sprites.ColorBox(unit.rect, HEROCOLOR, CBOXLAYER))
                    for rect in self.engine.current_map.high_blocker_rects:
                        self.cbox_sprites.append(components.sprites.ColorBox(rect, HIGHBLOCKERCOLOR, CBOXLAYER))
                    for rect in self.engine.current_map.low_blocker_rects:
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
            value = self.engine.current_map.map_layer.zoom + ZOOMSPEED
            if value < MAXZOOM:
                self.engine.current_map.map_layer.zoom = value
        elif key_input[keys.ZOOMMIN[0]] or key_input[keys.ZOOMMIN[1]]:
            value = self.engine.current_map.map_layer.zoom - ZOOMSPEED
            if value > MINZOOM:
                self.engine.current_map.map_layer.zoom = value
        elif key_input[keys.ZOOMRESET[0]] or key_input[keys.ZOOMRESET[1]]:
            self.engine.current_map.map_layer.zoom = DEFZOOM

        self.party_sprites[0].speed(key_input)
        self.party_sprites[0].direction(key_input, dt)
        # todo, moet dit niet naar de unit class?
        self.party_sprites[0].check_blocker(self.engine.current_map.high_blocker_rects,
                                            self.engine.current_map.low_blocker_rects,
                                            None,
                                            self.engine.current_map.width,
                                            self.engine.current_map.height,
                                            dt)

        self.leader_trail(dt)

        # update ook in de data voor een savegame en nieuwe map
        self.engine.data.map_pos = self.party_sprites[0].rect.topleft
        self.engine.data.map_dir = self.party_sprites[0].last_direction

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

        if self.engine.current_map.width >= self.width and \
           self.engine.current_map.height >= self.height:
            self.group.center(self.party_sprites[0].rect.center)

        # update de plaatjes van de objecten
        for obj in self.engine.current_map.chests:
            chest_data = self.engine.data.treasure_chests[obj.chest_id]
            obj.update(chest_data['opened'])
        for obj in self.engine.current_map.sparkly:
            sparkly_data = self.engine.data.sparklies[obj.sparkly_id]
            obj.update(sparkly_data['taken'], dt)

    def render(self):
        """
        Teken de window inhoud.
        """
        self.group.draw(self.surface)

    def leader_trail(self, dt):
        """
        Als 1 van de 4 pijltoetsen gedrukt wordt en de zich ook daadwerkelijk verplaatst.
        Vul de history van de leader dan aan met allemaal data uit een methode van Unit.
        :param dt: self.clock.tick(FPS)/1000.0
        """
        # todo, voetstappen van party te weinig, ligt aan omdat 2e deel van _clip nooit aangeroepen wordt.
        if self.party_sprites[0].is_moving() and \
                (self.party_sprites[0].rect.x != self.leader_history[0][0] or  # bekijk de eerste uit de deque
                 self.party_sprites[0].rect.y != self.leader_history[0][1]):

            # todo, visuele trail met cboxes
            self.leader_history.appendleft(self.party_sprites[0].get_history_data())

            for i in range(1, len(self.party)):
                ps = self.party_sprites[i]
                # mv = self.party_sprites[0].movespeed
                # if mv == 60:
                #     index = 32 * i
                # if mv == 120:
                #     index = 16 * i
                # if mv == 240:
                #     index = 8 * i
                # if mv == 480:
                #     index = 4 * i

                index = i * GRIDSIZE
                ps.rect.x = self.leader_history[index][0]
                ps.rect.y = self.leader_history[index][1]
                ps.last_direction = self.leader_history[index][2]
                ps.move_direction = self.leader_history[index][3]
                ps.movespeed = self.leader_history[index][4]
                ps.animate(dt, make_sound=False)

    def check_sounds(self):
        """
        Bekijk op de kaart met welke sound de voeten colliden.
        Zet die naam van het object van de kaart als audio.footstep.
        """
        if len(self.party_sprites[0].feet.collidelistall(self.engine.current_map.sounds)) == 1:
            sound_nr = self.party_sprites[0].feet.collidelist(self.engine.current_map.sounds)
            name = self.engine.current_map.sounds[sound_nr].name
            self.engine.audio.footstep = name

    def check_portals(self):
        """
        Bekijk of hij collide met een portal.
        Zo ja, haal dan de van en naar data uit de portal.
        Hij gebruikt de van naam voor de startpositie in de nieuwe map.
        """
        if len(self.party_sprites[0].rect.collidelistall(self.engine.current_map.portals)) == 1:
            self.engine.timer = NEWMAPTIMEOUT
            portal_nr = self.party_sprites[0].rect.collidelist(self.engine.current_map.portals)
            self.prev_map_name = self.engine.current_map.portals[portal_nr].from_name
            self.engine.data.map_name = self.engine.current_map.portals[portal_nr].to_name
            self.engine.data.map_pos = self.engine.current_map.portals[portal_nr].to_pos
            self.engine.current_map = components.map.Map(self.engine.data.map_name)
            self.load_map()

    def check_chests(self):
        """
        Bekijk of collide met een chest.
        """
        if self.party_sprites[0].last_direction == screens.direction.Direction.North:
            if len(self.party_sprites[0].rect.collidelistall(self.engine.current_map.chests)) == 1:
                object_nr = self.party_sprites[0].rect.collidelist(self.engine.current_map.chests)
                chest_sprite = self.engine.current_map.chests[object_nr]
                chest_data = self.engine.data.treasure_chests[chest_sprite.chest_id]

                if chest_data['condition'] and chest_data['content']:
                    for key, value in chest_data['condition'].items():
                        text = ["Error!"]
                        if key == "mec":
                            text = ["There's a dangerous trap on this treasurechest.",
                                    "You need a level "+str(value)+" of the Mechanic Skill to",
                                    "disarm the trap."]
                        elif key == "thf":
                            text = ["There's a lock on this treasurechest.",
                                    "You need a level "+str(value)+" of the Thief Skill",
                                    "to pick the lock."]
                        highest = self.engine.data.party.get_highest_value_of_skill(key)
                        if highest < value:
                            push_object = components.messagebox.MessageBox(self.engine.gamestate, text)
                            self.engine.gamestate.push(push_object)
                            return

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
                    # push_object = screens.shop.display.Display()
                    self.engine.gamestate.push(push_object)

    def check_sparklies(self, check_rect):
        """
        Bekijk of collide met een sparkly.
        :param check_rect: een iets verplaatste rect van de player sprite zodat hij kan colliden met een obj dat anders
        niet collidebaar is. self.party_sprites[0].rect
        """
        if len(check_rect.collidelistall(self.engine.current_map.sparkly)) == 1:
            object_nr = check_rect.collidelist(self.engine.current_map.sparkly)
            sparkly_sprite = self.engine.current_map.sparkly[object_nr]
            sparkly_data = self.engine.data.sparklies[sparkly_sprite.sparkly_id]

            # hieronder is bijna een exacte kopie van check_chests() kan dat anders?
            if sparkly_data['content']:
                sparkly_data['taken'] = 1
                text = ["Found:"]
                image = []
                for key, value in sparkly_data['content'].items():
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
                self.engine.audio.play_sound(sfx.SPARKLY)
                sparkly_data['content'] = dict()
                sparkly_sprite.image = None
                push_object = components.messagebox.MessageBox(self.engine.gamestate, text, image)
                # push_object = screens.shop.display.Display()
                self.engine.gamestate.push(push_object)

    def get_check_rect(self):
        """
        Bij een check gebruik dan een rect op basis van de hero rect en verplaats die iets in de kijk richting.
        :return: de tijdelijk verplaatste rect, gemaakt op basis van de huidige hero rect.
        """
        last_dir = self.party_sprites[0].last_direction
        check_rect = self.party_sprites[0].rect
        if last_dir == screens.direction.Direction.North:
            check_rect = self.party_sprites[0].rect.move(0, -16)
        elif last_dir == screens.direction.Direction.South:
            check_rect = self.party_sprites[0].rect.move(0, 16)
        elif last_dir == screens.direction.Direction.West:
            check_rect = self.party_sprites[0].rect.move(-16, 0)
        elif last_dir == screens.direction.Direction.East:
            check_rect = self.party_sprites[0].rect.move(16, 0)
        return check_rect
