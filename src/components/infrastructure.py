import pygame
import settings

settings.init()
STEP_SIZE = settings.STEP_SIZE
CHUNK_SIZE = settings.CHUNK_SIZE
WIDTH = settings.WIDTH

class Board:

    dict_list = []

    h = 0

    def __init__(self, height):
        self.text_font = pygame.font.Font('freesansbold.ttf',int((3/4)*STEP_SIZE))
        self.h = height

        self.dict["black"] = {}
        self.dict["white"] = {}

        for key in self.dict_list:
            self.dict["black"][key] = 0
            self.dict["white"][key] = 0

    def text_objects(self, text, font, midleft):
        textSurface = font.render(text, True, (255,255,255))
        textRect = textSurface.get_rect()
        textRect.midleft = midleft
        return textSurface, textRect

    def get(self, team, resrc):
        return self.dict[team][resrc]

    def increaseResource(self, team, resrc, amt):
        self.dict[team][resrc] += amt

    def draw(self, surface):
        x_inc = STEP_SIZE*CHUNK_SIZE
        x = x_inc*WIDTH

        for color_key in self.dict:
            y = STEP_SIZE*(CHUNK_SIZE+self.h)+STEP_SIZE
            for resrc_key in self.dict[color_key]:
                s, r = self.text_objects("  "+resrc_key.capitalize()+": "+str(self.dict[color_key][resrc_key]), self.text_font, (x,y))
                surface.blit(s, r)
                y += STEP_SIZE
            x += x_inc

class Scoreboard(Board):

    dict_list = [
        "chk", "col", "cap", "tot"
    ]
    dict = {}

    def increaseCheckPoints(self, team, chk):
        self.dict[team]["chk"] += chk
        self.updateTotal(team)

    def increaseCapturePoints(self, team, cap):
        self.dict[team]["cap"] += cap
        self.updateTotal(team)

    def increaseCollectionPoints(self, team, col):
        self.dict[team]["col"] += col
        self.updateTotal(team)

    def updateTotal(self, team):
        self.dict[team]["tot"] = self.dict[team]["chk"] + self.dict[team]["col"] + self.dict[team]["cap"]

    def getWinner(self):
        for team in self.dict:
            if(self.dict[team]["chk"]>=250
                or self.dict[team]["cap"]>=250
                    or self.dict[team]["col"]>=250
                        or self.dict[team]["tot"]>=600):
                return team
        return None

class ResourceBoard(Board):

    dict_list = [
        "hay", "crop", "lumber", "stone", "gold"
    ]
    dict = {}

class Map:

    matrix = []
    castle_code = {
        "white": 'a',
        "black": 'b'
    }

    def __init__(self):
        self.h = 0
        self.w = 0

    def decompress(self, f):
        '''
        Convert text file encoded to represent map
        w = water
        s = stone
        f = field
        c = crop
        l = lumber
        e = empty
        t = castle
        '''
        i = 0
        for line in f:
            self.matrix.append([])
            for c in line:
                if(c != "\n"):
                    self.matrix[i].append(c)
            i += 1
        self.h = len(self.matrix)
        if(self.h > 0):
            self.w = len(self.matrix[0])
        else:
            self.w = 0

    def get(self, x, y, needFullWord=False):
        '''
        Return character in at (x, y)
        '''
        if(not needFullWord):
            return self.matrix[y][x]

        dict = {
            "s": "stone",
            "f": "hay",
            "c": "crop",
            "l": "lumber",
            "w": "water",
            "a": "castle",
            "b": "castle",
            "e": "empty"
        }

        return dict[self.matrix[y][x]]

    def has(self, x, y, inSquares=False):
        if(not inSquares):
            x = int(x/STEP_SIZE) #convert coords to units [Squares]
            y = int(y/STEP_SIZE)

        return x < self.w and y < self.h

    def putCastle(self, team, x, y):
        '''
        Initialiaze 4x4 castle at point in units [Squares]
        '''

        for i in range(x, x+4):
            for j in range(y, y+4):
                self.matrix[j][i] = self.castle_code[team]

    def isCastleAt(self, x, y):
        '''
        Return true if square on castle grounds
        Takes in coords in units [Squares]
        '''

        if(self.isWaterAt(x*STEP_SIZE, y*STEP_SIZE)):
            return False
        else:
            return self.matrix[y][x] == "a" or self.matrix[y][x] == "b"

    def isColorCastleAt(self, team, x, y):
        '''
        Return true if square on castle grounds
        Takes in coords in units [Squares]
        '''

        if(self.isWaterAt(x*STEP_SIZE, y*STEP_SIZE)):
            return False
        else:
            return self.matrix[y][x] == self.castle_code[team]

    def isEmptyAt(self, x, y):
        '''
        Return true if square on castle grounds
        Takes in coords in units [Squares]
        '''

        if(self.isWaterAt(x*STEP_SIZE, y*STEP_SIZE)):
            return False
        else:
            return self.matrix[y][x] == "e"

    def isWaterAt(self, x, y, inSquares=False):
        '''
        Return true for collision with water or end of map
        Takes in coords in units [SQpixels]
        '''
        if(not inSquares):
            x = int(x/STEP_SIZE) #convert coords to units [Squares]
            y = int(y/STEP_SIZE)
        if(y >= len(self.matrix)): return True
        if(x >= len(self.matrix[y])): return True
        return self.matrix[y][x] == "w"

    def toString(self):
        ret_string = ""
        for row in self.matrix:
            for c in row:
                ret_string += c
            ret_string += "\n"

        return ret_string

class Castle:

    piece_name = "Castle"
    _image_path = "sprites/_castle_80x80.png"

    def __init__(self, x, y):
       self.x = x*STEP_SIZE
       self.y = y*STEP_SIZE
       self._image_surf = pygame.image.load(self._image_path).convert()

    def draw(self, surface):
        surface.blit(self._image_surf,(self.x,self.y))

    def get_pos(self):
        return (self.x, self.y)

    def toString(self):
        return self.piece_name+"@"+str(self.get_pos())
