from pygame.locals import *
from random import randint
import pygame
import time

import components.pieces as pieces
from components.pieces import *
from components.chunkmap import ChunkMap
from components.moves import *
from components.infrastructure import *
from components.menus import *

import settings

settings.init()
STEP_SIZE = settings.STEP_SIZE
MAP_PATH = settings.MAP_PATH
WIDTH = settings.WIDTH
HEIGHT = settings.HEIGHT

class App:
    '''
    Creates window for gameplay and holds all game data
    '''

    pieces = []
    castles = {}
    moves = []
    captures = []
    map = Map()
    scoreboard = None
    checkMultiplier = {"white": 1, "black": 1}
    resrcboard = None
    menu = None
    selected_piece = None
    color_turn = None
    second_move = False
    moved_already = False

    def __init__(self, w, h):
        self._running = True
        self._display_surf = None

        #window size defined in pixels
        self.windowWidth = w
        self.windowHeight = h

    def on_init(self):
        pygame.init()
        self.scoreboard = Scoreboard(1)
        self.resrcboard = ResourceBoard(6)
        self.menu = Menu()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
        pygame.display.set_caption('Chesterman')
        self._running = True
        self._back_surf = pygame.image.load(MAP_PATH+".png").convert()
        self._white_turn = pygame.image.load("sprites/white_turn_.png").convert()
        self._black_turn = pygame.image.load("sprites/black_turn_.png").convert()
        self._turn_surf = self._black_turn
        self.map.decompress(open(MAP_PATH+".txt"))

        self.on_setup()

    def validCastleLocation(self, x, y):
        for i in range(x, x+4):
            for j in range(y, y+4):
                if(self.map.isWaterAt(i*STEP_SIZE, j*STEP_SIZE) or self.map.isCastleAt(i, j)):
                    return False
        return True

    def establishCastle(self, x, y, team):
        self.castles[team] = Castle(x, y)

        self.moves = []
        self.moves.append(LegalEstablishment(x, y+2, "west"))
        self.moves.append(LegalEstablishment(x+2, y, "north"))
        self.moves.append(LegalEstablishment(x+2, y+3, "south"))
        self.moves.append(LegalEstablishment(x+3, y+2, "east"))

    def getPiece(self, team, kind):
        for piece in self.pieces:
            if piece.getKind() == kind and piece.getTeam() == team:
                return piece
        return None

    def loadPieces(self, team):
        king = self.getPiece(team, "King")
        x, y = king.getSquare()
        corner = king.getCorner()

        if(corner == "north" or corner == "south"):
            self.pieces.append(Queen(team, x-1, y))
            self.pieces.append(Bishop(team, x+1, y))
            self.pieces.append(Bishop(team, x-2, y))
        elif(corner == "east" or corner == "west"):
            self.pieces.append(Queen(team, x, y-1))
            self.pieces.append(Bishop(team, x, y+1))
            self.pieces.append(Bishop(team, x, y-2))

        if(corner == "north"):
            self.pieces.append(Rook(team, x, y+1))
            self.pieces.append(Rook(team, x-1, y+1))
            self.pieces.append(Knight(team, x+1, y+1))
            self.pieces.append(Knight(team, x-2, y+1))
            self.pieces.append(Pawn(team, x, y-1))
            self.pieces.append(Pawn(team, x-1, y-1))
            self.pieces.append(Pawn(team, x+1, y-1))
            self.pieces.append(Pawn(team, x-2, y-1))
        elif(corner == "south"):
            self.pieces.append(Rook(team, x, y-1))
            self.pieces.append(Rook(team, x-1, y-1))
            self.pieces.append(Knight(team, x+1, y-1))
            self.pieces.append(Knight(team, x-2, y-1))
            self.pieces.append(Pawn(team, x, y+1))
            self.pieces.append(Pawn(team, x-1, y+1))
            self.pieces.append(Pawn(team, x+1, y+1))
            self.pieces.append(Pawn(team, x-2, y+1))
        elif(corner == "west"):
            self.pieces.append(Rook(team, x+1, y))
            self.pieces.append(Rook(team, x+1, y-1))
            self.pieces.append(Knight(team, x+1, y+1))
            self.pieces.append(Knight(team, x+1, y-2))
            self.pieces.append(Pawn(team, x-1, y))
            self.pieces.append(Pawn(team, x-1, y-1))
            self.pieces.append(Pawn(team, x-1, y+1))
            self.pieces.append(Pawn(team, x-1, y-2))
        elif(corner == "east"):
            self.pieces.append(Rook(team, x-1, y))
            self.pieces.append(Rook(team, x-1, y-1))
            self.pieces.append(Knight(team, x-1, y+1))
            self.pieces.append(Knight(team, x-1, y-2))
            self.pieces.append(Pawn(team, x+1, y))
            self.pieces.append(Pawn(team, x+1, y-1))
            self.pieces.append(Pawn(team, x+1, y+1))
            self.pieces.append(Pawn(team, x+1, y-2))

    def on_setup(self):
        self.color_turn = "black"
        run_setup = True

        self.menu.createPrompt("Position your castle")

        while( run_setup ):
            ev = pygame.event.get()

            for event in ev:

                #handle mouse click
                if event.type == pygame.MOUSEBUTTONUP:
                    #get mouse position in unit [pixels]
                    pos = pygame.mouse.get_pos()

                    #convert mouse position into unit [SQpixels]
                    x = pos[0] - pos[0]%STEP_SIZE
                    y = pos[1] - pos[1]%STEP_SIZE

                    #convert mouse position into unit [Squares]
                    x = int(x/STEP_SIZE)
                    y = int(y/STEP_SIZE)

                    clicked_king = False

                    for move in self.moves:
                        #compare move sprite location to mouse click
                        if move.getSquare() == (x, y):
                            #move selected piece to this move if clicked
                            if(move.getCorner() == "north"): self.pieces.append(King(self.color_turn, x, y+2, "north"))
                            elif(move.getCorner() == "south"): self.pieces.append(King(self.color_turn, x, y-2, "south"))
                            elif(move.getCorner() == "east"): self.pieces.append(King(self.color_turn, x-2, y, "east"))
                            elif(move.getCorner() == "west"): self.pieces.append(King(self.color_turn, x+2, y, "west"))

                            clicked_king = True

                            self.moves = []
                            self.loadPieces(self.color_turn)
                            self.color_turn = "white"
                            self._turn_surf = self._white_turn
                            if(len(self.castles) > 1):
                                self.menu.vanish()
                                run_setup = False
                            else:
                                self.menu.changePrompt("Position your castle")

                            self.map.putCastle(x, y)


                    if(not clicked_king and self.validCastleLocation(x, y)):
                        self.establishCastle(x, y, self.color_turn)
                        self.menu.changePrompt("Reposition your castle")
                        self.menu.addPrompt("OR choose a direction")

                #handle exit button being clicked
                if event.type == pygame.QUIT:
                    self._running = False
                    break

            if(not self._running): break

            #re-render app after handling clicks
            self.on_render()

            time.sleep (50.0 / 1000.0)

    def on_render(self):
        '''
        Render layers in following order:
            1) Background
            2) Infrastructure
            3) Moves
            4) Pieces
            5) Capturable Pieces
        '''
        self._display_surf.fill((0,0,0))
        self._display_surf.blit(self._back_surf,(0,0))
        self._display_surf.blit(self._turn_surf,(1040,0))
        for key in self.castles:
            self.castles[key].draw(self._display_surf)
        for move in self.moves:
            move.draw(self._display_surf)
        for piece in self.pieces:
            piece.draw(self._display_surf)
        for capture in self.captures:
            capture.draw(self._display_surf)
        self.scoreboard.draw(self._display_surf)
        self.resrcboard.draw(self._display_surf)
        if(self.menu.exists()): self.menu.draw(self._display_surf)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def creation(self, choice):
        self.moves = []
        possible_drops = self.selected_piece.avaliableDropPoints(self.pieces, self.map)
        for drop in possible_drops:
            self.moves.append(LegalDrop(drop, self.color_turn, choice))

    def annouceWinner(self, winner):
        self.menu.createPrompt(winner+" wins!")
        time.sleep(5)

    def turnSwitch(self):
        if(self.color_turn == "white"):
            opp_king = self.getPiece("black", "King")
            if(opp_king.isInCheck(self.pieces, self.map)):
                if(opp_king.isInCheckMate(self.pieces, self.map)):
                    self._running = False
                    self.annouceWinner("white")
                    return
                self.scoreboard.increaseCheckPoints("white", 5*self.checkMultiplier["white"])
                self.checkMultiplier["white"] += 1
            else:
                self.checkMultiplier["white"] = 1

            self.color_turn = "black"
            self._turn_surf = self._black_turn
        else:
            opp_king = self.getPiece("white", "King")
            if(opp_king.isInCheck(self.pieces, self.map)):
                if(opp_king.isInCheckMate(self.pieces, self.map)):
                    self._running = False
                    self.annouceWinner("black")
                    return
                self.scoreboard.increaseCheckPoints("black", 5*self.checkMultiplier["black"])
                self.checkMultiplier["black"] += 1
            else:
                self.checkMultiplier["black"] = 1

            self.color_turn = "white"
            self._turn_surf = self._white_turn
        self.second_move = False
        self.moved_already = False

    def kill(self, capture):
        self.pieces.remove(capture.getPieceObj())

    def unkill(self, capture):
        self.pieces.append(capture.getPieceObj())

    def on_gameplay(self):

        #don't let game run until it's been initialized
        if self.on_init() == False:
            self._running = False

        #run game
        while( self._running ):
            ev = pygame.event.get()

            for event in ev:

                #handle mouse click
                if event.type == pygame.MOUSEBUTTONUP:
                    #get mouse position in unit [pixels]
                    pos = pygame.mouse.get_pos()

                    #set break conditions
                    done_round = False

