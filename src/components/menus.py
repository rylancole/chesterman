import pygame
import settings

STEP_SIZE = settings.STEP_SIZE
CHUNK_SIZE = settings.CHUNK_SIZE

class Menu:

    options = None
    option_surfs = {}
    doesExist = False
    kind = None

    def __init__(self):
        self.update()

    def update(self):
        self.text_font = pygame.font.Font('freesansbold.ttf',int((3/4)*STEP_SIZE))
        self.popupSurf = pygame.Surface((STEP_SIZE*CHUNK_SIZE*2, STEP_SIZE*CHUNK_SIZE))
        if(self.options):
            i = 0
            for option in self.options.iter():
                textSurf = self.text_font.render(option, True, (255, 255, 255))
                textRect = textSurf.get_rect()
                self.option_surfs[option] = textRect
                textRect.midleft = (0,(i+1)*STEP_SIZE)
                i += 1
                self.popupSurf.blit(textSurf, textRect)
        self.popupRect = self.popupSurf.get_rect()
        self.popupRect.midleft = (1040, 400)

    def create(self):
        self.doesExist = True

    def vanish(self):
        self.doesExist = False

    def exists(self):
        return self.doesExist

    def grabClick(self, x, y):
        if(self.popupRect.collidepoint(x, y)):
            return "yes"
        return "none"

    def createKind(self, kind):
        self.create()
        self.kind = kind
        if(kind == "King"): self.options = KingOptions()
        elif(kind == "Queen"): self.options = QueenOptions()
        elif(kind == "Rook"): self.options = RookOptions()
        elif(kind == "Knight"): self.options = KnightOptions()
        elif(kind == "Bishop"): self.options = BishopOptions()
        elif(kind == "Pawn"): self.options = PawnOptions()
        self.update()

    def draw(self, surface):
        surface.blit(self.popupSurf, self.popupRect)

class Options():

    options = []

    def __init__(self):
        pass

    def iter(self):
        return self.options

    def firstChoice(self):
        pass

    def secondChoice(self):
        pass


class KingOptions(Options):

    options = [' >Create']

    def __init__(self):
        pass

class QueenOptions(Options):

    options = []

    def __init__(self):
        pass

class RookOptions(Options):

    options = [' >Build']

    def __init__(self):
        pass

class KnightOptions(Options):

    options = [' >Energy']

    def __init__(self):
        pass

class BishopOptions(Options):

    options = [' >Create']

    def __init__(self):
        pass

class PawnOptions(Options):

    options = [' >Collect']

    def __init__(self):
        pass
