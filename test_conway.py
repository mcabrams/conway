import unittest

from conway import Cell, Location, World


class LocationTestCase(unittest.TestCase):
    def test_location_has_coordinates(self):
        location = Location(1, 1)
        self.assertEqual(location.coordinates, (1, 1))

    def test_neighbors(self):
        location = Location(0, 0)
        expected_neighbor_coordinates = [(0, 1), (1, 1), (1, 0), (1, -1),
                                         (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        actual = [n.coordinates for n in location.neighbors]
        self.assertEqual(set(expected_neighbor_coordinates), set(actual))

    def test_is_neighbor_of(self):
        neighbor = Location(0, 0)
        location = Location(0, 1)
        self.assertTrue(neighbor.is_neighbor_of(location))

    def test_distant_location_is_not_neighbor_of(self):
        distant_location = Location(0, 0)
        location = Location(0, 2)
        self.assertFalse(distant_location.is_neighbor_of(location))


class WorldTestCase(unittest.TestCase):
    def setUp(self):
        self.location = Location(1, 1)

    def test_a_new_world_is_empty(self):
        world = World()
        self.assertTrue(world.is_empty)

    def test_a_world_with_a_living_cell_is_not_empty(self):
        world = World()
        world.set_living_at(self.location)
        self.assertFalse(world.is_empty)

    def test_a_new_worlds_cell_is_not_alive(self):
        world = World()
        self.assertFalse(world.is_alive_at(self.location))

    def test_a_cell_can_be_added_to_the_world(self):
        world = World()
        world.set_living_at(self.location)
        self.assertTrue(world.is_alive_at(self.location))

    def test_a_cell_can_be_set_dead_at_location(self):
        world = World()
        world.set_living_at(self.location)
        world.set_dead_at(self.location)
        self.assertFalse(world.is_alive_at(self.location))

    def test_a_cell_can_be_set_dead_at_location_if_already_dead(self):
        world = World()
        world.set_living_at(self.location)
        world.set_dead_at(self.location)
        world.set_dead_at(self.location)
        self.assertFalse(world.is_alive_at(self.location))

    def test_a_cell_can_be_set_dead_at_location_if_never_set_living(self):
        world = World()
        world.set_dead_at(self.location)
        self.assertFalse(world.is_alive_at(self.location))

    def test_cell_can_be_set_dead_and_retrieved_if_never_set_living(self):
        world = World()
        world.set_dead_at(self.location)
        self.assertIsInstance(world.get_cell_at(self.location), Cell)

    def test_is_alive_at_not_dependent_on_location_instance(self):
        world = World()
        world.set_living_at(self.location)
        location = Location(*self.location.coordinates)
        self.assertTrue(world.is_alive_at(location))

    def test_can_get_cell_at_location(self):
        world = World()
        world.set_living_at(self.location)
        self.assertIsInstance(world.get_cell_at(self.location), Cell)

    def test_get_cell_at_location_without_cell_returns_dead_cell(self):
        world = World()
        self.assertIsInstance(world.get_cell_at(self.location), Cell)
        self.assertFalse(world.get_cell_at(self.location).is_alive)

    def test_an_empty_world_stays_empty_after_a_tick(self):
        world = World.empty()
        next_world = world.tick()
        self.assertTrue(next_world.is_empty)


class CellTestCase(unittest.TestCase):
    location_coordinates = (0, 0)
    neighbor_coordinates = [(0, 1), (1, 1), (1, 0), (1, -1),
                            (0, -1), (-1, -1), (-1, 0), (-1, 1)]

    def _add_living_neighbors(self, count):
        for coordinates in self.neighbor_coordinates[:count]:
            self.world.set_living_at(Location(*coordinates))

    def setUp(self):
        self.location = Location(*self.location_coordinates)
        self.world = World()

    def test_a_new_cell_is_alive(self):
        cell = Cell(self.location, self.world)
        self.assertTrue(cell.is_alive)

    def test_a_killed_cell_is_not_alive(self):
        cell = Cell(self.location, self.world)
        cell.kill()
        self.assertFalse(cell.is_alive)

    def test_a_cell_can_be_set_dead(self):
        cell = Cell(self.location, self.world, alive=False)
        self.assertFalse(cell.is_alive)

    def test_cell_is_at_location(self):
        for coordinates in [(0, 0), (10, 10)]:
            location = Location(*coordinates)
            cell = Cell(location, self.world)
            self.assertTrue(cell.is_at(Location(*coordinates)))

    def test_cell_is_dead_next_generation_if_fewer_than_2_live_neighbors(self):
        self.world.set_living_at(self.location)
        cell = self.world.get_cell_at(self.location)
        self.assertFalse(cell.is_alive_next_generation)

    def test_cell_is_alive_next_generation_if_3_neighbors(self):
        self.world.set_living_at(self.location)
        self._add_living_neighbors(3)

        cell = self.world.get_cell_at(self.location)

        self.assertTrue(cell.is_alive_next_generation)

    def test_cell_is_dead_from_overcrowding_next_gen_if_4_neighbors(self):
        self.world.set_living_at(self.location)
        self._add_living_neighbors(4)

        cell = self.world.get_cell_at(self.location)

        self.assertFalse(cell.is_alive_next_generation)

    def test_lone_dead_cell_is_dead_next_generation(self):
        self.world.set_dead_at(self.location)
        cell = self.world.get_cell_at(self.location)
        self.assertFalse(cell.is_alive_next_generation)

    def test_dead_cell_with_three_living_neighbors_is_alive_next_gen(self):
        self.world.set_dead_at(self.location)
        self._add_living_neighbors(3)

        cell = self.world.get_cell_at(self.location)

        self.assertTrue(cell.is_alive_next_generation)

unittest.main()
