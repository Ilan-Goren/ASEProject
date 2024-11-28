from django.test import TestCase
from pyramid.solver_functions.solver import Solver
from pyramid.solver_functions.pyramid_board import pyramid_board
from pyramid.solver_functions.piece import Piece
from pyramid.solver_functions.algorithm_x_functions import Matrix, add_row, solve, generate_solutions

class SolverTestCase(TestCase):
    def setUp(self):
        # Set up the test case with a solver, a board, and some pieces
        self.solver = Solver()
        self.board = pyramid_board(5)
        self.pieces = [Piece(1), Piece(2)]  # Mock pieces with ids 1 and 2

    def test_generate_board_cell_indexes(self):
        # Test if the board cell indexes are generated correctly
        self.solver.generate_board_cell_indexes(self.board)
        self.assertEqual(len(self.solver.cell_to_index), self.board.count_cells())
        self.assertEqual(len(self.solver.index_to_cell), self.board.count_cells())

    def test_initialise_packing_matrix(self):
        # Test if the packing matrix is initialized correctly
        matrix = self.solver.initialise_packing_matrix(self.board, self.pieces)
        self.assertIsInstance(matrix, Matrix)
        self.assertEqual(matrix.num_rows, self.board.count_cells() + len(self.pieces))

    def test_initialise_packing_matrix_partial_config(self):
        # Test if the packing matrix is initialized correctly with a partially configured board
        self.board.cells[(0, 0, 0)] = 1  # Mock a placed piece
        matrix = self.solver.initialise_packing_matrix_partial_config(self.board, self.pieces)
        self.assertIsInstance(matrix, Matrix)
        self.assertEqual(matrix.num_rows, self.board.count_cells() + len(self.pieces) + 1)

    def test_solve_no_solution(self):
        # Test if the solver correctly identifies no solution
        self.board.cells[(0, 0, 0)] = 1  # Mock a placed piece
        self.pieces = []  # No remaining pieces
        result = self.solver.solve(self.pieces, self.board)
        self.assertFalse(result)

    def test_solve_with_solution(self):
        # Test if the solver finds a solution
        result = self.solver.solve(self.pieces, self.board)
        self.assertTrue(result)

    def test_rows_to_array_sol(self):
        # Test if the rows are correctly converted to a solution array
        rows = [[1, 0, 0, 1], [0, 1, 1, 0]]  # Mock solution rows
        solution_array = self.solver.rows_to_array_sol(rows, self.board)
        self.assertEqual(len(solution_array), self.board.layers)
        self.assertEqual(solution_array[0][0][0], 1)

    def test_generate_solutions(self):
        # Test if the solver generates solutions
        solutions = list(self.solver.generate_solutions(self.pieces, self.board))
        self.assertTrue(solutions)
