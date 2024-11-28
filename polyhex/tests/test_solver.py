from django.test import TestCase

from ..solver_functions import solver, board, piece, algorithm_x_functions

class HexSolverTestCase(TestCase):
    def test_generate_board_cell_indexes(self):
        s = solver.Solver()
        b = board.Board()
        s.generate_board_cell_indexes(b.board)
        print(b.board)
        print(s.index_to_cell)
        print(s.cell_to_index)

    def test_packing_matrix(self):
        s = solver.Solver()
        b = board.Board()
        pieces = []
        for p in piece.pieces:
            pieces.append(piece.Piece(p))

        s.initialise_packing_matrix(b, pieces)
        print(algorithm_x_functions.pretty_print(s.matrix))

    def test_packing_matrix_partial_config(self):
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
        print(algorithm_x_functions.pretty_print(s.matrix))