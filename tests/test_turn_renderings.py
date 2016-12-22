import unittest

from game_of_life.render_to_world import render_to_world
from game_of_life.turn_renderings import turn_renderings

from .test_world_renderer import RenderingTestsMixin


class TurnRenderingsTestCase(unittest.TestCase, RenderingTestsMixin):
    def setUp(self):
        self.set_living_and_dead_cells_to_plus_and_minus()

    def test_can_render_0_turns(self):
        world = render_to_world('++-+\n' +
                                '+-++\n' +
                                '++-+\n' +
                                '-+--')
        actual = turn_renderings(world, turns=0)
        expected = [('Turn 0:\n' +
                     '++-+\n' +
                     '+-++\n' +
                     '++-+\n' +
                     '-+--')]
        self.assertEqual(list(actual), expected)

    def test_can_render_1_turn(self):
        world = render_to_world('++-+\n' +
                                '+-++\n' +
                                '++-+\n' +
                                '-+--')
        actual = turn_renderings(world, turns=1)
        expected = [('Turn 0:\n' +
                     '++-+\n' +
                     '+-++\n' +
                     '++-+\n' +
                     '-+--'),
                    ('Turn 1:\n' +
                     '++-+\n' +
                     '---+\n' +
                     '+--+\n' +
                     '+++-')]
        self.assertEqual(list(actual), expected)

    def test_can_render_2_turns(self):
        world = render_to_world('++-+\n' +
                                '+-++\n' +
                                '++-+\n' +
                                '-+--')
        actual = turn_renderings(world, turns=2)
        expected = [('Turn 0:\n' +
                     '++-+\n' +
                     '+-++\n' +
                     '++-+\n' +
                     '-+--'),
                    ('Turn 1:\n' +
                     '++-+\n' +
                     '---+\n' +
                     '+--+\n' +
                     '+++-'),
                    ('Turn 2:\n' +
                     '--+-\n' +
                     '++-+\n' +
                     '+--+\n' +
                     '+++-')]
        self.assertEqual(list(actual), expected)
