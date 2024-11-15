from django.test import TestCase

from ..solver_functions import solver, pyramid_board, piece, algorithm_x_functions

class SolverTestCase(TestCase):
    def test_generate_board_cell_indexes(self):
        s = solver.Solver()
        b = pyramid_board.pyramid_board(2)
        s.generate_board_cell_indexes(b)
        print(b.cells)
        print(s.index_to_cell)
        print(s.cell_to_index)

    def test_packing_matrix(self):
        s = solver.Solver()
        b = pyramid_board.pyramid_board(2)
        pieces = []
        for p in piece.pieces:
            pieces.append(piece.Piece(p))

        s.initialise_packing_matrix(b, pieces)
        # num cols in matrix should be num of board cells + num of pieces
        #print(b.count_cells())
        #print(len(pieces))
        #print(s.matrix.num_cols)
        #print(algorithm_x_functions.pretty_print(s.matrix))

    def test_solve(self):
        s = solver.Solver()
        b = pyramid_board.pyramid_board(2)
        pieces = []

        pieces.append(piece.Piece(11, [(0, 0, 0), (0, 2, 0), (2, 0, 0)]))
        pieces.append(piece.Piece(12, [(0, 0, 0)]))
        pieces.append(piece.Piece(13, [(0, 0, 0)]))

        print(s.solve(pieces, b))

    def test_rows_to_array_sol(self):
        s = solver.Solver()
        b = pyramid_board.pyramid_board(2)
        pieces = []

        pieces.append(piece.Piece(11, [(0, 0, 0), (0, 2, 0), (2, 0, 0)]))
        pieces.append(piece.Piece(12, [(0, 0, 0)]))
        pieces.append(piece.Piece(13, [(0, 0, 0)]))

        rows = s.solve(pieces, b)
        print(s.rows_to_array_sol(rows,b))
