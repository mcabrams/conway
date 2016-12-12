from collections import defaultdict, namedtuple


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


def get_min_coordinates(locations):
    location_with_min_x = min(locations, key=lambda location: location.x)
    location_with_min_y = min(locations, key=lambda location: location.y)
    return location_with_min_x.x, location_with_min_y.y


def get_max_coordinates(locations):
    location_with_max_x = max(locations, key=lambda location: location.x)
    location_with_max_y = max(locations, key=lambda location: location.y)
    return location_with_max_x.x, location_with_max_y.y


def get_location_grid(lower_bound_location, upper_bound_location):
    """ Returns dict with keys corresponding to x coordinates (ascending), and
    values that are lists of locations that fall in that x coordinate, in
    ascending y coordinate value.

    args:
        lower_bound_location: a location with coordinates representing minimum
            x and y coordinates to be represented in location grid
        upper_bound_location: a location with coordinates representing maximum
            x and y coordinates to be represented in location grid
    """
    rows = defaultdict(list)

    x_range = range(lower_bound_location.x, upper_bound_location.x + 1)
    y_range = range(lower_bound_location.y, upper_bound_location.y + 1)

    locations = []
    for x in x_range:
        for y in y_range:
            locations.append(Location(x, y))

    rows = sort_locations(locations, indexed_by='y')

    return rows


def sort_locations(locations, indexed_by='x'):
    """ Returns dict with keys representing x-coordinate int, and value being
    a list of Locations containing that x-coordinate, sorted by y-coordinate
    in ascending order """

    if indexed_by not in ('x', 'y'):
        raise ValueError("indexed_by must either be 'x' or 'y'!")

    rows = defaultdict(list)

    for location in locations:
        locations_index_key = getattr(location, indexed_by)

        values_ascend_by = 'y' if indexed_by == 'x' else 'x'

        rows[locations_index_key].append(location)
        rows[locations_index_key].sort(
            key=lambda location: getattr(location, values_ascend_by))

    return rows


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

        min_coordinate = get_min_coordinates(living_locations)
        max_coordinate = get_max_coordinates(living_locations)
        lower_bound_location = Location(*min_coordinate)
        upper_bound_location = Location(*max_coordinate)

        sorted_locations = sort_locations(living_locations, indexed_by='y')
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
