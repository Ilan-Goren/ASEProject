from django.test import TestCase
from ..solver_functions import pyramid_board

class PyramidBoardTestCase(TestCase):
    def test_creating_board(self):
        """
        Test that a pyramid board with the specified number of levels is created correctly.
        """
        board = pyramid_board.pyramid_board(5)
        self.assertEqual(len(board.levels), 5)

    def test_convert_to_from_3D_array(self):
        """
        Test the conversion of the board to a 3D array and back to ensure consistency.
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
        Test that the count_cells method returns the correct number of cells in the board.
        """
        board = pyramid_board.pyramid_board(2)
        self.assertEqual(board.count_cells(), 5)

    def test_is_region_free(self):
        """
        Test that the is_region_free method correctly identifies if a region is free of occupied cells.
        """
        board = pyramid_board.pyramid_board(2)
        region = [(0, 0, 0), (0, 2, 0), (2, 0, 0), (2, 2, 0), (1, 1, 1)]
        self.assertTrue(board.is_region_free(region))
        board.cells[(0, 0, 0)] = 1
        self.assertFalse(board.is_region_free(region))

    def test_get_matching_empty_regions(self):
        """
        Test that the get_matching_empty_regions method finds all regions that match the given pattern and are empty.
        """
        board = pyramid_board.pyramid_board(3)
        region = [(0, 0, 0), (0, 2, 0), (2, 0, 0)]
        matching_regions = board.get_matching_empty_regions(region)
        self.assertEqual(len(matching_regions), 1)  # Assuming there is only one matching region