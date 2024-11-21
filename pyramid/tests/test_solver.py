from django.test import TestCase
from ..solver_functions import solver, pyramid_board, piece, algorithm_x_functions

class SolverTestCase(TestCase):
    def test_generate_board_cell_indexes(self):
        """
        Test the generate_board_cell_indexes method to ensure it generates indexes correctly.
        """
        s = solver.Solver()
        b = pyramid_board.pyramid_board(2)
        s.generate_board_cell_indexes(b)
        self.assertTrue(b.cells)
        self.assertTrue(s.index_to_cell)
        self.assertTrue(s.cell_to_index)

    def test_packing_matrix(self):
        """
        Test the initialise_packing_matrix method to ensure it initializes the packing matrix correctly.
        """
        s = solver.Solver()
        b = pyramid_board.pyramid_board(2)
        pieces = [piece.Piece(p) for p in piece.pieces]
        s.initialise_packing_matrix(b, pieces)
        self.assertEqual(s.matrix.num_cols, b.count_cells() + len(pieces))

    def test_solve(self):
        """
        Test the solve method to ensure it solves the puzzle correctly.
        """
        s = solver.Solver()
        b = pyramid_board.pyramid_board(2)
        pieces = [piece.Piece(11, [(0, 0, 0), (0, 2, 0), (2, 0, 0)]),
                  piece.Piece(12, [(0, 0, 0)]),
                  piece.Piece(13, [(0, 0, 0)])]
        rows = s.solve(pieces, b)
        self.assertTrue(rows)

    def test_rows_to_array_sol(self):
        """
        Test the rows_to_array_sol method to ensure it converts rows to array solution correctly.
        """
        s = solver.Solver()
        b = pyramid_board.pyramid_board(2)
        pieces = [piece.Piece(11, [(0, 0, 0), (0, 2, 0), (2, 0, 0)]),
                  piece.Piece(12, [(0, 0, 0)]),
                  piece.Piece(13, [(0, 0, 0)])]
        rows = s.solve(pieces, b)
        solution_array = s.rows_to_array_sol(rows, b)
        self.assertTrue(solution_array)

    def test_generate_solutions(self):
        """
        Test the generate_solutions method to ensure it generates solutions correctly.
        """
        s = solver.Solver()
        b = pyramid_board.pyramid_board(5)
        pieces = [piece.Piece(p) for p in piece.pieces]
        solutions = list(s.generate_solutions(pieces, b))
        self.assertTrue(solutions)