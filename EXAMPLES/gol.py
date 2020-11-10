import os
import rl2d
import pygame as pg
import random

"""
haven't quite figured out the rules for this lmao
"""

def asset_path(fname):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets\\" + fname)

def turn(grid, wrap = True):
    w, h  = len(grid[0]), len(grid)

    old = [[grid[y][x] for x in range(w)] for y in range(h)]

    for y in range(h):
        for x in range(w):
            # count neighbors
            n = 0
            for i in (-1, 0, 1):
                for j in (-1, 0, 1):
                    if i == j == 0:
                        continue

                    a, b = (y + i), (x + j)

                    if not wrap and (a < 0 or a >= w or b < 0 or b >= h):
                        continue

                    n += old[a % w][b % h]

            # apply rules
            if old[y][x] and (n == 2 or n == 3):
                pass
            elif not old[y][x] and n == 3:
                grid[y][x] = 1
            else:
                grid[y][x] = 0

def main():
    pg.init()
    screen = pg.display.set_mode((800, 800))
    timer = pg.time.Clock()

    rl2d.tileset.load_tileset((10, 10),
        asset_path("drake_10x10.png"),
        asset_path("gol.txt"))

    size = (80, 80)
    layer = rl2d.Layer((10, 10), size)

    grid = [[random.randint(0, 1) for i in range(size[0])] for j in range(size[1])]

    while True:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                exit(0)

        timer.tick(15)

        for y in range(size[1]):
            for x in range(size[0]):
                layer.set((x, y), ("dead", "alive")[grid[y][x]])

        turn(grid)

        screen.fill((0, 0, 0))
        screen.blit(layer, (0, 0))

        pg.display.flip()

if __name__ == '__main__':
    main()
