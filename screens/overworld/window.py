
"""
class: Window
"""

import collections

import pygame

import audio as sfx

from components import ColorBox
from components import ConfirmBox
from components import Grid
from components import Map
from components import MessageBox
from components import Player
from components import Transition

from constants import Direction

from database import InnDatabase
from database import HeroDatabase
from database import PeopleDatabase
from database import SchoolDatabase
from database import ShopDatabase
from database import SignDatabase

from database import PouchItemDatabase

from inventoryitems import EquipmentItem
from inventoryitems import PouchItem
from inventoryitems import QuestItem
import keys
import screens.shop.display


BACKGROUNDCOLOR = pygame.Color("gray12")
GRIDCOLOR = pygame.Color("gray36")
HEROCOLOR = pygame.Color("blue")
HIGHBLOCKERCOLOR = pygame.Color("yellow")
LOWBLOCKERCOLOR = pygame.Color("purple")
SHOPCOLOR = pygame.Color("black")

PLAYERLAYER = 5

ZOOMSPEED = .1
MAXZOOM = 3.1
DEFZOOM = 1.0
MINZOOM = .5

GRIDLAYER = 8
CBOXLAYER = 9
GRIDSIZE = 32
ICONSIZE = 32

NEWMAPTIMEOUT = 0.5  # minimale keyblock. Zonder deze timer kun je op de movement keys drukken terwijl de map laadt.


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

        self.inn_box = None     # confirmbox
        self.inn_data = None
        self.hero_box = None    # confirmbox
        self.hero_data = None
        self.quest_box = None   # confirmbox
        self.quest_data = None
        self.person_face = None

    def load_map(self):
        """
        Maak een nieuwe map aan met de hero's in het veld.
        """
        self.group = self.engine.current_map.view
        self.grid_sprite = None
        self.cbox_sprites = []

        start_pos = self.engine.data.map_pos           # normaliter is map_pos een point, behalve bij het laden van een
        start_dir = self.engine.data.map_dir           # map, dan is het een string. bv start_game of ersin_forest_centr

        for pos in self.engine.current_map.start_pos:  # kijk in de start_pos list van de map
            if pos.name == start_pos:                  # van alle start_possen, welke komt overeen met 'start_game'
                start_pos = pos.x, pos.y               # zet dan de x,y waarde op dié start_pos, maak van de string
                break                                  # dus weer een point.

        for pos in self.engine.current_map.start_pos:                            # in een .tmx map kun je bij start_pos
            if getattr(pos, 'direction', None) and (pos.x, pos.y) == start_pos:  # een 'direction' property meegeven.
                start_dir = Direction[pos.direction]                             # als dat een Direction Enum is dan
                break                                   # dan start de unit in de nieuw geladen map in die kijkrichting.

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
        for hero in self.engine.current_map.heroes:
            if not self.engine.data.party.contains(hero.sprite_id):
                self.group.add(hero)
                # voeg alleen nu een blocker toe als de hero er daadwerkelijk is.
                # dit zit niet in de map class vanwege imports. maar nu moet hij in window al 2x checken op dit.
                self.engine.current_map.high_blocker_rects.append(hero.get_blocker())
        self.group.add(self.engine.current_map.shops)
        self.group.add(self.engine.current_map.schools)
        self.group.add(self.engine.current_map.inns)
        self.group.add(self.engine.current_map.people)
        self.group.add(self.engine.current_map.signs)
        self.group.add(self.engine.current_map.chests)
        self.group.add(self.engine.current_map.sparkly)

        self.engine.audio.set_bg_music(self.engine.gamestate.peek().name)
        self.engine.audio.set_bg_sounds(self.engine.gamestate.peek().name)

        # want deze is alleen nodig voor de audio, dus nadien weghalen.
        # hij wordt vanaf nu (22-06-2016) ook voor beginpositie bepaling gebruikt, maar hij mag nog steeds weg nadien.
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

    def on_enter(self):
        """
        Als een hero confirmbox in beeld is geweest.
        Als de inn confirmbox in beeld is geweest.
        Als de quest confirmbox in beeld is geweest.
        """
        if self.hero_box:
            choice, yes, scr_capt = self.hero_box.on_exit()
            if choice == yes:
                if self.engine.data.party.add(self.hero_data):
                    self.engine.key_timer = NEWMAPTIMEOUT
                    self.engine.current_map = Map(self.engine.data.map_name)
                    self.load_map()
                else:
                    text = ["It seems your party is full already."]
                    push_object = MessageBox(self.engine.gamestate, text,
                                             face_image=self.hero_data.FAC, scr_capt=scr_capt)
                    self.engine.gamestate.push(push_object)

            self.hero_box = None
            self.hero_data = None

        elif self.inn_box:
            choice, yes, scr_capt = self.inn_box.on_exit()
            if choice == yes:
                gold = PouchItem(**PouchItemDatabase.gold.value)
                if self.engine.data.pouch.remove(gold, self.inn_data['price']):
                    self.engine.audio.play_sound(sfx.COINS)
                    self.engine.gamestate.push(Transition(self.engine.gamestate))
                    push_object = MessageBox(self.engine.gamestate, InnDatabase.paid_text(),
                                             face_image=self.inn_data['face'], scr_capt=scr_capt)
                    self.engine.gamestate.push(push_object)
                    # todo, health afhandelen.
                else:
                    push_object = MessageBox(self.engine.gamestate, InnDatabase.fail_text(),
                                             face_image=self.inn_data['face'], scr_capt=scr_capt)
                    self.engine.gamestate.push(push_object)
            else:
                push_object = MessageBox(self.engine.gamestate, InnDatabase.deny_text(),
                                         face_image=self.inn_data['face'], scr_capt=scr_capt)
                self.engine.gamestate.push(push_object)

            self.inn_box = None
            self.inn_data = None

        elif self.quest_box:
            choice, yes, scr_capt = self.quest_box.on_exit()
            if choice == yes:
                self.engine.gamestate.push(Transition(self.engine.gamestate))
                # hij kan voldoen, komt daarom met text en plaatjes terug, om dat weer te kunnen geven.
                text, image = self.quest_data.fulfill(self.engine.data)
                push_object = MessageBox(self.engine.gamestate, text, spr_image=image, scr_capt=scr_capt)
                self.engine.gamestate.push(push_object)

                # nog een bedank berichtje van de quest owner.
                push_object = MessageBox(self.engine.gamestate, self.quest_data.get_text(),
                                         face_image=self.person_face, scr_capt=scr_capt)
                self.engine.gamestate.push(push_object)

                # zet de state op Rewarded.
                self.quest_data.confirm_contact(self.engine.data)

            self.quest_box = None
            self.quest_data = None
            self.person_face = None

    def single_input(self, event):
        """
        Handelt de muis en keyboard input af.
        :param event: pygame.event.get()
        """
        if event.type == pygame.KEYDOWN:

            if event.key == keys.ALIGN:
                self.party_sprites[0].align_to_grid(GRIDSIZE)
                self.align()

            elif event.key == keys.ACTION:
                self.check_heroes(self.party_sprites[0].get_check_rect())
                self.check_shops(self.party_sprites[0].get_check_rect())
                self.check_schools(self.party_sprites[0].get_check_rect())
                self.check_inns(self.party_sprites[0].get_check_rect())
                self.check_people(self.party_sprites[0].get_check_rect())
                self.check_signs()
                self.check_chests()
                self.check_sparklies(self.party_sprites[0].get_check_rect())  # sparklys moeten ook van boven kunnen

            elif event.key == keys.GRID:
                if self.grid_sprite is None:
                    self.grid_sprite = Grid(self.engine.current_map.width,
                                            self.engine.current_map.height,
                                            GRIDCOLOR, GRIDSIZE, GRIDLAYER)
                    self.group.add(self.grid_sprite)
                else:
                    self.group.remove(self.grid_sprite)
                    self.grid_sprite = None

            elif event.key == keys.CBOX:
                if len(self.cbox_sprites) == 0:                             # als de lijst leeg is.
                    for unit in self.party_sprites:
                        self.cbox_sprites.append(ColorBox(unit.rect, HEROCOLOR, CBOXLAYER))
                    for rect in self.engine.current_map.high_blocker_rects:
                        self.cbox_sprites.append(ColorBox(rect, HIGHBLOCKERCOLOR, CBOXLAYER))
                    for rect in self.engine.current_map.low_blocker_rects:
                        self.cbox_sprites.append(ColorBox(rect, LOWBLOCKERCOLOR, CBOXLAYER))
                    for obj in self.engine.current_map.people:
                        if getattr(obj, 'wander_area', None):
                            self.cbox_sprites.append(ColorBox(obj.wander_area, SHOPCOLOR, CBOXLAYER))
                    for obj_group in (self.engine.current_map.heroes,
                                      self.engine.current_map.shops,
                                      self.engine.current_map.schools,
                                      self.engine.current_map.inns,
                                      self.engine.current_map.people,
                                      self.engine.current_map.signs,
                                      self.engine.current_map.chests,
                                      self.engine.current_map.sparkly):
                        for obj in obj_group:
                            self.cbox_sprites.append(ColorBox(obj.rect, SHOPCOLOR, CBOXLAYER))
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
                                            [sprite.get_blocker() for sprite in self.engine.current_map.people if
                                             getattr(sprite, 'wander_area', None)],  # alleen maar lopende sprites,
                                            None,                                    # standing sprites hebben al een
                                            self.engine.current_map.width,           # blocker
                                            self.engine.current_map.height,
                                            dt)

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
        self.check_portals()

        # Update locaties (indien F11).
        # misschien gaat dit een probleem geven wanneer ingame de party grootte wordt gewijzigd.
        # dan heeft bijv een boom een unit.rect.topleft oid.
        if len(self.cbox_sprites) > 0:
            for index, unit in enumerate(self.party_sprites):  # dit kan om dat de eerste paar die aan cbox_sprites bij
                self.cbox_sprites[index].rect.topleft = unit.rect.topleft  # F11 zijn toegevoegd zijn de unit.rects

        # Centreer op de hero als de kaart groter is dan de window.
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

        # beweeg wandering people.
        # niet alleen maar wandering staan in c_m.people, maar update wordt ge-pass-t bij standing people
        for obj in self.engine.current_map.people:
            obj.update(self.party_sprites,
                       self.engine.current_map.high_blocker_rects,
                       self.engine.current_map.low_blocker_rects,
                       [sprite for sprite in self.engine.current_map.people if  # alleen maar lopende sprites,
                        getattr(sprite, 'wander_area', None)],                  # standing sprites hebben al een blocker
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
                # dit was een poging tot een andere manier van trailing. werkt niet goed genoeg.
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
            self.engine.key_timer = NEWMAPTIMEOUT
            portal_nr = self.party_sprites[0].rect.collidelist(self.engine.current_map.portals)
            self.prev_map_name = self.engine.current_map.portals[portal_nr].from_name
            self.engine.data.map_name = self.engine.current_map.portals[portal_nr].to_name
            self.engine.data.map_pos = self.prev_map_name       # zet de point om naar een string naam.
            self.engine.current_map = Map(self.engine.data.map_name)
            self.load_map()
            self.engine.gamestate.push(Transition(self.engine.gamestate, full_screen=False))

    def check_heroes(self, check_rect):
        """
        Bekijk of collide met een hero.
        """
        if len(check_rect.collidelistall(self.engine.current_map.heroes)) == 1:
            object_name = check_rect.collidelist(self.engine.current_map.heroes)
            hero_sprite = self.engine.current_map.heroes[object_name]
            # ook hier moet een hero in party niet gecheckt worden
            if not self.engine.data.party.contains(hero_sprite.sprite_id):
                self.hero_data = self.engine.data.heroes[hero_sprite.sprite_id]

                hero_sprite.turn(self.party_sprites[0].rect)

                self.hero_box = ConfirmBox(self.engine.gamestate, self.engine.audio,
                                           HeroDatabase.opening(self.hero_data.RAW),
                                           face_image=self.hero_data.FAC)
                self.engine.gamestate.push(self.hero_box)

    def check_shops(self, check_rect):
        """
        Bekijk of collide met een shopkeeper. Update de richting van de sprite.
        :param check_rect: een iets verplaatste rect van de player sprite zodat hij kan colliden met een obj dat anders
        niet collidebaar is. self.party_sprites[0].rect
        """
        if len(check_rect.collidelistall(self.engine.current_map.shops)) == 1:
            object_nr = check_rect.collidelist(self.engine.current_map.shops)
            shop_sprite = self.engine.current_map.shops[object_nr]
            shop_data = ShopDatabase[shop_sprite.sprite_id].value

            # check alle shops, zijn ze zichtbaar, hebben ze dezelfde id, turn die dan allemaal.
            for spr in self.engine.current_map.shops:
                if spr.show_sprite:
                    if spr.sprite_id == shop_sprite.sprite_id:
                        spr.turn(self.party_sprites[0].rect)

            push_object = screens.shop.display.Display(self.engine, shop_data['content'],
                                                       shop_data.get('material'),  # material is geen garantie
                                                       shop_data['face'],)
            self.engine.gamestate.push(push_object)
            self.engine.gamestate.push(Transition(self.engine.gamestate))

    def check_schools(self, check_rect):
        """
        Bekijk of je collide met een school.
        """
        if len(check_rect.collidelistall(self.engine.current_map.schools)) == 1:
            object_nr = check_rect.collidelist(self.engine.current_map.schools)
            school_sprite = self.engine.current_map.schools[object_nr]
            school_data = SchoolDatabase[school_sprite.sprite_id].value

            school_sprite.turn(self.party_sprites[0].rect)

    def check_inns(self, check_rect):
        """
        Er kunnen ook inns zijn zonder sprite, die moeten dan geupdate worden. Maar alle anderen met sprite wel omdat
        de lege een verlengde is van de gevulde. Hij vergelijkt sprite_id, dus hij turnt alleen met dezelfde id.
        """
        if len(check_rect.collidelistall(self.engine.current_map.inns)) == 1:
            object_nr = check_rect.collidelist(self.engine.current_map.inns)
            inn_sprite = self.engine.current_map.inns[object_nr]
            self.inn_data = InnDatabase[inn_sprite.sprite_id].value

            for spr in self.engine.current_map.inns:
                if spr.show_sprite:
                    if spr.sprite_id == inn_sprite.sprite_id:
                        spr.turn(self.party_sprites[0].rect)

            self.inn_box = ConfirmBox(self.engine.gamestate, self.engine.audio,
                                      InnDatabase.welcome_text(self.inn_data['price']), self.inn_data['face'])
            self.engine.gamestate.push(self.inn_box)

    def check_people(self, check_rect):
        """
        Bekijk of hij collide met een standing of wandering person.
        """
        if len(check_rect.collidelistall(self.engine.current_map.people)) == 1:
            object_nr = check_rect.collidelist(self.engine.current_map.people)
            person_sprite = self.engine.current_map.people[object_nr]
            person_data = PeopleDatabase[person_sprite.sprite_id].value

            # doe gewoon eerst het draaien zoals normaal
            person_sprite.turn(self.party_sprites[0].rect)

            # maar dan, als de persoon een quest heeft
            if person_data.get('quest'):
                # stop hem in data.logbook en haal de juiste self.quest_data er weer uit.
                quest_key = person_data['quest'].name
                quest_value = person_data['quest'].value
                if not self.engine.data.logbook.get(quest_key):
                    self.engine.data.logbook[quest_key] = QuestItem(**quest_value)
                self.quest_data = self.engine.data.logbook[quest_key]

                # het gezicht is in on_enter() weer nodig, vandaar deze declaratie.
                self.person_face = person_data['face']

                push_object = MessageBox(self.engine.gamestate, self.quest_data.get_text(), self.person_face)
                self.engine.gamestate.push(push_object)
                # als hij voldoet aan de voorwaarden
                if self.quest_data.confirm_contact(self.engine.data):
                    # kom dan met een confirmbox
                    self.quest_box = ConfirmBox(self.engine.gamestate, self.engine.audio, self.quest_data.get_text(0))
                    self.engine.gamestate.push(self.quest_box)
                    # draai de messagebox en confirmbox om in de stack.
                    self.engine.gamestate.swap()
                # als hij niet voldoet aan de voorwaarden, dan heeft hij nog wel confirm_contact uitgevoerd.

            # of als hij dat niet heeft
            else:
                push_object = MessageBox(self.engine.gamestate, person_data['text'], person_data['face'])
                self.engine.gamestate.push(push_object)

    def check_signs(self):
        """
        Bekijk of collide met een sign.
        """
        if self.party_sprites[0].last_direction == Direction.North:
            if len(self.party_sprites[0].rect.collidelistall(self.engine.current_map.signs)) == 1:
                object_nr = self.party_sprites[0].rect.collidelist(self.engine.current_map.signs)
                sign_sprite = self.engine.current_map.signs[object_nr]
                sign_data = SignDatabase[sign_sprite.sign_id].value

                push_object = MessageBox(self.engine.gamestate, sign_data)
                self.engine.gamestate.push(push_object)

    # noinspection PyUnresolvedReferences
    def check_chests(self):
        """
        Bekijk of collide met een chest.
        """
        if self.party_sprites[0].last_direction == Direction.North:
            if len(self.party_sprites[0].rect.collidelistall(self.engine.current_map.chests)) == 1:
                object_nr = self.party_sprites[0].rect.collidelist(self.engine.current_map.chests)
                chest_sprite = self.engine.current_map.chests[object_nr]
                chest_data = self.engine.data.treasure_chests[chest_sprite.chest_id]

                # v = skill value, h = hero naam
                mec_v, mec_h = 0, ""
                thf_v, thf_h = 0, ""
                if chest_data.get('condition') and chest_data['content']:
                    for key, value in chest_data['condition'].items():
                        if key == "mec":
                            mec_v, mec_h = self.engine.data.party.get_highest_value_of_skill(key)
                            if mec_v < value:
                                text = self.engine.data.treasure_chests.mec_text(chest_data['condition'][key])
                                push_object = MessageBox(self.engine.gamestate, text)
                                self.engine.gamestate.push(push_object)
                                return
                        elif key == "thf":
                            thf_v, thf_h = self.engine.data.party.get_highest_value_of_skill(key)
                            if thf_v < value:
                                text = self.engine.data.treasure_chests.thf_text(chest_data['condition'][key])
                                push_object = MessageBox(self.engine.gamestate, text)
                                self.engine.gamestate.push(push_object)
                                return

                # voortijdig weghalen condition weer verwijderd. anders kan open_chest() de condition niet meer lezen

                if chest_data['content']:
                    chest_data['opened'] = 1
                    text = self.engine.data.treasure_chests.open_chest(chest_data.get('condition'),
                                                                       mec_v, mec_h, thf_v, thf_h)
                    image = []
                    for key, value in chest_data['content'].items():
                        if key.startswith('eqp'):
                            equipment_item = EquipmentItem(**value['nam'].value)
                            equipment_item_spr = pygame.image.load(equipment_item.SPR).subsurface(
                                equipment_item.COL, equipment_item.ROW, ICONSIZE, ICONSIZE).convert_alpha()
                            self.engine.data.inventory.add_i(equipment_item, quantity=value['qty'])
                            text.append("{} {}".format(value['qty'], equipment_item.NAM))
                            image.append(equipment_item_spr)
                        elif key.startswith('itm'):
                            pouch_item = PouchItem(**value['nam'].value)
                            pouch_item_spr = pygame.image.load(pouch_item.SPR).convert_alpha()
                            self.engine.data.pouch.add(pouch_item, quantity=value['qty'])
                            text.append("{} {}".format(value['qty'], pouch_item.NAM))
                            image.append(pouch_item_spr)
                    self.engine.audio.play_sound(sfx.CHEST)
                    chest_data['content'] = dict()
                    push_object = MessageBox(self.engine.gamestate, text, spr_image=image)
                    self.engine.gamestate.push(push_object)

    # noinspection PyUnresolvedReferences
    def check_sparklies(self, check_rect):
        """
        Bekijk of collide met een sparkly.
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
                        equipment_item = EquipmentItem(**value['nam'].value)
                        equipment_item_spr = pygame.image.load(equipment_item.SPR).subsurface(
                            equipment_item.COL, equipment_item.ROW, ICONSIZE, ICONSIZE).convert_alpha()
                        self.engine.data.inventory.add_i(equipment_item, quantity=value['qty'])
                        text.append("{} {}".format(value['qty'], equipment_item.NAM))
                        image.append(equipment_item_spr)
                    elif key.startswith('itm'):
                        pouch_item = PouchItem(**value['nam'].value)
                        pouch_item_spr = pygame.image.load(pouch_item.SPR).convert_alpha()
                        self.engine.data.pouch.add(pouch_item, quantity=value['qty'])
                        text.append("{} {}".format(value['qty'], pouch_item.NAM))
                        image.append(pouch_item_spr)
                self.engine.audio.play_sound(sfx.SPARKLY)
                sparkly_data['content'] = dict()
                push_object = MessageBox(self.engine.gamestate, text, spr_image=image)
                self.engine.gamestate.push(push_object)
