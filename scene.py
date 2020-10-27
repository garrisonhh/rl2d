import pygame as pg
from rl2d.elements import *
from rl2d import tileset as tset

class Layer(pg.Surface):
    """
    Layers have basic functionality for drawing tilesets onto a grid.
    """
    def __init__(self, size, tilesize):
        self.size = size
        self.tsize = tilesize

        super().__init__(
            (size[0] * self.tsize[0], size[1] * self.tsize[1]),
            flags = pg.SRCALPHA
        )

    def set(self, loc, key):
        loc = (loc[0] * self.tsize[0], loc[1] * self.tsize[1])
        self.blit(tset.get(key), loc)

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
    Scenes consist of a background Layer and foreground elements (particles
    and sprites) that are drawn over the background.

    Scene automatically manages updating the screen when fg elements move.
        Scene draws groups back-to-front (group 0 is on top, group N is back)
            within groups, sprites are ordered based upon y position (and offset
            if a drawheightoffset is specified)

    """
    def __init__(self, size, tilesize, elementgroups = 1, defaultgroup = 0):
        self.bg = Layer(size, tilesize)
        super().__init__(self.bg.get_size())

        self.tsize = tilesize

        self.dgroup = defaultgroup
        self.groups = []
        for i in range(elementgroups):
            self.groups.append(pg.sprite.LayeredUpdates())
        self.pspawners = []

    def add(self, element, group = -1):
        if isinstance(element, pg.sprite.Sprite):
            if group == -1:
                group = self.dgroup
            self.groups[group].add(element)
        return element

    def add_pspawner(self, pspawner):
        self.pspawners.append(pspawner)

    def update(self, dt):
        self.blit(self.bg, (0, 0))

        for spawner in self.pspawners:
            spawner.update(dt)

        for group in self.groups[::-1]:
            group.update(dt)

            #determine sprite layers (this looks hacky and slow but it runs better than the more complicated stuff I tried)
            for sprite in group.sprites():
                group.change_layer(sprite, sprite.draw_height())

            group.draw(self)
