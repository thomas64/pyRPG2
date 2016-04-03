
"""
class: Animation
"""

import os

import pygame

PATH = 'resources/backgrounds/titlescreen/'
ANIMATIONSPEED = 10


class Animation(object):
    """
    De bewegende achtergrond.
    """
    def __init__(self):

        self.speed = 0

        self.animation = self._load_all_images(PATH)

        self.current = None

        self.width = self.animation[0].get_width()
        self.height = self.animation[0].get_height()
        self.position = (0, 0)

    @staticmethod
    def _load_all_images(path):
        """
        Laadt alle plaatjes uit de map in een dict.
        :return: de dict
        """
        images = {}
        for index, file in enumerate(os.listdir(path)):
            images[index] = pygame.image.load(os.path.join(path, file)).convert()
        return images

    def set_position(self, screen_width, screen_height):
        """
        Zet de animatie op de juiste positie.
        :param screen_width: de totale breedte van de achtergrond waarop de animatie zich bevind
        :param screen_height: de totale hoogte van de achtergrond waarop de animatie zich bevind
        """
        pos_x = (screen_width - self.width) / 2
        pos_y = (screen_height - self.height) / 2
        self.position = (pos_x, pos_y)

    def update(self, dt):
        """
        Bepaalt de snelheid aan de hand van deltatime en tekent de animatie.
        :param dt: self.clock.tick(FPS)/1000.0
        """
        self.speed += dt * ANIMATIONSPEED
        i = int(round(self.speed))
        if i >= len(self.animation):
            self.speed = 0
            i = 0
        self.current = self.animation[i]

    def render(self, screen):
        """
        :param screen: self.screen van de menuscreen
        """
        screen.blit(self.current, self.position)
