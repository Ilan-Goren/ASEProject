from django.test import TestCase

from ..solver_functions import solver, board, piece, algorithm_x_functions

class HexSolverTestCase(TestCase):
    """
    Test cases for the Solver class and helper functions functionality.
    """
    def test_generate_board_cell_indexes(self):
        """
        Test the `generate_board_cell_indexes` function.

        This function verifies the board cell indexing, ensuring that:
        - The generated board matches the expected board structure.
        - The `index_to_cell` and `cell_to_index` mappings are accurate.
        - Mappings are bidirectional and consistent.

        :return: None
        """
        s = solver.Solver()
        b = board.Board()
        s.generate_board_cell_indexes(b.board)
        expected_board = [[[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0], [0, 0], [0]], [[0, 0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0], [0, 0], [0]], [[0, 0, 0, 0], [0, 0, 0], [0, 0], [0]], [[0, 0, 0], [0, 0], [0]], [[0, 0], [0]], [[0]]]
        expected_index_to_cell = {1: (0, 0, 0), 2: (1, 0, 0), 3: (2, 0, 0), 4: (3, 0, 0), 5: (4, 0, 0), 6: (5, 0, 0), 7: (0, 1, 0), 8: (1, 1, 0), 9: (2, 1, 0), 10: (3, 1, 0), 11: (4, 1, 0), 12: (0, 2, 0), 13: (1, 2, 0), 14: (2, 2, 0), 15: (3, 2, 0), 16: (0, 3, 0), 17: (1, 3, 0), 18: (2, 3, 0), 19: (0, 4, 0), 20: (1, 4, 0), 21: (0, 5, 0), 22: (0, 0, 1), 23: (1, 0, 1), 24: (2, 0, 1), 25: (3, 0, 1), 26: (4, 0, 1), 27: (0, 1, 1), 28: (1, 1, 1), 29: (2, 1, 1), 30: (3, 1, 1), 31: (0, 2, 1), 32: (1, 2, 1), 33: (2, 2, 1), 34: (0, 3, 1), 35: (1, 3, 1), 36: (0, 4, 1), 37: (0, 0, 2), 38: (1, 0, 2), 39: (2, 0, 2), 40: (3, 0, 2), 41: (0, 1, 2), 42: (1, 1, 2), 43: (2, 1, 2), 44: (0, 2, 2), 45: (1, 2, 2), 46: (0, 3, 2), 47: (0, 0, 3), 48: (1, 0, 3), 49: (2, 0, 3), 50: (0, 1, 3), 51: (1, 1, 3), 52: (0, 2, 3), 53: (0, 0, 4), 54: (1, 0, 4), 55: (0, 1, 4), 56: (0, 0, 5)}
        expected_cell_to_index = {(0, 0, 0): 1, (1, 0, 0): 2, (2, 0, 0): 3, (3, 0, 0): 4, (4, 0, 0): 5, (5, 0, 0): 6, (0, 1, 0): 7, (1, 1, 0): 8, (2, 1, 0): 9, (3, 1, 0): 10, (4, 1, 0): 11, (0, 2, 0): 12, (1, 2, 0): 13, (2, 2, 0): 14, (3, 2, 0): 15, (0, 3, 0): 16, (1, 3, 0): 17, (2, 3, 0): 18, (0, 4, 0): 19, (1, 4, 0): 20, (0, 5, 0): 21, (0, 0, 1): 22, (1, 0, 1): 23, (2, 0, 1): 24, (3, 0, 1): 25, (4, 0, 1): 26, (0, 1, 1): 27, (1, 1, 1): 28, (2, 1, 1): 29, (3, 1, 1): 30, (0, 2, 1): 31, (1, 2, 1): 32, (2, 2, 1): 33, (0, 3, 1): 34, (1, 3, 1): 35, (0, 4, 1): 36, (0, 0, 2): 37, (1, 0, 2): 38, (2, 0, 2): 39, (3, 0, 2): 40, (0, 1, 2): 41, (1, 1, 2): 42, (2, 1, 2): 43, (0, 2, 2): 44, (1, 2, 2): 45, (0, 3, 2): 46, (0, 0, 3): 47, (1, 0, 3): 48, (2, 0, 3): 49, (0, 1, 3): 50, (1, 1, 3): 51, (0, 2, 3): 52, (0, 0, 4): 53, (1, 0, 4): 54, (0, 1, 4): 55, (0, 0, 5): 56}
        self.assertEqual(b.board, expected_board)
        self.assertEqual(s.index_to_cell, expected_index_to_cell)
        self.assertEqual(s.cell_to_index, expected_cell_to_index)
        for key, value in s.index_to_cell.items():
            self.assertTrue(value in s.cell_to_index.keys())
            self.assertTrue(s.cell_to_index[value] in  s.index_to_cell.keys())

    def test_packing_matrix(self):
        """
        Test the initialization of the packing matrix.

        This function ensures that:
        - The packing matrix has the correct number of columns and rows in the default case of an empty board.
        - The matrix configuration aligns with the board's cell count and the number of pieces.

        :return: None
        """
        s = solver.Solver()
        b = board.Board()
        pieces = []
        for p in piece.pieces:
            pieces.append(piece.Piece(p))

        s.initialise_packing_matrix(b, pieces)
        self.assertEqual(s.matrix.num_cols, b.count_cells() + len(pieces))
        self.assertEqual(s.matrix.num_rows, 4224)

    def test_packing_matrix_partial_config(self):
        """
        Test the initialization of the packing matrix with a partial board configuration.

        This function verifies:
        - The handling of pre-filled board cells.
        - The packing matrix correctly accounts for pieces excluded from the initial configuration.

        :return: None
        """
        s = solver.Solver()
        b = board.Board()
        pieces = []
        for p in piece.pieces:
            if p != 11:
                pieces.append(piece.Piece(p))

        b.board[0][0][0] = 11
        b.board[0][1][0] = 11
        b.board[1][0][0] = 11
        b.board[1][1][0] = 11

        s.initialise_packing_matrix_partial_config(b, pieces)
        self.assertEqual(s.matrix.num_cols, b.count_cells() + len(pieces) + 1) # + 1 as piece 11 was never added to pieces[]
        self.assertEqual(s.matrix.num_rows, 3375)


    def test_solve(self):
        """
        Test the solving functionality of the solver.

        This function ensures:
        - Pieces are correctly placed on the board.
        - The generated solution is valid and verified against the board constraints.

        :return: None
        """
        s = solver.Solver()
        b = board.Board()
        pieces = []
        for p in piece.pieces:
            pieces.append(piece.Piece(p))

        rows = s.solve(pieces, b)
        sol = s.rows_to_array_sol(rows, b)
        self.assertTrue(sol)
        b.board = sol
        self.assertTrue(b.verify_board()) # use verify board to check all pieces are placed in valid placements

    def test_generate_solutions(self):
        """
        Test the generation of multiple solutions.

        This function verifies:
        - The solver can generate multiple valid solutions.
        - Each solution satisfies board constraints and piece placements.
        - The process stops after 10 solutions have been generated to save on runtime of the test.

        :return: None
        """
        s = solver.Solver()
        b = board.Board()
        pieces = []
        for p in piece.pieces:
            pieces.append(piece.Piece(p))

        count = 1
        for rows in s.generate_solutions(pieces, b):
            if count >= 10:
                break
            sol = s.rows_to_array_sol(rows, b)
            self.assertTrue(sol)
            b.board = sol
            self.assertTrue(b.verify_board())  # use verify board to check all pieces are placed in valid placements
            count += 1
        self.assertEqual(count, 10)

