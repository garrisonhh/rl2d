import pygame as pg
import os
from rl2d import RLScene, init

def _fpath(name):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), name)

def main():
    pg.init()
    screen = pg.display.set_mode((1024, 512))
    pg.display.set_caption("RL2D char picker")

    font = pg.image.load(_fpath("terminal.png"))
    palette = pg.image.load(_fpath("blood.png"))

    init()
    scene = RLScene((16, 1))
    scene.load_font(2, 0)

    text = "pick a char!"

    ch = 0
    fg = 1
    bg = 0

    scene.write(text, (0, 0))

    while True:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                exit(0)
            elif e.type == pg.MOUSEBUTTONDOWN:
                x = int(e.pos[0] / 32)
                y = int(e.pos[1] / 32)

                if x < 16:
                    ch = x * 16 + y
                elif y == 0:
                    c = min(x - 16, 4)

                    if e.button == 1:
                        fg = c
                    else:
                        bg = c

                text = "%s, %s, %s" % (ch, fg, bg)

                scene.new_rune("picked", ch, fg, bg)

                scene.fill(" ")
                scene.draw("picked", (0, 0))
                scene.write(text, (2, 0))

        screen.fill((0, 0, 0))

        screen.blit(pg.transform.scale(font, (512, 512)), (0, 0))
        screen.blit(pg.transform.scale(palette, (160, 32)), (512, 0))

        screen.blit(pg.transform.scale(scene, (512, 32)), (512, 64))

        pg.display.flip()

if __name__ == '__main__':
    main()
