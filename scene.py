import pygame as pg
from rl2d.elements import *

class Layer(pg.Surface):
    """
    Layers have basic functionality for drawing tilesets onto a grid.
    """
    def __init__(self, size, tileset):
        self.size = size
        self.tset = tileset

        super().__init__(
            (size[0] * tileset.tsize[0], size[1] * tileset.tsize[1]),
            flags = pg.SRCALPHA
        )

    def set(self, loc, key):
        loc = (loc[0] * self.tset.tsize[0], loc[1] * self.tset.tsize[1])
        self.blit(self.tset[key], loc)

    def rect(self, rect, key):
        for y in range(rect[1], rect[1] + rect[3]):
            for x in range(rect[0], rect[0] + rect[2]):
                self.set((x, y), key)

    def sfill(self, key):
        self.rect((0, 0, *self.size), key)

class Scene(pg.Surface):
    """
    Scenes consist of a background Layer, and foreground elements (particles
    and sprites) that are drawn over it.
    Scene dynamically manages updating the screen when fg elements move.
    """
    def __init__(self, size, tileset):
        self.bg = Layer(size, tileset)
        super().__init__(self.bg.get_size())

        self.particles = pg.sprite.Group()
        self.sprites = pg.sprite.LayeredUpdates()

    # adds a sprite to group, and returns it for later reference
    def new_sprite(self, image, loc):
        sprite = Sprite(image, loc, self.bg.tset.tsize)
        self.sprites.add(sprite)
        return sprite

    def new_particle(self, image, loc, lifespan, **kwflags):
        particle = Particle(image, loc, self.bg.tset.tsize, lifespan, **kwflags)
        self.particles.add(particle)

    def update(self, dt):
        self.blit(self.bg, (0, 0))

        self.particles.update(dt)
        self.particles.draw(self)

        self.sprites.update(dt)
        self.sprites.draw(self)
