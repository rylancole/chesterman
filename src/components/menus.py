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
                self.optionClick(x-self.x, y-(self.y-STEP_SIZE*CHUNK_SIZE))
            return self.options
        return False

    def createEndMenu(self):
        self.create()
        self.options = EndOptions()
        self.update()

    def createExButton(self, can_coll):
        self.create()
        self.options = ExButton(can_coll)
        self.update()

    def createExMenu(self):
        self.create()
        self.options = ExMenu()
        self.update()

    def createCollectMenu(self, amount_of):
        self.create()
        self.options = CollectMenu(amount_of)
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
        return self.options.getKind() == "prompt"

    def createKind(self, piece):
        self.create()
        self.kind = piece.getKind()
        if(self.kind == "king"): self.options = KingOptions(piece)
        elif(self.kind == "queen"): self.options = QueenOptions(piece)
        elif(self.kind == "rook"): self.options = RookOptions(piece)
        elif(self.kind == "knight"): self.options = KnightOptions(piece)
        elif(self.kind == "bishop"): self.options = BishopOptions(piece)
        elif(self.kind == "pawn"): self.options = PawnOptions(piece)
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
        return option.capitalize()

    def size(self):
        return len(self.options)

    def getKind(self):
        return self.kind

    def clicked(self, map):
        return {"func": None}


class KingOptions(Options):

    options = ['queen', 'rook', 'bishop', 'knight', 'pawn']
    selected_option = None
    kind = "king"

    def clicked(self, map):
        if(self.selected_option == None):
            return None
        return {
            "func": "create",
            "choice": self.selected_option,
            "cost": self.costs[self.selected_option]
            }

    def stringify(self, option):
        cost = self.costs[option]
        return option.capitalize()+" for "+str(cost[0])+" "+cost[1]

class QueenOptions(Options):

    options = []
    kind = "queen"

class RookOptions(Options):

    options = ["wall", "port"]
    selected_option = None
    kind = "rook"

    def stringify(self, option):
        cost = self.costs[option]
        return "Build "+option+" for "+str(cost[0])+" "+cost[1]

    def clicked(self, map):
        if(self.selected_option == None):
            return None
        return {
            "func": "create",
            "choice": self.selected_option,
            "cost": self.costs[self.selected_option]
            }

class KnightOptions(Options):

    options = []
    kind = "knight"

class BishopOptions(Options):

    options = ['knight', 'pawn']
    selected_option = None
    use_cost = True
    kind = "bishop"

    def clicked(self, map):
        if(self.selected_option == None):
            return None
        return {
            "func": "create",
            "choice": self.selected_option,
            "cost": (self.costs[self.selected_option][0]-1, self.costs[self.selected_option][1])
            }

    def stringify(self, option):
        cost = self.costs[option]
        return option.capitalize()+" for "+str(cost[0]-1)+" "+cost[1]

class PawnOptions(Options):

    options = []
    kind = "pawn"

class EndOptions(Options):

    options = ['end']
    kind = "End"

    def __init__(self):
        pass

    def stringify(self, option):
        return option.capitalize()+" Turn"

    def clicked(self, string):
        return {"func": "end"}

class ExMenu(Options):

    options = ['hay', 'stone', 'lumber', 'crop', 'gold']
    selected_option = None
    kind = "exchange"

    def __init__(self):
        pass

    def stringify(self, option):
        if(option == 'gold'):
            return '5 gold -> '+str(GOLD_WORTH)+' pnts'
        return '5 '+option+' -> 1 gold'

    def clicked(self, string):
        if(self.selected_option == None):
            return None
        return {
            "func": "exchange",
            "choice": self.selected_option
        }

class CollectMenu(Options):

    selected_option = None
    kind = "collect"

    def __init__(self, amount_of):
        self.amount_of = amount_of
        self.options = []
        for key in amount_of:
            if(amount_of[key] > 0):
                self.options.append(key)

    def stringify(self, option):
        return 'Collect '+str(self.amount_of[option])+" "+option

    def clicked(self, string):
        if(self.selected_option): ret_option = self.selected_option
        elif(len(self.options) > 0): ret_option = self.options[0]
        else: return None
        return {
            "func": "collect",
            "resrc": ret_option,
            "amount": self.amount_of[ret_option]
        }

class ExButton(Options):

    options = ['exchange', 'collect']
    selected_option = None
    kind = "ExButton"

    def __init__(self, can_coll):
        if(can_coll): self.options = ['exchange', 'collect']
        else: self.options = ['exchange', 'no collect']

    def clicked(self, string):
        return {"func": self.selected_option}


class Prompt(Options):

    options = ['']
    kind = "prompt"

    def __init__(self, string):
        self.options[0] = string

    def stringify(self, option):
        return option

    def changePrompt(self, string):
        self.options = [string]

    def addPrompt(self, string):
        self.options.append(string)
