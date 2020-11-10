import os
import rl2d
import pygame as pg
import random

def asset_path(fname):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets\\" + fname)

# for a spawner
def note_particle():
    return rl2d.Particle((8, 8), (39, 48), random.choice(["note", "notes"]), 1000, vector = (2, -5))

def main():
    tsize = (8, 8)
    csize = (80, 50)

    pg.init()
    screen = pg.display.set_mode((tsize[0] * csize[0], tsize[1] * csize[1]))
    timer = pg.time.Clock()

    rl2d.tileset.load_font(tsize,
        asset_path("CGA8x8thin.png"))
    rl2d.tileset.load_tileset(tsize,
        asset_path("CGA8x8thin.png"),
        asset_path("stuff.txt"))

    scene = rl2d.Scene(tsize, csize)

    scene.bg.box((1, 1, 78, 20), "block")
    scene.bg.box((2, 2, 76, 18), " ")
    scene.bg.set((3, 21), "/")
    scene.bg.set((2, 22), "smile")

    with open(asset_path("dummytext.txt")) as f:
        scene.bg.write((3, 3), "\t" + f.read(), wrap = 74)

    scene.bg.set((39, 49), "box")
    scene.add_spawner(rl2d.Spawner(note_particle, 250, 200))

    while True:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                exit(0)

        timer.tick(60)
        scene.update(timer.get_time())

        screen.fill((0, 0, 0))

        screen.blit(scene, (0, 0))

        pg.display.flip()

if __name__ == '__main__':
    main()
