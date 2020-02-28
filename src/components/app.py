from pygame.locals import *
from random import randint
import pygame
import time

import components.pieces as pieces
from components.pieces import *
from components.pieceloader import PieceLoader
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
GOLD_WORTH = settings.GOLD_WORTH

class App:
    '''
    Creates window for gameplay and holds all game data
    '''

    pieces = []
    castles = {}
    moves = []
    captures = []
    can_coll = {'white': True, 'black': True}
    map = Map()
    scoreboard = None
    checkMultiplier = {"white": 1, "black": 1}
    resrcboard = None
    menu = None
    ex_butt = None
    selected_piece = None
    prev_piece = None
    color_turn = None
    second_move = False
    moved_already = False
    turn_number = 0

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
        self.menu = Menu(1040, 400)
        self.ex_butt = Menu(1040, 675)
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
        pygame.display.set_caption('Chesterman Demo')
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
        for i in range(x-3, x+7):
            for j in range(y-3, y+7):
                if(self.map.isCastleAt(i, j)):
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
        king = self.getPiece(team, "king")
        loader = PieceLoader()
        loader.loadPieces(king, self.pieces)

    def stealGold(self, team):
        if(self.resrcboard.get(self.notColor(team), "gold") > 0):
            self.resrcboard.increaseResource(self.notColor(team), "gold", -1)
            self.resrcboard.increaseResource(team, "gold", 1)

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
                            corner = move.getCorner()
                            team = self.color_turn
                            if(corner == "north"):
                                self.pieces.append(King(team, x, y+2, "north"))
                                self.map.putCastle(team, x-2, y)
                            elif(corner == "south"):
                                self.pieces.append(King(team, x, y-2, "south"))
                                self.map.putCastle(team, x-2, y-3)
                            elif(corner == "east"):
                                self.pieces.append(King(team, x-2, y, "east"))
                                self.map.putCastle(team, x-3, y-2)
                            elif(corner == "west"):
                                self.pieces.append(King(team, x+2, y, "west"))
                                self.map.putCastle(team, x, y-2)

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
        if(self.ex_butt.exists()): self.ex_butt.draw(self._display_surf)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def creation(self, choice):
        self.moves = []
        possible_drops = self.selected_piece.avaliableDropPoints(self.pieces, self.map)
        for drop in possible_drops:
            legal_drop = LegalDrop(drop, self.color_turn, choice)
            if(not legal_drop.checksKing(self.notColor(self.color_turn), self.pieces, self.map)):
                self.moves.append(legal_drop)

    def annouceWinner(self, winner):
        self.menu.createPrompt(winner+" wins!")
        time.sleep(5)

    def notColor(self, team):
        if(team == "white"):
            return "black"
        if(team == "black"):
            return "white"

    def turnSwitch(self):
        self.turn_number += 1
        self.prev_piece = self.selected_piece
        if(self.selected_piece and self.selected_piece.getKind() == "knight" and self.selected_piece.onColorCastle(self.map, self.notColor(self.color_turn))):
            self.stealGold(self.color_turn)
        if(self.can_coll[self.color_turn] == None):
            self.can_coll[self.color_turn] = False
        elif(self.can_coll[self.color_turn] == False):
            self.can_coll[self.color_turn] = True
        opp_king = self.getPiece(self.notColor(self.color_turn), "king")
        if(opp_king.isInCheck(self.pieces, self.map)):
            if(opp_king.isInCheckMate(self.pieces, self.map)):
                self.scoreboard.increaseCheckPoints(self.color_turn, 250)
            else:
                self.scoreboard.increaseCheckPoints(self.color_turn, 5*self.checkMultiplier[self.color_turn])
                self.checkMultiplier[self.color_turn] += 1
        else:
            self.checkMultiplier[self.color_turn] = 1

        if(self.color_turn == "white"):
            self.color_turn = "black"
            self._turn_surf = self._black_turn
        else:
            self.color_turn = "white"
            self._turn_surf = self._white_turn
        self.second_move = False
        self.moved_already = False

        self.winner = self.scoreboard.getWinner()
        if(self.winner):
            print(self.winner+" wins!")
            self._running = False
            return

    def convert(self, bishop, pawn):
        b_coord = bishop.getSQpixels()
        p_coord = pawn.getSQpixels()

        bishop.moveTo(p_coord)
        pawn.moveTo(b_coord)

        pawn.changeTeam(bishop.getTeam())

    def unconvert(self, bishop, pawn):
        b_coord = bishop.getSQpixels()
        p_coord = pawn.getSQpixels()

        bishop.moveTo(p_coord)
        pawn.moveTo(b_coord)

        pawn.changeTeam(self.notColor(bishop.getTeam()))

    def kill(self, capture):
        self.pieces.remove(capture.getPieceObj())

    def unkill(self, capture):
        self.pieces.append(capture.getPieceObj())

    def on_gameplay(self):

        #don't let game run until it's been initialized
        if self.on_init() == False:
            self._running = False

        self.ex_butt.createExButton()
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

#HANDLE EXCHANGE BUTTON
                    selected_option = self.ex_butt.grabClick(pos[0], pos[1])
                    if(selected_option):
                        opt_obj = selected_option.clicked(self.map)
                        if(opt_obj["func"] == "exchange"):
                            done_round = True
                            self.menu.createExMenu()

