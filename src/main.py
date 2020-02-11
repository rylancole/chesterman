from components.app import App

import settings

settings.init()
CHUNK_SIZE = settings.CHUNK_SIZE
STEP_SIZE = settings.STEP_SIZE
WIDTH = settings.WIDTH
HEIGHT = settings.HEIGHT

if __name__ == "__main__" :
    '''
    Build the app in units of pixels
    Each square is STEP_SIZExSTEP_SIZE pixels
    Each chunk is CHUNK_SIZExCHUNK_SIZE squares
    App is WIDTH chunks long and HEIGHT chunks tall
    The +3 allows room for the player console
    '''
    theApp = App((WIDTH+3)*CHUNK_SIZE*STEP_SIZE, HEIGHT*CHUNK_SIZE*STEP_SIZE)
    theApp.on_gameplay()
