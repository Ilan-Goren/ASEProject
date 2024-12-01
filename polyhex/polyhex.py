from .solver_functions import solver, piece, board


class Polyhex_Solver:
    def __init__(self):
        self.board = None
        self.pieces_placed = []


    def solve(self, solutions):
        s = solver.Solver()
        b = board.Board(self.board)

        if self.board:
            if not b.verify_board():
                b = board.Board()
                print('not valid board')
                return False
            b.board = self.board

        pieces_to_place = []
        for p in piece.pieces:
            print(self.pieces_placed)
            if p in self.pieces_placed:
                continue
            pieces_to_place.append(piece.Piece(p))

        i = 0
        for rows in s.generate_solutions(pieces_to_place, b):
            solutions.append(s.rows_to_array_sol(rows, b))
            i+=1
            print(i)
        return True