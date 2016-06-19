
"""
class: InfoBox
"""

import pygame

BACKGROUNDCOLOR = pygame.Color("black")
LINECOLOR = pygame.Color("white")

TEXTOFFSET = 10
COL1, COL2 = 0, 150

FONTCOLOR = pygame.Color("white")
FONT = 'verdana'
FONTSIZE = 12
LINEHEIGHT = 15


class InfoBox(object):
    """
    Waar in het partyscreen alle omschrijvingen worden weergegeven.
    """
    def __init__(self, position, width, height):
        self.surface = pygame.Surface((width, height))
        self.surface = self.surface.convert()
        self.rect = self.surface.get_rect()
        self.rect.topleft = position

        self.subsurf = pygame.Surface((width - TEXTOFFSET*2, height - TEXTOFFSET*2))
        self.subsurf = self.subsurf.convert()
        self.subrect = self.subsurf.get_rect()

        self.font = pygame.font.SysFont(FONT, FONTSIZE)

        self.index = 0

    def render(self, screen, text):
        """
        Teken de labels bovenop de achtergrond. Keuze uit 3 soorten tekst aanlevering.
        :param screen: self.screen van partyscreen
        :param text: de tekst om weer te geven
        """
        self.surface.blit(self.subsurf, (TEXTOFFSET, TEXTOFFSET))
        self.subsurf.fill(BACKGROUNDCOLOR)
        pygame.draw.rect(self.surface, LINECOLOR, self.surface.get_rect(), 1)

        self.index = 0

        # als het tuple is met comma's gescheiden voor een nieuwe regel
        if type(text) == tuple:
            for line in text:
                # Beschouw de door komma gescheiden regels toch als individuele string_text.
                self.string_text(line)

        # als het een list is met paren van tuples
        elif type(text) == list:
            self.tuple_pair_text(text)

        # als het alleen maar text achter elkaar is
        elif type(text) == str:
            self.string_text(text)

        screen.blit(self.surface, self.rect.topleft)

    def tuple_pair_text(self, text):
        """
        :param text:
        """
        for i, line in enumerate(text):
            label1 = self.font.render(line[0], True, FONTCOLOR).convert_alpha()
            label2 = self.font.render(line[1], True, FONTCOLOR).convert_alpha()
            self.subsurf.blit(label1, (COL1, i * LINEHEIGHT))
            self.subsurf.blit(label2, (COL2, i * LINEHEIGHT))

    def string_text(self, text):
        """
        :param text:
        """
        while text:
            chars = 1
            # determine maximum width of line
            while self.font.size(text[:chars])[0] < self.subrect.width and chars < len(text):
                chars += 1
            # if we've wrapped the text, then adjust the wrap to the last word
            if chars < len(text):
                chars = text.rfind(" ", 0, chars) + 1
            label = self.font.render(text[:chars], True, FONTCOLOR).convert_alpha()
            self.subsurf.blit(label, (COL1, self.index * LINEHEIGHT))
            # remove the text we just blitted
            text = text[chars:]
            self.index += 1
