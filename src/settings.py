def init():
    global CHUNK_SIZE
    CHUNK_SIZE = 4 #must be even to make checkerboard

    global STEP_SIZE
    STEP_SIZE = 20

    global ISLAND_SIZE
    ISLAND_SIZE = 75

    global MAP_PATH
    # MAP_PATH = "maps/map1"
    MAP_PATH = "maps/map2"
    # MAP_PATH = "maps/map3"
    # MAP_PATH = "maps/map4"
    # MAP_PATH = "maps/map5"

    global WIDTH
    WIDTH = 13

    global HEIGHT
    HEIGHT = 8

    global COST_DICT
    COST_DICT = {
        "queen": (3, "gold"),
        "rook": (3, "stone"),
        "knight": (3, "hay"),
        "bishop": (1, "gold"),
        "pawn": (3, "crop"),
        "wall": (1, "stone")
    }

    global GOLD_WORTH
    GOLD_WORTH = 35

    global LOAD_VERSION
    LOAD_VERSION = 1 # every piece
    # LOAD_VERSION = 2 # just rook
    # LOAD_VERSION = 3 # just knight
    # LOAD_VERSION = 4 # queen, rook, knight
    # LOAD_VERSION = 5 # bishop, rook, knight
