import unittest
from unittest.mock import Mock

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

    def test_instances_of_location_with_same_coordinates_should_be_equal(self):
        location_a, location_b = Location(0, 0), Location(0, 0)
        self.assertTrue(location_a == location_b)


class WorldTestCase(unittest.TestCase):
    def setUp(self):
        self.location = Mock(name='location')

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

    # Smell, maybe unnecessary test?
    def test_is_alive_at_not_dependent_on_location_instance(self):
        coordinates = (0, 0)
        self.location = Location(*coordinates)
        world = World()
        world.set_living_at(self.location)

        location = Location(*coordinates)

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

    def test_a_world_with_one_cell_is_empty_after_a_tick(self):
        # Potential smell here, given that we have to use real location
        # instance here for this to pass. Mock approach will not work.
        self.location = Location(0, 0)

        world = World.empty()
        world.set_living_at(self.location)
        next_world = world.tick()
        self.assertTrue(next_world.is_empty)

    #  def test_a_world_with_one_cell_is_empty_after_a_tick(self):
        #  # Potential smell here, given that we have to use real location
        #  # instance here for this to pass. Mock approach will not work.
        #  self.location = Location(0, 0)

        #  world = World.empty()
        #  world.set_living_at(self.location)
        #  next_world = world.tick()
        #  self.assertTrue(next_world.is_empty)


class CellTestCase(unittest.TestCase):
    def test_a_new_cell_is_alive(self):
        cell = Cell()
        self.assertTrue(cell.is_alive)

    def test_a_dead_cell_is_not_alive(self):
        cell = Cell()
        cell.die()
        self.assertFalse(cell.is_alive)

    def test_a_cell_can_be_set_dead(self):
        cell = Cell(alive=False)
        self.assertFalse(cell.is_alive)

    def test_cell_is_still_alive_next_gen_if_in_stable_neighborhood(self):
        for i in Cell.STABLE_NEIGHBOR_RANGE:
            with self.subTest(stable_neighbor_count=i):
                cell = Cell()
                cell.is_alive_next_generation(i)
                self.assertTrue(cell.is_alive_next_generation)

    def test_cell_is_dead_next_generation_if_lt_stable_count(self):
        cell = Cell()
        min_stable = Cell.STABLE_NEIGHBOR_RANGE[0]
        is_alive_next_gen = cell.is_alive_next_generation(min_stable - 1)
        self.assertFalse(is_alive_next_gen)

    def test_cell_is_dead_from_overcrowding_next_gen_if_gt_stable_count(self):
        cell = Cell()
        max_stable = Cell.STABLE_NEIGHBOR_RANGE[-1]
        is_alive_next_gen = cell.is_alive_next_generation(max_stable + 1)
        self.assertFalse(is_alive_next_gen)

    def test_dead_cell_in_fertile_neighboorhood_is_alive_next_generation(self):
        cell = Cell(alive=False)
        is_alive_next_generation = cell.is_alive_next_generation(
                Cell.FERTILE_NEIGHBOR_COUNT)
        self.assertTrue(is_alive_next_generation)

    def test_dead_cell_is_dead_next_gen_if_lt_fertile_neighbor_count(self):
        cell = Cell(alive=False)
        lt_fertile_count = Cell.FERTILE_NEIGHBOR_COUNT - 1
        is_alive_next_gen = cell.is_alive_next_generation(lt_fertile_count)
        self.assertFalse(is_alive_next_gen)

    def test_dead_cell_is_dead_next_gen_if_gt_fertile_neighbor_count(self):
        cell = Cell(alive=False)
        gt_fertile_count = Cell.FERTILE_NEIGHBOR_COUNT + 1
        is_alive_next_gen = cell.is_alive_next_generation(gt_fertile_count)
        self.assertFalse(is_alive_next_gen)


unittest.main()
