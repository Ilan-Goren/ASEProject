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

    def test_rows_to_array_sol_5_layer(self):
        s = solver.Solver()
        b = pyramid_board.pyramid_board(5)

        pieces = []
        for p in piece.pieces:
            pieces.append(piece.Piece(p))

        rows = s.solve(pieces, b)
        print(s.rows_to_array_sol(rows, b))


    def test_packing_matrix_partial_config(self):
        s = solver.Solver()
        b = pyramid_board.pyramid_board(0)

        array_board = [
            [[1, 0],
             [0, 2]],
            [[0]]
        ]

        b.convert_from_3D_array(array_board)

        pieces = [piece.Piece(3, [(0, 0, 0), (0, 2, 0), (2, 0, 0)])]

        matrix = s.initialise_packing_matrix_partial_config(b, pieces)

    def test_solve_partial_config(self):
        s = solver.Solver()
        b = pyramid_board.pyramid_board(0)

        array_board = [
            [[1, 0],
             [0, 2]],
            [[0]]
        ]

        b.convert_from_3D_array(array_board)

        pieces = [piece.Piece(3, [(0, 0, 0), (0, 2, 0), (2, 0, 0)])]

        rows = s.solve(pieces, b)
        print(s.rows_to_array_sol(rows, b))

    def test_generate_solutions(self):
        s = solver.Solver()
        b = pyramid_board.pyramid_board(0)

        array_board = [
            [[0, 0],
             [0, 0]],
            [[0]]
        ]

        b.convert_from_3D_array(array_board)
        pieces = [piece.Piece(3, [(0, 0, 0), (0, 2, 0), (2, 0, 0)]),
                  piece.Piece(1, [(0, 0, 0)]),
                  piece.Piece(2, [(0, 0, 0)])]

        for rows in s.generate_solutions(pieces, b):
            print(s.rows_to_array_sol(rows, b))

    def test_generate_solutions_with_input(self):
        s = solver.Solver()
        b = pyramid_board.pyramid_board(0)

        array_board = [
            [[0, 0],
             [0, 0]],
            [[0]]
        ]

        b.convert_from_3D_array(array_board)
        pieces = [piece.Piece(3, [(0, 0, 0), (0, 2, 0), (2, 0, 0)]),
                  piece.Piece(1, [(0, 0, 0)]),
                  piece.Piece(2, [(0, 0, 0)])]

        for rows in s.generate_solutions(pieces, b):
            print(s.rows_to_array_sol(rows, b))
            input("Press Enter to continue...")

    def test_generate_solutions_full(self):
        s = solver.Solver()
        b = pyramid_board.pyramid_board(5)

        pieces = []
        for p in piece.pieces:
            pieces.append(piece.Piece(p))

        i = 0
        for rows in s.generate_solutions(pieces, b):
            i += 1
            print(i)