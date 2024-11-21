
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
        Test the generate_board_cell_indexes method to ensure it generates indexes correctly.
        """
        self.solver.generate_board_cell_indexes(self.board)
        self.assertTrue(self.solver.cell_to_index)
        self.assertTrue(self.solver.index_to_cell)

    def test_initialise_packing_matrix(self):
        """
        Test the initialise_packing_matrix method to ensure it initializes the packing matrix correctly.
        """
        matrix = self.solver.initialise_packing_matrix(self.board, self.pieces)
        self.assertIsNotNone(matrix)

    def test_initialise_packing_matrix_partial_config(self):
        """
        Test the initialise_packing_matrix_partial_config method to ensure it initializes the packing matrix correctly.
        """
        matrix = self.solver.initialise_packing_matrix_partial_config(self.board, self.pieces)
        self.assertIsNotNone(matrix)

    def test_solve(self):
        """
        Test the solve method to ensure it solves the puzzle correctly.
        """
        rows = self.solver.solve(self.pieces, self.board)
        self.assertTrue(rows)

    def test_rows_to_array_sol(self):
        """
        Test the rows_to_array_sol method to ensure it converts rows to array solution correctly.
        """
        rows = self.solver.solve(self.pieces, self.board)
        solution_array = self.solver.rows_to_array_sol(rows, self.board)
        self.assertTrue(solution_array)

    def test_generate_solutions(self):
        """
        Test the generate_solutions method to ensure it generates solutions correctly.
        """
        solutions = list(self.solver.generate_solutions(self.pieces, self.board))
        self.assertTrue(solutions)