#HANDLE MENUS
                    if(self.menu.exists()):
                        selected_option = self.menu.grabClick(pos[0], pos[1])
                        if(selected_option):
                            done_round = True
                            opt_obj = selected_option.clicked(self.map)
                            if(opt_obj["func"] == None):
                                done_round = False
                            elif(opt_obj["func"] == "create"):
                                self.creation(opt_obj["choice"])
                            elif(opt_obj["func"] == "build"):
                                print("Build a wall")
                                self.moves = []
                                self.captures = []
                                self.menu.vanish()
                                self.turnSwitch()
                            elif(opt_obj["func"] == "energy"):
                                print("Use energy")
                                self.moves = []
                                self.captures = []
                                self.menu.vanish()
                                self.turnSwitch()
                            elif(opt_obj["func"] == "collect"):
                                self.resrcboard.increaseResource(
                                    self.color_turn,
                                    opt_obj["resrc"],
                                    1
                                )
                                self.moves = []
                                self.captures = []
                                self.menu.vanish()
                                self.turnSwitch()




                    #convert mouse position into unit [SQpixels]
                    x = pos[0] - pos[0]%STEP_SIZE
                    y = pos[1] - pos[1]%STEP_SIZE

#HANDLE CAPTURES
                    #check to see if a capture was clicked
                    if(not done_round):
                        for capture in self.captures:
                            #compare move sprite location to mouse click
                            if capture.getSQpixels() == (x, y):
                                #move selected piece into capture is clicked
                                self.kill(capture)
                                self.selected_piece.moveTo(capture.getSQpixels())
                                if(self.getPiece(self.color_turn, "King").isInCheck(self.pieces, self.map)):
                                    self.selected_piece.undoMove()
                                    self.unkill(capture)
                                    self.menu.createPrompt("Invalid move")
                                else:
                                    capture.capturedBy(self.selected_piece, self.scoreboard)
                                    self.moves = []
                                    self.captures = []
                                    self.menu.vanish()
                                    self.turnSwitch()
                                done_round = True

