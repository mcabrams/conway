import unittest

from game_of_life.location import Location
from game_of_life.render_to_world import render_to_world


class RenderToWorldTestCase(unittest.TestCase):
    def test_empty_render_generates_empty_world(self):
        world = render_to_world('')
        self.assertTrue(world.is_empty)

    def test_lone_living_cell_generates_world_with_cell_at_origin(self):
        world = render_to_world('+')
        self.assertTrue(world.is_alive_at(Location(0, 0)))

    def test_dimenions_of_rendering_dictate_dimensions_of_world(self):
        world = render_to_world('+')
        self.assertEqual(world.dimensions, (1, 1))

        world = render_to_world('+-')
        self.assertEqual(world.dimensions, (2, 1))

        world = render_to_world('+\n'
                                '-')
        self.assertEqual(world.dimensions, (1, 2))

        world = render_to_world('+-\n'
                                '-+')
        self.assertEqual(world.dimensions, (2, 2))

    def test_spaced_living_row_cells_create_proper_world(self):
        world = render_to_world('+-+')
        for living, coordinates in [(True, (0, 0)),
                                    (False, (1, 0)),
                                    (True, (2, 0))]:
            with self.subTest(coordinates=coordinates):
                self.assertEqual(living,
                                 world.is_alive_at(Location(*coordinates)))

    def test_column_cells_create_proper_world(self):
        world = render_to_world('+\n'
                                '+')
        for living, coordinates in [(True, (0, 0)),
                                    (True, (0, 1))]:
            with self.subTest(coordinates=coordinates):
                self.assertEqual(living,
                                 world.is_alive_at(Location(*coordinates)))

    def test_complicated_rendering_creates_proper_world(self):
        world = render_to_world('-+-\n'
                                '+--\n'
                                '-++')
        for living, coordinates in [(0, (0, 2)), (1, (1, 2)), (0, (2, 2)),
                                    (1, (0, 1)), (0, (1, 1)), (0, (2, 1)),
                                    (0, (0, 0)), (1, (1, 0)), (1, (2, 0))]:
            with self.subTest(coordinates=coordinates):
                self.assertEqual(bool(living),
                                 world.is_alive_at(Location(*coordinates)))
