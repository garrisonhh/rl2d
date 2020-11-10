import os
import rl2d
import pygame as pg
import numpy as np
import math

def asset_path(fname):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets\\" + fname)

ORTHO = np.array([[1.0, 0.5, 0.0],
                  [0.0, -.5, 1.0],
                  [0.0, 0.0, 0.0]])

ISO = np.array([[1, -1, 0],
                [.5, .5, -1],
                [0, 0, 0]])

def bresenham(a, b):
    #from https://www.gatevidyalay.com/bresenham-line-drawing-algorithm/
    reverse = False
    ystep = 1
    if a[0] > b[0]:
        a, b = b, a
        reverse = True
    if b[1] < a[1]:
        ystep = -1

    #only works from this point if x < bx, y < by, and dx >= dy
    dx, dy = abs(b[0] - a[0]), abs(b[1] - a[1])

    flipd = dy > dx
    if flipd:
        dx, dy = dy, dx

    p = 2 * dy - dx

    line = []
    y = 0

    for x in range(1, dx + 1):
        if p >= 0:
            p -= 2 * dx
            y += ystep
        p += 2 * dy

        if flipd:
            line.append((a[0] + (y * ystep), a[1] + (x * ystep)))
        else:
            line.append((a[0] + x, a[1] + y))

    if reverse:
        return line[::-1] + [tuple(a)]
    return [tuple(a)] + line

def project(x, y, z, scale = 1, offset = (0, 0), transform = None):
    vec = np.array((x, y, z)).reshape(3, 1)

    if transform is not None:
        vec = transform @ vec

    vec = ISO @ vec
    vec *= scale

    return int(vec[0, 0] + offset[0]), int(vec[1, 0] + offset[1])

def xy_rot_matrix(angle):
    return np.array([[math.cos(angle), math.cos(angle + math.pi / 2), 0],
                     [math.sin(angle), math.sin(angle + math.pi / 2), 0],
                     [0, 0, 1]])

def xz_rot_matrix(angle):
    return np.array([[math.cos(angle), 0, math.cos(angle + math.pi / 2)],
                     [0, 1, 0],
                     [math.sin(angle), 0, math.sin(angle + math.pi / 2)]])

# cube at pos, each side length is side
def make_cube(pos, side):
    # points and segments of a cube
    cube = [(pos[0] + x, pos[1] + y, pos[2] + z) for x in (0, side) for y in (0, side) for z in (0, side)]

    seg = [
        (0, 1), (1, 3), (3, 2), (2, 0), # top face
        (4, 5), (5, 7), (7, 6), (6, 4), # bottom face
        (0, 4), (1, 5), (2, 6), (3, 7), # sides
    ]

    return cube, seg

def main():
    pg.init()
    screen = pg.display.set_mode((800, 800))
    timer = pg.time.Clock()
    t = 0

    rl2d.tileset.load_tileset((10, 10),
        asset_path("drake_10x10.png"),
        asset_path("gol.txt"))

    size = (80, 80)
    layer = rl2d.Layer((10, 10), size)

    pts, seg = make_cube((-10, -10, -10), 20)

    while True:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                exit(0)

        timer.tick()

        t += timer.get_time()
        if t >= 4000:
            t -= 4000

        layer.fill("dead")

        transform = xz_rot_matrix(math.pi * 2 * (t / 4000)) @ xy_rot_matrix(math.pi * 2 * (t / 4000))

        projected = []
        for pt in pts:
            projected.append(project(*pt, offset = (39, 39), transform = transform))

        for i, j in seg:
            for x, y in bresenham(projected[i], projected[j]):
                layer.set((x, y), "alive")

        screen.fill((0, 0, 0))
        screen.blit(layer, (0, 0))
        pg.display.flip()
        pg.display.set_caption("%.2ffps" % (timer.get_fps(),))

if __name__ == '__main__':
    main()
