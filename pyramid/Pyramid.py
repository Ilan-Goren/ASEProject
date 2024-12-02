from .solver_functions import solver, pyramid_board, piece
from .solver_functions.piece import pieces


class Pyramid_Solver:
    """
    A class to solve 3D pyramid puzzles by generating valid configurations
    for placing pieces on a board.

    Attributes
    ----------
    array_board : list
        A 3D array representing the current state of the pyramid board.
    pieces_placed : list
        A list of pieces that are already placed on the board.

    Methods
    -------
    solve(solutions)
        Generates and appends all possible solutions to the provided `solutions` list
        based on the current board state and pieces not yet placed.
    """

    def __init__(self):
        """
        Initializes the Pyramid_Solver with an empty board and no pieces placed.
        """
        self.array_board = []
        self.pieces_placed = []

    def solve(self, solutions):
        """
        Generates solutions for the pyramid puzzle.

        Parameters
        ----------
        solutions : list
            A list to store the generated solutions. Each solution is appended as a
            3D array representing a valid configuration of the pyramid.

        Returns
        -------
        bool
            Always returns True after generating and appending all solutions.

        Notes
        -----
        - Converts the current board state from a 3D array format before solving.
        - Skips pieces already placed on the board.
        - Uses an external solver module to generate valid solutions.
        - Prints the solution count incrementally during the process.
        """
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
            i += 1
            print(i)
        return True
