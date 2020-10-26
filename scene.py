import pygame as pg
from rl2d.elements import *

class Layer(pg.Surface):
    """
    Layers have basic functionality for drawing tilesets onto a grid.
    """
    def __init__(self, size, tilesize, tileset):
        self.size = size
        self.tsize = tilesize
        self.tset = tileset

        super().__init__(
            (size[0] * self.tsize[0], size[1] * self.tsize[1]),
            flags = pg.SRCALPHA
        )

    def set(self, loc, key):
        loc = (loc[0] * self.tsize[0], loc[1] * self.tsize[1])
        self.blit(self.tset[key], loc)

    """
    write functions write out each key in an iterable
    iterable being a string, a list, a tuple, etc.
    """
    def write(self, loc, iterable):
        i = 0
        for key in iterable:
            self.set((loc[0] + i, loc[1]), iterable[i])
            i += 1

    def smart_write(self, loc, string, wraplen = 0):
        pass

    def box(self, rect, key):
        for y in range(rect[1], rect[1] + rect[3]):
            for x in range(rect[0], rect[0] + rect[2]):
                self.set((x, y), key)

    def fill(self, key):
        self.box((0, 0, *self.size), key)

class Scene(pg.Surface):
    """
    Scenes consist of a background Layer, and foreground elements (particles
    and sprites) that are drawn over it.
    Scene automatically manages updating the screen when fg elements move.
    """
    def __init__(self, size, tilesize, tileset):
        self.bg = Layer(size, tilesize, tileset)
        super().__init__(self.bg.get_size())

        self.tsize = tilesize
        self.tset = tileset

        self.group = pg.sprite.LayeredUpdates()
        self.pspawners = []

    def add(self, element):
        if isinstance(element, pg.sprite.Sprite):
            self.group.add(element)
        else:
            raise ValueError("element %s is not a Sprite or Particle." % (str(element),))
        return element

    def add_pspawner(self, pspawner):
        self.pspawners.append(pspawner)

    def update(self, dt):
        self.blit(self.bg, (0, 0))

        for spawner in self.pspawners:
            spawner.update(dt)
        self.group.update(dt)

        #determine sprite layers (this looks hacky and slow but it runs better than the more complicated stuff I tried)
        for sprite in self.group.sprites():
            self.group.change_layer(sprite, sprite.rect.bottom)

        self.group.draw(self)
