import unittest

from game_of_life.location import Location
from game_of_life.world import World, WorldRenderer


class WorldRendererTestCase(unittest.TestCase):
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
