
"""
class: Person
class: Walking
"""

import random

import pygame

from constants import Direction
from constants import PersonState


HALFBLOCKERWIDTH = 32
HALFBLOCKERHEIGHT = 16

TRANSP = 'resources/sprites/transp.png'


class Person(pygame.sprite.Sprite):
    """
    Baseclass voor een pc unit in de overworld.
    """
    def __init__(self, person_id, sprite, rect, objectlayer, direction, dont_show_sprite):
        super().__init__()

        self.west_states = {0:  (32, 32, 32, 32), 1: (0, 32, 32, 32), 2: (32, 32, 32, 32), 3: (64, 32, 32, 32)}
        self.east_states = {0:  (32, 64, 32, 32), 1: (0, 64, 32, 32), 2: (32, 64, 32, 32), 3: (64, 64, 32, 32)}
        self.north_states = {0: (32, 96, 32, 32), 1: (0, 96, 32, 32), 2: (32, 96, 32, 32), 3: (64, 96, 32, 32)}
        self.south_states = {0: (32,  0, 32, 32), 1: (0,  0, 32, 32), 2: (32,  0, 32, 32), 3: (64,  0, 32, 32)}

        # Assign the spritesheet to self.full_sprite
        self.full_sprite = pygame.image.load(sprite).convert_alpha()
        # 'Clip' the sheet so that only one frame is displayed (the first frame of _south_states)
        if direction == Direction.North:
            self.full_sprite.set_clip(self.north_states[0])
        elif direction == Direction.West:
            self.full_sprite.set_clip(self.west_states[0])
        elif direction == Direction.East:
            self.full_sprite.set_clip(self.east_states[0])
        else:
            self.full_sprite.set_clip(self.south_states[0])
        # Create a rect to animate around the screen
        self.image = self.full_sprite.subsurface(self.full_sprite.get_clip())
        self.rect = rect

        self.person_id = person_id
        self._layer = objectlayer

        # als er in dont_show_sprite iets staat, dan is het een transparante sprite.
        self.show_sprite = True
        if dont_show_sprite:
            self.show_sprite = False
            self.image = pygame.image.load(TRANSP).convert_alpha()

    def turn(self, player_rect):
        """
        De meegegeven sprite draait naar de speler toe.
        Met welke berekening hij meekrijgt kies een ander subsurface.
        """
        if self.rect.left < player_rect.left and \
                abs(self.rect.centery - player_rect.centery) < \
                abs(self.rect.centerx - player_rect.centerx):
            states = self.east_states[0]
        elif self.rect.left > player_rect.left and \
                abs(self.rect.centery - player_rect.centery) < \
                abs(self.rect.centerx - player_rect.centerx):
            states = self.west_states[0]
        elif self.rect.top < player_rect.top and \
                abs(self.rect.centery - player_rect.centery) > \
                abs(self.rect.centerx - player_rect.centerx):
            states = self.south_states[0]
        elif self.rect.top > player_rect.top and \
                abs(self.rect.centery - player_rect.centery) > \
                abs(self.rect.centerx - player_rect.centerx):
            states = self.north_states[0]
        else:
            states = self.south_states[0]

        self.full_sprite.set_clip(states)
        self.image = self.full_sprite.subsurface(self.full_sprite.get_clip())

    def get_blocker(self):
        """
        :return: Een rect met zijn eigen locatie en opgegeven grootte.
        """
        return pygame.Rect(self.rect.x, self.rect.y, HALFBLOCKERWIDTH, HALFBLOCKERHEIGHT)


