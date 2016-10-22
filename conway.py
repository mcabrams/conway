class Location():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def coordinates(self):
        return (self.x, self.y)

    @property
    def neighbors(self):
        return [Location(x, y) for x, y in self._neighbor_coordinates()]

    def is_neighbor_of(self, location):
        return location.coordinates in self._neighbor_coordinates()

    def _neighbor_coordinates(self):
        neighbors_coordinates = []

        for x_offset in range(-1, 2):
            for y_offset in range(-1, 2):
                coordinates = (x_offset + self.x, y_offset + self.y)

                if coordinates == self.coordinates:
                    continue

                neighbors_coordinates.append(coordinates)

        return neighbors_coordinates


class World():
    def __init__(self):
        self.cells = []

    @classmethod
    def empty(cls):
        return cls()

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

    def tick(self):
        return self

    @property
    def is_empty(self):
        return len(self._living_cells) == 0

    @property
    def _living_cells(self):
        return [cell for cell in self.cells if cell.is_alive]

    @property
    def _living_cell_locations(self):
        return [lc.location for lc in self._living_cells]


class Cell():
    def __init__(self, location, alive=True):
        self.location = location
        self.alive = alive

    def is_at(self, location):
        return self.location.coordinates == location.coordinates

    @property
    def is_alive(self):
        return self.alive