#HANDLE MOVING
                    #check to see if a move was clicked
                    if(not done_round):
                        for move in self.moves:
                            #compare move sprite location to mouse click
                            if move.getSQpixels() == (x, y):
                                #move selected piece to this move if clicked
                                if(move.getType() == "move"):
                                    self.selected_piece.moveTo(move.getSQpixels())
                                elif(move.getType() == "drop"):
                                    self.pieces.append(move.getPiece())

                                if(self.getPiece(self.color_turn, "King").isInCheck(self.pieces, self.map)):
                                    self.selected_piece.undoMove()
                                    self.menu.createPrompt("Invalid move")
                                else:
                                    if(self.selected_piece.getKind() != "Pawn"):
                                        self.second_move = True
                                    else:
                                        if(self.moved_already):
                                            self.second_move = True
                                        else:
                                            self.moved_already = True
                                    self.moves = []
                                    self.captures = []
                                    self.menu.vanish()
                                    if(self.second_move): self.turnSwitch()
                                done_round = True


#HANDLE PIECE SELECTION
                    #check to see if a piece was clicked
                    if(not done_round):
                        for piece in self.pieces:
                            if self.moved_already and piece.getKind() != "Pawn":
                                pass
                            elif piece.getSQpixels() == (x, y):
                                if(piece.getTeam() == self.color_turn):
                                    #choose piece as selected if clicked
                                    self.selected_piece = piece
                                    self.menu.createKind(piece)
                                    self.moves = []
                                    self.captures = []
                                    #display legal moves and captures of selected piece
                                    possible_moves, possible_captures = piece.avaliableMoves(self.pieces, self.map)
                                    for move in possible_moves:
                                        self.moves.append(LegalMove(move))
                                    for capture in possible_captures:
                                        self.captures.append(LegalCapture(capture))
                                done_round = True
                                break

#HANDLE OFF FOCUS
                        #empty space was clicked
                        if(not done_round):
                            self.selected_piece = None
                            self.moves = []
                            self.captures = []
                            self.menu.vanish()

                #handle exit button being clicked
                if event.type == pygame.QUIT:
                    self._running = False

            #re-render app after handling clicks
            self.on_render()


            time.sleep (50.0 / 1000.0)

        self.on_cleanup()
