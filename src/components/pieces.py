import pygame
import settings

settings.init()
STEP_SIZE = settings.STEP_SIZE

direction_dict = {
    "east": (STEP_SIZE, 0),
    "west": (-STEP_SIZE, 0),
    "south": (0, STEP_SIZE),
    "north": (0, -STEP_SIZE),
    "northeast": (STEP_SIZE, -STEP_SIZE),
    "northwest": (-STEP_SIZE, -STEP_SIZE),
    "southeast": (STEP_SIZE, STEP_SIZE),
    "southwest": (-STEP_SIZE, STEP_SIZE)
}


class King:

    def __init__(self, team, x, y):
       self.x = x*STEP_SIZE
       self.y = y*STEP_SIZE
       self.team = team
       if(team == "white"):
           self._image_surf = pygame.image.load("sprites/white_king_20x20.png").convert()
       elif(team == "black"):
           self._image_surf = pygame.image.load("sprites/black_king_20x20.png").convert()

    def draw(self, surface):
        surface.blit(self._image_surf,(self.x,self.y))

    def movesInDirection(self, direction, map, pieces, limit=100):
        moves = []
        inc_i, inc_j = direction_dict[direction]
        i = inc_i
        j = inc_j
        count = 0
        break_out = False
        while(count < limit and not map.isWaterAt(int((self.x+i)/STEP_SIZE), int((self.y+j)/STEP_SIZE))):
            for piece in pieces:
                if piece.get_pos() == (self.x+i, self.y+j):
                    break_out = True
            if(break_out): break
            moves.append((self.x+i, self.y+j))
            i += inc_i
            j += inc_j
            count += 1

        return moves

    def avaliableMoves(self, pieces, map):
        moves = []

        moves.extend(self.movesInDirection("east", map, pieces, 1))
        moves.extend(self.movesInDirection("west", map, pieces, 1))
        moves.extend(self.movesInDirection("north", map, pieces, 1))
        moves.extend(self.movesInDirection("south", map, pieces, 1))
        moves.extend(self.movesInDirection("northeast", map, pieces, 1))
        moves.extend(self.movesInDirection("northwest", map, pieces, 1))
        moves.extend(self.movesInDirection("southeast", map, pieces, 1))
        moves.extend(self.movesInDirection("southwest", map, pieces, 1))

        return moves

    def moveTo(self, coord):
        self.x = coord[0]
        self.y = coord[1]

    def get_pos(self):
        return (self.x, self.y)

    def toString(self):
        return "King@"+str(self.get_pos())

class Queen:

    def __init__(self, team, x, y):
       self.x = x*STEP_SIZE
       self.y = y*STEP_SIZE
       self.team = team
       if(team == "white"):
           self._image_surf = pygame.image.load("sprites/white_queen_20x20.png").convert()
       elif(team == "black"):
           self._image_surf = pygame.image.load("sprites/black_queen_20x20.png").convert()

    def draw(self, surface):
        surface.blit(self._image_surf,(self.x,self.y))

    def movesInDirection(self, direction, map, pieces):
        moves = []
        inc_i, inc_j = direction_dict[direction]
        i = inc_i
        j = inc_j
        break_out = False
        while(not map.isWaterAt(int((self.x+i)/STEP_SIZE), int((self.y+j)/STEP_SIZE))):
            for piece in pieces:
                if piece.get_pos() == (self.x+i, self.y+j):
                    break_out = True
            if(break_out): break
            moves.append((self.x+i, self.y+j))
            i += inc_i
            j += inc_j

        return moves

    def avaliableMoves(self, pieces, map):
        moves = []

        moves.extend(self.movesInDirection("east", map, pieces))
        moves.extend(self.movesInDirection("west", map, pieces))
        moves.extend(self.movesInDirection("north", map, pieces))
        moves.extend(self.movesInDirection("south", map, pieces))
        moves.extend(self.movesInDirection("northeast", map, pieces))
        moves.extend(self.movesInDirection("northwest", map, pieces))
        moves.extend(self.movesInDirection("southeast", map, pieces))
        moves.extend(self.movesInDirection("southwest", map, pieces))

        return moves

    def moveTo(self, coord):
        self.x = coord[0]
        self.y = coord[1]

    def get_pos(self):
        return (self.x, self.y)

    def toString(self):
        return "Queen@"+str(self.get_pos())

class Rook:

    def __init__(self, team, x, y):
       self.x = x*STEP_SIZE
       self.y = y*STEP_SIZE
       self.team = team
       if(team == "white"):
           self._image_surf = pygame.image.load("sprites/white_rook_20x20.png").convert()
       elif(team == "black"):
           self._image_surf = pygame.image.load("sprites/black_rook_20x20.png").convert()

    def draw(self, surface):
        surface.blit(self._image_surf,(self.x,self.y))

    def movesInDirection(self, direction, map, pieces):
        moves = []
        inc_i, inc_j = direction_dict[direction]
        i = inc_i
        j = inc_j
        break_out = False
        while(not map.isWaterAt(int((self.x+i)/STEP_SIZE), int((self.y+j)/STEP_SIZE))):
            for piece in pieces:
                if piece.get_pos() == (self.x+i, self.y+j):
                    break_out = True
            if(break_out): break
            moves.append((self.x+i, self.y+j))
            i += inc_i
            j += inc_j

        return moves


    def avaliableMoves(self, pieces, map):
        moves = []

        moves.extend(self.movesInDirection("east", map, pieces))
        moves.extend(self.movesInDirection("west", map, pieces))
        moves.extend(self.movesInDirection("north", map, pieces))
        moves.extend(self.movesInDirection("south", map, pieces))

        return moves

    def moveTo(self, coord):
        self.x = coord[0]
        self.y = coord[1]

    def get_pos(self):
        return (self.x, self.y)

    def toString(self):
        return "Rook@"+str(self.get_pos())