#HANDLE MENUS
                    if(self.menu.exists()):
                        selected_option = self.menu.grabClick(pos[0], pos[1])
                        if(selected_option):
                            done_round = True
                            opt_obj = selected_option.clicked(self.map)
                            if(opt_obj["func"] == None):
                                done_round = False
                            elif(opt_obj["func"] == "create"):
                                cost, cost_resrc = opt_obj["cost"]
                                if(self.resrcboard.get(self.color_turn, cost_resrc) >= cost):
                                    self.creation(opt_obj["choice"])
                                else:
                                    self.menu.createPrompt("Invalid Move. Not enough "+cost_resrc)
                                    done_round = False
                            elif(opt_obj["func"] == "exchange"):
                                choice = opt_obj["choice"]
                                if(self.resrcboard.get(self.color_turn, choice) >= 5):
                                    if(choice == 'gold'):
                                        self.resrcboard.increaseResource(self.color_turn, 'gold', -5)
                                        self.scoreboard.increaseCollectionPoints(self.color_turn, GOLD_WORTH)
                                    else:
                                        self.resrcboard.increaseResource(self.color_turn, choice, -5)
                                        self.resrcboard.increaseResource(self.color_turn, 'gold', 1)
                            elif(opt_obj["func"] == "end"):
                                self.moves = []
                                self.captures = []
                                self.menu.vanish()
                                self.turnSwitch()
                            elif(opt_obj["func"] == "collect"):
                                self.resrcboard.increaseResource(self.color_turn, opt_obj["resrc"], 1)
                                self.can_coll[self.color_turn] = None
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
                                if(self.selected_piece.getKind() == "bishop" and capture.getPieceObj().getKind() == "pawn"):
                                    self.convert(self.selected_piece, capture.getPieceObj())
                                    converted = True
                                else:
                                    self.kill(capture)
                                    converted = False
                                self.selected_piece.moveTo(capture.getSQpixels())
                                if(self.getPiece(self.color_turn, "king").isInCheck(self.pieces, self.map)):
                                    self.selected_piece.undoMove()
                                    if(converted): self.unconvert(capture.getPieceObj())
                                    else: self.unkill(capture)
                                    self.menu.createPrompt("Invalid move. That puts you in check")
                                else:
                                    capture.capturedBy(self.selected_piece, self.scoreboard)
                                    self.moves = []
                                    self.captures = []
                                    self.menu.vanish()
                                    self.turnSwitch()
                                done_round = True
                                self.prev_piece = self.selected_piece

#HANDLE MOVING
                    #check to see if a move was clicked
                    if(not done_round):
                        for move in self.moves:
                            #compare move sprite location to mouse click
                            if move.getSQpixels() == (x, y):
                                dropped_piece = False
                                if(move.getType() == "move"):
                                    #move selected piece to this move if clicked
                                    self.selected_piece.moveTo(move.getSQpixels())
                                elif(move.getType() == "drop"
                                    and not self.selected_piece.isInCheck(self.pieces, self.map)
                                    and not self.getPiece(self.color_turn, "king").isInCheck(self.pieces, self.map)):
                                    # drop new piece to this position if clicked
                                    # and selected piece nor King are currently in check
                                    self.pieces.append(move.getPiece())
                                    self.resrcboard.increaseResource(self.color_turn, cost_resrc, -cost)
                                    dropped_piece = True

                                if(self.getPiece(self.color_turn, "king").isInCheck(self.pieces, self.map)):
                                    self.selected_piece.undoMove()
                                    if(dropped_piece): self.pieces.remove(move.getPiece())
                                    self.menu.createPrompt("Invalid move. You are in check.")
                                else:
                                    if(self.selected_piece.getKind() != "pawn"):
                                        self.second_move = True
                                    else:
                                        if(self.moved_already):
                                            self.second_move = True
                                        else:
                                            opp_king = self.getPiece(self.notColor(self.color_turn), "king")
                                            if(opp_king.isInCheck(self.pieces, self.map)):
                                                self.second_move = True
                                            else:
                                                self.moved_already = True
                                                self.menu.createEndMenu()
                                    self.moves = []
                                    self.captures = []
                                    if(not self.moved_already):
                                        self.menu.vanish()
                                    if(self.second_move):
                                        self.menu.vanish()
                                        self.turnSwitch()
                                done_round = True
                                self.prev_piece = self.selected_piece


#HANDLE PIECE SELECTION
                    #check to see if a piece was clicked
                    if(not done_round):
                        for piece in self.pieces:
                            if self.moved_already and (piece.getKind() != "pawn" or piece == self.prev_piece):
                                pass
                            elif piece.getSQpixels() == (x, y):
                                if(piece.getTeam() == self.color_turn):
                                    #choose piece as selected if clicked
                                    self.selected_piece = piece
                                    if(piece.getKind() != "pawn" or (self.can_coll[self.color_turn] and not self.moved_already)):
                                        self.menu.createKind(piece)
                                    self.moves = []
                                    self.captures = []
                                    #display legal moves and captures of selected piece
                                    possible_moves, possible_captures = piece.avaliableMoves(self.pieces, self.map)
                                    for move in possible_moves:
                                        self.moves.append(LegalMove(move))
                                    if(not self.moved_already and self.turn_number > 1):
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
                            if(not self.moved_already):
                                if(not self.menu.isPrompt()):
                                    self.menu.vanish()
                            else:
                                self.menu.createEndMenu()

                #handle exit button being clicked
                if event.type == pygame.QUIT:
                    self._running = False

            #re-render app after handling clicks
            self.on_render()

            time.sleep (50.0 / 1000.0)

        self.on_cleanup()
