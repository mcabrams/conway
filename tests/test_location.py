from collections import OrderedDict
import unittest

from game_of_life.location import (LocationGrid, Location,
                                   get_max_coordinates_location,
                                   get_min_coordinates_location,
                                   sort_locations)


class LocationTestCase(unittest.TestCase):
    def test_location_has_coordinates(self):
        location = Location(1, 1)
        self.assertEqual(location.coordinates, (1, 1))

    def test_neighbors(self):
        location = Location(0, 0)
        expected_neighbor_coordinates = [(0, 1), (1, 1), (1, 0), (1, -1),
                                         (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        actual = [n.coordinates for n in location.neighbors]
        self.assertEqual(set(actual), set(expected_neighbor_coordinates))

    def test_instances_of_location_with_same_coordinates_are_equal(self):
        location_a, location_b = Location(0, 0), Location(0, 0)
        self.assertTrue(location_a == location_b)


class GetMinCoordinatesLocationTestCase(unittest.TestCase):
    def test_with_one_location(self):
        actual = get_min_coordinates_location([Location(0, 0)])
        self.assertEqual(actual, Location(0, 0))

    def test_with_multiple_locations(self):
        actual = get_min_coordinates_location([Location(1, 0), Location(0, 7),
                                               Location(5, -3)])
        self.assertEqual(actual, Location(0, -3))


class GetMaxCoordinatesLocationTestCase(unittest.TestCase):
    def test_with_one_location(self):
        actual = get_max_coordinates_location([Location(0, 0)])
        self.assertEqual(actual, Location(0, 0))

    def test_with_multiple_locations(self):
        actual = get_max_coordinates_location([Location(1, 0), Location(0, 7),
                                               Location(5, -3)])
        self.assertEqual(actual, Location(5, 7))


class SortLocationsTestCase(unittest.TestCase):
    def test_lone_location_returns_lone_location(self):
        actual = sort_locations([Location(0, 0)])
        expected = {
            0: [Location(0, 0)]
        }
        self.assertEqual(dict(actual), expected)

    def test_locations_indexed_by_y_axis(self):
        sorted_locations = sort_locations([Location(0, 1), Location(0, 0)])
        expected = {
            0: [Location(0, 0)],
            1: [Location(0, 1)]
        }
        self.assertEqual(dict(sorted_locations), expected)

    def test_locations_at_same_y_coordinate_sorted_by_asc_x_coordinate(self):
        sorted_locations = sort_locations([Location(0, 0), Location(-1, 0),
                                           Location(1, 0)])
        expected = {
            0: [Location(-1, 0), Location(0, 0), Location(1, 0)]
        }
        self.assertEqual(dict(sorted_locations), expected)

    def test_locations_keyed_and_sorted_together(self):
        sorted_locations = sort_locations([Location(0, 0), Location(0, 1),
                                           Location(1, 0), Location(1, 1)])
        expected = {
            0: [Location(0, 0), Location(1, 0)],
            1: [Location(0, 1), Location(1, 1)]
        }

        self.assertEqual(dict(sorted_locations), expected)

    def test_locations_sorted_properly_by_desc_y_index(self):
        sorted_locations = sort_locations([Location(0, 5), Location(0, 3),
                                           Location(0, 7)])
        expected = OrderedDict([(7, [Location(0, 7)]), (5, [Location(0, 5)]),
                                (3, [Location(0, 3)])])

        self.assertEqual(sorted_locations, expected)


class LocationGridRowsTestCase(unittest.TestCase):
    def test_same_start_end(self):
        actual = LocationGrid(Location(0, 0), Location(0, 0)).rows
        expected = OrderedDict({
            0: [Location(0, 0)]
        })
        self.assertEqual(actual, expected)

    def test_with_proper_minimum_and_maximum(self):
        actual = LocationGrid(Location(0, 0), Location(2, 2)).rows
        expected = {
            0: [Location(0, 0), Location(1, 0), Location(2, 0)],
            1: [Location(0, 1), Location(1, 1), Location(2, 1)],
            2: [Location(0, 2), Location(1, 2), Location(2, 2)]
        }
        self.assertEqual(dict(actual), expected)

    def test_grid_rows_can_are_sorted_by_descending_y_index(self):
        location_grid = LocationGrid(Location(0, 0), Location(2, 2))
        actual = location_grid.rows
        expected = OrderedDict([
            (2, [Location(0, 2), Location(1, 2), Location(2, 2)]),
            (1, [Location(0, 1), Location(1, 1), Location(2, 1)]),
            (0, [Location(0, 0), Location(1, 0), Location(2, 0)])
        ])
        self.assertEqual(actual, expected)


class LocationGridLocationsTestCase(unittest.TestCase):
    def test_returns_proper_locations(self):
        actual = LocationGrid(Location(0, 0), Location(1, 1)).locations
        expected = [Location(0, 0), Location(1, 0), Location(0, 1),
                    Location(1, 1)]
        self.assertEqual(set(actual), set(expected))
