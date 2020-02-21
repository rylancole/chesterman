import pygame
import settings

settings.init()
STEP_SIZE = settings.STEP_SIZE
CHUNK_SIZE = settings.CHUNK_SIZE
WIDTH = settings.WIDTH

class Scoreboard:

    b_chk = 0
    b_cap = 0
    b_col = 0
    b_tot = 0

    w_chk = 0
    w_cap = 0
    w_col = 0
    w_tot = 0

    def __init__(self):
        self.text_font = pygame.font.Font('freesansbold.ttf',int((3/4)*STEP_SIZE))
        x_inc = STEP_SIZE*CHUNK_SIZE
        x = x_inc*WIDTH
        y = STEP_SIZE*(CHUNK_SIZE+1)

        self._black_label_surf, self._black_label_rect = self.text_objects("BLACK", self.text_font)
        self._black_label_rect.midleft = (x,y)

        self._white_label_surf, self._white_label_rect = self.text_objects("WHITE", self.text_font)
        self._white_label_rect.midleft = (x+x_inc,y)

    def text_objects(self, text, font):
        textSurface = font.render(text, True, (255,255,255))
        return textSurface, textSurface.get_rect()

    def increaseCheckPoints(self, team, chk):
        if(team == "white"): self.w_chk += chk
        elif(team == "black"): self.b_chk += chk

    def increaseCapturePoints(self, team, cap):
        if(team == "white"): self.w_cap += cap
        elif(team == "black"): self.b_cap += cap

    def increaseCollectionPoints(self, team, col):
        if(team == "white"): self.w_col += col
        elif(team == "black"): self.b_col += col

    def update(self):
        self.b_tot = self.b_chk + self.b_cap + self.b_col
        self.w_tot = self.w_chk + self.w_cap + self.w_col

        x_inc = STEP_SIZE*CHUNK_SIZE
        x = x_inc*WIDTH
        y = STEP_SIZE*(CHUNK_SIZE+1)+STEP_SIZE

        self._b_chk_surf, self._b_chk_rect = self.text_objects("  Chk: "+str(self.b_chk), self.text_font)
        self._b_chk_rect.midleft = (x,y)
        self._w_chk_surf, self._w_chk_rect = self.text_objects("  Chk: "+str(self.w_chk), self.text_font)
        self._w_chk_rect.midleft = (x+x_inc,y)
        y += STEP_SIZE

        self._b_cap_surf, self._b_cap_rect = self.text_objects("  Cap: "+str(self.b_cap), self.text_font)
        self._b_cap_rect.midleft = (x,y)
        self._w_cap_surf, self._w_cap_rect = self.text_objects("  Cap: "+str(self.w_cap), self.text_font)
        self._w_cap_rect.midleft = (x+x_inc,y)
        y += STEP_SIZE

        self._b_col_surf, self._b_col_rect = self.text_objects("  Coll: "+str(self.b_col), self.text_font)
        self._b_col_rect.midleft = (x,y)
        self._w_col_surf, self._w_col_rect = self.text_objects("  Coll: "+str(self.w_col), self.text_font)
        self._w_col_rect.midleft = (x+x_inc,y)
        y += STEP_SIZE

        self._b_tot_surf, self._b_tot_rect = self.text_objects("  Total: "+str(self.b_tot), self.text_font)
        self._b_tot_rect.midleft = (x,y)
        self._w_tot_surf, self._w_tot_rect = self.text_objects("  Total: "+str(self.w_tot), self.text_font)
        self._w_tot_rect.midleft = (x+x_inc,y)

    def draw(self, surface):
        self.update()

        surface.blit(self._black_label_surf, self._black_label_rect)
        surface.blit(self._b_chk_surf, self._b_chk_rect)
        surface.blit(self._b_cap_surf, self._b_cap_rect)
        surface.blit(self._b_col_surf, self._b_col_rect)
        surface.blit(self._b_tot_surf, self._b_tot_rect)

        surface.blit(self._white_label_surf, self._white_label_rect)
        surface.blit(self._w_chk_surf, self._w_chk_rect)
        surface.blit(self._w_cap_surf, self._w_cap_rect)
        surface.blit(self._w_col_surf, self._w_col_rect)
        surface.blit(self._w_tot_surf, self._w_tot_rect)

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

    def get(self, x, y):
        '''
        Return character in at (x, y)
        '''
        return self.matrix[y][x]

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
