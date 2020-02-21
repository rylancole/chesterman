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
            return self.options
        return False

    def createKind(self, piece):
        self.create()
        self.kind = piece.getKind()
        if(self.kind == "King"): self.options = KingOptions(piece)
        elif(self.kind == "Queen"): self.options = QueenOptions(piece)
        elif(self.kind == "Rook"): self.options = RookOptions(piece)
        elif(self.kind == "Knight"): self.options = KnightOptions(piece)
        elif(self.kind == "Bishop"): self.options = BishopOptions(piece)
        elif(self.kind == "Pawn"): self.options = PawnOptions(piece)
        self.update()

    def draw(self, surface):
        surface.blit(self.popupSurf, self.popupRect)

class Options():

    options = []

    def __init__(self, piece):
        pass

    def iter(self):
        return self.options

    def clicked(self, map):
        return {"func": None}


class KingOptions(Options):

    options = [' >Create']

    def __init__(self, piece):
        if(piece.getKind() != "King"):
            return
        self.piece = piece

    def clicked(self, map):
        return {"func": "create"}

class QueenOptions(Options):

    options = []

    def __init__(self, piece):
        if(piece.getKind() != "Queen"):
            return
        self.piece = piece

class RookOptions(Options):

    options = [' >Build']

    def __init__(self, piece):
        if(piece.getKind() != "Rook"):
            return
        self.piece = piece

    def clicked(self, map):
        return {"func": "build"}

class KnightOptions(Options):

    options = [' >Energy']

    def __init__(self, piece):
        if(piece.getKind() != "Knight"):
            return
        self.piece = piece

    def clicked(self, map):
        return {"func": "energy"}

class BishopOptions(Options):

    options = [' >Create']

    def __init__(self, piece):
        if(piece.getKind() != "Bishop"):
            return
        self.piece = piece

    def clicked(self, map):
        return {"func": "create"}

class PawnOptions(Options):

    options = [' >Collect']

    def __init__(self, piece):
        if(piece.getKind() != "Pawn"):
            return
        self.piece = piece

    def clicked(self, map):
        x, y = self.piece.getSquare()
        if(map.isWaterAt(x, y, True) or map.isCastleAt(x, y) or map.isEmptyAt(x, y)):
            return {"func": None}
        block = map.get(x, y)
        return {"func": "collect", "resrc": block}
