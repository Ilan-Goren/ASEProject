from django.test import TestCase
from ..solver_functions import solver, pyramid_board, piece, algorithm_x_functions

class SolverTestCase(TestCase):

    def setUp(self):
        """
        Initialize the test case with a solver instance, a pyramid board, and a list of pieces.
        """
        self.s = solver.Solver()
        self.b = pyramid_board.pyramid_board(2)
        self.pieces = [piece.Piece(p) for p in piece.pieces]

    def test_generate_board_cell_indexes(self):
        """
        Ensure generate_board_cell_indexes correctly generates indexes for the board cells.
        """
        self.s.generate_board_cell_indexes(self.b)
        self.assertTrue(self.b.cells)
        self.assertEqual(len(self.s.index_to_cell), self.b.count_cells())
        self.assertEqual(len(self.s.cell_to_index), self.b.count_cells())

    def test_packing_matrix(self):
        """
        Ensure initialise_packing_matrix correctly initializes the packing matrix.
        """
        self.s.initialise_packing_matrix(self.b, self.pieces)
        self.assertEqual(self.s.matrix.num_cols, self.b.count_cells() + len(self.pieces))

    def test_solve(self):
        """
        Ensure the solve method correctly solves the puzzle.
        """
        pieces = [piece.Piece(11, [(0, 0, 0), (0, 2, 0), (2, 0, 0)]),
                  piece.Piece(12, [(0, 0, 0)]),
                  piece.Piece(13, [(0, 0, 0)])]
        rows = self.s.solve(pieces, self.b)
        self.assertTrue(rows)
        self.assertEqual(len(rows), len(pieces))

    def test_rows_to_array_sol(self):
        """
        Ensure rows_to_array_sol correctly converts rows to an array solution.
        """
        pieces = [piece.Piece(11, [(0, 0, 0), (0, 2, 0), (2, 0, 0)]),
                  piece.Piece(12, [(0, 0, 0)]),
                  piece.Piece(13, [(0, 0, 0)])]
        rows = self.s.solve(pieces, self.b)
        solution_array = self.s.rows_to_array_sol(rows, self.b)
        self.assertTrue(solution_array)
        self.assertEqual(len(solution_array), self.b.count_cells())

    def test_generate_solutions(self):
        """
        Ensure generate_solutions correctly generates solutions for the puzzle.
        """
        b = pyramid_board.pyramid_board(5)
        solutions = list(self.s.generate_solutions(self.pieces, b))
        self.assertTrue(solutions)
        self.assertGreater(len(solutions), 0)

    def test_empty_board(self):
        """
        Ensure the solver handles an empty board correctly.
        """
        empty_board = pyramid_board.pyramid_board(0)
        rows = self.s.solve(self.pieces, empty_board)
        self.assertFalse(rows)

    def test_invalid_piece(self):
        """
        Ensure the solver handles an invalid piece correctly.
        """
        invalid_piece = piece.Piece(99, [(0, 0, 0), (0, 0, 1)])
        rows = self.s.solve([invalid_piece], self.b)
        self.assertFalse(rows)