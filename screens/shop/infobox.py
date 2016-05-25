
"""
class: InfoBox
"""

import pygame

COLORKEY = pygame.Color("white")
LINECOLOR = pygame.Color("black")

TEXTOFFSET = 10
COL1, COL2 = 0, 130

FONTCOLOR = pygame.Color("black")
FONT = 'verdana'
FONTSIZE = 14
LINEHEIGHT = 16


class InfoBox(object):
    """
    Waar in het shopscreen alle omschrijvingen worden weergegeven.
    """
    def __init__(self, x, y, width, height):
        self.surface = pygame.Surface((width, height))
        self.surface.set_colorkey(COLORKEY)
        self.surface = self.surface.convert()
        self.rect = self.surface.get_rect()
        self.rect.topleft = x, y

        self.subrect = self.surface.get_rect()
        self.subsurf = pygame.Surface((self.subrect.width, self.subrect.height))
        self.subsurf = self.subsurf.convert()

        self.background = pygame.Surface(self.surface.get_size())
        self.background.fill(COLORKEY)
        self.background = self.background.convert()

        self.font = pygame.font.SysFont(FONT, FONTSIZE)

    def render(self, screen, text):
        """
        Teken de labels bovenop de achtergrond. Keuze uit 3 soorten tekst aanlevering.
        :param screen: self.screen van shopscreen
        :param text: de tekst om weer te geven
        """
        self.surface.blit(self.subsurf, (0, 0))
        self.subsurf.blit(self.background, (0, 0))

        pygame.draw.rect(self.background, LINECOLOR, self.surface.get_rect(), 1)

        # als het tuple is met comma's gescheiden voor een nieuwe regel
        if type(text) == tuple:
            for i, line in enumerate(text):
                label = self.font.render(line, False, FONTCOLOR).convert_alpha()
                self.subsurf.blit(label, (COL1 + TEXTOFFSET, i * LINEHEIGHT + TEXTOFFSET))

        # als het een list is met paren van tuples
        elif type(text) == list:
            for i, line in enumerate(text):
                label1 = self.font.render(line[0], False, FONTCOLOR).convert_alpha()
                label2 = self.font.render(line[1], False, FONTCOLOR).convert_alpha()
                self.subsurf.blit(label1, (COL1 + TEXTOFFSET, i * LINEHEIGHT + TEXTOFFSET))
                self.subsurf.blit(label2, (COL2 + TEXTOFFSET, i * LINEHEIGHT + TEXTOFFSET))

        # als het alleen maar text achter elkaar is
        elif type(text) == str:
            i = 0
            while text:
                chars = 1
                # determine maximum width of line
                while self.font.size(text[:chars])[0] < self.subrect.width and chars < len(text):
                    chars += 1
                # if we've wrapped the text, then adjust the wrap to the last word
                if chars < len(text):
                    chars = text.rfind(" ", 0, chars) + 1
                label = self.font.render(text[:chars], False, FONTCOLOR).convert_alpha()
                self.subsurf.blit(label, (COL1 + TEXTOFFSET, i * LINEHEIGHT + TEXTOFFSET))
                # remove the text we just blitted
                text = text[chars:]
                i += 1

        screen.blit(self.surface, self.rect.topleft)
