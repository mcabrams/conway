class Location():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class World():
    def __init__(self):
        self.cells = []

    @property
    def _living_cells(self):
        return [cell for cell in self.cells if cell.is_alive]

    @property
    def _living_cell_locations(self):
        return [lc.location for lc in self._living_cells]

    def set_dead_at(self, location):
        cell = self.get_cell_at(location)
        if cell:
            self.cells.remove(cell)

    def set_living_at(self, location):
        self.cells.append(Cell(location))

    def get_cell_at(self, location):
        cells_at_location = [c for c in self.cells if c.is_at(location)]
        if cells_at_location:
            return cells_at_location[0]

        return None

    def is_alive_at(self, location):
        return location in self._living_cell_locations

    @property
    def is_empty(self):
        return len(self._living_cells) == 0


class Cell():
    def __init__(self, location, alive=True):
        self.location = location
        self.alive = alive

    def is_at(self, location):
        return self.location == location

    @property
    def is_alive(self):
        return self.alive
