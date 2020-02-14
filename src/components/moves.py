import pygame
from components.pieces import *

class LegalMove:

    def __init__(self, coord):
        #store move coordinates in unit [SQpixels]
        self.x = coord[0]
        self.y = coord[1]
        self._image_surf = pygame.image.load("sprites/block-green20x20.png").convert()

    def getSQpixels(self):
        return (self.x, self.y)

    def draw(self, surface):
        surface.blit(self._image_surf,(self.x,self.y))

class LegalCapture:

    image_dict = {
        "King": "sprites/red_king_20x20.png",
        "Queen": "sprites/red_queen_20x20.png",
        "Rook": "sprites/red_rook_20x20.png",
        "Knight": "sprites/red_knight_20x20.png",
        "Bishop": "sprites/red_bishop_20x20.png",
        "Pawn": "sprites/red_pawn_20x20.png"
    }

    value_dict = {
        "Queen": 9,
        "Rook": 5,
        "Knight": 3,
        "Bishop": 3,
        "Pawn": 1
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
