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
        self.pieces = [Piece(i) for i in range(1, 13)]  

    def test_generate_board_cell_indexes(self):
        # Test if the board cell indexes are generated correctly
        self.solver.generate_board_cell_indexes(self.board)
        self.assertEqual(len(self.solver.cell_to_index), self.board.count_cells())
        self.assertEqual(len(self.solver.index_to_cell), self.board.count_cells())

    def test_initialise_packing_matrix(self):
        # Adjust the expected number of columns
        matrix = self.solver.initialise_packing_matrix(self.board, self.pieces)
        expected_cols = self.board.count_cells() + len(self.pieces)
        self.assertIsInstance(matrix, Matrix)
        self.assertEqual(matrix.num_cols, expected_cols)

    def test_initialise_packing_matrix_partial_config(self):
         # Adjust the expected number of columns
         self.board.cells[(0, 0, 0)] = 1
         pieces_to_place = [Piece(i) for i in range(2, 13)]
         matrix = self.solver.initialise_packing_matrix_partial_config(self.board, pieces_to_place)
         expected_cols = self.board.count_cells() + len(pieces_to_place) + 1  
         self.assertEqual(matrix.num_cols, expected_cols)

    def test_solve_no_solution(self):
        # Test if the solver correctly identifies no solution
        self.board.cells[(0, 0, 0)] = 1  
        self.pieces = []  
        result = self.solver.solve(self.pieces, self.board)
        self.assertFalse(result)

    def test_solve_with_solution(self):
         # Ensure the solver finds a solution
         result = self.solver.solve(self.pieces, self.board)
         self.assertTrue(result)  

    def test_rows_to_array_sol(self):
         # Use a real solution generation
         solutions = []
         for i, solution in enumerate(self.solver.generate_solutions(self.pieces, self.board)):
             if i >= 5:
                 break
             solutions.append(solution)
         if solutions:
             rows = solutions[0]  # Use the first generated solution
             solution_array = self.solver.rows_to_array_sol(rows, self.board)
             self.assertEqual(len(solution_array), self.board.layers)
             self.assertTrue(all(isinstance(layer, list) for layer in solution_array))  

    def test_generate_solutions(self):
         # Ensure the solver generates solutions
         solutions = []
         for i, solution in enumerate(self.solver.generate_solutions(self.pieces, self.board)):
             if i >= 5:
                 break
             solutions.append(solution)
         self.assertEqual(len(solutions), 5)