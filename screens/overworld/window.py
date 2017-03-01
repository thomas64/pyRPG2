
"""
class: Window
"""

import collections

import pygame

from components import ColorBox
from components import ConfirmBox
from components import Grid
from components import Map
from components import MessageBox
from components import Player
from components import Transition

from constants import Direction
from constants import PersonState
from constants import Keys
from constants import SFX

from database import InnDatabase
from database import HeroDatabase
from database import PeopleDatabase
from database import SchoolDatabase
from database import ShopDatabase
from database import TrainerDatabase
from database import NoteDatabase
from database import SignDatabase
from database import TreasureChestDatabase

from database import PouchItemDatabase

import inventoryitems

from screens import School
from screens import Shop
from screens import Trainer


BACKGROUNDCOLOR = pygame.Color("gray12")
GRIDCOLOR = pygame.Color("gray36")
HEROCOLOR = pygame.Color("blue")
HIGHBLOCKERCOLOR = pygame.Color("yellow")
LOWBLOCKERCOLOR = pygame.Color("purple")
OBJECTCOLOR = pygame.Color("black")
WANDERBOXCOLOR = pygame.Color("green")
TEXTEVENTCOLOR = pygame.Color("red")

PLAYERLAYER = 5

ZOOMSPEED = .1
MAXZOOM = 3.1
DEFZOOM = 2.0
MINZOOM = .5

GRIDLAYER = 8
CBOXLAYER = 9
GRIDSIZE = 32
ICONSIZE = 32

NEWMAPTIMEOUT = 1.0  # minimale keyblock. Zonder deze timer kun je op de movement keys drukken terwijl de map laadt.


