from django.test import TestCase

from ..solver_functions import board

class BoardTestCase(TestCase):
    """
    Test cases for the Board class functionality.
    """
    def test_board(self):
        """
        Test the board initialization and cell count.

        - Verifies that the board is initialized to the expected structure.
        - Confirms the total number of cells is correct.

        :raises AssertionError: If the board structure or cell count is incorrect.
        """
        b = board.Board()
        expected_board = [[[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0], [0, 0], [0]], [[0, 0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0], [0, 0], [0]], [[0, 0, 0, 0], [0, 0, 0], [0, 0], [0]], [[0, 0, 0], [0, 0], [0]], [[0, 0], [0]], [[0]]]
        self.assertEqual(b.board, expected_board)
        self.assertEqual(b.count_cells(), 56)

    def test_is_region_free(self):
        """
        Test the `is_region_free` method.

        - Checks if regions on the board are unoccupied.
        - Verifies behavior with both valid, invalid due to occupation and out-of-bounds coordinates.

        :raises AssertionError: If the method's output does not match expected results.
        """
        b = board.Board()
        self.assertTrue(b.is_region_free([(0,0,0),(1,0,0),(0,0,5)]))
        b.board[0][0][0] = 1
        self.assertFalse(b.is_region_free([(0,0,0)]))
        self.assertFalse(b.is_region_free([(6,6,6)]))

    def test_get_matching_empty_regions(self):
        """
        Test the `get_matching_empty_regions` method.

        - Ensures the method identifies all empty regions matching a given pattern.
        - Confirms handling of invalid patterns with out-of-bounds coordinates.

        :raises AssertionError: If the output does not match expected results.
        """
        b = board.Board()
        expected_matching_regions = [[(0, 0, 0), (1, 0, 0)], [(1, 0, 0), (2, 0, 0)], [(2, 0, 0), (3, 0, 0)], [(3, 0, 0), (4, 0, 0)], [(4, 0, 0), (5, 0, 0)], [(0, 1, 0), (1, 1, 0)], [(1, 1, 0), (2, 1, 0)], [(2, 1, 0), (3, 1, 0)], [(3, 1, 0), (4, 1, 0)], [(0, 2, 0), (1, 2, 0)], [(1, 2, 0), (2, 2, 0)], [(2, 2, 0), (3, 2, 0)], [(0, 3, 0), (1, 3, 0)], [(1, 3, 0), (2, 3, 0)], [(0, 4, 0), (1, 4, 0)], [(0, 0, 1), (1, 0, 1)], [(1, 0, 1), (2, 0, 1)], [(2, 0, 1), (3, 0, 1)], [(3, 0, 1), (4, 0, 1)], [(0, 1, 1), (1, 1, 1)], [(1, 1, 1), (2, 1, 1)], [(2, 1, 1), (3, 1, 1)], [(0, 2, 1), (1, 2, 1)], [(1, 2, 1), (2, 2, 1)], [(0, 3, 1), (1, 3, 1)], [(0, 0, 2), (1, 0, 2)], [(1, 0, 2), (2, 0, 2)], [(2, 0, 2), (3, 0, 2)], [(0, 1, 2), (1, 1, 2)], [(1, 1, 2), (2, 1, 2)], [(0, 2, 2), (1, 2, 2)], [(0, 0, 3), (1, 0, 3)], [(1, 0, 3), (2, 0, 3)], [(0, 1, 3), (1, 1, 3)], [(0, 0, 4), (1, 0, 4)]]
        self.assertEqual(b.get_matching_empty_regions([(0,0,0),(1,0,0)]), expected_matching_regions)
        self.assertFalse(b.get_matching_empty_regions([(0,0,0),(6,6,6)]))

    def test_verify_board(self):
        """
        Test the `verify_board` method.

        - Ensures the board is valid when pieces are correctly placed.
        - Confirms invalid boards with invalid piece placements fail verification.

        :raises AssertionError: If the method's validation output is incorrect.
        """
        b = board.Board()
        b.board = [[[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [7, 7, 7, 0], [7, 0, 7], [0, 0], [0]],
                   [[0, 0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0], [0, 0], [0]], [[0, 0, 0, 0], [0, 0, 0], [0, 0], [0]],
                   [[0, 0, 0], [0, 0], [0]], [[0, 0], [0]], [[0]]]

        self.assertTrue(b.verify_board())
        b.board = [[[0, 0, 0, 0, 0, 0], [0, 7, 0, 0, 0], [7, 0, 7, 0], [7, 0, 7], [0, 0], [0]],
                   [[0, 0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0], [0, 0], [0]], [[0, 0, 0, 0], [0, 0, 0], [0, 0], [0]],
                   [[0, 0, 0], [0, 0], [0]], [[0, 0], [0]], [[0]]]
        self.assertFalse(b.verify_board())