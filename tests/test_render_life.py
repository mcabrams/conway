import unittest

from game_of_life.render_to_world import render_to_world
from game_of_life.render_life import render_life


class RenderLifeTestCase(unittest.TestCase):
    def test_can_render_0_turns(self):
        world = render_to_world('++-+\n' +
                                '+-++\n' +
                                '++-+\n' +
                                '-+--\n')
        actual = render_life(world, turns=0)
        expected = ('Turn 0:\n' +
                    '++-+\n' +
                    '+-++\n' +
                    '++-+\n' +
                    '-+--\n')
        self.assertEqual(actual, expected,
                         msg='\n\nExpected: \n{}\nBut instead got: \n{}'
                             .format(expected, actual))

    def test_can_render_1_turn(self):
        world = render_to_world('++-+\n' +
                                '+-++\n' +
                                '++-+\n' +
                                '-+--\n')
        actual = render_life(world, turns=1)
        expected = ('Turn 0:\n' +
                    '++-+\n' +
                    '+-++\n' +
                    '++-+\n' +
                    '-+--\n' +
                    'Turn 1:\n' +
                    '++-+\n' +
                    '---+\n' +
                    '+--+\n' +
                    '+++-\n')
        self.assertEqual(actual, expected,
                         msg='\n\nExpected: \n{}\nBut instead got: \n{}'
                             .format(expected, actual))

    def test_can_render_2_turns(self):
        world = render_to_world('++-+\n' +
                                '+-++\n' +
                                '++-+\n' +
                                '-+--\n')
        actual = render_life(world, turns=2)
        expected = ('Turn 0:\n' +
                    '++-+\n' +
                    '+-++\n' +
                    '++-+\n' +
                    '-+--\n' +
                    'Turn 1:\n' +
                    '++-+\n' +
                    '---+\n' +
                    '+--+\n' +
                    '+++-\n' +
                    'Turn 2:\n' +
                    '--+-\n' +
                    '++-+\n' +
                    '+--+\n' +
                    '+++-\n')
        self.assertEqual(actual, expected,
                         msg='\n\nExpected: \n{}\nBut instead got: \n{}'
                             .format(expected, actual))
