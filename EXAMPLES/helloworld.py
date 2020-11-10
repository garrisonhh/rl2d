import os
import pygame as pg
import rl2d

def asset_path(filename):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets\\" + filename)

def main():
    pg.init()

    # display constants
    tile_s = 12, 12
    console_s = 80, 50
    screen_s = tile_s[0] * console_s[0], tile_s[1] * console_s[1]

    # init pygame surfaces for display
    screen = pg.display.set_mode(screen_s)
    layer = rl2d.Layer(tile_s, console_s)

    # init tileset with the bitmap font 'assets\alloy_12x12.png'
    rl2d.tileset.load_font(tile_s, asset_path('alloy_12x12.png'))

    # write to screen
    layer.write((1, 1), "Hello World! :)")

    while True:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                exit(0)

        screen.fill((0, 0, 0))

        screen.blit(layer, (0, 0))

        pg.display.flip()

if __name__ == '__main__':
    main()
