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

class GamePiece:

    piece_name = None   # used for toString and getKind
    _white_image_path = None    # used to initialize image
    _black_image_path = None
    captures = []
    prev_x = None
    prev_y = None

    def __init__(self, team, x, y):
        # store move coordinates in unit [SQpixels]
        self.x = x*STEP_SIZE
        self.y = y*STEP_SIZE

        self.multiplier = 1
        self.team = team
        if(team == "white"):
            self._image_surf = pygame.image.load("sprites/"+self.getKind()+"/white_"+self.getKind()+"20x20.png").convert_alpha()
        elif(team == "black"):
            self._image_surf = pygame.image.load("sprites/"+self.getKind()+"/black_"+self.getKind()+"20x20.png").convert_alpha()
        elif(team == "neutral"):
            self._image_surf = pygame.image.load(self._neutral_image_path).convert_alpha()

    def draw(self, surface):
        surface.blit(self._image_surf,(self.x,self.y))

    def changeTeam(self, new_team):
        self.team = new_team
        if(new_team == "white"):
            self._image_surf = pygame.image.load("sprites/"+self.getKind()+"/white_"+self.getKind()+"20x20.png").convert_alpha()
        elif(new_team == "black"):
            self._image_surf = pygame.image.load("sprites/"+self.getKind()+"/black_"+self.getKind()+"20x20.png").convert_alpha()
        elif(new_team == "neutral"):
            self._image_surf = pygame.image.load(self._neutral_image_path).convert_alpha()

    def movesInDirection(self, direction, map, pieces, limit=None, allowCapture=True):
        moves = []
        inc_i, inc_j = direction_dict[direction]
        i = inc_i
        j = inc_j
        count = 0
        break_out = False
        while((limit == None or count < limit) and not map.isWaterAt(self.x+i, self.y+j)):
            for piece in pieces:
                if piece.getSQpixels() == (self.x+i, self.y+j):
                    if(allowCapture and piece.team != self.team): self.captures.append(piece)
                    break_out = True
            if(break_out): break
            moves.append((self.x+i, self.y+j))
            i += inc_i
            j += inc_j
            count += 1
        return moves

    def movesInWater(self, direction, map, pieces, limit=None, allowCapture=True):
        moves = []
        inc_i, inc_j = direction_dict[direction]
        i = inc_i
        j = inc_j
        count = 0
        break_out = False
        while((limit == None or count < limit) and map.isWaterAt(self.x+i, self.y+j) and map.has(self.x+i, self.y+j)):
            for piece in pieces:
                if piece.getSQpixels() == (self.x+i, self.y+j):
                    if(allowCapture and piece.team != self.team and piece.getKind() != "port"): self.captures.append(piece)
                    break_out = True
            if(break_out): break
            moves.append((self.x+i, self.y+j))
            i += inc_i
            j += inc_j
            count += 1
        if((limit == None or count < limit) and not map.isWaterAt(self.x+i, self.y+j) and map.has(self.x+i, self.y+j)):
            skip = False
            for piece in pieces:
                if piece.getSQpixels() == (self.x+i, self.y+j):
                    skip = True
            if(not skip):
                moves.append((self.x+i, self.y+j))
        return moves

    def avaliableDropPoints(self, pieces, map):
        if(self.onMyCastle(map)): return self.castleDrop(pieces, map)
        moves = []
        self.captures = []
        moves.extend(self.movesInDirection("east", map, pieces, 1, False))
        moves.extend(self.movesInDirection("west", map, pieces, 1, False))
        moves.extend(self.movesInDirection("north", map, pieces, 1, False))
        moves.extend(self.movesInDirection("south", map, pieces, 1, False))
        moves.extend(self.movesInDirection("northeast", map, pieces, 1, False))
        moves.extend(self.movesInDirection("northwest", map, pieces, 1, False))
        moves.extend(self.movesInDirection("southeast", map, pieces, 1, False))
        moves.extend(self.movesInDirection("southwest", map, pieces, 1, False))
        return moves

    def avaliablePortPoints(self, pieces, map):
        moves = []

        for direction in direction_dict:
            i, j = direction_dict[direction]
            if(map.isWaterAt(self.x+i, self.y+j)):
                moves.append((self.x+i, self.y+j))

        return moves

    def castleDrop(self, pieces, map):
        moves = []

        x, y = self.getSquare()

        for i in range(x-3, x+3):
            for j in range(y-3, y+3):
                if(map.isColorCastleAt(self.team, i, j)):
                    skip = False
                    for piece in pieces:
                        if piece.getSquare() == (i, j):
                            skip = True
                    if(not skip):
                        moves.append((i*STEP_SIZE, j*STEP_SIZE))

        return moves

    def avaliableMoves(self, pieces, map):
        moves = []
        self.captures = []
        #should create unique avaliableMoves() for each piece
        return moves, self.captures

    def moveTo(self, coord):
        #takes coords in units [SQpixels]
        self.prev_x = self.x
        self.prev_y = self.y

        self.x = coord[0]
        self.y = coord[1]

    def undoMove(self):
        self.x = self.prev_x
        self.y = self.prev_y

    def isInCheck(self, pieces, map):
        for piece in pieces:
            possible_moves, possible_captures = piece.avaliableMoves(pieces, map)
            for capture in possible_captures:
                if capture.getKind() == "king" and capture.getTeam() == self.team:
                    return True

        return False

    def getSQpixels(self):
        return (self.x, self.y)

    def getSquare(self):
        return (int(self.x/STEP_SIZE), int(self.y/STEP_SIZE))

    def getKind(self):
        return self.piece_name

    def getTeam(self):
        return self.team

    def getBlock(self, map, needFullWord=False):
        return map.get(int(self.x/STEP_SIZE), int(self.y/STEP_SIZE), needFullWord)

    def onMyCastle(self, map):
        return map.isColorCastleAt(self.team, int(self.x/STEP_SIZE), int(self.y/STEP_SIZE))

    def onColorCastle(self, map, team):
        return map.isColorCastleAt(team, int(self.x/STEP_SIZE), int(self.y/STEP_SIZE))

    def getCorner(self):
        # only Kings should return a valid corner
        return None

    def getMultiplier(self):
        return self.multiplier

    def setMultiplier(self, m):
        self.multiplier = m

    def incMultiplier(self):
        self.multiplier += 1

    def toString(self):
        return self.piece_name+"@"+str(self.getSQpixels())

