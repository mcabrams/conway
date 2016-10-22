import unittest

from conway import Cell, Location, World


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

    def test_can_get_cell_at_location(self):
        world = World()
        world.set_living_at(self.location)
        self.assertIsInstance(world.get_cell_at(self.location), Cell)

    def test_get_cell_at_location_without_cell_returns_none(self):
        world = World()
        self.assertIsNone(world.get_cell_at(self.location))

class CellTestCase(unittest.TestCase):
    def setUp(self):
        self.location = Location(1, 1)

    def test_a_new_cell_is_alive(self):
        cell = Cell(self.location)
        self.assertTrue(cell.is_alive)

    def test_a_cell_can_be_set_dead(self):
        cell = Cell(self.location, alive=False)
        self.assertFalse(cell.is_alive)

    def test_cell_is_at_location(self):
        for coordinates in [(0, 0), (10, 10)]:
            location = Location(*coordinates)
            cell = Cell(location)
            self.assertTrue(cell.is_at(location))

unittest.main()
