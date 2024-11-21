from django.test import TestCase
from ..solver_functions.solver import Solver
from ..solver_functions.pyramid_board import pyramid_board
from ..solver_functions.piece import Piece

class SolverFunctionsTestCase(TestCase):
    def setUp(self):
        self.solver = Solver()
        self.board = pyramid_board(5)
        self.pieces = [Piece(i) for i in range(1, 13)]

    def test_generate_board_cell_indexes(self):
        """
        Verify that the board cell indexes are generated correctly.
        """
        self.solver.generate_board_cell_indexes(self.board)
        self.assertEqual(len(self.solver.cell_to_index), len(self.board))
        self.assertEqual(len(self.solver.index_to_cell), len(self.board))

    def test_initialise_packing_matrix(self):
        """
        Verify that the packing matrix is initialized correctly.
        """
        matrix = self.solver.initialise_packing_matrix(self.board, self.pieces)
        expected_matrix_size = len(self.board) * len(self.pieces)
        self.assertEqual(len(matrix), expected_matrix_size)

    def test_initialise_packing_matrix_partial_config(self):
        """
        Verify that the packing matrix with partial configuration is initialized correctly.
        """
        matrix = self.solver.initialise_packing_matrix_partial_config(self.board, self.pieces)
        expected_matrix_size = len(self.board) * len(self.pieces)
        self.assertEqual(len(matrix), expected_matrix_size)

    def test_solve(self):
        """
        Verify that the solver finds a solution for the puzzle.
        """
        rows = self.solver.solve(self.pieces, self.board)
        self.assertEqual(len(rows), len(self.board))

    def test_rows_to_array_sol(self):
        """
        Verify that rows are correctly converted to an array solution.
        """
        rows = self.solver.solve(self.pieces, self.board)
        solution_array = self.solver.rows_to_array_sol(rows, self.board)
        self.assertEqual(len(solution_array), len(self.board))

    def test_generate_solutions(self):
        """
        Verify that multiple solutions are generated correctly.
        """
        solutions = list(self.solver.generate_solutions(self.pieces, self.board))
        self.assertGreater(len(solutions), 0)