class Knight:

    def __init__(self, team, x, y):
       self.x = x*STEP_SIZE
       self.y = y*STEP_SIZE
       self.team = team
       if(team == "white"):
           self._image_surf = pygame.image.load("sprites/white_knight_20x20.png").convert()
       elif(team == "black"):
           self._image_surf = pygame.image.load("sprites/black_knight_20x20.png").convert()

    def draw(self, surface):
        surface.blit(self._image_surf,(self.x,self.y))

    def avaliableMoves(self, pieces, map):
        s = STEP_SIZE
        ss = STEP_SIZE*2

        moves = []
        moves.append((self.x-s, self.y+ss))
        moves.append((self.x+s, self.y+ss))

        moves.append((self.x-s, self.y-ss))
        moves.append((self.x+s, self.y-ss))

        moves.append((self.x+ss, self.y-s))
        moves.append((self.x+ss, self.y+s))

        moves.append((self.x-ss, self.y-s))
        moves.append((self.x-ss, self.y+s))
        return moves

    def moveTo(self, coord):
        self.x = coord[0]
        self.y = coord[1]

    def get_pos(self):
        return (self.x, self.y)

    def toString(self):
        return "Knight@"+str(self.get_pos())

class Bishop:

    def __init__(self, team, x, y):
       self.x = x*STEP_SIZE
       self.y = y*STEP_SIZE
       self.team = team
       if(team == "white"):
           self._image_surf = pygame.image.load("sprites/white_bishop_20x20.png").convert()
       elif(team == "black"):
           self._image_surf = pygame.image.load("sprites/black_bishop_20x20.png").convert()

    def draw(self, surface):
        surface.blit(self._image_surf,(self.x,self.y))

    def movesInDirection(self, direction, map, pieces):
        moves = []
        inc_i, inc_j = direction_dict[direction]
        i = inc_i
        j = inc_j
        break_out = False
        while(not map.isWaterAt(int((self.x+i)/STEP_SIZE), int((self.y+j)/STEP_SIZE))):
            for piece in pieces:
                if piece.get_pos() == (self.x+i, self.y+j):
                    break_out = True
            if(break_out): break
            moves.append((self.x+i, self.y+j))
            i += inc_i
            j += inc_j

        return moves


    def avaliableMoves(self, pieces, map):
        moves = []

        moves.extend(self.movesInDirection("northeast", map, pieces))
        moves.extend(self.movesInDirection("northwest", map, pieces))
        moves.extend(self.movesInDirection("southeast", map, pieces))
        moves.extend(self.movesInDirection("southwest", map, pieces))

        return moves

    def moveTo(self, coord):
        self.x = coord[0]
        self.y = coord[1]

    def get_pos(self):
        return (self.x, self.y)

    def toString(self):
        return "Bishop@"+str(self.get_pos())

class Pawn:

    def __init__(self, team, x, y):
       self.x = x*STEP_SIZE
       self.y = y*STEP_SIZE
       self.team = team
       if(team == "white"):
           self._image_surf = pygame.image.load("sprites/white_pawn_20x20.png").convert()
       elif(team == "black"):
           self._image_surf = pygame.image.load("sprites/black_pawn_20x20.png").convert()

    def draw(self, surface):
        surface.blit(self._image_surf,(self.x,self.y))

    def movesInDirection(self, direction, map, pieces, limit=100):
        moves = []
        inc_i, inc_j = direction_dict[direction]
        i = inc_i
        j = inc_j
        count = 0
        break_out = False
        while(count < limit and not map.isWaterAt(int((self.x+i)/STEP_SIZE), int((self.y+j)/STEP_SIZE))):
            for piece in pieces:
                if piece.get_pos() == (self.x+i, self.y+j):
                    break_out = True
            if(break_out): break
            moves.append((self.x+i, self.y+j))
            i += inc_i
            j += inc_j
            count += 1

        return moves

    def avaliableMoves(self, pieces, map):
        moves = []

        moves.extend(self.movesInDirection("east", map, pieces, 2))
        moves.extend(self.movesInDirection("west", map, pieces, 2))
        moves.extend(self.movesInDirection("north", map, pieces, 2))
        moves.extend(self.movesInDirection("south", map, pieces, 2))
        moves.extend(self.movesInDirection("northeast", map, pieces, 2))
        moves.extend(self.movesInDirection("northwest", map, pieces, 2))
        moves.extend(self.movesInDirection("southeast", map, pieces, 2))
        moves.extend(self.movesInDirection("southwest", map, pieces, 2))

        return moves

    def moveTo(self, coord):
        self.x = coord[0]
        self.y = coord[1]

    def get_pos(self):
        return (self.x, self.y)

    def toString(self):
        return "Pawn@"+str(self.get_pos())
