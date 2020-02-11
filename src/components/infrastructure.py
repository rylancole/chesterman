import pygame
import settings

settings.init()
STEP_SIZE = settings.STEP_SIZE

class Map:

    matrix = []

    def __init__(self):
        pass

    def decompress(self, f):
        i = 0
        for line in f:
            self.matrix.append([])
            for c in line:
                if(c != "\n"):
                    self.matrix[i].append(c)
            i += 1

    def get(self, x, y):
        return self.matrix[y][x]

    def isWaterAt(self, x, y):
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

    def __init__(self, x, y):
       self.x = x*STEP_SIZE
       self.y = y*STEP_SIZE
       self._image_surf = pygame.image.load("sprites/_castle_80x80.png").convert()

    def draw(self, surface):
        surface.blit(self._image_surf,(self.x,self.y))

    def get_pos(self):
        return (self.x, self.y)

    def toString(self):
        return "Castle@"+str(self.get_pos())
