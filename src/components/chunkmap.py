from random import randint
from random import choice
from termcolor import colored, cprint
from PIL import Image

import settings

DARK = True
resource_list = [
    "stone", "stone",
    "field", "field",
    "crop", "crop",
    "empty", "empty",
    "empty", "empty", "empty"
    ]
resource_list = [
    "stone", "stone",
    "field", "field",
    "crop", "crop",
    "empty", "empty",
    "empty", "empty", "empty"
    ]

CHUNK_SIZE = settings.CHUNK_SIZE

class Square:

    character = "  "
    color = "white"

    char_dict = {
        "water": "/\\",
        "land": "[]"
    }
    color_dict = {
        "stone": "red",
        "field": "yellow",
        "crop": "green",
        "empty": "white"
    }
    pixel_dict = {
        "red": (220,20,60),
        "yellow": (240,230,140),
        "green": (154,205,50),
        "white": (192, 192, 192),
        "cyan": (224,255,255)
    }
    dark_pixel_dict = {
        "red": (128,0,0),
        "yellow": (189,183,107),
        "green": (85,107,47),
        "white": (0, 0, 0),
        "cyan": (175,238,238)
    }

    def __init__(self, resource, isDark, type="water"):
        self.setResource(resource)
        self.isDark = isDark
        self.setType(type)

    def setResource(self, resource):
        self.resource = resource
        self.setColor(resource)

    def setColor(self, resource):
        if(resource in self.color_dict):
            self.color = self.color_dict[resource]
        else:
            print("Color error: No resource called ", resource)

    def getPixelColors(self):
        if(self.type == "water"):
            if(self.isDark): return self.dark_pixel_dict["cyan"]
            else: return self.pixel_dict["cyan"]

        if(self.isDark): return self.dark_pixel_dict[self.color]
        else: return self.pixel_dict[self.color]

    def setType(self, type):
        self.type = type
        self.setCharacter(type)

    def setCharacter(self, type):
        if(type in self.char_dict):
            self.character = self.char_dict[type]
        else:
            print("Character Error: No type called ", type)

    def getCompression(self):
        if(self.type == "water"):
            return "w"

        return self.resource[0]

    def print(self):
        if(self.type == "water"):
            pColor = "cyan"
        else:
            pColor = self.color

        if(self.isDark):
            cprint(self.character, pColor, attrs=['dark'], end='')
        else:
            cprint(self.character, pColor, end='')

    def isLand(self):
        return self.type != "water"

class Chunk:

    def __init__(self, resource=""):
        self.chunk = []
        self.resource = resource
        isDark = True

        for i in range(0, CHUNK_SIZE):
            self.chunk.append([])
            if(resource != ""):
                for j in range(0, CHUNK_SIZE):
                    self.chunk[i].append(Square(resource, isDark))
                    isDark = not isDark
                isDark = not isDark

    def iter(self):
        return self.chunk

    def get(self, x, y):
        if(y >= len(self.chunk)):
            return None
        if(x >= len(self.chunk[y])):
            return None

        return self.chunk[y][x]

    def print(self):
        for line in self.chunk:
            for sq in line:
                sq.print()
            print()

class ChunkRow:

    def __init__(self):
        self.row = Chunk()

    def append(self, chunk):
        head = self.row.iter()
        new = chunk.iter()

        for i in range(0, CHUNK_SIZE):
            head[i].extend(new[i])

    def get(self, x, y):
        return self.row.get(x, y)

    def print(self):
        for line in self.row.iter():
            for sq in line:
                sq.print()
            print()

class ChunkMap:
    width = 0
    height = 0
    rows = []

    def __init__(self, w, h, step_size, fill=True):
        self.width = w
        self.height = h
        self.step_size = step_size

        if(fill):
            for i in range(0, h):
                chunks = ChunkRow()
                for j in range(0, w):
                    chunks.append(Chunk(choice(resource_list)))
                self.rows.append(chunks)

    def makeIsland(self, x, y, n):
        if(self.get(x,y) == None or self.get(x,y).isLand()):
            return

        self.get(x,y).setType("land")

        xyxy = []
        if(x < self.width*10-1): xyxy.append((1,0))
        if(x > 0): xyxy.append((-1,0))
        if(y < self.height*10-1): xyxy.append((0,1))
        if(y > 0): xyxy.append((0,-1))

        xyxy = shuffle(xyxy)
        for tup in xyxy:
            if(randint(1, n) != 1):
                self.makeIsland(x+tup[0], y+tup[1], n-1)

    def getChunkRow(self, i):
        return self.rows[i]

    def get(self, x, y):
        y_1 = y%CHUNK_SIZE
        y_10 = int((y - y_1)/CHUNK_SIZE)

        if(y_10 >= len(self.rows)):
            return None

        return self.rows[y_10].get(x, y_1)

    def saveAsPNG(self, name="newmap"):
        s = self.step_size
        # PIL accesses images in Cartesian co-ordinates, so it is Image[columns, rows]
        img = Image.new( 'RGB', (self.width*CHUNK_SIZE*s,self.height*CHUNK_SIZE*s), "black") # create a new black image
        pixels = img.load() # create the pixel map

        for i in range(img.size[0]):    # for every col:
            x = int((i - i%s)/s)
            for j in range(img.size[1]):    # For every row
                y = int((j - j%s)/s)
                p, q, r = self.get(x, y).getPixelColors()
                pixels[i,j] = (p, q, r) # set the colour accordingly

        img.save(name, format="png")

    def saveAsTxt(self, name="newmap"):
        f = open(name, 'w+')
        for chunk_row in self.rows:
            for line in chunk_row.row.iter():
                for sq in line:
                    f.write(sq.getCompression())
                f.write("\n")

    def print(self):
        for chunk_row in self.rows:
            chunk_row.print()

def shuffle(in_list):
    ret_list = []

    while(in_list):
        ret_list.append(in_list.pop(randint(0, len(in_list)-1)))

    return ret_list


if __name__ == "__main__" :
    w = 13
    h = 8
    map = ChunkMap(w, h, 20)
    map.makeIsland(int(w*CHUNK_SIZE/2), int(h*CHUNK_SIZE/2), 75)
    map.print()
    map.saveAsPNG("../maps/map1.png")
    map.saveAsTxt("../maps/map1.txt")
