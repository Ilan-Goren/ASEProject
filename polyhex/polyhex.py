from .solver_functions import solver, piece, board

class Polyhex_Solver:
    """
    Solver class for the Polyhex puzzle.

    This class is responsible for solving the Polyhex puzzle by verifying the board and generating solutions based on the available pieces.

    Attributes:
        board (list): The current state of the Polyhex puzzle board.
        pieces_placed (list): A list of pieces that have already been placed on the board.
    """
    def __init__(self):
        """
        Initializes the Polyhex_Solver instance.

        This constructor sets up the initial empty board and an empty list for the pieces placed on the board.
        """
        self.board = None
        self.pieces_placed = []


    def solve(self, solutions):
        """
        Solves the Polyhex puzzle by generating all possible solutions for the current board state.

        This method uses the `solver.Solver` to generate solutions based on the available pieces and board state. 
        It validates the board before generating the solutions and appends them to the provided `solutions` list.

        Args:
            solutions (multiprocessing.Manager.list): A shared list to store generated solutions.

        Returns:
            bool: True if the solutions were successfully generated, False if the board is invalid.
        """
        s = solver.Solver()
        b = board.Board(self.board)

         # Verify board validity
        if self.board:
            if not b.verify_board():
                b = board.Board()
                print('not valid board')
                return False
            b.board = self.board

        # Prepare pieces to place on the board
        pieces_to_place = []
        for p in piece.pieces:
            print(self.pieces_placed)
            if p in self.pieces_placed:
                continue
            pieces_to_place.append(piece.Piece(p))

        # Generate solutions
        i = 0
        for rows in s.generate_solutions(pieces_to_place, b):
            solutions.append(s.rows_to_array_sol(rows, b))
            i+=1
            print(i)
        return True