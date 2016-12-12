from .cell import Cell
from .location import (get_max_coordinates_location,
                       get_min_coordinates_location, sort_locations,
                       get_location_grid)


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


class WorldRenderer():
    def __init__(self, world):
        self.world = world

    def render(self):
        living_locations = self.world.living_locations

        if not living_locations:
            return '-'

        lower_bound_location = get_min_coordinates_location(living_locations)
        upper_bound_location = get_max_coordinates_location(living_locations)

        sorted_locations = sort_locations(living_locations)
        grid_locations = get_location_grid(lower_bound_location,
                                           upper_bound_location)

        rendering = ''

        location_lists = sorted_locations.values()
        sorted_locations = [sub_location
                            for location_list in location_lists
                            for sub_location in location_list]

        grid_locations_sorted_by_y_desc = sorted(grid_locations.items(),
                                                 key=lambda item: item[0],
                                                 reverse=True)

        for y_coordinate, y_row_locations in grid_locations_sorted_by_y_desc:
            if y_coordinate != upper_bound_location.y:
                rendering += '\n'

            rendering += self._render_row(y_row_locations, sorted_locations)

        return rendering

    def _render_row(self, row_locations, living_locations):
        rendering = ''

        for location in row_locations:
            rendering += '+' if location in living_locations else '-'

        return rendering
