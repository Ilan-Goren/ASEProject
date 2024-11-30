from .solver_functions import solver, pyramid_board, piece
from .solver_functions.piece import pieces


class Pyramid_Solver:
    def __init__(self):
        self.array_board = []
        self.pieces_placed = []

    def solve(self, solutions):
        s = solver.Solver()
        b = pyramid_board.pyramid_board(5)

        if self.array_board:
            b.convert_from_3D_array(self.array_board)

        pieces_to_place = []

        for p in piece.pieces:
            if p in self.pieces_placed:
                continue
            pieces_to_place.append(piece.Piece(p))
        i = 0
        for rows in s.generate_solutions(pieces_to_place, b):
            solutions.append(s.rows_to_array_sol(rows, b))
            i+=1
            print(i)
        return True
