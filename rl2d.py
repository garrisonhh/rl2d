import pygame as pg
import os

TSIZE = [8, 8]
SHEET = []
PALETTE = []

def init():
    print("initializing rl2d")
    _load_sheet("terminal.png")
    _load_palette("blood.png")

def _fpath(name):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), name)

def _load_sheet(sheetname):
    img = pg.image.load(_fpath(sheetname))
    for col in range(0, img.get_width(), TSIZE[0]):
        for row in range(0, img.get_height(), TSIZE[1]):
            SHEET.append(img.subsurface((col, row, *TSIZE)))

def _load_palette(palettename):
    img = pg.image.load(_fpath(palettename))
    for i in range(img.get_width()):
        PALETTE.append(img.get_at((i, 0)))

class RLScene(pg.Surface):
    def __init__(self, size):
        self.size = size
        self.runes = {}

        super().__init__((self.size[0] * TSIZE[0], self.size[1] * TSIZE[1]))

    def new_rune(self, name, ch, foreground, background = -1):
        #fg, bg refer to palette colors
        #if bg = -1 returns transparent background

        if type(ch) is str:
            ch = ord(ch.encode(encoding = "cp437"))
        img = pg.Surface(TSIZE, flags = pg.SRCALPHA)

        if background >= 0:
            img.fill(PALETTE[background])
        else:
            img.fill((0, 0, 0, 0))

        arr = pg.surfarray.array2d(SHEET[ch])

        for y in range(TSIZE[1]):
            for x in range(TSIZE[0]):
                if arr[x, y] == SHEET[ch].map_rgb((255, 255, 255)):
                    img.set_at((x, y), PALETTE[foreground])

        self.runes[name] = img

    def load_rune_file(self, filepath):
        with open(filepath, 'r') as f:
            for line in f.readlines():
                #skip empty lines and comments
                if line == "\n" or line.startswith("#"):
                    continue

                params = line.split()

                for i in range(1, len(params)):
                    params[i] = int(params[i])

                try:
                    self.new_rune(*params)
                except:
                    raise Exception("rune definition invalid: " + line + \
                                    "runes are defined with params (name, character, foreground, background = -1)")

    def load_font(self, foreground, background = -1):
        for ch in range(33, 127):
            self.new_rune(chr(ch), ch, foreground, background)
        self.new_rune(' ', 0, foreground, background)

    def draw(self, name, loc):
        self.blit(self.runes[name], (loc[0] * TSIZE[0], loc[1] * TSIZE[1]))

    def fill(self, name):
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                self.draw(name, (x, y))

    def write(self, str, loc, bg_rune = None):
        if bg_rune is not None:
            for i in range(len(str)):
                self.draw(bg_rune, [loc[0] + i, loc[1]])

        for i in range(len(str)):
            self.draw(str[i], [loc[0] + i, loc[1]])

    def box(self, rect, name):
        x, y, w, h = rect
        for rx in range(x, x + w):
            for ry in range(y, y + h):
                self.draw(name, (rx, ry))

    def box_outline(self, rect, name, corner = None, vert = None):
        if corner is None:
            corner = name
        if vert is None:
            vert = name

        x, y, w, h = rect

        for rx in (x, x + w - 1):
            #left, right sides
            for ry in range(y + 1, y + h - 1):
                self.draw(name, (rx, ry))

            #corners
            for ry in (y, y + h - 1):
                self.draw(corner, (rx, ry))

        for ry in (y, y + h - 1):
            #top, bottom sides
            for rx in range(x + 1, x + w - 1):
                self.draw(vert, (rx, ry))
