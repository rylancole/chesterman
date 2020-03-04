import pygame
from components.pieces import *

class LegalType:

    image_dict = {
        "king": "sprites/king/green_king20x20.png",
        "queen": "sprites/queen/green_queen20x20.png",
        "rook": "sprites/rook/green_rook20x20.png",
        "knight": "sprites/knight/green_knight20x20.png",
        "bishop": "sprites/bishop/green_bishop20x20.png",
        "pawn": "sprites/pawn/green_pawn20x20.png",
        "wall": "sprites/wall/green_wall_20x20.png",
        "port": "sprites/port/green_port_20x20.png",
        "north": "sprites/arrow/green_north_20x20.png",
        "south": "sprites/arrow/green_south_20x20.png",
        "east": "sprites/arrow/green_east_20x20.png",
        "west": "sprites/arrow/green_west_20x20.png"
    }
    _image_surf = None
    piece = None

    def __init__(self, coord):
        #store move coordinates in unit [SQpixels]
        self.x = coord[0]
        self.y = coord[1]
        self._image_surf = pygame.image.load("sprites/arrow/move_border20x20.png").convert_alpha()

    def setImageSurf(self, choice):
        self._image_surf = pygame.image.load(self.image_dict[choice]).convert_alpha()

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
        elif(choice == "port"): self.piece = Port(team, x, y)

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
        "king": "sprites/king/red_king20x20.png",
        "queen": "sprites/queen/red_queen20x20.png",
        "rook": "sprites/rook/red_rook20x20.png",
        "knight": "sprites/knight/red_knight20x20.png",
        "bishop": "sprites/bishop/red_bishop20x20.png",
        "pawn": "sprites/pawn/red_pawn20x20.png",
        "wall": "sprites/wall/red_wall_20x20.png",
        "boat": "sprites/port/red_boat20x20.png"
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
        if(self.kind == "boat"):
            self.kind = piece.getSailorKind()
        self._image_surf = pygame.image.load(self.image_dict[self.kind]).convert_alpha()

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
