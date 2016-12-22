from .location import LocationGrid

LIVE_CELL_CHAR = ' +'
DEAD_CELL_CHAR = ' -'


class WorldRenderer():
    def __init__(self, world):
        self.world = world

    def render(self):
        living_locations = self.world.living_locations

        rendering = ''

        location_grid = LocationGrid(self.world.min_location,
                                     self.world.max_location)

        for y_coordinate, y_row_locations in location_grid.rows.items():
            if y_coordinate != self.world.max_location.y:
                rendering += '\n'

            rendering += self._render_row(y_row_locations, living_locations)

        return rendering

    def _render_row(self, row_locations, living_locations):
        rendering = ''

        for location in row_locations:
            is_alive = location in living_locations
            rendering += LIVE_CELL_CHAR if is_alive else DEAD_CELL_CHAR

        return rendering
