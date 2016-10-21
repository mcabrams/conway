class World():
    def __init__(self):
        self.living_cells = []

    def set_living_at(self, x, y):
        self.living_cells.append((x, y))

    def is_alive_at(self, x, y):
        return (x, y) in self.living_cells

    @property
    def is_empty(self):
        return len(self.living_cells) == 0
