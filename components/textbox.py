
"""
class: TextBox
"""

import pygame

COLORKEY = pygame.Color("green")
LINECOLOR = pygame.Color("black")

TEXTOFFSETX = 10
TEXTOFFSETY = 8
COL1, COL2 = 0, 150

FONTCOLOR = pygame.Color("black")
FONT = 'verdana'
FONTSIZE = 11
LINEHEIGHT = 13


class TextBox(object):
    """
    Een mogelijkheid om text weer te geven.
    """
    def __init__(self, position, width, height):
        self.surface = pygame.Surface((width, height))
        self.surface.set_colorkey(COLORKEY)
        self.surface.fill(COLORKEY)
        self.surface = self.surface.convert()
        self.rect = self.surface.get_rect()
        self.rect.topleft = position

        self.subsurf = pygame.Surface((width - TEXTOFFSETX*2, height - TEXTOFFSETY*2))
        self.subsurf = self.subsurf.convert()
        self.subrect = self.subsurf.get_rect()

        self.background = pygame.Surface(self.surface.get_size())
        self.background.fill(COLORKEY)
        self.background = self.background.convert()

        self.index = 0

        # het rijtje hieronder overnemen voor een subclass als je het anders wil hebben dan de standaard waarden.
        self.font = pygame.font.SysFont(FONT, FONTSIZE)
        self.fontcolor = FONTCOLOR
        self.lineheight = LINEHEIGHT
        self.linecolor = LINECOLOR
        self.col1 = COL1
        self.col2 = COL2

    def render(self, screen, text):
        """
        Teken de labels bovenop de subsurf. Keuze uit 3 soorten tekst aanlevering.
        :param screen: self.screen van partyscreen
        :param text: de tekst om weer te geven
        """
        self.surface.blit(self.subsurf, (TEXTOFFSETX, TEXTOFFSETY))
        self.subsurf.blit(self.background, (0, 0))
        pygame.draw.rect(self.surface, self.linecolor, self.surface.get_rect(), 1)

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
        De AA staat op False omdat anders de colorkey doorkomt.
        :param text:
        """
        for i, line in enumerate(text):
            label1 = self.font.render(line[0], False, self.fontcolor).convert_alpha()
            label2 = self.font.render(line[1], False, self.fontcolor).convert_alpha()
            self.subsurf.blit(label1, (self.col1, i * self.lineheight))
            self.subsurf.blit(label2, (self.col2, i * self.lineheight))

    def string_text(self, text):
        """
        De AA staat op False omdat anders de colorkey doorkomt.
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
            label = self.font.render(text[:chars], False, self.fontcolor).convert_alpha()
            self.subsurf.blit(label, (self.col1, self.index * self.lineheight))
            # remove the text we just blitted
            text = text[chars:]
            self.index += 1
