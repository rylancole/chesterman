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
    castles = []
    moves = []
    captures = []
    map = Map()
    scoreboard = None
    menu = None
    selected_piece = None
    color_turn = None

    def __init__(self, w, h):
        self._running = True
        self._display_surf = None

        #window size defined in pixels
        self.windowWidth = w
        self.windowHeight = h

    def on_init(self):
        pygame.init()
        self.scoreboard = Scoreboard()
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

    def createCastle(self, x, y, team):
        self.castles.append(Castle(x, y))
        self.map.putCastle(x, y)

        #create white pieces
        self.pieces.append(King(team, x+1, y+1))
        self.pieces.append(Queen(team, x+2, y+1))
        self.pieces.append(Rook(team, x+1, y))
        self.pieces.append(Rook(team, x+2, y))
        self.pieces.append(Knight(team, x+3, y+1))
        self.pieces.append(Knight(team, x, y))
        self.pieces.append(Bishop(team, x, y+1))
        self.pieces.append(Bishop(team, x+3, y))
        self.pieces.append(Pawn(team, x, y+2))
        self.pieces.append(Pawn(team, x+1, y+2))
        self.pieces.append(Pawn(team, x+2, y+2))
        self.pieces.append(Pawn(team, x+3, y+2))

    def on_setup(self):
        self.color_turn = "black"
        while( len(self.castles) < 2 ):
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

                    if(self.validCastleLocation(x, y)):
                        self.createCastle(x, y, self.color_turn)
                        self.color_turn = "white"
                        self._turn_surf = self._white_turn

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
        for castle in self.castles:
            castle.draw(self._display_surf)
        for move in self.moves:
            move.draw(self._display_surf)
        for piece in self.pieces:
            piece.draw(self._display_surf)
        for capture in self.captures:
            capture.draw(self._display_surf)
        self.scoreboard.draw(self._display_surf)
        if(self.menu.exists()): self.menu.draw(self._display_surf)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def turnSwitch(self):
        if(self.color_turn == "white"):
            self.color_turn = "black"
            self._turn_surf = self._black_turn
        else:
            self.color_turn = "white"
            self._turn_surf = self._white_turn

    def kill(self, capture):
        self.pieces.remove(capture.getPieceObj())

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

                    if(self.menu):
                        selected_option = self.menu.grabClick(pos[0], pos[1])
                        print(selected_option)

                    #convert mouse position into unit [SQpixels]
                    x = pos[0] - pos[0]%STEP_SIZE
                    y = pos[1] - pos[1]%STEP_SIZE

                    #set break conditions
                    in_captures = False
                    in_moves = False
                    in_pieces = False

                    #check to see if a move was clicked
                    for capture in self.captures:
                        #compare move sprite location to mouse click
                        if capture.getSQpixels() == (x, y):
                            #move selected piece into capture is clicked
                            capture.capturedBy(self.selected_piece, self.scoreboard)
                            self.kill(capture)
                            self.selected_piece.moveTo(capture.getSQpixels())
                            self.moves = []
                            self.captures = []
                            self.menu.vanish()
                            in_captures = True

                            self.turnSwitch()

                    #check to see if a move was clicked
                    if(not in_captures):
                        for move in self.moves:
                            #compare move sprite location to mouse click
                            if move.getSQpixels() == (x, y):
                                #move selected piece to this move if clicked
                                self.selected_piece.moveTo(move.getSQpixels())
                                self.moves = []
                                self.captures = []
                                self.menu.vanish()
                                in_moves = True

                                self.turnSwitch()

                    #check to see if a piece was clicked
                    if(not in_captures and not in_moves):
                        for piece in self.pieces:
                            if piece.getSQpixels() == (x, y):
                                if(piece.getTeam() == self.color_turn):
                                    #choose piece as selected if clicked
                                    self.selected_piece = piece
                                    self.menu.createKind(piece.getKind())
                                    self.moves = []
                                    self.captures = []
                                    #display legal moves and captures of selected piece
                                    possible_moves, possible_captures = piece.avaliableMoves(self.pieces, self.map)
                                    for move in possible_moves:
                                        self.moves.append(LegalMove(move))
                                    for capture in possible_captures:
                                        self.captures.append(LegalCapture(capture))
                                in_pieces = True
                                break
                        #empty space was clicked
                        if(not in_pieces):
                            self.selected_piece = None
                            self.moves = []
                            self.captures = []
                            #self.menu.vanish()

                #handle exit button being clicked
                if event.type == pygame.QUIT:
                    self._running = False

            #re-render app after handling clicks
            self.on_render()


            time.sleep (50.0 / 1000.0)

        self.on_cleanup()
