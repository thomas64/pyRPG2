
"""
class: Animation
"""

import pygame

PATH = 'resources/backgrounds/titlescreen/'
ANIMATION01 = PATH+'animation01.jpg'
# ANIMATION02 = PATH+'animation02.png'
# ANIMATION03 = PATH+'animation03.png'
# ANIMATION04 = PATH+'animation04.png'
# ANIMATION05 = PATH+'animation05.png'
# ANIMATION06 = PATH+'animation06.png'
# ANIMATION07 = PATH+'animation07.png'
# ANIMATION08 = PATH+'animation08.png'
# ANIMATION09 = PATH+'animation09.png'

ANIMATIONSPEED = 10


# todo, alle animaties uit de dir halen zoals bij audio

class Animation(object):
    """
    De bewegende achtergrond.
    """
    def __init__(self):

        self.speed = 0

        self.animation = {0: pygame.image.load(ANIMATION01).convert()}
                          # 1: pygame.image.load(ANIMATION02).convert_alpha(),
                          # 2: pygame.image.load(ANIMATION03).convert_alpha(),
                          # 3: pygame.image.load(ANIMATION04).convert_alpha(),
                          # 4: pygame.image.load(ANIMATION05).convert_alpha(),
                          # 5: pygame.image.load(ANIMATION06).convert_alpha(),
                          # 6: pygame.image.load(ANIMATION07).convert_alpha(),
                          # 7: pygame.image.load(ANIMATION08).convert_alpha(),
                          # 8: pygame.image.load(ANIMATION09).convert_alpha()}
        self.current = None

        self.width = self.animation[0].get_width()
        self.height = self.animation[0].get_height()
        self.position = (0, 0)

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
