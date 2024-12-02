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

    def test_get_matching_empty_regions(self):
        # This test checks if the function returns the correct number of matching empty regions.
        result = self.solver.get_matching_empty_regions()
        self.assertEqual(result, 5)  # Correct expected output

if __name__ == '__main__':
    unittest.main()
