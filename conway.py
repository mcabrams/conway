from collections import namedtuple


class Location(namedtuple('Location', ['x', 'y'])):
    @property
    def coordinates(self):
        return (self.x, self.y)

    @property
    def neighbors(self):
        return [Location(x, y) for x, y in self._neighbor_coordinates()]

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
        self._cells = {}

    @classmethod
    def empty(cls):
        return cls()

    def set_dead_at(self, location):
        cell = self._find_cell_at(location)
        if cell:
            cell.die()
        else:
            self._add_cell(Cell(alive=False), location)

    def set_living_at(self, location):
        self._add_cell(Cell(), location)

    def get_cell_at(self, location):
        cell = self._find_cell_at(location)
        if cell:
            return cell
        else:
            self.set_dead_at(location)
            return self.get_cell_at(location)

    def is_alive_at(self, location):
        living_locations = [l for l, c in self._cells.items() if c.is_alive]
        return location in living_locations

    def _get_living_neighbor_count(self, location):
        neighbor_locations = location.neighbors
        living_neighbor_cells = [self.get_cell_at(nl)
                                 for nl in neighbor_locations
                                 if self.is_alive_at(nl)]
        return len(living_neighbor_cells)

    def tick(self):
        for location, cell in self._cells.items():
            neighbor_count = self._get_living_neighbor_count(location)
            if not cell.is_alive_next_generation(neighbor_count):
                cell.die()

        return self

    @property
    def is_empty(self):
        return len(self._living_cells) == 0

    @property
    def _living_cells(self):
        return [cell
                for location, cell in self._cells.items()
                if cell.is_alive]

    def _add_cell(self, cell, location):
        self._cells[location] = cell

    def _find_cell_at(self, location):
        cells_at_location = [c
                             for l, c in self._cells.items()
                             if l == location]
        if cells_at_location:
            return cells_at_location[0]
        else:
            return None


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
