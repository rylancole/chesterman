from pygame.locals import *
from random import randint
import pygame
import time

import components.pieces as pieces
from components.pieces import *
from components.chunkmap import ChunkMap
from components.moves import LegalMove
from components.infrastructure import *

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
    map = Map()
    selected_piece = None

    def __init__(self, w, h):
        self._running = True
        self._display_surf = None

        #window size defined in pixels
        self.windowWidth = w
        self.windowHeight = h


    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
        pygame.display.set_caption('Chesterman')
        self._running = True
        self._back_surf = pygame.image.load(MAP_PATH+".png").convert()
        self.map.decompress(open(MAP_PATH+".txt"))

        self.on_setup()

    def on_setup(self):
        #create castles
        self.castles.append(Castle(24, 8))
        self.castles.append(Castle(12, 24))

        #create white pieces
        self.pieces.append(King("white", 25, 9))
        self.pieces.append(Queen("white", 36, 19))
        self.pieces.append(Rook("white", 36, 12))
        self.pieces.append(Knight("white", 23, 14))
        self.pieces.append(Bishop("white", 30, 6))
        self.pieces.append(Pawn("white", 31, 20))

        #create black pieces
        self.pieces.append(King("black", 25, 10))
        self.pieces.append(Queen("black", 36, 20))
        self.pieces.append(Rook("black", 36, 13))
        self.pieces.append(Knight("black", 23, 15))
        self.pieces.append(Bishop("black", 30, 7))
        self.pieces.append(Pawn("black", 31, 21))

    def on_render(self):
        '''
        Render layers in following order:
            1) Background
            2) Infrastructure
            3) Moves
            4) Pieces
        '''
        self._display_surf.fill((0,0,0))
        self._display_surf.blit(self._back_surf,(0,0))
        for castle in self.castles:
            castle.draw(self._display_surf)
        for move in self.moves:
            move.draw(self._display_surf)
        for piece in self.pieces:
            piece.draw(self._display_surf)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

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

                    #convert mouse position into unit [SQpixels]
                    x = pos[0] - pos[0]%STEP_SIZE
                    y = pos[1] - pos[1]%STEP_SIZE

                    #set break conditions
                    in_moves = False
                    in_pieces = False

                    #check to see if a move was clicked
                    for move in self.moves:
                        #compare move sprite location to mouse click
                        if move.getSQpixels() == (x, y):
                            print(self.selected_piece.toString(), "->", move.getSQpixels())
                            #move selected piece to this move if clicked
                            self.selected_piece.moveTo(move.getSQpixels())
                            self.moves = []
                            in_moves = True

                    #check to see if a piece was clicked
                    if(not in_moves):
                        for piece in self.pieces:
                            if piece.getSQpixels() == (x, y):
                                #choose piece as selected if clicked
                                self.selected_piece = piece
                                print(piece.toString())
                                self.moves = []
                                #display legal moves of selected piece
                                for move in piece.avaliableMoves(self.pieces, self.map):
                                    self.moves.append(LegalMove(move))
                                in_pieces = True
                                break
                        #empty space was clicked
                        if(not in_pieces):
                            print("Empty@("+str(x)+", "+str(y)+")")
                            self.selected_piece = None
                            self.moves = []

                #handle exit button being clicked
                if event.type == pygame.QUIT:
                    self._running = False

            #re-render app after handling clicks
            self.on_render()

            time.sleep (50.0 / 1000.0)

        self.on_cleanup()
