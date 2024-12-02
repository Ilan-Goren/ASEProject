from django.test import TestCase
from pyramid.solver_functions.solver import Solver
from pyramid.solver_functions.pyramid_board import pyramid_board
from pyramid.solver_functions.piece import Piece
from pyramid.solver_functions.algorithm_x_functions import Matrix

class SolverTestCase(TestCase):
    def setUp(self):
        # Initialize the solver, board, and pieces for each test
        self.solver = Solver()
        self.board = pyramid_board(5)
        self.pieces = [Piece(1), Piece(2)]  # Mock pieces with ids 1 and 2
        self.solver.id_conversions = {1: 1, 2: 2, -51: 0, -52: 0}  # Mock id conversions

    def test_generate_board_cell_indexes(self):
        # Test if the board cell indexes are generated correctly
        self.solver.generate_board_cell_indexes(self.board)
        self.assertEqual(len(self.solver.cell_to_index), self.board.count_cells())
        self.assertEqual(len(self.solver.index_to_cell), self.board.count_cells())

    def test_initialise_packing_matrix(self):
        # Adjust the expected number of rows
        matrix = self.solver.initialise_packing_matrix(self.board, self.pieces)
        expected_rows = self.board.count_cells() + len(self.pieces)  # Adjust this logic if needed
        self.assertIsInstance(matrix, Matrix)
        self.assertEqual(matrix.num_rows, expected_rows)

    def test_initialise_packing_matrix_partial_config(self):
        # Adjust the expected number of rows
        self.board.cells[(0, 0, 0)] = 1  # Mock a placed piece
        matrix = self.solver.initialise_packing_matrix_partial_config(self.board, self.pieces)
        expected_rows = self.board.count_cells() + len(self.pieces) + 1  # Adjust this logic if needed
        self.assertIsInstance(matrix, Matrix)
        self.assertEqual(matrix.num_rows, expected_rows)

    def test_solve_no_solution(self):
        # Test if the solver correctly identifies no solution
        self.board.cells[(0, 0, 0)] = 1  # Mock a placed piece
        self.pieces = []  # No remaining pieces
        result = self.solver.solve(self.pieces, self.board)
        self.assertFalse(result)

    def test_solve_with_solution(self):
        # Ensure the solver finds a solution
        result = self.solver.solve(self.pieces, self.board)
        self.assertTrue(result)

    def test_rows_to_array_sol(self):
        # Fix the rows_to_array_sol method
        rows = [[1, 0, 0, 1], [0, 1, 1, 0]]  # Mock solution rows
        self.solver.id_conversions = {1: 1, 2: 2, -51: 0, -52: 0}  # Ensure poly_id exists in id_conversions
        solution_array = self.solver.rows_to_array_sol(rows, self.board)
        self.assertEqual(len(solution_array), self.board.layers)
        self.assertEqual(solution_array[0][0][0], 1)

    def test_generate_solutions(self):
        # Ensure the solver generates solutions
        solutions = list(self.solver.generate_solutions(self.pieces, self.board))
        self.assertTrue(solutions)
