class Cell():
    STABLE_NEIGHBOR_RANGE = range(2, 4)
    FERTILE_NEIGHBOR_COUNT = 3

    def __init__(self, alive=True):
        self.alive = alive

    def die(self):
        self.alive = False

    @property
    def is_alive(self):
        return self.alive

    def is_alive_next_generation(self, neighbor_count):
        if self.is_alive:
            return self._has_stable_neighborhood(neighbor_count)
        else:
            return self._has_fertile_neighborhood(neighbor_count)

    def _has_stable_neighborhood(self, neighbor_count):
        return neighbor_count in self.STABLE_NEIGHBOR_RANGE

    def _has_fertile_neighborhood(self, neighbor_count):
        return neighbor_count == self.FERTILE_NEIGHBOR_COUNT
