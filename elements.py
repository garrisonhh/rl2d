import pygame as pg

def _scale(loc, tsize):
    return (loc[0] * tsize[0], loc[1] * tsize[1])

class Sprite(pg.sprite.Sprite):
    def __init__(self, image, loc, tsize):
        super().__init__()

        self.image = image
        self.rect = pg.Rect(*_scale(loc, tsize), *image.get_size())
        self.tsize = tsize

        #movement vars
        self.cur = loc #current location
        self.dest = loc #destination location
        self.move = 0
        self.totmove = 0

    #sprite moves to loc over time (in ms)
    def goto_loc(self, loc, time = 0):
        self.dest = loc

        if time == 0:
            self.rect.topleft = _scale(loc, self.tsize)
        else:
            self.move = time
            self.totmove = time

    def goto_rel(self, rel, time = 0):
        self.goto_loc((self.cur[0] + rel[0], self.cur[1] + rel[1]), time)

    def update(self, dt):
        #move if necessary
        if self.move > 0:
            dist = min(dt, self.move) / self.totmove
            self.move = max(self.move - dt, 0)

            if self.move == 0:
                self.rect.topleft = _scale(self.dest, self.tsize)
                self.cur = self.dest
            else:
                self.rect.topleft = _scale(
                    [self.dest[i] + (self.cur[i] - self.dest[i]) * (self.move / self.totmove) for i in (0, 1)],
                    self.tsize)

class Particle(Sprite):
    """
    particles are sprites with a limited lifespan
    they spawn with the center at loc rather than the top left corner
    particles can move TODO more features!
    """
    def __init__(self, image, loc, tsize, lifespan,
        reldest = None):
        super().__init__(image, loc, tsize)
        self.rect.center = loc

        self.lifespan = lifespan
        self.age = 0

        if reldest is not None:
            self.goto_rel(reldest, lifespan)

    def update(self, dt):
        if self.age >= self.lifespan:
            self.kill()
            return

        self.age += dt

        super().update(dt)
