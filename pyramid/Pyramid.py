from .solver_functions import solver, pyramid_board, piece

class Pyramid:
    def __init__(self):
        pass
    def solve_partial_config(self, pyramid):
        pass
    def generate_all_solutions(self):
        pass


def pyramid_get_all_solutions(solutions):
    s = solver.Solver()
    b = pyramid_board.pyramid_board(5)

    pieces = []
    for p in piece.pieces:
        pieces.append(piece.Piece(p))

    i = 0
    for rows in s.generate_solutions(pieces, b):
        solutions.append(s.rows_to_array_sol(rows, b))
        i+=1
        print(i)


def pyramid_get_partial_config_solutions(array_board, pieces):
    s = solver.Solver()
    b = pyramid_board.pyramid_board(5)
    print(array_board)

    b.convert_from_3D_array(array_board)
    print(b)

    piecesPlaced = []
    for p in pieces:
        piecesPlaced.append(piece.Piece(p))

    rows = s.solve(piecesPlaced, b)
    return s.rows_to_array_sol(rows, b)