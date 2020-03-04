

class PieceStorage():

    piece_sets = {}

    def __init__(self, teams):
        self.teams = teams
        for team in teams:
            self.piece_sets[team] = PieceSet(team)

    def append(self, piece):
        self.piece_sets[piece.getTeam()].append(piece)

    def remove(self, piece):
        self.piece_sets[piece.getTeam()].remove(piece)

    def iter(self):
        iterable = []
        for team in self.piece_sets:
            iterable.extend(self.piece_sets[team].iter())
        return iterable


class PieceSet():

    pieces = {
        "king": [],
        "queen": [],
        "rook": [],
        "bishop": [],
        "knight": [],
        "pawn": []
    }

    def __init__(self, color):
        self.color = color

    def getColor(self):
        return self.color

    def iter(self):
        iterable = self.pieces["king"]
        iterable.extend(self.pieces["queen"])
        iterable.extend(self.pieces["rook"])
        iterable.extend(self.pieces["bishop"])
        iterable.extend(self.pieces["knight"])
        iterable.extend(self.pieces["pawn"])
        return iterable

    def append(self, piece):
        self.pieces[piece.getKind()].append(piece)

    def remove(self, piece):
        self.pieces[piece.getKind()].remove(piece)

    def getKing(self):
        return self.pieces["king"][0]

    def getQueens(self):
        return self.pieces["queen"]

    def getRooks(self):
        return self.pieces["rook"]

    def getBishops(self):
        return self.pieces["bishop"]

    def getKnights(self):
        return self.pieces["knight"]

    def getPawns(self):
        return self.pieces["pawn"]