class Walking(Person):
    """
    Struinend Persoon
    """
    def __init__(self, person_id, sprite, rect, objectlayer, direction):
        super().__init__(person_id, sprite, rect, objectlayer, direction, None)

        self.directions = {1: Direction.North, 2: Direction.South, 3: Direction.West, 4: Direction.East}

        self.true_position = list(self.rect.topleft)  # true_pos is een float, dat is nodig voor timebased movement
        self.old_position = list(self.rect.topleft)
        self.last_direction = direction
        self.move_direction = None

        self.wander_area = pygame.Rect(self.rect.x-64, self.rect.y-64, 160, 160)
        self.WANDER_SPEED = 60
        self.STEP_SPEED = 15
        self.step_count = 0
        self.step_animation = 0

        self.state = PersonState.Resting
        self.state_time = random.random() + .5

    def turn(self, player_rect):
        """
        Gebruikt turn van Person. Maar zet die sprite ook 5 seconden stil daarna.
        """
        super().turn(player_rect)
        self.state = PersonState.Resting
        self.state_time = 5

    def update(self, pb, hb, lb, sb, dt):
        """
        Update de status van een Walking Person.
        :param pb: player blocker
        :param hb: high blocker
        :param lb: low blocker
        :param sb: sprite blocker
        :param dt: self.clock.tick(FPS)/1000.0
        """
        self.state_time -= dt

        if self.state == PersonState.Moving:
            self._move(dt)
            self._check_blocker(pb, hb, lb, sb, dt)
            self._animate(dt)

        if self.state_time > 0:
            return
        self.state_time = random.random() + .5

        if self.state == PersonState.Resting:
            self.state = PersonState.Moving
            rnd = random.randint(1, 4)
            self.move_direction = self.directions[rnd]

        elif self.state == PersonState.Moving:
            self.state = PersonState.Resting
            self._stand()
            self._animate(dt)

    def _stand(self):
        """
        Laat de unit stoppen met bewegen.
        """
        self.last_direction = self.move_direction
        self.move_direction = None
        self.old_position = list(self.rect.topleft)
        self.true_position = list(self.rect.topleft)

    def _move(self, dt):
        """
        Verzet de positie in de opgegeven richting.
        """
        self.old_position = list(self.rect.topleft)

        if self.move_direction == Direction.North:
            self.full_sprite.set_clip(self.north_states[0])
        elif self.move_direction == Direction.West:
            self.full_sprite.set_clip(self.west_states[0])
        elif self.move_direction == Direction.East:
            self.full_sprite.set_clip(self.east_states[0])
        else:
            self.full_sprite.set_clip(self.south_states[0])
        self.image = self.full_sprite.subsurface(self.full_sprite.get_clip())

        if self.move_direction == Direction.North:
            self.true_position[1] -= self.WANDER_SPEED * dt
        elif self.move_direction == Direction.South:
            self.true_position[1] += self.WANDER_SPEED * dt
        elif self.move_direction == Direction.West:
            self.true_position[0] -= self.WANDER_SPEED * dt
        elif self.move_direction == Direction.East:
            self.true_position[0] += self.WANDER_SPEED * dt

        self.rect.x = round(self.true_position[0])
        self.rect.y = round(self.true_position[1])

    def _check_blocker(self, pb, hb, lb, sb, dt):
        """
        Bekijk of de unit tegen een andere sprite aan loopt.
        """
        csb = sb.copy()         # kopie van zichzelf
        csb.remove(self.rect)   # verwijder eigen sprite uit de kopie, want anders stopt hij op zichzelf

        if not self.wander_area.contains(self.rect) or \
                self.rect.collidelist(pb) > -1 or \
                self.rect.collidelist(hb) > -1 or \
                self.rect.collidelist(lb) > -1 or \
                self.rect.collidelist(csb) > -1:         # check ook op andere (kopie van) people sprites.
            self._move_back(dt)
            self.state = PersonState.Resting
            self._stand()

    def _move_back(self, dt):
        """
        Verzet de positie in de tegenovergestelde richting.
        """
        if self.move_direction == Direction.North:
            self.true_position[1] += self.WANDER_SPEED * dt
        elif self.move_direction == Direction.South:
            self.true_position[1] -= self.WANDER_SPEED * dt
        elif self.move_direction == Direction.West:
            self.true_position[0] += self.WANDER_SPEED * dt
        elif self.move_direction == Direction.East:
            self.true_position[0] -= self.WANDER_SPEED * dt

        self.rect.x = round(self.true_position[0])
        self.rect.y = round(self.true_position[1])

    def _animate(self, dt, make_sound=False):
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
            self.step_count = self.STEP_SPEED         # zodat hij direct een stap animeert uit stilstand
            self.step_animation = 0
            self.full_sprite.set_clip(pygame.Rect(clipped_rect))
        # return clipped_rect

    def _get_frame(self, frame_set, dt, make_sound):
        self.step_count += self.WANDER_SPEED * dt
        if self.step_count > self.STEP_SPEED:
            self.step_count = 0
            # if self.step_animation in (0, 2) and make_sound:
            #     self.audio.play_step_sound()
            self.step_animation += 1
            if self.step_animation > 3:
                self.step_animation = 0
        return frame_set[self.step_animation]