class King(GamePiece):

    piece_name = "king"
    captures = []

    def __init__(self, team, x, y, corner=""):
        #store move coordinates in unit [SQpixels]
        self.x = x*STEP_SIZE
        self.y = y*STEP_SIZE

        self.multiplier = 1
        self.team = team
        self.corner = corner
        if(team == "white"):
            self._image_surf = pygame.image.load("sprites/"+self.getKind()+"/white_"+self.getKind()+"20x20.png").convert_alpha()
        elif(team == "black"):
            self._image_surf = pygame.image.load("sprites/"+self.getKind()+"/black_"+self.getKind()+"20x20.png").convert_alpha()

    def getCorner(self):
        return self.corner

    def avaliableMoves(self, pieces, map):
        moves = []
        self.captures = []
        if(self.onMyCastle(map)): lim = 2
        else: lim = 1
        moves.extend(self.movesInDirection("east", map, pieces, lim))
        moves.extend(self.movesInDirection("west", map, pieces, lim))
        moves.extend(self.movesInDirection("north", map, pieces, lim))
        moves.extend(self.movesInDirection("south", map, pieces, lim))
        moves.extend(self.movesInDirection("northeast", map, pieces, lim))
        moves.extend(self.movesInDirection("northwest", map, pieces, lim))
        moves.extend(self.movesInDirection("southeast", map, pieces, lim))
        moves.extend(self.movesInDirection("southwest", map, pieces, lim))
        return moves, self.captures

    def isInCheckMate(self, pieces, map):
        if(not self.isInCheck(pieces, map)):
            return False

        moves, captures = self.avaliableMoves(pieces, map)

        for move in moves:
            self.moveTo(move)
            if(not self.isInCheck(pieces, map)):
                self.undoMove()
                return False
            self.undoMove()

        for cap in captures:
            self.moveTo(cap.getSquare())
            if(not self.isInCheck(pieces, map)):
                self.undoMove()
                return False
            self.undoMove()

        return True


class Queen(GamePiece):

    piece_name = "queen"
    captures = []

    def avaliableMoves(self, pieces, map):
        moves = []
        self.captures = []
        moves.extend(self.movesInDirection("east", map, pieces))
        moves.extend(self.movesInDirection("west", map, pieces))
        moves.extend(self.movesInDirection("north", map, pieces))
        moves.extend(self.movesInDirection("south", map, pieces))
        moves.extend(self.movesInDirection("northeast", map, pieces))
        moves.extend(self.movesInDirection("northwest", map, pieces))
        moves.extend(self.movesInDirection("southeast", map, pieces))
        moves.extend(self.movesInDirection("southwest", map, pieces))
        return moves, self.captures

class Rook(GamePiece):

    piece_name = "rook"
    captures = []

    def avaliableMoves(self, pieces, map):
        moves = []
        self.captures = []
        moves.extend(self.movesInDirection("east", map, pieces))
        moves.extend(self.movesInDirection("west", map, pieces))
        moves.extend(self.movesInDirection("north", map, pieces))
        moves.extend(self.movesInDirection("south", map, pieces))
        return moves, self.captures

