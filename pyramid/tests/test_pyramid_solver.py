from django.test import TestCase
from ..pyramid_solver import PyramidSolver

class PyramidSolverTestCase(TestCase):
    def setUp(self):
        """
        Set up the PyramidSolver instance for testing.
        """
        self.solver = PyramidSolver()

    def test_initialize_board(self):
        """
        Ensure the board is initialized with the correct structure.
        """
        board = self.solver._initialize_board()
        self.assertEqual(len(board), 5)
        for level in range(5):
            self.assertEqual(len(board[level]), 5 - level)

    def test_initialize_pieces(self):
        """
        Ensure pieces are initialized correctly.
        """
        pieces = self.solver._initialize_pieces()
        self.assertEqual(len(pieces), 3)  

    def test_place_piece(self):
        """
        Ensure a piece is placed correctly on the board.
        """
        self.solver.place_piece(1, 0, 0, 0)
        self.assertEqual(self.solver.board[0][0][0], 1)

    def test_place_piece_invalid(self):
        """
        Ensure invalid piece placements are handled correctly.
        """
        self.assertFalse(self.solver.place_piece(1, 5, 0, 0))  # Invalid level
        self.assertFalse(self.solver.place_piece(1, 0, 5, 0))  # Invalid row
        self.assertFalse(self.solver.place_piece(1, 0, 0, 5))  # Invalid column

    def test_remove_piece(self):
        """
        Ensure a piece is removed correctly from the board.
        """
        self.solver.place_piece(1, 0, 0, 0)
        self.solver.remove_piece(1)
        self.assertIsNone(self.solver.board[0][0][0])

    def test_remove_piece_invalid(self):
        """
        Ensure invalid piece removals are handled correctly.
        """
        self.assertFalse(self.solver.remove_piece(99))  # Non-existent piece

    def test_is_board_empty(self):
        """
        Ensure the board is correctly identified as empty or not.
        """
        self.assertTrue(self.solver.is_board_empty())
        self.solver.place_piece(1, 0, 0, 0)
        self.assertFalse(self.solver.is_board_empty())