def init():
    global CHUNK_SIZE
    CHUNK_SIZE = 4 #must be even to make checkerboard

    global STEP_SIZE
    STEP_SIZE = 20

    global ISLAND_SIZE
    ISLAND_SIZE = 75

    global MAP_PATH
    MAP_PATH = "maps/map1"

    global WIDTH
    WIDTH = 13

    global HEIGHT
    HEIGHT = 8

    global COST_DICT
    COST_DICT = {
        "Queen": (3, "gold"),
        "Rook": (3, "stone"),
        "Knight": (3, "hay"),
        "Bishop": (1, "gold"),
        "Pawn": (3, "crop")
    }

    global GOLD_WORTH
    GOLD_WORTH = 35

    global LOAD_VERSION
    LOAD_VERSION = 1 # every piece
    # LOAD_VERSION = 2 # just rook
    # LOAD_VERSION = 3 # just knight
    # LOAD_VERSION = 4 # queen, rook, knight
    # LOAD_VERSION = 5 # bishop, rook, knight
