import unittest

from conway import Cell, World

class WorldTestCase(unittest.TestCase):
    def test_a_new_world_is_empty(self):
        world = World()
        self.assertTrue(world.is_empty)

    def test_a_world_with_a_living_cell_is_not_empty(self):
        world = World()
        world.set_living_at(1, 1)
        self.assertFalse(world.is_empty)

    def test_a_new_worlds_cell_is_not_alive(self):
        world = World()
        self.assertFalse(world.is_alive_at(1, 1))

    def test_a_cell_can_be_added_to_the_world(self):
        world = World()
        world.set_living_at(1, 1)
        self.assertTrue(world.is_alive_at(1, 1))

    def test_a_cell_can_be_set_dead_at_coordinate(self):
        world = World()
        world.set_living_at(1, 1)
        world.set_dead_at(1, 1)
        self.assertFalse(world.is_alive_at(1, 1))


class CellTestCase(unittest.TestCase):
    def test_a_new_cell_is_alive(self):
        cell = Cell(0, 0)
        self.assertTrue(cell.is_alive)

    def test_a_cell_can_be_set_dead(self):
        cell = Cell(0, 0, alive=False)
        self.assertFalse(cell.is_alive)

    def test_can_set_cells_coordinates(self):
        for coordinates in [(0, 0), (10, 10)]:
            cell = Cell(*coordinates)
            self.assertEqual(cell.coordinates, coordinates)

    def test_cell_is_at_coordinate(self):
        for coordinates in [(0, 0), (10, 10)]:
            cell = Cell(*coordinates)
            self.assertTrue(cell.is_at(*coordinates))

unittest.main()
