import os
import rl2d
import pygame as pg
import random

def asset_path(fname):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets\\" + fname)

def main():
    tsize = (8, 8)
    csize = (88, 66)

    pg.init()
    screen = pg.display.set_mode((tsize[0] * csize[0], tsize[1] * csize[1]))
    timer = pg.time.Clock()

    img = pg.image.load(asset_path("CGA8x8thin.png"))
    l = rl2d.Layer(tsize, csize)

    for y in range(16):
        for x in range(16):
            n = y * 16 + x
            rl2d.tileset.load_tile(img, n, rect = (x * 8, y * 8, 8, 8))

    while True:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                exit(0)

        timer.tick(60)

        for y in range(csize[1]):
            for x in range(csize[0]):
                l.set((x, y), random.randint(0, 255))

        screen.fill((0, 0, 0))

        screen.blit(l, (0, 0))

        pg.display.flip()
        pg.display.set_caption("%.0f fps" % (timer.get_fps(),))

if __name__ == '__main__':
    main()
