
"""
class: InfoBox
"""

import pygame

BACKGROUNDCOLOR = pygame.Color("black")
LINECOLOR = pygame.Color("white")

BOXWIDTH = 405
BOXHEIGHT = 160
TEXTX, TEXTY = -20, -20
COL2 = 150

FONTCOLOR = pygame.Color("white")
FONT = 'verdana'
FONTSIZE = 12
LINEHEIGHT = 18


class InfoBox(object):
    """
    Waar in het partyscreen alle omschrijvingen worden weergegeven.
    """
    def __init__(self, position):
        self.surface = pygame.Surface((BOXWIDTH, BOXHEIGHT))
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

    def draw(self, screen, text):
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
                self.subsurf.blit(label, (0, i * LINEHEIGHT))
            screen.blit(self.subsurf, self.subrect.topleft)

        # als het een list is met paren van tuples
        elif type(text) == list:
            for i, line in enumerate(text):
                label1 = self.font.render(line[0], True, FONTCOLOR).convert_alpha()
                label2 = self.font.render(line[1], True, FONTCOLOR).convert_alpha()
                self.subsurf.blit(label1, (0, i * LINEHEIGHT))
                self.subsurf.blit(label2, (COL2, i * LINEHEIGHT))
            screen.blit(self.subsurf, self.subrect.topleft)

        # als het alleen maar text achter elkaar is
        elif type(text) == str:
            # draw some text into an area of a surface,
            # automatically wraps words,
            # returns any text that didn't get blitted
            y = self.subrect.top
            # get the height of the font
            font_height = self.font.size("Tg")[1]
            while text:
                i = 1
                # determine if the row of text will be outside our area
                if y + font_height > self.subrect.bottom:
                    break
                # determine maximum width of line
                while self.font.size(text[:i])[0] < self.subrect.width and i < len(text):
                    i += 1
                # if we've wrapped the text, then adjust the wrap to the last word
                if i < len(text):
                    i = text.rfind(" ", 0, i) + 1
                label = self.font.render(text[:i], True, FONTCOLOR).convert_alpha()
                screen.blit(label, (self.subrect.left, y))
                y += font_height
                # remove the text we just blitted
                text = text[i:]
            return text
