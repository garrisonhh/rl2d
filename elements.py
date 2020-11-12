from pygame import Rect, sprite, Surface
from rl2d import tileset

class Sprite(sprite.Sprite):
    """
    Sprite assumes that it is the same size as the tilesize, unless spritesize is specified
        the bottom center of the sprite will always be the at the bottom center of the tile, regardless of sprite size
    """
    def __init__(self, tilesize, location, image, grouplayer = 0, drawheightoffset = 0, static = False):
        super().__init__()

        self.image = image
        self.rect = Rect(0, 0, *tilesize)
        self._layer = grouplayer # for ElementGroup

        self.tsize = tilesize
        self.dhoffset = drawheightoffset * self.tsize[1]
        self.static = static # whether sprite is drawn relative to screen, or the Scene() origin
        self.animated = isinstance(self.image, SpriteAnimation)

        #detect image
        if self.animated:
            self.rect = Rect(0, 0, *self.image.spritesize)
        elif not isinstance(self.image, Surface):
            self.image = tileset.get_tile(image)

        #movement vars
        self.curpos = (0, 0) #current position, because Rect doesn't take float arguments
        self.dstloc = (0, 0) #location after motion
        self.movvec = (0, 0) #offset in 1000 ms (1s)
        self.movdur = 0 #duration of movement remaining

        self.__setabsloc(location)

    """
    boolean moving
    """
    def moving(self):
        return self.movdur > 0

    """
    move to absolute location with __move
    """
    def move_abs(self, loc, duration = 0):
        self.__move((loc[0] - self.dstloc[0], loc[1] - self.dstloc[1]), loc, duration)

    """
    move by offset with __move
    """
    def move_rel(self, rel, duration = 0):
        self.__move(rel, (rel[0] + self.dstloc[0], rel[1] + self.dstloc[1]), duration)

    """
    current location on grid
    """
    def cur_loc(self):
        return self.__descale((self.rect.x, self.rect.y))

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

    # called by Scene().update(dt)
    def update(self, dt):
        if self.animated:
            self.image.update(dt)

        # movement
        if self.movdur != 0:
            # move along vector
            time = dt / 1000
            dx, dy = self.__scale((time * self.movvec[0], time * self.movvec[1]))
            self.curpos = (self.curpos[0] + dx, self.curpos[1] + dy)
            self.rect.midbottom = (self.curpos[0] + (self.tsize[0] / 2), self.curpos[1] + self.tsize[1])

            # if move duration is finite, tick move duration down until 0
            if self.movdur > 0:
                self.movdur -= dt

                if self.movdur <= 0:
                    self.movdur = 0
                    self.__setabsloc(self.dstloc)

class Particle(Sprite):
    """
    particles are sprites with a limited lifespan (in ms)
    they spawn with the center at loc rather than the top left corner
    give particles an animation for the cool effects u want!
    """
    def __init__(self, tilesize, location, image, lifespan, vector = 0, **kwargs):
        super().__init__(tilesize, location, image, **kwargs)

        self.lifespan = lifespan
        self.age = 0

        if vector:
            self.move_rel(vector, -1)

    # called by Scene().update(dt)
    def update(self, dt):
        self.age += dt

        if self.age >= self.lifespan:
            self.kill()
            return

        super().update(dt)

class SpriteAnimation(Surface):
    """
    animations should be a dict for each row of the image
        image will choose the first row
        key will be the name of the animation
        value can be:
            tuple (numFrames, durationFrames)
            list [duration0, duration1, ... durationN]
        Sprite.anims will become a dict of {key : [(frame0, dur0), (frame1, dur1), ... (frameN, durN)]}
    frame durations:
        dur >= 0 will play for at least one frame, and go to next frame after 'dur' ms
        dur < 0 will stop forever
    """
    def __init__(self, spritesize, image, animations, default_anim = 0):
        super().__init__(spritesize)

        self.spritesize = spritesize
        self.frame = 0 # current frame
        self.framedur = 0 # ms left on current frame
        self.anims = {}
        self.anim = 0 # current animation list from self.anims

        # get anim dict
        w, h = self.spritesize
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

        self.set_anim(default_anim)

    """
    change animation
    """
    def set_anim(self, key, frame = 0):
        self.frame = frame
        self.anim = self.anims[key]
        self.image, self.framedur = self.anim[self.frame]
        self.__draw()

    def __draw(self):
        super().blit(self.anim[self.frame][0], (0, 0))

    # called by Sprite().update(dt)
    def update(self, dt):
        # animate as necessary
        if self.anim[self.frame][1] >= 0:
            self.framedur -= dt

            if self.framedur <= 0:
                self.frame += 1
                self.frame %= len(self.anim)
                self.framedur = max(self.framedur + self.anim[self.frame][1], 0)
                self.__draw()

class ElementGroup(sprite.LayeredUpdates):
    """
    sorts sprites within each layer based upon their bottom y position and their draw height offset
    """
    def order_sprites(self):
        # pop sprites, sort into layers
        layers = {}
        maxlayer = 0
        while len(self._spritelist) > 0:
            spr = self._spritelist.pop()
            layer = self._spritelayers[spr]
            if layer in layers:
                layers[layer].append(spr)
            else:
                layers[layer] = [spr]

            if layer > maxlayer:
                maxlayer = layer

        # sort each layer and add back to group
        sort = lambda spr: spr.rect.bottom + spr.dhoffset
        for i in range(maxlayer + 1):
            if i in layers:
                self._spritelist += sorted(layers[i], key = sort)

    """
    draw sprites to surface in order, returns updated rects on screen
    pass an origin to change blit location for entire group
    """
    def draw(self, surface, origin = (0, 0)):
        updated = self.lostsprites
        self.lostsprites = []

        for spr in self.sprites():
            sprpos = spr.rect.topleft
            if not spr.static:
                sprpos = [sprpos[i] + origin[i] for i in (0, 1)]

            rec = self.spritedict[spr]
            newrect = surface.blit(spr.image, sprpos)

            if rec is self._init_rect:
                updated.append(newrect)
            else:
                if newrect.colliderect(rec):
                    updated.append(newrect.union(rec))
                else:
                    updated.append(newrect)
                    updated.append(rec)
            self.spritedict[spr] = newrect

        return updated
