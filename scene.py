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
        self.blit(tset.get_tile(key), loc)

    """
    write allows writing an iterable of keys
    if you have loaded a font, it will also write strings
        wrapping will not cut off words, but push them to the next line
        automatically handles newline and tab characters
            tab may not behave as expected with very small wrap lengths
    wrap:
        pass a wrap > 0 to wrap after wrap index
            if wrap is smaller than the longest word, then the word will be cut off
        if wrap is 0 or no wrap is passed, iterable will automatically wrap at
        the end of the layer
        if wrap is negative, no
    """
    def write(self, loc, iterable, wrap = 0):
        lines = []

        # automatically wrap inside
        if wrap == 0:
            wrap = self.size[0]

        # wrap iterable, format string
        if type(iterable) is str:
            line = ""
            for c in iterable:
                if c == '\n':
                    lines.append(line)
                    line = ""
                elif c == '\t':
                    line += "    "
                else:
                    line += c

                if wrap > 0 and len(line) >= wrap:
                    # don't cut words off if possible
                    word = ""
                    found = False
                    for c2 in line[::-1]:
                        if c2 == ' ':
                            found = True
                            break
                        else:
                            word = c2 + word

                    if found:
                        lines.append(line[:-len(word) - 1])
                        line = word
                    else: # wrap is smaller than the word, cut it off
                        lines.append(line)
                        line = ""

            if len(line) > 0:
                lines.append(line)

        else: # non-string iterable
            if wrap > 0:
                lines = [iterable[i:i + wrap] for i in range(0, len(iterable), wrap)]
            else:
                lines = [iterable]

        # write wrapped and formatted lines
        for i in range(len(lines)):
            if loc[1] + i >= self.size[1]:
                break

            self.__write((loc[0], loc[1] + i), lines[i])

    # writes a single line, no formatting attempts
    def __write(self, loc, iterable):
        for i in range(len(iterable)):
            self.set((loc[0] + i, loc[1]), iterable[i])

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

        self.spawners = []
        self.dgroup = defaultgroup
        self.groups = []
        for i in range(elementgroups):
            self.groups.append(pg.sprite.LayeredUpdates())

    def add(self, element, group = None):
        if isinstance(element, pg.sprite.Sprite):
            if group is None:
                group = self.dgroup
            self.groups[group].add(element)
        return element

    def add_spawner(self, spawner):
        spawner.scene = self
        self.spawners.append(spawner)

    def update(self, dt):
        self.fill((0, 0, 0))
        self.blit(self.bg, (0, 0))

        for spawner in self.spawners:
            spawner.update(dt)

        for group in self.groups[::-1]:
            group.update(dt)

            #determine sprite layers (this looks hacky and slow but it runs better than the more complicated stuff I tried)
            for sprite in group.sprites():
                group.change_layer(sprite, sprite.draw_height())

            group.draw(self)
