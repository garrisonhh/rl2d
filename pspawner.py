import random

class ParticleSpawner:
    """
    *WIP* not happy with the state of this implementation rn
    spawns a particle every interval +-variance milliseconds
    unusable in current state, need to extend and rewrite get_particle() to return a valid particle
    """
    def __init__(self, scene, interval, variance, group = 0):
        self.scene = scene
        self.interval = interval
        self.variance = variance
        self.group = group

        self.tick = 0

        self.__next_interval()

    def get_particle(self):
        return None

    def __next_interval(self):
        self.tick += self.interval + (random.randint(-self.variance, self.variance))

    def update(self, dt):
        self.tick -= dt

        if self.tick <= 0:
            self.scene.add(self.get_particle(), group = self.group)
            self.__next_interval()
