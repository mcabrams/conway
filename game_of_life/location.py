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


def get_min_coordinates_location(locations):
    """ From a list of Locations, get a location with coordinates representing
    the minimum x and y coordinate found in all location coordinates """
    location_with_min_x = min(locations, key=lambda location: location.x)
    location_with_min_y = min(locations, key=lambda location: location.y)
    return Location(location_with_min_x.x, location_with_min_y.y)


def get_max_coordinates_location(locations):
    """ From a list of Locations, get a location with coordinates representing
    the maximum x and y coordinate found in all location coordinates """
    location_with_max_x = max(locations, key=lambda location: location.x)
    location_with_max_y = max(locations, key=lambda location: location.y)
    return Location(location_with_max_x.x, location_with_max_y.y)


class LocationGrid:
    def __init__(self, lower_bound_location, upper_bound_location):
        """
        args:
            lower_bound_location: a location with coordinates representing
                minimum x and y coordinates to be represented in location grid
            upper_bound_location: a location with coordinates representing
                maximum x and y coordinates to be represented in location grid
        """
        self.lower_bound_location = lower_bound_location
        self.upper_bound_location = upper_bound_location

    def get_rows(self):
        """ Returns dict with keys corresponding to x coordinates (ascending), and
        values that are lists of locations that fall in that x coordinate, in
        ascending y coordinate value.
        """
        rows = defaultdict(list)

        x_range = range(self.lower_bound_location.x,
                        self.upper_bound_location.x + 1)
        y_range = range(self.lower_bound_location.y,
                        self.upper_bound_location.y + 1)

        locations = []
        for x in x_range:
            for y in y_range:
                locations.append(Location(x, y))

        rows = sort_locations(locations)

        return rows


def sort_locations(locations):
    """ Returns dict with keys representing x-coordinate int, and value being
    a list of Locations containing that x-coordinate, sorted by y-coordinate
    in ascending order """

    rows = defaultdict(list)

    for location in locations:
        rows[location.y].append(location)
        rows[location.y].sort(key=lambda location: location.x)

    return rows
