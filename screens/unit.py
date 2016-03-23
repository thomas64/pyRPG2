
"""
class: Unit
"""

import pygame

from screens.direction import Direction
import keys

FEETWIDTH = 2       # hele kleine voetjes
FEETHEIGHT = 2

MOVESPEED1 = 60
MOVESPEED2 = 120    # pixels/second
MOVESPEED3 = 240
MOVESPEED4 = 480
STEPSPEED = 30      # een waarde? lager is snellere stappen
TURNDELAY = 7/60    # van een seconde
VIEWSPEED = 8       # todo, deze moet nog aangepast worden


class Unit(pygame.sprite.Sprite):
    """
    Unit extends the pygame.sprite.Sprite class
    """
    def __init__(self, spritesheet, position, direction, audio):
        pygame.sprite.Sprite.__init__(self)

        self.west_states = {0:  (32, 32, 32, 32), 1: (0, 32, 32, 32), 2: (32, 32, 32, 32), 3: (64, 32, 32, 32)}
        self.east_states = {0:  (32, 64, 32, 32), 1: (0, 64, 32, 32), 2: (32, 64, 32, 32), 3: (64, 64, 32, 32)}
        self.north_states = {0: (32, 96, 32, 32), 1: (0, 96, 32, 32), 2: (32, 96, 32, 32), 3: (64, 96, 32, 32)}
        self.south_states = {0: (32,  0, 32, 32), 1: (0,  0, 32, 32), 2: (32,  0, 32, 32), 3: (64,  0, 32, 32)}

        # Assign the spritesheet to self.full_sprite
        self.full_sprite = pygame.image.load(spritesheet).convert_alpha()
        # 'Clip' the sheet so that only one frame is displayed (the first frame of _south_states)
        self.full_sprite.set_clip(pygame.Rect(self.south_states[0]))

        # Create a rect to animate around the screen
        self.image = self.full_sprite.subsurface(self.full_sprite.get_clip())
        self.rect = self.image.get_rect()
        self.feet = pygame.Rect(0, 0, FEETWIDTH, FEETHEIGHT)
        self.mask = pygame.mask.from_surface(self.image)

        self.audio = audio

        # Assign the position parameter value to the topleft x-y values of the rect
        self.rect.topleft = position
        self.feet.midbottom = self.rect.midbottom
        self.true_position = list(self.rect.topleft)    # true_pos is een float, dat is nodig voor timebased movement
        self.old_position = list(self.rect.topleft)
        self.last_direction = direction
        self.move_direction = None

        self.movespeed = 0
        self.step_count = 0
        self.step_animation = 0

        self.time_up = 0
        self.time_down = 0
        self.time_left = 0
        self.time_right = 0
        self.time_delay = 0

    def speed(self, key_input):
        """
        Geef de unit een snelheid mee.
        :param key_input: list van integers
        """
        self.movespeed = MOVESPEED2
        if (key_input[keys.MVSPEED1_1] or key_input[keys.MVSPEED1_2]) and \
           (key_input[keys.MVSPEED3_1] or key_input[keys.MVSPEED3_2]):
            self.movespeed = MOVESPEED4
        elif key_input[keys.MVSPEED3_1] or key_input[keys.MVSPEED3_2]:
            self.movespeed = MOVESPEED3
        elif key_input[keys.MVSPEED1_1] or key_input[keys.MVSPEED1_2]:
            self.movespeed = MOVESPEED1

    def direction(self, key_input, dt):
        """
        Geef de unit een richting mee.
        :param key_input: list van integers
        :param dt: self.clock.tick(FPS)/1000.0
        """
        # Als je helemaal geen knoppen indrukt, ga dan in de stilstand pose.
        if not (key_input[keys.UP] or key_input[keys.DOWN] or
                key_input[keys.LEFT] or key_input[keys.RIGHT]):
            self.time_delay = 0
            self._stand()
            self.animate(dt)

        if key_input[keys.UP]:
            self.time_up += 1
        else:
            self.time_up = 0
        if key_input[keys.DOWN]:
            self.time_down += 1
        else:
            self.time_down = 0
        if key_input[keys.LEFT]:
            self.time_left += 1
        else:
            self.time_left = 0
        if key_input[keys.RIGHT]:
            self.time_right += 1
        else:
            self.time_right = 0

        # Als hij nog geen stappen heeft gezet en hij kijkt naar een andere kant dan je drukt, stel een delay in.
        if self.move_direction is None and ((self.time_up > 0 and not self.last_direction == Direction.North) or
                                            (self.time_down > 0 and not self.last_direction == Direction.South) or
                                            (self.time_left > 0 and not self.last_direction == Direction.West) or
                                            (self.time_right > 0 and not self.last_direction == Direction.East)):
            self.time_delay = TURNDELAY

        # Als je meerdere knoppen indrukt, ga dan naar de richting van de laatst ingedrukte knop.
        if self.time_up > 0 and ((self.time_up <= self.time_down and self.time_down > 0) or
                                 (self.time_up <= self.time_left and self.time_left > 0) or
                                 (self.time_up <= self.time_right and self.time_right > 0)):
            self.last_direction = Direction.North
        elif self.time_down > 0 and ((self.time_down <= self.time_up and self.time_up > 0) or
                                     (self.time_down <= self.time_left and self.time_left > 0) or
                                     (self.time_down <= self.time_right and self.time_right > 0)):
            self.last_direction = Direction.South
        elif self.time_left > 0 and ((self.time_left <= self.time_up and self.time_up > 0) or
                                     (self.time_left <= self.time_down and self.time_down > 0) or
                                     (self.time_left <= self.time_right and self.time_right > 0)):
            self.last_direction = Direction.West
        elif self.time_right > 0 and ((self.time_right <= self.time_up and self.time_up > 0) or
                                      (self.time_right <= self.time_down and self.time_down > 0) or
                                      (self.time_right <= self.time_left and self.time_left > 0)):
            self.last_direction = Direction.East
        # Of ga in de richting van de enige knop die je indrukt.
        elif self.time_up > 0:
            self.last_direction = Direction.North
        elif self.time_down > 0:
            self.last_direction = Direction.South
        elif self.time_left > 0:
            self.last_direction = Direction.West
        elif self.time_right > 0:
            self.last_direction = Direction.East

        # Als je een knop indrukt, en er is geen delay, beweeg dan in die richting.
        if key_input[keys.UP] or key_input[keys.DOWN] or \
           key_input[keys.LEFT] or key_input[keys.RIGHT]:
            if self.time_delay > 0:
                self.time_delay -= 1 * dt
            else:
                self._move(dt)
                self.animate(dt)

    def _move(self, dt):
        """
        Verzet de positie in de opgegeven richting.
        """
        self.move_direction = self.last_direction
        self.old_position = list(self.rect.topleft)

        if self.move_direction == Direction.North:
            self.true_position[1] -= self.movespeed * dt
        elif self.move_direction == Direction.South:
            self.true_position[1] += self.movespeed * dt
        elif self.move_direction == Direction.West:
            self.true_position[0] -= self.movespeed * dt
        elif self.move_direction == Direction.East:
            self.true_position[0] += self.movespeed * dt

        self.rect.x = round(self.true_position[0])
        self.rect.y = round(self.true_position[1])
        self.feet.midbottom = self.rect.midbottom

    def align_to_grid(self, grid_size):
        """
        Align de unit op de grid.
        :param grid_size: grootte van een hokje
        """
        self.rect.topleft = (round(self.rect.x / grid_size) * grid_size, round(self.rect.y / grid_size) * grid_size)
        self.feet.midbottom = self.rect.midbottom

    def check_blocker(self, high_blockers, low_blockers, moverange, map_width, map_height, dt):
        """
        Bekijk of de unit tegen een andere sprite aan loopt.
        :param high_blockers: lijst van rects van map1.high_blocker_rects
        :param low_blockers: lijst van rects van map1.low_blocker_rects
        :param moverange: jouw moverange sprite
        :param map_width: breedte van de map
        :param map_height: hoogte van de map
        :param dt: self.clock.tick(FPS)/1000.0
        """
        t = False   # deze variabele is er om te kijken of true_pos aangepast moet worden aan het eind.

        # loop tegen de rand van een high_blocker aan
        # er mag maar 1 high_blocker in deze lijst zijn
        if len(self.rect.collidelistall(high_blockers)) == 1:
            # obj_nr is het nummer van de betreffende high_blocker
            obj_nr = self.rect.collidelist(high_blockers)
            self._move_side(high_blockers[obj_nr], dt)
            t = True

        # loop tegen de rand van een low_blocker aan, bijv water
        if len(self.rect.collidelistall(low_blockers)) == 1:
            obj_nr = self.rect.collidelist(low_blockers)
            self._move_side(low_blockers[obj_nr], dt)
            t = True

        # loop recht tegen een high_ of low_blocker aan
        while self.rect.collidelist(high_blockers) > -1 or \
                self.rect.collidelist(low_blockers) > -1:
            self._move_back()
            t = True

        # loop tegen de rand van de map aan
        if self.rect.top < 0:
            self.rect.top = 0
            t = True
        if self.rect.left < 0:
            self.rect.left = 0
            t = True
        if self.rect.bottom > map_height:
            self.rect.bottom = map_height
            t = True
        if self.rect.right > map_width:
            self.rect.right = map_width
            t = True

        # als er een moverange bestaat en je loopt tegen de rand van je moverange
        if moverange is not None:
            if pygame.sprite.collide_mask(self, moverange):
                self.rect.topleft = list(self.old_position)
                self.feet.midbottom = self.rect.midbottom
                t = True

        if t:
            self.true_position = list(self.rect.topleft)

    def _move_back(self):
        """
        Verzet de positie in de tegenovergestelde richting.
        """
        if self.move_direction == Direction.North:
            self.true_position[1] += 1
        elif self.move_direction == Direction.South:
            self.true_position[1] -= 1
        elif self.move_direction == Direction.West:
            self.true_position[0] += 1
        elif self.move_direction == Direction.East:
            self.true_position[0] -= 1

        self.rect.x = round(self.true_position[0])
        self.rect.y = round(self.true_position[1])
        self.feet.midbottom = self.rect.midbottom

    def _move_side(self, blocker_rect, dt):
        """
        Verzet de positie richting naast een object.
        :param blocker_rect: een blocker rectangle, zoals bijv een tree
        """
        if self.move_direction in (Direction.North, Direction.South):
            # als midden van unit groter is dan rechts van object
            # if self.rect.centerx > blocker_rect.right:               # code comment out is van voor timebased movement
            if self.true_position[0] + (self.rect.width / 2) > blocker_rect.right:
                self.true_position[0] += self.movespeed * dt
                # als links van char groter is dan rechts van object
                # if self.rect.left > blocker_rect.right:
                if self.true_position[0] > blocker_rect.right:
                    # self.rect.left = blocker_rect.right
                    self.true_position[0] = blocker_rect.right
            # object oost van je
            # if self.rect.centerx < blocker_rect.left:
            if self.true_position[0] + (self.rect.width / 2) < blocker_rect.left:
                self.true_position[0] -= self.movespeed * dt
                # if self.rect.right < blocker_rect.left:
                if self.true_position[0] + self.rect.width < blocker_rect.left:
                    # self.rect.left = blocker_rect.left - self.rect.width
                    self.true_position[0] = blocker_rect.left - self.rect.width

        if self.move_direction in (Direction.West, Direction.East):
            # object noord van je
            # if self.rect.centery > blocker_rect.bottom:
            if self.true_position[1] + (self.rect.height / 2) > blocker_rect.bottom:
                self.true_position[1] += self.movespeed * dt
                # if self.rect.top > blocker_rect.bottom:
                if self.true_position[1] > blocker_rect.bottom:
                    # self.rect.top = blocker_rect.bottom
                    self.true_position[1] = blocker_rect.bottom
            # object zuid van je
            # if self.rect.centery < blocker_rect.top:
            if self.true_position[1] + (self.rect.height / 2) < blocker_rect.top:
                self.true_position[1] -= self.movespeed * dt
                # if self.rect.bottom < blocker_rect.top:
                if self.true_position[1] + self.rect.height < blocker_rect.top:
                    # self.rect.top = blocker_rect.top - self.rect.height
                    self.true_position[1] = blocker_rect.top - self.rect.height

        self.rect.x = round(self.true_position[0])
        self.rect.y = round(self.true_position[1])
        self.feet.midbottom = self.rect.midbottom

    def _stand(self):
        """
        Laat de unit stoppen met bewegen.
        """
        self.move_direction = None
        self.old_position = list(self.rect.topleft)
        self.true_position = list(self.rect.topleft)

    def animate(self, dt, make_sound=True):
        """
        Kijkt of de unit beweegt. Geef dan de hele dir_states dict door ipv alleen waarde 0.
        :param dt: self.clock.tick(FPS)/1000.0
        :param make_sound: boolean, moeten de stappen geluid maken?
        """
        if self.move_direction is None:
            if self.last_direction == Direction.North:
                self._clip(self.north_states[0], dt, make_sound)
            if self.last_direction == Direction.South:
                self._clip(self.south_states[0], dt, make_sound)
            if self.last_direction == Direction.West:
                self._clip(self.west_states[0], dt, make_sound)
            if self.last_direction == Direction.East:
                self._clip(self.east_states[0], dt, make_sound)
        else:
            if self.move_direction == Direction.North:
                self._clip(self.north_states, dt, make_sound)
            if self.move_direction == Direction.South:
                self._clip(self.south_states, dt, make_sound)
            if self.move_direction == Direction.West:
                self._clip(self.west_states, dt, make_sound)
            if self.move_direction == Direction.East:
                self._clip(self.east_states, dt, make_sound)

        # Update the image for each pass
        self.image = self.full_sprite.subsurface(self.full_sprite.get_clip())

    def _clip(self, clipped_rect, dt, make_sound):
        if type(clipped_rect) is dict:
            self.full_sprite.set_clip(pygame.Rect(self._get_frame(clipped_rect, dt, make_sound)))
        else:
            self.step_count = STEPSPEED         # zodat hij direct een stap animeert uit stilstand
            self.step_animation = 0
            self.full_sprite.set_clip(pygame.Rect(clipped_rect))
        # return clipped_rect

    def _get_frame(self, frame_set, dt, make_sound):
        if self.movespeed != MOVESPEED4:  # geen animatie of geluid bij MOVESPEED4
            self.step_count += self.movespeed * dt
            if self.step_count > STEPSPEED:
                self.step_count = 0
                if self.step_animation in (0, 2) and make_sound:
                    self.audio.play_step_sound()
                self.step_animation += 1
                if self.step_animation > 3:
                    self.step_animation = 0
        return frame_set[self.step_animation]

    def get_history_data(self):
        """
        Geef een aantal waarden van de character terug.
        """
        return self.rect.x, self.rect.y, self.last_direction, self.move_direction, self.movespeed
