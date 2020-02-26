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

    piece_name = None   #used for toString
    _white_image_path = None    #used to initialize image
    _black_image_path = None
    captures = []
    prev_x = None
    prev_y = None


    def __init__(self, team, x, y):
        #store move coordinates in unit [SQpixels]
        self.x = x*STEP_SIZE
        self.y = y*STEP_SIZE

        self.multiplier = 1
        self.team = team
        if(team == "white"):
            self._image_surf = pygame.image.load(self._white_image_path).convert()
        elif(team == "black"):
            self._image_surf = pygame.image.load(self._black_image_path).convert()

    def draw(self, surface):
        surface.blit(self._image_surf,(self.x,self.y))

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

    def avaliableDropPoints(self, pieces, map):
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

    def getSQpixels(self):
        return (self.x, self.y)

    def getSquare(self):
        return (int(self.x/STEP_SIZE), int(self.y/STEP_SIZE))

    def getKind(self):
        return self.piece_name

    def getTeam(self):
        return self.team

    def getCorner(self):
        # only Kings should return a valid corner
        return None

    def getMultiplier(self):
        return self.multiplier

    def incMultiplier(self):
        self.multiplier += 1

    def toString(self):
        return self.piece_name+"@"+str(self.getSQpixels())

class King(GamePiece):

    piece_name = "King"
    _white_image_path = "sprites/white_king_20x20.png"
    _black_image_path = "sprites/black_king_20x20.png"
    captures = []

    def __init__(self, team, x, y, corner=""):
        #store move coordinates in unit [SQpixels]
        self.x = x*STEP_SIZE
        self.y = y*STEP_SIZE

        self.multiplier = 1
        self.team = team
        self.corner = corner
        if(team == "white"):
            self._image_surf = pygame.image.load(self._white_image_path).convert()
        elif(team == "black"):
            self._image_surf = pygame.image.load(self._black_image_path).convert()

    def getCorner(self):
        return self.corner

    def avaliableMoves(self, pieces, map):
        moves = []
        self.captures = []
        moves.extend(self.movesInDirection("east", map, pieces, 1))
        moves.extend(self.movesInDirection("west", map, pieces, 1))
        moves.extend(self.movesInDirection("north", map, pieces, 1))
        moves.extend(self.movesInDirection("south", map, pieces, 1))
        moves.extend(self.movesInDirection("northeast", map, pieces, 1))
        moves.extend(self.movesInDirection("northwest", map, pieces, 1))
        moves.extend(self.movesInDirection("southeast", map, pieces, 1))
        moves.extend(self.movesInDirection("southwest", map, pieces, 1))
        return moves, self.captures

    def isInCheck(self, pieces, map):
        for piece in pieces:
            possible_moves, possible_captures = piece.avaliableMoves(pieces, map)
            for capture in possible_captures:
                if capture.getKind() == "King" and capture.getTeam() == self.team:
                    return True

        return False

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

    piece_name = "Queen"
    _white_image_path = "sprites/white_queen_20x20.png"
    _black_image_path = "sprites/black_queen_20x20.png"
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

    piece_name = "Rook"
    _white_image_path = "sprites/white_rook_20x20.png"
    _black_image_path = "sprites/black_rook_20x20.png"
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

    piece_name = "Knight"
    _white_image_path = "sprites/white_knight_20x20.png"
    _black_image_path = "sprites/black_knight_20x20.png"
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

    piece_name = "Bishop"
    _white_image_path = "sprites/white_bishop_20x20.png"
    _black_image_path = "sprites/black_bishop_20x20.png"
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

    piece_name = "Pawn"
    _white_image_path = "sprites/white_pawn_20x20.png"
    _black_image_path = "sprites/black_pawn_20x20.png"
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
