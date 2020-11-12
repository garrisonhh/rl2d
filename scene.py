import pygame as pg
from rl2d.elements import *
from rl2d import tileset

class Layer(pg.Surface):
    """
    Layers have basic functionality for drawing tilesets onto a grid.
    """
    def __init__(self, tilesize, size):
        self.tsize = tilesize
        self.size = size

        super().__init__(
            (size[0] * self.tsize[0], size[1] * self.tsize[1]),
            flags = pg.SRCALPHA)

    """
    draw tile 'key' at (x, y) 'loc'
    """
    def set(self, loc, key):
        self.blit(tileset.get_tile(key), (loc[0] * self.tsize[0], loc[1] * self.tsize[1]))

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

    """
    draw tile 'key' in a filled rectangle (x, y, w, h) 'rect'
    """
    def box(self, rect, key):
        for y in range(rect[1], rect[1] + rect[3]):
            for x in range(rect[0], rect[0] + rect[2]):
                self.set((x, y), key)

    """
    fill layer with tile 'key'
    """
    def fill(self, key):
        self.box((0, 0, *self.size), key)

class OffsetLayer(Layer):
    """
    the same as Layer, except with a **PIXEL** offset (x, y) that can be moved around
    """
    def __init__(self, tilesize, size, origin = (0, 0)):
        super().__init__(tilesize, size)

        self.origin = list(origin)

    def set(self, loc, key):
        self.blit(tileset.get_tile(key), [(loc[i] * self.tsize[i]) + self.origin[i] for i in (0, 1)])

    def move_origin(self, rel):
        self.set_origin([self.origin[i] + rel[i] for i in (0, 1)])

    def set_origin(self, origin):
        self.origin = list(origin)
        self.clear_artifacts()

    # moving the origin leaves annoying artifacts on the screen, this removes them
    def clear_artifacts(self, bg_color = (0, 0, 0)):
        r1 = r2 = 0
        w, h = self.get_size()

        if self.origin[0] >= 0:
            r1 = (0, 0, self.origin[0], h)
        else:
            r1 = (self.origin[0] + w, 0, w - self.origin[0], h)

        if self.origin[1] >= 0:
            r2 = (0, 0, w, self.origin[1])
        else:
            r2 = (0, self.origin[1] + h, w, h - self.origin[1])

        #print(r1, r2)

        for r in r1, r2:
            pg.Surface.fill(self, bg_color, [int(v + .5) for v in r])

class Scene(pg.Surface):
    """
    Scenes consist of a background Layer and foreground elements (particles
    and sprites) that are drawn over the background.
    """
    def __init__(self, tilesize, size, origin = (0, 0)):
        self.bg = OffsetLayer(tilesize, size, origin = origin)
        super().__init__(self.bg.get_size())

        self.spawners = []
        self.group = ElementGroup()

    # origin ops affect both bg and fg elements, so wrapping them here
    def move_origin(self, rel):
        self.bg.move_origin(rel)

    def set_origin(self, origin):
        self.bg.set_origin(origin)

    """
    add element 'element' to Scene
    use Sprite kwarg 'layer' to change group player being placed on
    """
    def add(self, element):
        self.group.add(element)
        return element

    """
    add spawner 'spawner' to scene
    """
    def add_spawner(self, spawner):
        spawner.scene = self
        self.spawners.append(spawner)

    """
    call with a pg.time.Clock().get_time() for dt
    """
    def update(self, dt):
        self.fill((0, 0, 0))
        self.blit(self.bg, (0, 0))

        for spawner in self.spawners:
            spawner.update(dt)

        self.group.update(dt)
        self.group.order_sprites()
        self.group.draw(self, self.bg.origin)