class Knight(GamePiece):

    piece_name = "knight"
    captures = []

    direction_dict = {
        "left-right": (STEP_SIZE*2, STEP_SIZE),
        "up-down": (STEP_SIZE, STEP_SIZE*2),
    }

    def movesInDirection(self, direction, map, pieces, limit=None):
        moves = []
        i, j = self.direction_dict[direction]

        hit1 = map.isWaterAt(self.x+i, self.y+j)
        hit2 = map.isWaterAt(self.x+i, self.y-j)
        hit3 = map.isWaterAt(self.x-i, self.y+j)
        hit4 = map.isWaterAt(self.x-i, self.y-j)
        for piece in pieces:
            if not hit1 and piece.getSQpixels() == (self.x+i, self.y+j):
                if(piece.team != self.team): self.captures.append(piece)
                hit1 = True
            elif not hit2 and piece.getSQpixels() == (self.x+i, self.y-j):
                if(piece.team != self.team): self.captures.append(piece)
                hit2 = True
            elif not hit3 and piece.getSQpixels() == (self.x-i, self.y+j):
                if(piece.team != self.team): self.captures.append(piece)
                hit3 = True
            elif not hit4 and piece.getSQpixels() == (self.x-i, self.y-j):
                if(piece.team != self.team): self.captures.append(piece)
                hit4 = True

            if hit1 and hit2 and hit3 and hit4:
                break

        if(not hit1): moves.append((self.x+i, self.y+j))
        if(not hit2): moves.append((self.x+i, self.y-j))
        if(not hit3): moves.append((self.x-i, self.y+j))
        if(not hit4): moves.append((self.x-i, self.y-j))

        return moves


    def avaliableMoves(self, pieces, map):
        moves = []
        self.captures = []
        moves.extend(self.movesInDirection("left-right", map, pieces))
        moves.extend(self.movesInDirection("up-down", map, pieces))
        return moves, self.captures

class Bishop(GamePiece):

    piece_name = "bishop"
    captures = []

    def avaliableMoves(self, pieces, map):
        moves = []
        self.captures = []
        moves.extend(self.movesInDirection("northeast", map, pieces))
        moves.extend(self.movesInDirection("northwest", map, pieces))
        moves.extend(self.movesInDirection("southeast", map, pieces))
        moves.extend(self.movesInDirection("southwest", map, pieces))
        return moves, self.captures

class Pawn(GamePiece):

    piece_name = "pawn"
    captures = []

    def avaliableMoves(self, pieces, map):
        moves = []
        self.captures = []
        moves.extend(self.movesInDirection("east", map, pieces, 2, False))
        moves.extend(self.movesInDirection("west", map, pieces, 2, False))
        moves.extend(self.movesInDirection("north", map, pieces, 2, False))
        moves.extend(self.movesInDirection("south", map, pieces, 2, False))
        moves.extend(self.movesInDirection("northeast", map, pieces, 2))
        moves.extend(self.movesInDirection("northwest", map, pieces, 2))
        moves.extend(self.movesInDirection("southeast", map, pieces, 2))
        moves.extend(self.movesInDirection("southwest", map, pieces, 2))
        return moves, self.captures

class Wall(GamePiece):
    piece_name = "wall"
    _neutral_image_path = "sprites/wall/neutral_wall_20x20.png"

    def avaliableMoves(self, pieces=None, map=None):
        return [], []

class Port(GamePiece):
    piece_name = "port"
    _white_image_path = "sprites/port/white_port_20x20.png"
    _black_image_path = "sprites/port/black_port_20x20.png"
    _active_image_path = "sprites/port/boat20x20.png"
    active = False
    boat = None

    def activate(self):
        self.active = True
        self._image_surf = pygame.image.load(self._active_image_path).convert_alpha()

    def deactivate(self):
        self.active = False
        if(self.team == "white"):
            self._image_surf = pygame.image.load("sprites/"+self.getKind()+"/white_"+self.getKind()+"20x20.png").convert_alpha()
        elif(self.team == "black"):
            self._image_surf = pygame.image.load("sprites/"+self.getKind()+"/white_"+self.getKind()+"20x20.png").convert_alpha()

    def isActive(self):
        return self.active

    def avaliableMoves(self, pieces=None, map=None):
        return [], []

class Boat(GamePiece):
    piece_name = "boat"
    _image_path = "sprites/port/boat20x20.png"

    def __init__(self, x, y, sailor):
        self.x = x*STEP_SIZE
        self.y = y*STEP_SIZE
        self.sailor = sailor
        self.team = sailor.getTeam()
        self.multiplier = sailor.getMultiplier()
        self._image_surf = pygame.image.load(self._image_path).convert_alpha()

    def getSailorKind(self):
        return self.sailor.getKind()

    def getSailor(self):
        self.sailor.setMultiplier(self.multiplier)

        self.sailor.moveTo((self.x, self.y))
        return self.sailor

    def avaliableMoves(self, pieces, map):
        moves = []
        self.captures = []
        lim = 5
        moves.extend(self.movesInWater("east", map, pieces, lim))
        moves.extend(self.movesInWater("west", map, pieces, lim))
        moves.extend(self.movesInWater("north", map, pieces, lim))
        moves.extend(self.movesInWater("south", map, pieces, lim))
        moves.extend(self.movesInWater("northeast", map, pieces, lim))
        moves.extend(self.movesInWater("northwest", map, pieces, lim))
        moves.extend(self.movesInWater("southeast", map, pieces, lim))
        moves.extend(self.movesInWater("southwest", map, pieces, lim))
        return moves, self.captures

    def draw(self, surface):
        surface.blit(self.sailor._image_surf,(self.x,self.y))
        surface.blit(self._image_surf,(self.x,self.y))
