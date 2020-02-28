import pygame
from components.pieces import *

class LegalType:

    image_dict = {
        "king": "sprites/green_king_20x20.png",
        "queen": "sprites/green_queen_20x20.png",
        "rook": "sprites/green_rook_20x20.png",
        "knight": "sprites/green_knight_20x20.png",
        "bishop": "sprites/green_bishop_20x20.png",
        "pawn": "sprites/green_pawn_20x20.png",
        "wall": "sprites/green_wall_20x20.png",
        "north": "sprites/green_north_20x20.png",
        "south": "sprites/green_south_20x20.png",
        "east": "sprites/green_east_20x20.png",
        "west": "sprites/green_west_20x20.png"
    }
    _image_surf = None
    piece = None

    def __init__(self, coord):
        #store move coordinates in unit [SQpixels]
        self.x = coord[0]
        self.y = coord[1]
        self._image_surf = pygame.image.load("sprites/block-green20x20.png").convert()

    def setImageSurf(self, choice):
        self._image_surf = pygame.image.load(self.image_dict[choice]).convert()

    def getSQpixels(self):
        return (self.x, self.y)

    def getSquare(self):
        return (int(self.x/STEP_SIZE), int(self.y/STEP_SIZE))

    def getPiece(self):
        return self.piece

    def draw(self, surface):
        surface.blit(self._image_surf,(self.x,self.y))

class LegalMove(LegalType):

    def getType(self):
        return "move"

class LegalEstablishment(LegalType):

    def __init__(self, x, y, corner=None):
        #store move coordinates in unit [SQpixels]
        self.x = x*STEP_SIZE
        self.y = y*STEP_SIZE
        self.corner = corner
        self.setImageSurf(corner)

    def getType(self):
        return "establishment"

    def getCorner(self):
        return self.corner


class LegalDrop(LegalType):

    def __init__(self, coord, team, choice):
        #store move coordinates in unit [SQpixels]
        self.x = coord[0]
        self.y = coord[1]
        self.initPiece(team, choice)

    def initPiece(self, team, choice):
        x = int(self.x/STEP_SIZE)
        y = int(self.y/STEP_SIZE)

        if(choice == "queen"): self.piece = Queen(team, x, y)
        elif(choice == "rook"): self.piece = Rook(team, x, y)
        elif(choice == "bishop"): self.piece = Bishop(team, x, y)
        elif(choice == "knight"): self.piece = Knight(team, x, y)
        elif(choice == "pawn"): self.piece = Pawn(team, x, y)
        elif(choice == "wall"): self.piece = Wall("neutral", x, y)

        self.setImageSurf(choice)

    def checksKing(self, other_team, pieces, map):
        moves, captures = self.piece.avaliableMoves(pieces, map)
        for capture in captures:
            if capture.getKind() == "king" and capture.getTeam() == other_team:
                return True
        return False

    def getType(self):
        return "drop"

class LegalCapture:

    image_dict = {
        "king": "sprites/red_king_20x20.png",
        "queen": "sprites/red_queen_20x20.png",
        "rook": "sprites/red_rook_20x20.png",
        "knight": "sprites/red_knight_20x20.png",
        "bishop": "sprites/red_bishop_20x20.png",
        "pawn": "sprites/red_pawn_20x20.png",
        "wall": "sprites/red_wall_20x20.png"
    }

    value_dict = {
        "queen": 9,
        "rook": 5,
        "knight": 3,
        "bishop": 3,
        "pawn": 1,
        "wall": 0
    }

    def __init__(self, piece):
        #store move coordinates in unit [SQpixels]
        self.x, self.y = piece.getSQpixels()
        self.piece_obj = piece
        self.kind = piece.getKind()
        self._image_surf = pygame.image.load(self.image_dict[self.kind]).convert()

    def getValue(self):
        return self.value_dict[self.kind]

    def getPieceObj(self):
        return self.piece_obj

    def capturedBy(self, piece, scoreboard): #piece passed in is the capturer, self.piece_obj is the captured
        points = self.getValue() * piece.getMultiplier()
        scoreboard.increaseCapturePoints(piece.getTeam(), points)
        piece.incMultiplier()

    def getSQpixels(self):
        return (self.x, self.y)

    def draw(self, surface):
        surface.blit(self._image_surf,(self.x,self.y))
