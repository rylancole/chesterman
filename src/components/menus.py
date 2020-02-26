import pygame
import settings

STEP_SIZE = settings.STEP_SIZE
CHUNK_SIZE = settings.CHUNK_SIZE

COST_DICT = settings.COST_DICT
GOLD_WORTH = settings.GOLD_WORTH

class Menu:

    options = None
    option_surfs = {}
    doesExist = False
    kind = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.update()

    def update(self):
        self.text_font = pygame.font.Font('freesansbold.ttf',int((3/4)*STEP_SIZE))
        self.popupSurf = pygame.Surface((STEP_SIZE*CHUNK_SIZE*3, STEP_SIZE*CHUNK_SIZE*2))
        if(self.options):
            i = 0
            self.option_surfs = {}
            for option in self.options.iter():
                s = " >"+self.options.stringify(option)
                textSurf = self.text_font.render(s, True, (255, 255, 255))
                textRect = textSurf.get_rect()
                self.option_surfs[option] = textRect
                textRect.midleft = (0,(i+1)*STEP_SIZE)
                i += 1
                self.popupSurf.blit(textSurf, textRect)
        self.popupRect = self.popupSurf.get_rect()
        self.popupRect.midleft = (self.x, self.y)

    def create(self):
        self.doesExist = True

    def vanish(self):
        self.doesExist = False

    def exists(self):
        return self.doesExist

    def optionClick(self, x, y):
        for key in self.option_surfs:
            if(self.option_surfs[key].collidepoint(x, y)):
                self.options.selected_option = key

    def grabClick(self, x, y):
        if(self.popupRect.collidepoint(x, y)):
            if(self.options.size() > 1):
                self.optionClick(x-1040, y-(400-STEP_SIZE*CHUNK_SIZE))
            return self.options
        return False

    def createEndMenu(self):
        self.create()
        self.options = EndOptions()
        self.update()

    def createExButton(self):
        self.create()
        self.options = ExButton()
        self.update()

    def createExMenu(self):
        self.create()
        self.options = ExMenu()
        self.update()

    def createPrompt(self, string):
        self.create()
        self.options = Prompt(string)
        self.update()

    def changePrompt(self, string):
        self.options.changePrompt(string)
        self.update()

    def addPrompt(self, string):
        self.options.addPrompt(string)
        self.update()

    def isPrompt(self):
        return self.options.getKind() == "Prompt"

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
    costs = COST_DICT

    def __init__(self, piece):
        if(piece.getKind() != self.kind):
            return
        self.piece = piece

    def iter(self):
        return self.options

    def stringify(self, option):
        return option

    def size(self):
        return len(self.options)

    def getKind(self):
        return self.kind

    def clicked(self, map):
        return {"func": None}


class KingOptions(Options):

    options = ['Queen', 'Rook', 'Bishop', 'Knight', 'Pawn']
    selected_option = None
    kind = "King"

    def clicked(self, map):
        return {
            "func": "create",
            "choice": self.selected_option,
            "cost": self.costs[self.selected_option]
            }

    def stringify(self, option):
        cost = self.costs[option]
        return option+" for "+str(cost[0])+" "+cost[1]

class QueenOptions(Options):

    options = []
    kind = "Queen"

class RookOptions(Options):

    options = []
    kind = "Rook"

class KnightOptions(Options):

    options = []
    kind = "Knight"

class BishopOptions(Options):

    options = ['Knight', 'Pawn']
    selected_option = None
    use_cost = True
    kind = "Bishop"

    def clicked(self, map):
        return {
            "func": "create",
            "choice": self.selected_option,
            "cost": self.costs[self.selected_option]-1
            }

    def stringify(self, option):
        cost = self.costs[option]
        return option+" for "+str(cost[0]-1)+" "+cost[1]

class PawnOptions(Options):

    options = ['Collect']
    kind = "Pawn"

    def clicked(self, map):
        x, y = self.piece.getSquare()
        # returning the wrong thing here
        if(map.isWaterAt(x, y, True) or map.isCastleAt(x, y) or map.isEmptyAt(x, y)):
            return {"func": None}
        block = map.get(x, y, True)
        return {"func": "collect", "resrc": block}

class EndOptions(Options):

    options = ['End Turn']
    kind = "End"

    def __init__(self):
        pass

    def clicked(self, string):
        return {"func": "end"}

class ExMenu(Options):

    options = ['hay', 'stone', 'crop', 'gold']
    kind = "Exchange"

    def __init__(self):
        pass

    def stringify(self, option):
        if(option == 'gold'):
            return '5 gold -> '+str(GOLD_WORTH)+' pnts'
        return '5 '+option+' -> 1 gold'

    def clicked(self, string):
        return {
            "func": "exchange",
            "choice": self.selected_option
        }

class ExButton(Options):

    options = ['Exchange']
    kind = "ExButton"

    def __init__(self):
        pass

    def clicked(self, string):
        return {"func": "exchange"}


class Prompt(Options):

    options = ['']
    kind = "Prompt"

    def __init__(self, string):
        self.options[0] = string

    def changePrompt(self, string):
        self.options = [string]

    def addPrompt(self, string):
        self.options.append(string)
