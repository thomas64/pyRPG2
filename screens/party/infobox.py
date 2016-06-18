
"""
class: InfoBox
"""

import pygame

BACKGROUNDCOLOR = pygame.Color("black")
LINECOLOR = pygame.Color("white")

TEXTX, TEXTY = -20, -20     # positie van de tekst in de box. -20 betekent +10. -30 zou +15 betekenen.
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

        self.subrect = self.rect.inflate(TEXTX, TEXTY)
        self.subsurf = pygame.Surface((self.subrect.width, self.subrect.height))
        self.subsurf = self.subsurf.convert()

        self.background = pygame.Surface(self.surface.get_size())
        self.background.fill(BACKGROUNDCOLOR)
        self.background = self.background.convert()

        self.font = pygame.font.SysFont(FONT, FONTSIZE)

    def render(self, screen, text):
        """
        Teken de labels bovenop de achtergrond. Keuze uit 3 soorten tekst aanlevering.
        :param screen: self.screen van partyscreen
        :param text: de tekst om weer te geven
        """
        self.surface.blit(self.background, (0, 0))
        pygame.draw.rect(self.background, LINECOLOR, self.surface.get_rect(), 1)
        screen.blit(self.surface, self.rect.topleft)
        self.subsurf.fill(BACKGROUNDCOLOR)

        # als het tuple is met comma's gescheiden voor een nieuwe regel
        if type(text) == tuple:
            for i, line in enumerate(text):
                label = self.font.render(line, True, FONTCOLOR).convert_alpha()
                self.subsurf.blit(label, (COL1, i * LINEHEIGHT))

        # als het een list is met paren van tuples
        elif type(text) == list:
            for i, line in enumerate(text):
                label1 = self.font.render(line[0], True, FONTCOLOR).convert_alpha()
                label2 = self.font.render(line[1], True, FONTCOLOR).convert_alpha()
                self.subsurf.blit(label1, (COL1, i * LINEHEIGHT))
                self.subsurf.blit(label2, (COL2, i * LINEHEIGHT))

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
                label = self.font.render(text[:chars], True, FONTCOLOR).convert_alpha()
                self.subsurf.blit(label, (COL1, i * LINEHEIGHT))
                # remove the text we just blitted
                text = text[chars:]
                i += 1

        screen.blit(self.subsurf, self.subrect.topleft)
