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
        self._cells = []

    @classmethod
    def empty(cls):
        return cls()

    def set_dead_at(self, location):
        cell = self._find_cell_at(location)
        if cell:
            cell.kill()
        else:
            self._add_cell(Cell(location, self, alive=False))

    def set_living_at(self, location):
        self._add_cell(Cell(location, self))

    def get_cell_at(self, location):
        cell = self._find_cell_at(location)
        if cell:
            return cell
        else:
            self.set_dead_at(location)
            return self.get_cell_at(location)


    def is_alive_at(self, location):
        return location.coordinates in self._living_cell_coordinates

    def tick(self):
        return self

    @property
    def is_empty(self):
        return len(self._living_cells) == 0

    @property
    def _living_cells(self):
        return [cell for cell in self._cells if cell.is_alive]

    @property
    def _living_cell_locations(self):
        return [lc.location for lc in self._living_cells]

    @property
    def _living_cell_coordinates(self):
        return [lcl.coordinates for lcl in self._living_cell_locations]

    def _add_cell(self, cell):
        self._cells.append(cell)

    def _find_cell_at(self, location):
        cells_at_location = [c for c in self._cells if c.is_at(location)]
        if cells_at_location:
            return cells_at_location[0]
        else:
            return None



class Cell():
    def __init__(self, location, world, alive=True):
        self.world = world
        self.location = location
        self.alive = alive

    def is_at(self, location):
        return self.location.coordinates == location.coordinates

    def kill(self):
        self.alive = False

    @property
    def is_alive(self):
        return self.alive

    @property
    def is_alive_next_generation(self):
        if not self.is_alive and self._living_neighbor_count == 3:
            return True

        if self._living_neighbor_count > 3:
            return False

        if self._living_neighbor_count > 2:
            return True

        return False

    @property
    def _living_neighbor_count(self):
        neighbor_locations = self.location.neighbors
        living_neighbor_cells = [self.world.get_cell_at(nl)
                                 for nl in neighbor_locations
                                 if self.world.is_alive_at(nl)]
        return len(living_neighbor_cells)

