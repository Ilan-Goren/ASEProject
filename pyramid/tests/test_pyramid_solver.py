import unittest
from pyramid_solver import PyramidSolver

class TestPyramidSolver(unittest.TestCase):

    def setUp(self):
        self.solver = PyramidSolver()

    def test_initialize_board(self):
        # This test checks if the board is initialized correctly with the expected dimensions for each level.
        board = self.solver._initialize_board()
        self.assertEqual(len(board), 5)  # 5 levels
        self.assertEqual(len(board[0]), 5)  # Level 0 has 5x5 grid
        self.assertEqual(len(board[1]), 4)  # Level 1 has 4x4 grid
        self.assertEqual(len(board[4]), 1)  # Level 4 has 1x1 grid

    def test_initialize_pieces(self):
        # This test verifies that the pieces are initialized correctly and checks their attributes.
        pieces = self.solver._initialize_pieces()
        self.assertEqual(len(pieces), 3)  # 3 pieces initialized
        self.assertEqual(pieces[0]["id"], 1)
        self.assertEqual(pieces[1]["shape"], "L")

    def test_place_piece(self):
        # This test checks if a piece can be placed on the board and verifies that it is removed from the available pieces.
        result = self.solver.place_piece(1, 0, 0, 0)
        self.assertTrue(result)
        self.assertEqual(self.solver.board[0][0][0], 1)
        self.assertNotIn({"id": 1, "shape": "T", "color": "red"}, self.solver.pieces_left)

        # This part of the test ensures that the same piece cannot be placed again.
        result = self.solver.place_piece(1, 0, 0, 0)
        self.assertFalse(result)

    def test_can_place(self):
        # This test checks if a piece can be placed at a specific location on the board.
        piece = {"id": 1, "shape": "T", "color": "red"}
        self.assertTrue(self.solver._can_place(piece, 0, 0, 0))
        
        # This part of the test ensures that a piece cannot be placed in an occupied spot.
        self.solver.board[0][0][0] = 1  # Manually place a piece
        self.assertFalse(self.solver._can_place(piece, 0, 0, 0))

    def test_remove_piece(self):
        # This test checks if a piece can be removed from the board and returned to the available pieces.
        self.solver.place_piece(1, 0, 0, 0)
        result = self.solver.remove_piece(1)
        self.assertTrue(result)
        self.assertIsNone(self.solver.board[0][0][0])
        self.assertIn({"id": 1, "shape": "Unknown", "color": "Unknown"}, self.solver.pieces_left)

        # This part of the test ensures that the same piece cannot be removed again.
        result = self.solver.remove_piece(1)
        self.assertFalse(result)

    def test_is_board_empty(self):
        # This test checks if the board is empty initially and after placing a piece.
        self.assertTrue(self.solver.is_board_empty())
        self.solver.place_piece(1, 0, 0, 0)
        self.assertFalse(self.solver.is_board_empty())

if __name__ == '__main__':
    unittest.main()
