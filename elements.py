import pygame as pg
import random

class Sprite(pg.sprite.Sprite):
    """
    Sprite assumes that it is the same size as the tilesize, unless spritesize is specified
        the bottom center of the sprite will always be the at the bottom center of the tile, regardless of sprite size
    if specified, animations should be a dict for each row of the image
        image will choose the first row
        key will be the name of the animation
        value can be:
            tuple (numFrames, durationFrames)
            list [duration0, duration1, ... durationN]
        Sprite.anims will become a dict of {key : [(frame0, dur0), (frame1, dur1), ... (frameN, durN)]}
    set startanim to an animation key to set the animation at initialization
        otherwise, it will attempt to access animations[0]
    """
    def __init__(self, tilesize, location, image, spritesize = 0, animations = 0, startanim = 0):
        super().__init__()

        self.image = 0
        self.rect = 0
        self.tsize = tilesize

        self.ssize = spritesize
        self.anims = 0
        self.anim = 0 # current animation arr
        self.frame = 0 # current frame
        self.framedur = 0 #time left on frame

        #detect sprite size as necessary
        if not self.ssize:
            #get sprite size (ssize)
            if image.get_width() != self.tsize[0] or image.get_height() != self.tsize[1]:
                self.ssize = image.get_size()
            else:
                self.ssize = self.tsize

        #get image(s)
        if animations:
            self.anims = {}
            w, h = self.ssize
            y = 0

            for k, v in animations.items():
                self.anims[k] = []

                if type(v) is tuple:
                    for i in range(v[0]):
                        self.anims[k].append((image.subsurface((i * w, y, w, h)), v[1]))
                elif type(v) is list:
                    for i in range(len(v)):
                        self.anims[k].append((image.subsurface((i * w, y, w, h)), v[i]))

                y += h

            self.set_anim(startanim)
        else:
            self.image = image

        self.rect = pg.Rect((0, 0, *self.ssize))

        #movement vars
        self.curpos = (0, 0) #current position, because Rect doesn't take float arguments
        self.dstloc = (0, 0) #location after motion
        self.movvec = (0, 0) #offset in 1000 ms (1s)
        self.movdur = 0 #duration of movement remaining

        self.__setabsloc(location)

    def moving(self):
        return self.movdur > 0

    def set_anim(self, key, frame = 0):
        self.anim = self.anims[key]
        self.frame = frame
        self.image, self.framedur = self.anim[frame]

    #move to absolute location with __move
    def move_abs(self, loc, duration = 0):
        self.__move((loc[0] - self.dstloc[0], loc[1] - self.dstloc[1]), loc, duration)

    #move by offset with __move
    def move_rel(self, rel, duration = 0):
        self.__move(rel, (rel[0] + self.dstloc[0], rel[1] + self.dstloc[1]), duration)

    def __scale(self, loc):
        return (loc[0] * self.tsize[0], loc[1] * self.tsize[1])

    def __descale(self, pos):
        return (pos[0] / self.tsize[0], pos[1] / self.tsize[1])

    #if duration < 0, moves forever and takes rel is a vector over 1000 ms
    def __move(self, rel, loc, dur):
        self.dstloc = (self.dstloc[0] + rel[0], self.dstloc[1] + rel[1])

        if (dur == 0): #teleport
            self.__setabsloc(loc)
        else:
            dscale = 1
            if dur > 0:
                dscale = 1000 / dur

            self.movdur = dur
            self.movvec = (rel[0] * dscale, rel[1] * dscale)

    def __setabsloc(self, loc):
        self.dstloc = loc
        self.curpos = self.__scale(loc)
        self.rect.midbottom = (self.curpos[0] + int(self.tsize[0] // 2), self.curpos[1] + self.tsize[1])

    def update(self, dt):
        #movement
        if self.movdur != 0:
            #move along vector
            time = dt / 1000
            dx, dy = self.__scale((time * self.movvec[0], time * self.movvec[1]))
            self.curpos = (self.curpos[0] + dx, self.curpos[1] + dy)
            self.rect.midbottom = (self.curpos[0] + (self.tsize[0] / 2), self.curpos[1] + self.tsize[1])

            #if move duration is finite, tick move duration down until 0
            if self.movdur > 0:
                self.movdur -= dt

                if self.movdur <= 0:
                    self.movdur = 0
                    self.__setabsloc(self.dstloc)

        #animate as necessary
        if self.anims and len(self.anim) > 1:
            self.framedur -= dt

            if self.framedur <= 0:
                self.frame += 1
                self.frame %= len(self.anim)

                self.image = self.anim[self.frame][0]
                self.framedur += self.anim[self.frame][1]

class Particle(Sprite):
    """
    particles are sprites with a limited lifespan
    they spawn with the center at loc rather than the top left corner
    particles can move over lifespan by setting rel to an offset
        unsure of what other features to add
            rotating/scaling doesn't make sense for pixelated format
        give particles an animation for the cool effects u want!
    """
    def __init__(self, tilesize, location, image, lifespan, vector = 0, **kwargs):
        super().__init__(tilesize, location, image, **kwargs)

        self.lifespan = lifespan
        self.age = 0

        if vector:
            self.move_rel(vector, -1)

    def update(self, dt):
        self.age += dt

        if self.age >= self.lifespan:
            self.kill()
            return

        super().update(dt)

class ParticleSpawner:
    """
    *WIP* not happy with the state of this implementation rn
    spawns a particle every interval +-variance milliseconds
    unusable in current state, need to extend and rewrite get_particle() to return a valid particle
    """
    def __init__(self, scene, interval, variance):
        self.scene = scene
        self.interval = interval
        self.variance = variance

        self.tick = 0

        self.__next_interval()

    def get_particle(self):
        return None

    def __next_interval(self):
        self.tick += self.interval + (random.randint(-self.variance, self.variance))

    def update(self, dt):
        self.tick -= dt

        if self.tick <= 0:
            self.scene.add(self.get_particle())
            self.__next_interval()
