from .solver_functions import solver, pyramid_board, piece
from .solver_functions.piece import pieces

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


def pyramid_get_partial_config_solutions(array_board, pieces_placed):
    s = solver.Solver()
    b = pyramid_board.pyramid_board(5)
    solutions = []

    b.convert_from_3D_array(array_board)

    pieces_to_place = []

    for p in list(pieces.keys()):
        if p in pieces_placed:
            continue
        pieces_to_place.append(piece.Piece(p))

    for rows in s.generate_solutions(pieces_to_place, b):
        solutions.append(s.rows_to_array_sol(rows, b))
    return solutions
