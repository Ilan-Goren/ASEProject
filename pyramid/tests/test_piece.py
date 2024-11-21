from django.test import TestCase
from ..pyramid_solver import PyramidSolver

class PieceTestCase(TestCase):

    def setUp(self):
        """
        Set up the test case with a PyramidSolver instance and an initial board state.
        """
        self.solver = PyramidSolver()
        
    def tearDown(self):
        """
        Clean up after each test case.
        """
        self.solver = None

    def test_creating_piece(self):
        """
        Test that a Piece object is created with the correct transformations.
        """
        piece_id = 1
        level, row, col = 0, 0, 0
        result = self.solver.place_piece(piece_id, level, row, col)
        self.assertTrue(result)
        self.assertEqual(self.solver.board[level][row][col], piece_id)

    def test_visualise_piece(self):
        """
        Test that the visualise_piece function runs without errors for all pieces.
        """
        for piece in self.solver.pieces_left:
            try:
                self.solver.visualise_piece(piece)
            except Exception as e:
                self.fail(f"visualise_piece raised an exception: {e}")

    def test_place_piece(self):
        """
        Test that a piece is placed correctly on the board.
        """
        self.assertTrue(self.solver.place_piece(1, 0, 0, 0))
        self.assertEqual(self.solver.board[0][0][0], 1)

    def test_place_piece_invalid(self):
        """
        Test that invalid piece placements are handled correctly.
        """
        self.assertFalse(self.solver.place_piece(1, 5, 0, 0))  # Invalid level
        self.assertFalse(self.solver.place_piece(1, 0, 5, 0))  # Invalid row
        self.assertFalse(self.solver.place_piece(1, 0, 0, 5))  # Invalid column

    def test_remove_piece(self):
        """
        Test that a piece is removed correctly from the board.
        """
        self.solver.place_piece(1, 0, 0, 0)
        self.solver.remove_piece(1)
        self.assertIsNone(self.solver.board[0][0][0])

    def test_remove_piece_invalid(self):
        """
        Test that invalid piece removals are handled correctly.
        """
        self.assertFalse(self.solver.remove_piece(99))  # Non-existent piece

    def test_is_board_empty(self):
        """
        Test that the board is correctly identified as empty or not.
        """
        self.assertTrue(self.solver.is_board_empty())
        self.solver.place_piece(1, 0, 0, 0)
        self.assertFalse(self.solver.is_board_empty())

