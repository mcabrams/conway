from .cell import Cell
from .location import (LocationGrid, Location, sort_locations)

DEFAULT_MIN_LOCATION = Location(0, 0)
DEFAULT_MAX_LOCATION = Location(0, 0)


class World():
    def __init__(self, min_location=DEFAULT_MIN_LOCATION,
                 max_location=DEFAULT_MAX_LOCATION):
        self._cells = {}
        self.min_location = min_location
        self.max_location = max_location

    @classmethod
    def empty(cls, *args, **kwargs):
        return cls(*args, **kwargs)

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
        # Shortcoming is that this only accounts for living cells
        for location, cell in self._cells.items():
            neighbor_count = self._get_living_neighbor_count(location)
            if not cell.is_alive_next_generation(neighbor_count):
                cell.die()

        return self

        # To handle shortcoming where we only iterate over cells that are in
        # the living cell we need to incorporate some way of iterating over
        # cells that are dead as well. One thought is to rely on getting a
        # grid location (all possible locations) and then a sort location
        # (which will cover living cells), and then we should be able to
        # iterate over all. We likely need someway handling cells that are on
        # the border of are grid (maybe not, we'll see). Another thought that
        # comes to mind is whether the current model for location grid should
        # be modified; in this case we really need a list of locations, and
        # don't care much about the y/x index, but we do care about whether
        # a  cell is dead or alive.

    @property
    def is_empty(self):
        return len(self._living_cells) == 0

    @property
    def dead_cell_count(self):
        x_length = self.max_location.x - self.min_location.x + 1
        y_length = self.max_location.y - self.min_location.y + 1
        return (x_length * y_length) - len(self._living_cells)

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


class WorldRenderer():
    def __init__(self, world):
        self.world = world

    def render(self):
        living_locations = self.world.living_locations

        sorted_locations = sort_locations(living_locations)
        location_grid = LocationGrid(self.world.min_location,
                                     self.world.max_location)

        rendering = ''

        location_lists = sorted_locations.values()
        sorted_locations = [sub_location
                            for location_list in location_lists
                            for sub_location in location_list]

        grid_locations_sorted_by_y_desc = sorted(location_grid.get_rows().items(),
                                                 key=lambda item: item[0],
                                                 reverse=True)

        for y_coordinate, y_row_locations in grid_locations_sorted_by_y_desc:
            if y_coordinate != self.world.max_location.y:
                rendering += '\n'

            rendering += self._render_row(y_row_locations, sorted_locations)

        return rendering

    def _render_row(self, row_locations, living_locations):
        rendering = ''

        for location in row_locations:
            rendering += '+' if location in living_locations else '-'

        return rendering
