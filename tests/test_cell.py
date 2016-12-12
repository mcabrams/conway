import unittest

from game_of_life.cell import Cell


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
