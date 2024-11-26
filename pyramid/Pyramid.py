from .solver_functions.solver import Solver, pyramid_board, piece

class Pyramid:
    def __init__(self):
        pass
    def solve_partial_config(self, pyramid):
        pass
    def generate_all_solutions(self):
        pass


def pyramid_get_all_solutions(solutions):
    s = Solver()
    b = pyramid_board.pyramid_board(5)

    pieces = []
    for p in piece.pieces:
        pieces.append(piece.Piece(p))

    i = 0
    for rows in s.generate_solutions(pieces, b):
        solutions.append(s.rows_to_array_sol(rows, b))
        i+=1
        print(i)