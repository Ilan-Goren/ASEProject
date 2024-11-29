from .solver_functions import solver, piece, board

def solve_partial_config(board, pieces_placed):
    s = solver.Solver()
    b = board
    pieces = []
    for p in piece.pieces:
        if p in pieces_placed:
            continue
        pieces.append(piece.Piece(p))

    rows = s.solve(pieces, b)
    print(s.rows_to_array_sol(rows, b))