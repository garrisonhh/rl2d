import rl2d
import pygame as pg

def main():
    pg.init()
    screen = pg.display.set_mode((800, 600))

    rl2d.init()
    scene = rl2d.RLScene((30, 20))
    scene.new_rune("tile", 0, 0, 11)
    scene.new_rune("player", "@", 4)

    while True:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                exit(0)

        screen.fill((0, 0, 0))

        scene.fill("tile")
        scene.draw("player", (14, 9))

        pg.transform.scale(scene, screen.get_size(), screen)

        pg.display.flip()

if __name__ == '__main__':
    main()
