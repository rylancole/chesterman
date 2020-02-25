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

    def increaseResource(self, team, resrc, amt):
        self.dict[team][resrc] += amt

    def draw(self, surface):
        x_inc = STEP_SIZE*CHUNK_SIZE
        x = x_inc*WIDTH

        for color_key in self.dict:
            y = STEP_SIZE*(CHUNK_SIZE+self.h)+STEP_SIZE
            for resrc_key in self.dict[color_key]:
                s, r = self.text_objects("  "+resrc_key+": "+str(self.dict[color_key][resrc_key]), self.text_font, (x,y))
                surface.blit(s, r)
                y += STEP_SIZE
            x += x_inc

class Scoreboard(Board):

    dict_list = [
        "Chk", "Col", "Cap", "Tot"
    ]
    dict = {}

    def increaseCheckPoints(self, team, chk):
        self.dict[team]["Chk"] += chk
        self.updateTotal(team)

    def increaseCapturePoints(self, team, cap):
        self.dict[team]["Cap"] += cap
        self.updateTotal(team)

    def increaseCollectionPoints(self, team, col):
        self.dict[team]["Col"] += col
        self.updateTotal(team)

    def updateTotal(self, team):
        self.dict[team]["Tot"] = self.dict[team]["Chk"] + self.dict[team]["Col"] + self.dict[team]["Cap"]

class ResourceBoard(Board):

    dict_list = [
        "Hay", "Crop", "Stone", "Gold"
    ]
    dict = {}

class Map:

    matrix = []

    def __init__(self):
        pass

    def decompress(self, f):
        '''
        Convert text file encoded to represent map
        w = water
        s = stone
        f = field
        c = crop
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

    def get(self, x, y, needFullWord=False):
        '''
        Return character in at (x, y)
        '''
        if(not needFullWord):
            return self.matrix[y][x]

        dict = {
            "s": "Stone",
            "f": "Hay",
            "c": "Crop"
        }

        return dict[self.matrix[y][x]]

    def putCastle(self, x, y):
        '''
        Initialiaze 4x4 castle at point in units [Squares]
        '''
        for i in range(x, x+4):
            for j in range(y, y+4):
                self.matrix[j][i] = "t"

    def isCastleAt(self, x, y):
        '''
        Return true if square on castle grounds
        Takes in coords in units [Squares]
        '''

        if(self.isWaterAt(x*STEP_SIZE, y*STEP_SIZE)):
            return False
        else:
            return self.matrix[y][x] == "t"

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
