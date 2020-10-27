import pygame as pg

TILES = {}

def load_tile(sheet, key, rect = 0, palette = 0, fg = None, bg = None):
    tile = 0
    if rect == 0: # no rect -> whole image is tile
        rect = (0, 0, *sheet.get_size())
        tile = sheet.copy()
    else: # rect -> subsurface of image is tile
        tile = sheet.subsurface(rect).copy()

    # recolor
    if palette:
        fg = palette.get_at((fg, 0))
        if bg is not None:
            bg = palette.get_at((bg, 0))
        else:
            bg = (0, 0, 0, 0)
        for y in range(rect[3]):
            for x in range(rect[2]):
                if tile.get_at((x, y))[:3] == (0, 0, 0):
                    tile.set_at((x, y), bg)
                elif tile.get_at((x, y))[:3] == (255, 255, 255):
                    tile.set_at((x, y), fg)

    global TILES
    TILES[key] = tile

"""
defs look like this:
; this is a comment
key x y ; no palette
key x y fg ; yes palette, white -> fg, black -> transparent
key x y fg bg ; yes palette, white -> fg, black -> bg

one load_sheet() call, one tilesize. u can load multiple sized images
using multiple load_sheet() or load_tile() calls
"""
def load_sheet(tilesize, tilesheet, definitions, palette = 0):
    sheet = pg.image.load(tilesheet).convert_alpha()

    if palette:
        palette = pg.image.load(palette)

    with open(definitions, 'r') as defs:
        for line in defs.readlines():
            if ';' in line:
                line = line[:line.index(';')]

            line = line.split()

            if len(line) == 0:
                continue

            key = line[0]
            rect = (int(line[1]) * tilesize[0], int(line[2]) * tilesize[1], *tilesize)

            if palette:
                #get colors
                fg = int(line[3])
                bg = None
                if len(line) > 4:
                    bg = int(line[4])

                load_tile(sheet, key, rect, palette, fg, bg)
            else:
                load_tile(sheet, key, rect)

"""
loads all possible printable characters for the tilesheet in specified encoding
    assumes horizontal format
see python 3's encodings documentation for reference on encoding:
https://docs.python.org/3/library/codecs.html#standard-encodings
"""
def load_font(charsize, tilesheet, encoding = 'ascii', palette = 0, fg = None, bg = None):
    sheet = pg.image.load(tilesheet).convert_alpha()

    if palette:
        palette = pg.image.load(palette)

    row = int(sheet.get_width() / charsize[0])
    for y in range(int(sheet.get_height() / charsize[1])):
        for x in range(row):
            #this turns the index of the character into a string of the specified encoding.
            c = bytes([y * row + x])
            c = c.decode(encoding, errors = 'ignore')

            if c.isprintable():
                load_tile(sheet, c, (x * charsize[0], y * charsize[1], *charsize), palette, fg, bg)

def get(key):
    return TILES[key]
