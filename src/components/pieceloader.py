from components.pieces import *
import settings

LOAD_VERSION = settings.LOAD_VERSION


class PieceLoader():

    version = LOAD_VERSION

    def init(self):
        pass

    def loadPieces(self, king, pieces):
        if(self.version == 1):
            self.everyPiece(king, pieces)
        elif(self.version == 2):
            self.justRook(king, pieces)
        elif(self.version == 3):
            self.justKnight(king, pieces)
        elif(self.version == 4):
            self.queenRookKnight(king, pieces)
        elif(self.version == 5):
            self.bishopRookKnight(king, pieces)


    def everyPiece(self, king, pieces):
        '''
        Load Version: 1
            1 King      1 Queen
            2 Rooks     2 Bishops
            2 Knights   4 Pawns
        '''
        x, y = king.getSquare()
        corner = king.getCorner()
        team = king.getTeam()

        if(corner == "north" or corner == "south"):
            pieces.append(Queen(team, x-1, y))
            pieces.append(Bishop(team, x+1, y))
            pieces.append(Bishop(team, x-2, y))
        elif(corner == "east" or corner == "west"):
            pieces.append(Queen(team, x, y-1))
            pieces.append(Bishop(team, x, y+1))
            pieces.append(Bishop(team, x, y-2))

        if(corner == "north"):
            pieces.append(Rook(team, x, y+1))
            pieces.append(Rook(team, x-1, y+1))
            pieces.append(Knight(team, x+1, y+1))
            pieces.append(Knight(team, x-2, y+1))
            pieces.append(Pawn(team, x, y-1))
            pieces.append(Pawn(team, x-1, y-1))
            pieces.append(Pawn(team, x+1, y-1))
            pieces.append(Pawn(team, x-2, y-1))
        elif(corner == "south"):
            pieces.append(Rook(team, x, y-1))
            pieces.append(Rook(team, x-1, y-1))
            pieces.append(Knight(team, x+1, y-1))
            pieces.append(Knight(team, x-2, y-1))
            pieces.append(Pawn(team, x, y+1))
            pieces.append(Pawn(team, x-1, y+1))
            pieces.append(Pawn(team, x+1, y+1))
            pieces.append(Pawn(team, x-2, y+1))
        elif(corner == "west"):
            pieces.append(Rook(team, x+1, y))
            pieces.append(Rook(team, x+1, y-1))
            pieces.append(Knight(team, x+1, y+1))
            pieces.append(Knight(team, x+1, y-2))
            pieces.append(Pawn(team, x-1, y))
            pieces.append(Pawn(team, x-1, y-1))
            pieces.append(Pawn(team, x-1, y+1))
            pieces.append(Pawn(team, x-1, y-2))
        elif(corner == "east"):
            pieces.append(Rook(team, x-1, y))
            pieces.append(Rook(team, x-1, y-1))
            pieces.append(Knight(team, x-1, y+1))
            pieces.append(Knight(team, x-1, y-2))
            pieces.append(Pawn(team, x+1, y))
            pieces.append(Pawn(team, x+1, y-1))
            pieces.append(Pawn(team, x+1, y+1))
            pieces.append(Pawn(team, x+1, y-2))

    def justRook(self, king, pieces):
        '''
        Load Version: 2
            1 King      1 Rook      2 Pawns
        '''
        x, y = king.getSquare()
        corner = king.getCorner()
        team = king.getTeam()

        if(corner == "north" or corner == "south"):
            pieces.append(Rook(team, x-1, y))
        elif(corner == "east" or corner == "west"):
            pieces.append(Rook(team, x, y-1))

        if(corner == "north"):
            pieces.append(Pawn(team, x, y-1))
            pieces.append(Pawn(team, x-1, y-1))
        elif(corner == "south"):
            pieces.append(Pawn(team, x, y+1))
            pieces.append(Pawn(team, x-1, y+1))
        elif(corner == "west"):
            pieces.append(Pawn(team, x-1, y))
            pieces.append(Pawn(team, x-1, y-1))
        elif(corner == "east"):
            pieces.append(Pawn(team, x+1, y))
            pieces.append(Pawn(team, x+1, y-1))

    def justKnight(self, king, pieces):
        '''
        Load Version: 3
            1 King      1 Knight      2 Pawns
        '''
        x, y = king.getSquare()
        corner = king.getCorner()
        team = king.getTeam()

        if(corner == "north" or corner == "south"):
            pieces.append(Knight(team, x-1, y))
        elif(corner == "east" or corner == "west"):
            pieces.append(Knight(team, x, y-1))

        if(corner == "north"):
            pieces.append(Pawn(team, x, y-1))
            pieces.append(Pawn(team, x-1, y-1))
        elif(corner == "south"):
            pieces.append(Pawn(team, x, y+1))
            pieces.append(Pawn(team, x-1, y+1))
        elif(corner == "west"):
            pieces.append(Pawn(team, x-1, y))
            pieces.append(Pawn(team, x-1, y-1))
        elif(corner == "east"):
            pieces.append(Pawn(team, x+1, y))
            pieces.append(Pawn(team, x+1, y-1))

    def queenRookKnight(self, king, pieces):
        '''
        Load Version: 4
            1 King      1 Queen
            1 Rook      2 Knight
            4 Pawns
        '''
        x, y = king.getSquare()
        corner = king.getCorner()
        team = king.getTeam()

        if(corner == "north" or corner == "south"):
            pieces.append(Queen(team, x-1, y))
            pieces.append(Rook(team, x+1, y))
            pieces.append(Knight(team, x-2, y))
        elif(corner == "east" or corner == "west"):
            pieces.append(Queen(team, x, y-1))
            pieces.append(Rook(team, x, y+1))
            pieces.append(Knight(team, x, y-2))

        if(corner == "north"):
            pieces.append(Pawn(team, x, y-1))
            pieces.append(Pawn(team, x-1, y-1))
            pieces.append(Pawn(team, x+1, y-1))
            pieces.append(Pawn(team, x-2, y-1))
        elif(corner == "south"):
            pieces.append(Pawn(team, x, y+1))
            pieces.append(Pawn(team, x-1, y+1))
            pieces.append(Pawn(team, x+1, y+1))
            pieces.append(Pawn(team, x-2, y+1))
        elif(corner == "west"):
            pieces.append(Pawn(team, x-1, y))
            pieces.append(Pawn(team, x-1, y-1))
            pieces.append(Pawn(team, x-1, y+1))
            pieces.append(Pawn(team, x-1, y-2))
        elif(corner == "east"):
            pieces.append(Pawn(team, x+1, y))
            pieces.append(Pawn(team, x+1, y-1))
            pieces.append(Pawn(team, x+1, y+1))
            pieces.append(Pawn(team, x+1, y-2))

    def bishopRookKnight(self, king, pieces):
        '''
        Load Version: 5
            1 King      1 Bishop
            1 Rook      2 Knight
            4 Pawns
        '''
        x, y = king.getSquare()
        corner = king.getCorner()
        team = king.getTeam()

        if(corner == "north" or corner == "south"):
            pieces.append(Bishop(team, x-1, y))
            pieces.append(Rook(team, x+1, y))
            pieces.append(Knight(team, x-2, y))
        elif(corner == "east" or corner == "west"):
            pieces.append(Bishop(team, x, y-1))
            pieces.append(Rook(team, x, y+1))
            pieces.append(Knight(team, x, y-2))

        if(corner == "north"):
            pieces.append(Pawn(team, x, y-1))
            pieces.append(Pawn(team, x-1, y-1))
            pieces.append(Pawn(team, x+1, y-1))
            pieces.append(Pawn(team, x-2, y-1))
        elif(corner == "south"):
            pieces.append(Pawn(team, x, y+1))
            pieces.append(Pawn(team, x-1, y+1))
            pieces.append(Pawn(team, x+1, y+1))
            pieces.append(Pawn(team, x-2, y+1))
        elif(corner == "west"):
            pieces.append(Pawn(team, x-1, y))
            pieces.append(Pawn(team, x-1, y-1))
            pieces.append(Pawn(team, x-1, y+1))
            pieces.append(Pawn(team, x-1, y-2))
        elif(corner == "east"):
            pieces.append(Pawn(team, x+1, y))
            pieces.append(Pawn(team, x+1, y-1))
            pieces.append(Pawn(team, x+1, y+1))
            pieces.append(Pawn(team, x+1, y-2))
