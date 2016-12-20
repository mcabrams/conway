from .location import Location
from .world import World


def render_to_world(render):
    if not render:
        return World.empty()
    else:
        rows = render.split('\n')
        height = len(rows)
        width = len(rows[0])
        world = World.empty(min_location=Location(0, 0),
                            max_location=Location(width - 1, height - 1))

        for y_delta, row in enumerate(rows, start=1):
            cells = list(row)

            for x_coordinate, cell in enumerate(cells):
                if cell == '+':
                    y_coordinate = height - y_delta
                    world.set_living_at(Location(x_coordinate, y_coordinate))

        return world
