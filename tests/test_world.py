import unittest
from unittest.mock import Mock

from game_of_life.cell import Cell
from game_of_life.location import Location
from game_of_life.world import World


def _get_location_cluster(cluster_number):
    location = Location(0, 0)
    return [location] + location.neighbors[:cluster_number]


def _get_stable_world():
    world = World()
    stable_location_cluster = _get_location_cluster(
        Cell.STABLE_NEIGHBOR_RANGE[0] + 1)

    for location in stable_location_cluster:
        world.set_living_at(location)

    return world


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

    def test_a_world_with_stable_neighborhood_is_not_empty_after_a_tick(self):
        world = _get_stable_world()
        next_world = world.tick()
        self.assertFalse(next_world.is_empty)

    def test_living_locations_includes_living_cells(self):
        world = World.empty()
        world.set_living_at(self.location)
        self.assertEqual(world.living_locations, [self.location])

    def test_dead_locations_not_in_living_locations(self):
        world = World.empty()
        world.set_dead_at(self.location)
        self.assertEqual(world.living_locations, [])
