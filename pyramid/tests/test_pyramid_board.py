from django.test import TestCase
from ..solver_functions import pyramid_board

class PyramidBoardTestCase(TestCase):
    def test_creating_board(self):
        """
        Test the creation of a pyramid board.
        """
        board = pyramid_board.pyramid_board(5)
        self.assertEqual(len(board.levels), 5)

    def test_convert_to_from_3D_array(self):
        """
        Test the conversion to and from a 3D array.
        """
        board = pyramid_board.pyramid_board(5)
        array_board = [
            [[1, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 1, 0, 0]],
            [[0, 0, 0, 0],
             [0, 0, 0, 0],
             [0, 0, 0, 0],
             [0, 0, 0, 0]],
            [[0, 0, 0],
             [0, 0, 0],
             [0, 0, 0]],
            [[0, 0],
             [0, 0]],
            [[0]]
        ]
        board.convert_from_3D_array(array_board)
        arr = board.convert_to_3D_array()
        self.assertEqual(arr, array_board)

    def test_count_cells(self):
        """
        Test the count_cells method to ensure it counts cells correctly.
        """
        board = pyramid_board.pyramid_board(2)
        self.assertEqual(board.count_cells(), 5)

    def test_is_region_free(self):
        """
        Test the is_region_free method to ensure it checks regions correctly.
        """
        board = pyramid_board.pyramid_board(2)
        region = [(0, 0, 0), (0, 2, 0), (2, 0, 0), (2, 2, 0), (1, 1, 1)]
        self.assertTrue(board.is_region_free(region))
        board.cells[(0, 0, 0)] = 1
        self.assertFalse(board.is_region_free(region))

    def test_get_matching_empty_regions(self):
        """
        Test the get_matching_empty_regions method to ensure it finds matching regions correctly.
        """
        board = pyramid_board.pyramid_board(3)
        region = [(0, 0, 0), (0, 2, 0), (2, 0, 0)]
        matching_regions = board.get_matching_empty_regions(region)
        self.assertTrue(matching_regions)