class Window(object):
    """
    De window met de kaart en hero's.
    """
    def __init__(self, engine):
        self.engine = engine

        self.prev_map_name = None
        self.portal_to_nr = None
        self.group = None
        self.grid_sprite = None
        self.cbox_sprites = None
        self.party_sprites = None
        self.party = None
        self.maxlen = None
        self.leader_history = None

        self.current_map = None
        self.load_map()

        self.width = self.current_map.window_width
        self.height = self.current_map.window_height
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(BACKGROUNDCOLOR)
        self.surface = self.surface.convert()

        self.inn_box = None     # confirmbox
        self.inn_data = None
        self.hero_box = None    # confirmbox
        self.hero_data = None
        self.quest_box = None   # confirmbox
        self.person_face = None
        self.person_id = None

        self.auto_move_event = False
        self.auto_move_script = list()
        self.auto_move_script_index = 0
        self.auto_move_part = list()
        self.auto_move_timer = 0

    def load_map(self):
        """
        Maak een nieuwe map aan met de hero's in het veld.
        """
        self.current_map = Map(self.engine.data)
        self.group = self.current_map.view
        self.grid_sprite = None
        self.cbox_sprites = []

        # normaliter is map_pos een point, behalve bij het laden van een
        # map, dan is het een string. bv start_game of ersin_forest_centr
        start_pos = self.current_map.get_position(self.engine.data.map_pos, self.portal_to_nr)
        start_dir = self.current_map.get_direction(start_pos, self.engine.data.map_dir)

        self.party_sprites = []
        self.party = list(self.engine.data.party.values())
        for hero in self.party:
            self.party_sprites.append(Player(hero.SPR, start_pos, PLAYERLAYER, start_dir, self.engine.audio))
        self.party_sprites.reverse()               # voeg de party_sprites in juiste volgorde toe
        self.group.add(self.party_sprites)         # maar als sprites moeten ze precies andersom staan
        self.party_sprites.reverse()               # want daar wil je party_sprites[0] bovenop weergegeven hebben

        self.maxlen = ((len(self.party)-1)*GRIDSIZE)+1                  # bereken de lengte van het deck
        self.leader_history = collections.deque(maxlen=self.maxlen)     # maak een lege deck aan
        self.align()

        # voeg alle objecten toe van uit de map
        for hero in self.current_map.heroes:
            if not self.engine.data.party.contains(hero.person_id):
                self.group.add(hero)
                # voeg alleen nu een blocker toe als de hero er daadwerkelijk is.
                # dit zit niet in de map class vanwege imports. maar nu moet hij in window al 2x checken op dit.
                self.current_map.high_blocker_rects.append(hero.get_blocker())
        self.group.add(self.current_map.shops)
        self.group.add(self.current_map.schools)
        self.group.add(self.current_map.trainers)
        self.group.add(self.current_map.inns)
        self.group.add(self.current_map.signs)
        self.group.add(self.current_map.chests)
        self.group.add(self.current_map.sparkly)
        self.group.add(self.current_map.people)  # people onderaan, dan lopen ze boven andere dingen.

    def align(self):
        """
        Positioneer de party achter de hero. Vul de geschiedenis vol met de huidige positie data.
        """
        for unit in self.party_sprites:
            unit.rect.topleft = list(self.party_sprites[0].rect.topleft)
            unit.last_direction = self.party_sprites[0].last_direction
        for _ in range(self.maxlen):
            self.leader_history.appendleft(self.party_sprites[0].get_history_data())

    def on_enter(self):
        """
        Als een hero confirmbox in beeld is geweest.
        Als de inn confirmbox in beeld is geweest.
        Als de quest confirmbox in beeld is geweest.
        """
        if self.hero_box:
            choice = self.hero_box.cur_item
            yes = self.hero_box.TOPINDEX
            scr_capt = self.hero_box.scr_capt
            if choice == yes:
                if self.engine.data.party.add(self.hero_data):
                    self.engine.audio.play_sound(SFX.join)
                    self.engine.key_timer = NEWMAPTIMEOUT
                    self.load_map()
                    self.engine.gamestate.push(Transition())
                else:
                    text = ["It seems your party is full already."]
                    push_object = MessageBox(text, face_image=self.hero_data.FAC, scr_capt=scr_capt, last=True)
                    self.engine.gamestate.push(push_object)
            else:
                self.engine.audio.play_sound(SFX.done)

            self.hero_box = None
            self.hero_data = None

        elif self.inn_box:
            choice = self.inn_box.cur_item
            yes = self.inn_box.TOPINDEX
            scr_capt = self.inn_box.scr_capt
            if choice == yes:
                gold = inventoryitems.factory_pouch_item(PouchItemDatabase.gold)
                if self.engine.data.pouch.remove(gold, self.inn_data['price']):
                    self.engine.gamestate.push(Transition())
                    push_object = MessageBox(InnDatabase.paid_text(), face_image=self.inn_data['face'],
                                             scr_capt=scr_capt, sound=SFX.coins, last=True)
                    self.engine.gamestate.push(push_object)
                    for hero in self.party:
                        hero.recover_full_hp()
                else:
                    push_object = MessageBox(InnDatabase.fail_text(), face_image=self.inn_data['face'],
                                             scr_capt=scr_capt, last=True)
                    self.engine.gamestate.push(push_object)
            else:
                push_object = MessageBox(InnDatabase.deny_text(), face_image=self.inn_data['face'],
                                         scr_capt=scr_capt, last=True)
                self.engine.gamestate.push(push_object)

            self.inn_box = None
            self.inn_data = None

        elif self.quest_box:
            # roept de callback aan die is meegegeven aan confirmbox bij de logbook quest
            # de callback hier is decided() uit inventoryitems\quest.py
            self.quest_box.callback(self.engine.gamestate, self.engine.data, self.engine.audio, self.person_face,
                                    self.quest_box.cur_item, self.quest_box.TOPINDEX, self.quest_box.scr_capt,
                                    self.person_id, self.display_loot)

            self.quest_box = None
            self.person_face = None
            self.person_id = None

    def single_input(self, event):
        """
        Handelt de muis en keyboard input af.
        :param event: pygame.event.get()
        """
        if event.type == pygame.KEYDOWN:

            if event.key == Keys.Align.value:
                if self.engine.debug_mode:
                    self.party_sprites[0].align_to_grid(GRIDSIZE)
                    self.align()

            elif event.key == Keys.Grid.value:
                if self.engine.debug_mode:
                    if self.grid_sprite is None:
                        self.grid_sprite = Grid(self.current_map.width, self.current_map.height,
                                                GRIDCOLOR, GRIDSIZE, GRIDLAYER)
                        self.group.add(self.grid_sprite)
                    else:
                        self.group.remove(self.grid_sprite)
                        self.grid_sprite = None

            elif event.key == Keys.Cbox.value:
                if self.engine.debug_mode:
                    if len(self.cbox_sprites) == 0:                             # als de lijst leeg is.
                        for unit in self.party_sprites:
                            self.cbox_sprites.append(ColorBox(unit.rect, HEROCOLOR, CBOXLAYER))
                        for rect in self.current_map.high_blocker_rects:
                            self.cbox_sprites.append(ColorBox(rect, HIGHBLOCKERCOLOR, CBOXLAYER))
                        for rect in self.current_map.low_blocker_rects:
                            self.cbox_sprites.append(ColorBox(rect, LOWBLOCKERCOLOR, CBOXLAYER))
                        for obj in self.current_map.people:
                            if getattr(obj, 'wander_area', None):
                                self.cbox_sprites.append(ColorBox(obj.wander_area, WANDERBOXCOLOR, CBOXLAYER))
                        for obj_group in (self.current_map.locations,
                                          self.current_map.text_events,
                                          self.current_map.move_events):
                            for obj in obj_group:
                                self.cbox_sprites.append(ColorBox(obj.rect, TEXTEVENTCOLOR, CBOXLAYER))
                        for obj_group in (self.current_map.heroes,
                                          self.current_map.shops,
                                          self.current_map.schools,
                                          self.current_map.trainers,
                                          self.current_map.inns,
                                          self.current_map.people,
                                          self.current_map.notes,
                                          self.current_map.signs,
                                          self.current_map.chests,
                                          self.current_map.sparkly):
                            for obj in obj_group:
                                self.cbox_sprites.append(ColorBox(obj.rect, OBJECTCOLOR, CBOXLAYER))
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

        # geen key_input mogelijk bij automatisch bewegen
        if not self.auto_move_event:

            if self.engine.debug_mode:
                if key_input[Keys.Zoomplus.value[0]] or key_input[Keys.Zoomplus.value[1]]:
                    value = self.current_map.map_layer.zoom + ZOOMSPEED
                    if value < MAXZOOM:
                        self.current_map.map_layer.zoom = value
                elif key_input[Keys.Zoommin.value[0]] or key_input[Keys.Zoommin.value[1]]:
                    value = self.current_map.map_layer.zoom - ZOOMSPEED
                    if value > MINZOOM:
                        self.current_map.map_layer.zoom = value
                elif key_input[Keys.Zoomreset.value[0]] or key_input[Keys.Zoomreset.value[1]]:
                    self.current_map.map_layer.zoom = DEFZOOM

            if self.engine.debug_mode:
                self.party_sprites[0].speed(key_input)
            self.party_sprites[0].direction(key_input, dt)
            # todo, moet dit niet naar de unit class?
            self.party_sprites[0].check_blocker(self.current_map.high_blocker_rects,
                                                self.current_map.low_blocker_rects,
                                                self.current_map.quest_blocker_rects,
                                                [sprite.get_blocker() for sprite in self.current_map.people if
                                                 getattr(sprite, 'wander_area', None)],  # alleen maar lopende sprites,
                                                None,                                    # standing sprites hebben al
                                                self.current_map.width,                  # een blocker
                                                self.current_map.height,
                                                dt)
        else:
            self.run_move_event(dt)

        self.leader_trail(dt)

        # update ook in de data voor een savegame en nieuwe map
        self.engine.data.map_pos = self.party_sprites[0].rect.topleft
        self.engine.data.map_dir = self.party_sprites[0].last_direction

    def update(self, dt):
        """
        :param dt: self.clock.tick(FPS)/1000.0
        """
        # Is de hero tegen een soundobject of een portal aangelopen
        self.check_sounds()
        self.check_text_events()  # deze staat voor portals vanwege een evt vloeiende Transition.
        self.check_portals()
        self.check_move_events()
        self.check_locations()

        # Update locaties (indien F11).
        # misschien gaat dit een probleem geven wanneer ingame de party grootte wordt gewijzigd.
        # dan heeft bijv een boom een unit.rect.topleft oid.
        if len(self.cbox_sprites) > 0:
            for index, unit in enumerate(self.party_sprites):  # dit kan om dat de eerste paar die aan cbox_sprites bij
                self.cbox_sprites[index].rect.topleft = unit.rect.topleft  # F11 zijn toegevoegd zijn de unit.rects

        # Centreer op de hero als de kaart groter is dan de window.
        # if self.current_map.width >= self.width and \
        #    self.current_map.height >= self.height:
        self.group.center(self.party_sprites[0].rect.center)

        # update de plaatjes van de objecten
        for obj in self.current_map.chests:
            chest_data = self.engine.data.treasure_chests[obj.chest_id]
            obj.update(chest_data['opened'])
        for obj in self.current_map.sparkly:
            sparkly_data = self.engine.data.sparklies[obj.sparkly_id]
            obj.update(sparkly_data['taken'], dt)
        # en update eventuele quest blockers
        self.current_map.remove_rewarded_quest_blockers(self.engine.data.logbook)

        # beweeg wandering people.
        # er staan niet alleen maar wandering in c_m.people, ook standing people, maar update wordt daarbij ge-pass-t
        for obj in self.current_map.people:
            obj.update(self.party_sprites,
                       self.current_map.high_blocker_rects,
                       self.current_map.low_blocker_rects,
                       [sprite for sprite in self.current_map.people if  # alleen maar lopende sprites,
                        getattr(sprite, 'wander_area', None)],           # standing sprites hebben al een blocker
                       dt)

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
                mv = self.party_sprites[0].movespeed
                # dit was een poging tot een andere manier van trailing. werkt niet goed genoeg.
                # if mv == 60:
                #     index = 32 * i
                # if mv == 120:
                #     index = 16 * i
                # if mv == 240:
                #     index = 8 * i
                # if mv == 960:
                #     index = 2 * i

                # index = i * (round(mv * dt))
                index = i * GRIDSIZE
                ps.rect.x = self.leader_history[index][0]
                ps.rect.y = self.leader_history[index][1]
                ps.last_direction = self.leader_history[index][2]
                ps.move_direction = self.leader_history[index][3]
                ps.movespeed = self.leader_history[index][4]
                ps.animate(dt, make_sound=False)

    def run_move_event(self, dt):
        """
        Beweeg de hero automatisch indien
        """
        if self.auto_move_event:

            if self.auto_move_part[0] == PersonState.Moving:
                self.party_sprites[0].last_direction = self.auto_move_part[1]
                self.party_sprites[0].move_direction = self.auto_move_part[1]
                self.party_sprites[0].auto_move(dt)
            elif self.auto_move_part[0] == PersonState.Resting:
                self.party_sprites[0].last_direction = self.auto_move_part[1]
                self.party_sprites[0].move_direction = None
                self.party_sprites[0].auto_move(dt)

            # handel de automatisch beweging timer af.
            # auto_move_part[2] is de timer. [1] is de direction. [0] is de personstate
            if self.auto_move_timer > 0.0:
                self.auto_move_timer -= dt
            if self.auto_move_timer <= 0.0:
                # als hij aan het eind van het move script is.
                if self.auto_move_script_index >= len(self.auto_move_script) - 1:
                    self.auto_move_event = False
                    self.auto_move_script = None
                    self.auto_move_script_index = 0
                    self.auto_move_part = None
                    self.auto_move_timer = 0
                else:
                    self.auto_move_script_index += 1
                    self.auto_move_part = self.auto_move_script[self.auto_move_script_index]
                    self.auto_move_timer = self.auto_move_part[2]  # [2] is de timer

    def check_sounds(self):
        """
        Bekijk op de kaart met welke sound de voeten colliden.
        Zet die naam van het object van de kaart als audio.footstep.
        """
        if len(self.party_sprites[0].feet.collidelistall(self.current_map.sounds)) == 1:
            sound_nr = self.party_sprites[0].feet.collidelist(self.current_map.sounds)
            name = self.current_map.sounds[sound_nr].name
            self.engine.audio.footstep = name

    def check_portals(self):
        """
        Bekijk of hij collide met een portal.
        Zo ja, haal dan de van en naar data uit de portal.
        Hij gebruikt de van naam voor de startpositie in de nieuwe map.
        """
        if len(self.party_sprites[0].rect.collidelistall(self.current_map.portals)) == 1:
            self.engine.key_timer = NEWMAPTIMEOUT
            portal_nr = self.party_sprites[0].rect.collidelist(self.current_map.portals)
            self.prev_map_name = self.current_map.portals[portal_nr].from_name
            self.engine.data.map_name = self.current_map.portals[portal_nr].to_name
            self.engine.data.map_pos = self.prev_map_name       # zet de point om naar een string naam.
            # als er een .to_nr is, namelijk het obj.type van een portal, gebruik dan .to_nr voor lokatiebepaling
            self.portal_to_nr = self.current_map.portals[portal_nr].to_nr
            self.engine.audio.fade_bg_music_when_loading_a_new_map()
            self.engine.audio.fade_bg_sounds_when_loading_a_new_map()
            self.load_map()
            self.engine.gamestate.push(Transition(full_screen=False))

    def check_text_events(self):
        """
        Bekijk of hij collide met een text event. Laat dan een reeks msgboxen zien.
        Verwijder daarna het eenmalige event.
        """
        if not self.party_sprites[0].is_highspeed_moving():
            if len(self.party_sprites[0].rect.collidelistall(self.current_map.text_events)) == 1:
                object_nr = self.party_sprites[0].rect.collidelist(self.current_map.text_events)
                event_name = self.current_map.text_events[object_nr].name
                event_text = self.engine.data.text_events[event_name]['text']

                if event_text:

                    # kan een boolean of een functie zijn
                    event_condition = self.engine.data.text_events[event_name]['condition']
                    # kijk of het een functie is
                    if callable(event_condition):
                        # voer met de () erachter de methode uit die in die dict staat.
                        event_condition = event_condition(None, self.engine.data)  # de None is voor niet static method.
                        # en maak er een boolean van
                    if event_condition:

                        # zwarte of normale achtergrond?
                        scr_capt = None  # normale achtergrond
                        if self.current_map.text_events[object_nr].opt:  # als er iets in .opt staat
                            self.engine.gamestate.push(Transition(full_screen=False))
                            scr_capt = False  # zwarte achtergrond

                        event_face = self.engine.data.text_events[event_name]['face']
                        event_face.reverse()
                        for i, text_part in enumerate(reversed(event_text)):
                            push_object = MessageBox(text_part, face_image=event_face[i], scr_capt=scr_capt,
                                                     last=(True if i == 0 else False))
                            self.engine.gamestate.push(push_object)

                        self.engine.data.text_events[event_name]['text'] = None
                        self.engine.data.text_events[event_name]['face'] = None
                        self.engine.data.text_events[event_name]['condition'] = False

    def check_move_events(self):
        """
        Collide je met een move_event. Zet daarna uit.
        """
        if not self.party_sprites[0].is_highspeed_moving():
            if len(self.party_sprites[0].rect.collidelistall(self.current_map.move_events)) == 1:
                object_nr = self.party_sprites[0].rect.collidelist(self.current_map.move_events)
                event_name = self.current_map.move_events[object_nr].name
                event_data = self.engine.data.move_events[event_name]

                # voer maar 1x uit
                if event_data['condition']:
                    event_data['condition'] = False

                    self.auto_move_event = True
                    self.auto_move_script = event_data['movement']
                    self.auto_move_script_index = 0
                    self.auto_move_part = self.auto_move_script[self.auto_move_script_index]
                    self.auto_move_timer = self.auto_move_part[2]  # [2] is de timer

    def check_locations(self):
        """
        Als je collide met een location.
        """
        if not self.party_sprites[0].is_highspeed_moving():
            if len(self.party_sprites[0].rect.collidelistall(self.current_map.locations)) == 1:
                object_nr = self.party_sprites[0].rect.collidelist(self.current_map.locations)
                location_name = self.current_map.locations[object_nr].name

                if location_name.startswith('quest'):
                    the_quest = self.engine.data.logbook[location_name]
                    the_quest.condition = True

                elif location_name.startswith('chapter'):
                    chapter_data = self.engine.data.chapters[location_name]
                    chapter_data['condition'] = True

    def action_button(self):
        """
        Check al deze methods bij het klikken van de action key.
        """
        self.check_heroes(self.party_sprites[0].get_check_rect())
        self.check_shops(self.party_sprites[0].get_check_rect())
        self.check_schools(self.party_sprites[0].get_check_rect())
        self.check_trainers(self.party_sprites[0].get_check_rect())
        self.check_inns(self.party_sprites[0].get_check_rect())
        self.check_people(self.party_sprites[0].get_check_rect())
        self.check_notes(self.party_sprites[0].get_check_rect())
        self.check_signs()
        self.check_chests()
        self.check_sparklies(self.party_sprites[0].get_check_rect())  # sparklys moeten ook van boven kunnen

    def check_heroes(self, check_rect):
        """
        Bekijk of collide met een hero.
        """
        if len(check_rect.collidelistall(self.current_map.heroes)) == 1:
            object_name = check_rect.collidelist(self.current_map.heroes)
            hero_sprite = self.current_map.heroes[object_name]
            # ook hier moet een hero in party niet gecheckt worden
            if not self.engine.data.party.contains(hero_sprite.person_id):
                self.hero_data = self.engine.data.heroes[hero_sprite.person_id]

                hero_sprite.turn(self.party_sprites[0].rect)

                self.hero_box = ConfirmBox(HeroDatabase.opening(self.hero_data.RAW), face_image=self.hero_data.FAC)
                self.engine.gamestate.push(self.hero_box)
                self.prev_map_name = self.engine.data.map_name  # deze is voor het geluid recht te breien.

    def check_shops(self, check_rect):
        """
        Bekijk of collide met een shopkeeper. Update de richting van de sprite.
        :param check_rect: een iets verplaatste rect van de player sprite zodat hij kan colliden met een obj dat anders
        niet collidebaar is. self.party_sprites[0].rect
        """
        if len(check_rect.collidelistall(self.current_map.shops)) == 1:
            object_nr = check_rect.collidelist(self.current_map.shops)
            shop_id = self.current_map.shops[object_nr].person_id
            shop_data = ShopDatabase[shop_id].value

            # check alle shops, zijn ze zichtbaar, hebben ze dezelfde id, turn die dan allemaal.
            for spr in self.current_map.shops:
                if spr.show_sprite:
                    if spr.person_id == shop_id:
                        spr.turn(self.party_sprites[0].rect)

            self.engine.audio.play_sound(SFX.scroll)
            # material is geen garantie, daarom heeft die .get()
            push_object = Shop(self.engine, shop_data['content'], shop_data.get('material'), shop_data['face'])
            self.engine.gamestate.push(push_object)
            self.engine.gamestate.push(Transition())

    def check_schools(self, check_rect):
        """
        Bekijk of je collide met een school.
        """
        if len(check_rect.collidelistall(self.current_map.schools)) == 1:
            object_nr = check_rect.collidelist(self.current_map.schools)
            school_sprite = self.current_map.schools[object_nr]
            school_data = SchoolDatabase[school_sprite.person_id].value

            school_sprite.turn(self.party_sprites[0].rect)

            self.engine.audio.play_sound(SFX.scroll)
            push_object = School(self.engine, school_data['content'], school_data['face'])
            self.engine.gamestate.push(push_object)
            self.engine.gamestate.push(Transition())

    def check_trainers(self, check_rect):
        """
        Bekijk of je collide met een trainer.
        """
        if len(check_rect.collidelistall(self.current_map.trainers)) == 1:
            object_nr = check_rect.collidelist(self.current_map.trainers)
            trainer_id = self.current_map.trainers[object_nr].person_id
            trainer_data = TrainerDatabase[trainer_id].value

            for spr in self.current_map.trainers:
                if spr.show_sprite:
                    if spr.person_id == trainer_id:
                        spr.turn(self.party_sprites[0].rect)

            self.engine.audio.play_sound(SFX.scroll)
            push_object = Trainer(self.engine, trainer_data['content'], trainer_data['face'])
            self.engine.gamestate.push(push_object)
            self.engine.gamestate.push(Transition())

    def check_inns(self, check_rect):
        """
        Er kunnen ook inns zijn zonder sprite, die moeten dan geupdate worden. Maar alle anderen met sprite wel omdat
        de lege een verlengde is van de gevulde. Hij vergelijkt person_id, dus hij turnt alleen met dezelfde id.
        """
        if len(check_rect.collidelistall(self.current_map.inns)) == 1:
            object_nr = check_rect.collidelist(self.current_map.inns)
            inn_id = self.current_map.inns[object_nr].person_id
            self.inn_data = InnDatabase[inn_id].value

            for spr in self.current_map.inns:
                if spr.show_sprite:
                    if spr.person_id == inn_id:
                        spr.turn(self.party_sprites[0].rect)

            self.inn_box = ConfirmBox(InnDatabase.welcome_text(self.inn_data['price']),
                                      face_image=self.inn_data['face'])
            self.engine.gamestate.push(self.inn_box)

    def check_people(self, check_rect):
        """
        Bekijk of hij collide met een standing of wandering person.
        """
        if len(check_rect.collidelistall(self.current_map.people)) == 1:
            object_nr = check_rect.collidelist(self.current_map.people)
            person_sprite = self.current_map.people[object_nr]
            person_data = PeopleDatabase[person_sprite.person_id].value

            # doe gewoon eerst het draaien zoals normaal
            person_sprite.turn(self.party_sprites[0].rect)

            # maar dan, als de persoon een quest heeft
            if person_data.get('quest'):
                quest_key = person_data['quest'].name
                the_quest = self.engine.data.logbook[quest_key]
                # het gezicht is in on_enter() weer nodig, vandaar deze declaratie.
                self.person_face = person_data['face']
                # idem voor person_id
                self.person_id = person_sprite.person_id

                self.quest_box = the_quest.show_message(self.engine.gamestate, self.engine.audio, self.engine.data,
                                                        self.person_face, self.person_id, self.display_loot)

            # of als hij dat niet heeft
            else:
                for i, text_part in enumerate(reversed(person_data['text'])):
                    push_object = MessageBox(text_part, face_image=person_data['face'],
                                             last=(True if i == 0 else False))
                    self.engine.gamestate.push(push_object)

    def check_notes(self, check_rect):
        """
        Bekijk met welke note objectnummer hij in de list collide.
        Dat is een NamedRect, dus bekijk zijn .name adhv het objectnummer.
        Haal dan de tekst uit de database, die zit in een lijst van lijsten.
        In tegenovergestelde volgorde moet hij op de stack komen.
        """
        if len(check_rect.collidelistall(self.current_map.notes)) == 1:
            object_nr = check_rect.collidelist(self.current_map.notes)
            note_id = self.current_map.notes[object_nr].name
            note_text = NoteDatabase[note_id].value
            # als het nog geen list (wat moet), bijvoorbeeld bij een plaatje, maak dan van de "string" een ["string"]
            if type(note_text) != list:
                note_text = [note_text]
            for i, text_part in enumerate(reversed(note_text)):
                push_object = MessageBox(text_part, last=(True if i == 0 else False))
                self.engine.gamestate.push(push_object)

    def check_signs(self):
        """
        Bekijk of collide met een sign.
        """
        if self.party_sprites[0].last_direction == Direction.North:
            if len(self.party_sprites[0].rect.collidelistall(self.current_map.signs)) == 1:
                object_nr = self.party_sprites[0].rect.collidelist(self.current_map.signs)
                sign_id = self.current_map.signs[object_nr].sign_id
                sign_data = SignDatabase[sign_id].value

                push_object = MessageBox(sign_data, last=True)
                self.engine.gamestate.push(push_object)

    def check_chests(self):
        """
        Bekijk of collide met een chest.
        """
        if self.party_sprites[0].last_direction == Direction.North:
            if len(self.party_sprites[0].rect.collidelistall(self.current_map.chests)) == 1:
                object_nr = self.party_sprites[0].rect.collidelist(self.current_map.chests)
                chest_id = self.current_map.chests[object_nr].chest_id
                chest_data = self.engine.data.treasure_chests[chest_id]

                # v = skill value, h = hero naam
                mec_v, mec_h = 0, ""
                thf_v, thf_h = 0, ""
                if chest_data.get('condition') and chest_data['content']:
                    for key, value in chest_data['condition'].items():
                        if key == "mec":
                            mec_v, mec_h = self.engine.data.party.get_highest_value_of_skill(key)
                            if mec_v < value:
                                text = TreasureChestDatabase.mec_text(chest_data['condition'][key])
                                push_object = MessageBox(text)
                                self.engine.gamestate.push(push_object)
                                return
                        elif key == "thf":
                            thf_v, thf_h = self.engine.data.party.get_highest_value_of_skill(key)
                            if thf_v < value:
                                text = TreasureChestDatabase.thf_text(chest_data['condition'][key])
                                push_object = MessageBox(text)
                                self.engine.gamestate.push(push_object)
                                return

                # voortijdig weghalen condition weer verwijderd. anders kan open_chest() de condition niet meer lezen

                if chest_data['content']:
                    chest_data['opened'] = 1
                    text = TreasureChestDatabase.open_chest(chest_data.get('condition'), mec_v, mec_h, thf_v, thf_h)
                    image = []
                    text, image = self.display_loot(chest_data['content'], text, image)
                    chest_data['content'] = dict()
                    push_object = MessageBox(text, spr_image=image, sound=SFX.chest)
                    self.engine.gamestate.push(push_object)

    def check_sparklies(self, check_rect):
        """
        Bekijk of collide met een sparkly.
        """
        if len(check_rect.collidelistall(self.current_map.sparkly)) == 1:
            object_nr = check_rect.collidelist(self.current_map.sparkly)
            sparkly_id = self.current_map.sparkly[object_nr].sparkly_id
            sparkly_data = self.engine.data.sparklies[sparkly_id]

            if sparkly_data['content']:
                sparkly_data['taken'] = 1
                text = ["Found:"]
                image = []
                text, image = self.display_loot(sparkly_data['content'], text, image)
                sparkly_data['content'] = dict()
                push_object = MessageBox(text, spr_image=image, sound=SFX.sparkly)
                self.engine.gamestate.push(push_object)

    def display_loot(self, content_data, text, image):
        """
        Soort van static method. geeft alleen de gevraagde dingen terug.
        :return: geeft de tekst en de plaatjes terug voor een messagebox
        """
        for key, value in content_data.items():
            if key.startswith('eqp'):
                equipment_item = inventoryitems.factory_equipment_item(value['nam'])
                equipment_item_spr = pygame.image.load(equipment_item.SPR).subsurface(
                    equipment_item.COL, equipment_item.ROW, ICONSIZE, ICONSIZE).convert_alpha()
                self.engine.data.inventory.add_i(equipment_item, quantity=value['qty'])
                text.append("{} {}".format(value['qty'], equipment_item.NAM))
                image.append(equipment_item_spr)
            elif key.startswith('itm'):
                pouch_item = inventoryitems.factory_pouch_item(value['nam'])
                pouch_item_spr = pygame.image.load(pouch_item.SPR).convert_alpha()
                self.engine.data.pouch.add(pouch_item, quantity=value['qty'])
                text.append("{} {}".format(value['qty'], pouch_item.NAM))
                image.append(pouch_item_spr)

        return text, image
