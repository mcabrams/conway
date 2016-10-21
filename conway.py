class World():
    def __init__(self):
        self.cells = []

    @property
    def _living_cells(self):
        return [cell for cell in self.cells if cell.is_alive]

    @property
    def living_cell_coordinates(self):
        return [lc.coordinates for lc in self._living_cells]

    def set_dead_at(self, x, y):
        cells_to_kill = [c for c in self.cells if c.is_at(x, y)]

        for cell in cells_to_kill:
            self.cells.remove(cell)

    def set_living_at(self, x, y):
        self.cells.append(Cell(x, y))

    def is_alive_at(self, x, y):
        return (x, y) in self.living_cell_coordinates

    @property
    def is_empty(self):
        return len(self._living_cells) == 0


class Cell():
    def __init__(self, x, y, alive=True):
        self.x = x
        self.y = y
        self.alive = alive

    def is_at(self, x, y):
        return self.coordinates == (x, y)

    @property
    def coordinates(self):
        return (self.x, self.y)

    @property
    def is_alive(self):
        return self.alive
