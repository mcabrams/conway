import unittest

from conway import World

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

unittest.main()
