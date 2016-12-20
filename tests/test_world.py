import unittest

from game_of_life.cell import Cell
from game_of_life.location import Location
from game_of_life.render_to_world import render_to_world
from game_of_life.world import World, WorldRenderer


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
        self.location = Location(0, 0)

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

    def test_world_progresses_next_expected_outcome_after_a_tick(self):
        render = ('-+-\n'
                  '--+')
        expected_render_after_tick = ('---\n'
                                      '---')

        world = render_to_world(render)
        world = world.tick()
        actual = WorldRenderer(world).render()
        self.assertEqual(expected_render_after_tick, actual)

        render = ('-+-\n'
                  '-++')
        expected_render_after_tick = ('-++\n'
                                      '-++')

        world = render_to_world(render)
        world = world.tick()
        actual = WorldRenderer(world).render()
        self.assertEqual(expected_render_after_tick, actual,
                         msg='\n\nExpected: \n{}\nBut instead got: \n{}'
                             .format(expected_render_after_tick, actual))

    def test_an_empty_world_with_10_by_10_dimensions_has_100_dead_cells(self):
        world = World.empty(min_location=Location(0, 0),
                            max_location=Location(9, 9))
        self.assertEqual(world.dead_cell_count, 100)

    def test_an_empty_world_with_2_by_2_dimensions_has_4_dead_cells(self):
        world = World.empty(min_location=Location(0, 0),
                            max_location=Location(1, 1))
        self.assertEqual(world.dead_cell_count, 4)

    def test_2_by_2_world_with_one_living_cell_has_3_dead_cells(self):
        world = World.empty(min_location=Location(0, 0),
                            max_location=Location(1, 1))
        world.set_living_at(self.location)
        self.assertEqual(world.dead_cell_count, 3)

    def test_world_has_default_dimensions(self):
        world = World.empty()
        self.assertEqual((1, 1), world.dimensions)

    def test_world_dimensions_come_from_min_max_locations(self):
        world = World.empty(min_location=Location(0, 0),
                            max_location=Location(3, 3))
        self.assertEqual((4, 4), world.dimensions)

    def test_set_living_at_beyond_max_location_x_expands_max_location(self):
        world = World.empty(min_location=Location(0, 0),
                            max_location=Location(3, 3))

        world.set_living_at(Location(4, 0))
        self.assertEqual(world.dimensions, (5, 4))

    def test_set_living_at_beyond_max_location_y_expands_max_location(self):
        world = World.empty(min_location=Location(0, 0),
                            max_location=Location(3, 3))

        world.set_living_at(Location(0, 4))
        self.assertEqual(world.dimensions, (4, 5))

    def test_set_living_at_below_min_location_x_lowers_min_location(self):
        world = World.empty(min_location=Location(0, 0),
                            max_location=Location(3, 3))

        world.set_living_at(Location(-1, 0))
        self.assertEqual(world.dimensions, (5, 4))

    def test_set_living_at_below_min_location_y_lowers_min_location(self):
        world = World.empty(min_location=Location(0, 0),
                            max_location=Location(3, 3))

        world.set_living_at(Location(0, -1))
        self.assertEqual(world.dimensions, (4, 5))
