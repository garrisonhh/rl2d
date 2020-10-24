import pygame as pg

class Tileset:
    def __init__(self, tilesize):
        self.tsize = tilesize
        self.tiles = {}

    def load_sheet(self, sheetpath, defspath, palette = 0):
        sheet = pg.image.load(sheetpath).convert_alpha()

        if palette:
            palette = pg.image.load(palette)

        with open(defspath, 'r') as defs:
            for line in defs.readlines():
                if ';' in line:
                    line = line[:line.index(';')]

                line = line.split()

                if len(line) == 0:
                    continue

                key, x, y = line[0], int(line[1]), int(line[2])
                tile = sheet.subsurface((x * self.tsize[0], y * self.tsize[1], *self.tsize)).copy()

                if palette:
                    #get colors
                    fg = palette.get_at((int(line[3]), 0))
                    bg = (0, 0, 0, 0)
                    if len(line) > 4:
                        bg = palette.get_at((int(line[4]), 0))

                    #make new tile
                    for y in range(self.tsize[1]):
                        for x in range(self.tsize[0]):
                            if tile.get_at((x, y))[:3] == (0, 0, 0):
                                tile.set_at((x, y), bg)
                            elif tile.get_at((x, y))[:3] == (255, 255, 255):
                                tile.set_at((x, y), fg)

                self.tiles[key] = tile

    #allow access to tileset with Tileset[key]
    def __getitem__(self, key):
        return self.tiles[key]
