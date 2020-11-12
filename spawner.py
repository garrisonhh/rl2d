import random

class Spawner:
    """
    spawns an element every interval +-variance milliseconds
    pass a constructor function, assumes that constructor() will return a valid element
    """
    def __init__(self, constructor, interval, variance):
        self.scene = None # this is set in rl2d.Scene.add_spawner
        self.constructor = constructor
        self.interval = interval
        self.variance = variance

        self.tick = 0

        self.__next_interval()

    def __next_interval(self):
        self.tick += self.interval + (random.randint(-self.variance, self.variance))

    def update(self, dt):
        self.tick -= dt

        if self.tick <= 0:
            self.scene.add(self.constructor())
            self.__next_interval()
