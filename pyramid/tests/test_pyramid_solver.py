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
        Test the _initialize_board method to ensure it initializes a board with the correct length.
        """
        board = self.solver._initialize_board()
        self.assertEqual(len(board), 5)
        for level in range(5):
            self.assertEqual(len(board[level]), 5 - level)

    def test_initialize_pieces(self):
        """
        Test the _initialize_pieces method to ensure it initializes pieces correctly.
        """
        pieces = self.solver._initialize_pieces()
        self.assertTrue(pieces)
        self.assertEqual(len(pieces), 3)  # Assuming 3 pieces as per the placeholder

    def test_place_piece(self):
        """
        Test the place_piece method to ensure it places a piece correctly on the board.
        """
        result = self.solver.place_piece(1, 0, 0, 0)
        self.assertTrue(result)
        self.assertEqual(self.solver.board[0][0][0], 1)

    def test_place_piece_invalid(self):
        """
        Test the place_piece method with invalid inputs.
        """
        result = self.solver.place_piece(1, 5, 0, 0)  # Invalid level
        self.assertFalse(result)
        result = self.solver.place_piece(1, 0, 5, 0)  # Invalid row
        self.assertFalse(result)
        result = self.solver.place_piece(1, 0, 0, 5)  # Invalid column
        self.assertFalse(result)

    def test_remove_piece(self):
        """
        Test the remove_piece method to ensure it removes a piece correctly from the board.
        """
        self.solver.place_piece(1, 0, 0, 0)
        result = self.solver.remove_piece(1)
        self.assertTrue(result)
        self.assertIsNone(self.solver.board[0][0][0])

    def test_remove_piece_invalid(self):
        """
        Test the remove_piece method with invalid inputs.
        """
        result = self.solver.remove_piece(99)  # Non-existent piece
        self.assertFalse(result)

    def test_is_board_empty(self):
        """
        Test the is_board_empty method to ensure it correctly identifies if the board is empty.
        """
        self.assertTrue(self.solver.is_board_empty())
        self.solver.place_piece(1, 0, 0, 0)
        self.assertFalse(self.solver.is_board_empty())