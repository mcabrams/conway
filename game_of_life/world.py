from random import randint

from .cell import Cell
from .location import LocationGrid, Location

DEFAULT_MIN_LOCATION = Location(0, 0)
DEFAULT_MAX_LOCATION = Location(0, 0)


class World():
    def __init__(self, min_location=DEFAULT_MIN_LOCATION,
                 max_location=DEFAULT_MAX_LOCATION):
        self._cells = {}
        # consider allowing getting of min/max location, but restricting setting
        # due to its tendency to potentially change when setting a living cell
        # TODO: Consider moving location_grid to world
        self.min_location = min_location
        self.max_location = max_location

    @classmethod
    def empty(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    @classmethod
    def random(cls, *args, cell_count=1, **kwargs):
        world = cls(*args, **kwargs)
        for _ in range(cell_count):
            world.randomly_set_living()

        return world

    def randomly_set_living(self):
        x = randint(self.min_location.x, self.max_location.x)
        y = randint(self.min_location.y, self.max_location.y)

        if self.is_alive_at(Location(x, y)):
            self.randomly_set_living()
        else:
            self.set_living_at(Location(x, y))

    def set_dead_at(self, location):
        cell = self._find_cell_at(location)
        if cell:
            cell.die()
        else:
            self._add_cell(Cell(alive=False), location)

    def set_living_at(self, location):
        if location.x > self.max_location.x:
            self.max_location = Location(location.x, self.max_location.y)

        if location.y > self.max_location.y:
            self.max_location = Location(self.max_location.x, location.y)

        if location.x < self.min_location.x:
            self.min_location = Location(location.x, self.min_location.y)

        if location.y < self.min_location.y:
            self.min_location = Location(self.min_location.x, location.y)

        self._add_cell(Cell(), location)

    def get_cell_at(self, location):
        cell = self._find_cell_at(location)
        if cell:
            return cell
        else:
            self.set_dead_at(location)
            return self.get_cell_at(location)

    def is_alive_at(self, location):
        return location in self.living_locations

    @property
    def living_locations(self):
        return [l for l, c in self._cells.items() if c.is_alive]

    def _get_living_neighbor_count(self, location):
        neighbor_locations = location.neighbors
        living_neighbor_cells = [self.get_cell_at(nl)
                                 for nl in neighbor_locations
                                 if self.is_alive_at(nl)]
        return len(living_neighbor_cells)

    def tick(self):
        new_locations = []
        world_locations = LocationGrid(self.min_location,
                                       self.max_location).locations

        for location in world_locations:
            cell = self.get_cell_at(location)
            neighbor_count = self._get_living_neighbor_count(location)
            is_alive_next_gen = cell.is_alive_next_generation(neighbor_count)
            new_locations.append((location, is_alive_next_gen))

        for location, is_alive in new_locations:
            if is_alive:
                self.set_living_at(location)
            else:
                self.set_dead_at(location)

        return self

    @property
    def is_empty(self):
        return self.living_cell_count == 0

    @property
    def dead_cell_count(self):
        x_length = self.max_location.x - self.min_location.x + 1
        y_length = self.max_location.y - self.min_location.y + 1
        return (x_length * y_length) - self.living_cell_count

    @property
    def living_cell_count(self):
        return len(self._living_cells)

    @property
    def dimensions(self):
        x_length = self.max_location.x - self.min_location.x + 1
        y_length = self.max_location.y - self.min_location.y + 1
        return (x_length, y_length)

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
