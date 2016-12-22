import unittest
from unittest.mock import patch

from game_of_life.location import Location
from game_of_life.world import World
from game_of_life.world_renderer import WorldRenderer


class RenderingTestsMixin:
    def set_living_and_dead_cells_to_plus_and_minus(self):
        patches = [('game_of_life.world_renderer.LIVE_CELL_CHAR', '+'),
                   ('game_of_life.world_renderer.DEAD_CELL_CHAR', '-')]
        for path, new in patches:
            patcher = patch(path, new=new)
            patcher.start()
            self.addCleanup(patcher.stop)


class WorldRendererTestCase(unittest.TestCase, RenderingTestsMixin):
    def setUp(self):
        self.set_living_and_dead_cells_to_plus_and_minus()

    def test_empty_world_renders_as_expected(self):
        world = World.empty()
        render = WorldRenderer(world).render()
        expected = '-'
        self.assertEqual(render, expected)

    def test_world_with_lone_cell_renders_as_expected(self):
        world = World.empty()
        world.set_living_at(Location(0, 0))
        render = WorldRenderer(world).render()
        expected = '+'
        self.assertEqual(render, expected)

    def test_world_with_live_and_dead_cell_renders_as_expected(self):
        world = World.empty()
        world.set_living_at(Location(0, 0))
        world.set_living_at(Location(2, 0))
        render = WorldRenderer(world).render()
        expected = '+-+'
        self.assertEqual(render, expected)

    def test_world_that_is_vertical_renders_properly(self):
        world = World.empty()
        world.set_living_at(Location(0, 0))
        world.set_living_at(Location(0, 2))
        render = WorldRenderer(world).render()
        expected = ('+\n'
                    '-\n'
                    '+')
        self.assertEqual(render, expected)

    def test_world_renders_according_to_dimensions(self):
        world = World.empty(min_location=Location(0, 0),
                            max_location=Location(2, 0))

        render = WorldRenderer(world).render()
        expected = ('---')
        self.assertEqual(render, expected)

    @patch('game_of_life.world_renderer.LIVE_CELL_CHAR', new='X')
    @patch('game_of_life.world_renderer.DEAD_CELL_CHAR', new='O')
    def test_world_can_render_with_arbitrary_characters(self):
        world = World.empty()
        world.set_living_at(Location(0, 0))
        world.set_living_at(Location(2, 0))
        render = WorldRenderer(world).render()
        expected = 'XOX'
        self.assertEqual(render, expected)
