from .solver_functions import matrix_polyominoes, matrix_solver
from .solver_functions import matrix_transformations

class Polysphere:
    """
    A class to manage the Polysphere puzzle board, pieces, and solution generation.

    Attributes:
        pieces (dict): A dictionary containing the different puzzle pieces.
        pieces_left (dict): A copy of pieces indicating which pieces are yet to be placed.
        board_size (tuple): The dimensions of the puzzle board.
        board (list): The puzzle board grid.
        piece_positions (dict): A dictionary tracking the positions of placed pieces.
        all_solutions_partial_config (list): Stores solutions for partial configurations.
    """
    def __init__(self):
        self.pieces = {
            'A': [[1, 1, 1],
                [1, 0, 1]],

            'B': [[0, 0, 1, 1],
                [1, 1, 1, 0]],

            'C': [[0, 1, 0],
                [1, 1, 0],
                [0, 1, 1]],

            'D': [[0, 1, 0],
                [1, 1, 1]],

            'E': [[0, 1, 0, 0],
                [1, 1, 1, 1]],

            'F': [[0, 1, 1],
                [1, 1, 1]],

            'G': [[0, 1, 1],
                [1, 1, 0]],

            'H': [[1, 1],
                [1, 0],
                [1, 0]],

            'I': [[1, 1, 1],
                [0, 0, 1],
                [0, 0, 1]],

            'J': [[1, 0, 0, 0],
                [1, 1, 1, 1]],

            'K': [[1, 0],
                [1, 1]],

            'L': [[1, 1, 0],
                [0, 1, 1],
                [0, 0, 1]],
        }
        self.pieces_left = self.pieces.copy()
        self.board_size = (5, 11)
        self.board = [[0 for _ in range(self.board_size[1])] for _ in range(self.board_size[0])]
        self.piece_positions = {}
        self.all_solutions_partial_config = []

    def place_piece(self, piece_key, positions):
        """
        Places a piece on the board at specified positions if valid.

        Args:
            piece_key (str): The key of the piece.
            positions (list): List of (row, col) tuples where the piece should be placed.

        Returns:
            bool: True if the piece was successfully placed, False otherwise.
        """
        piece = self.pieces[piece_key]

        if not self.is_valid_placement(positions):
            print(f"Invalid placement for {piece_key} at {positions}")
            return False

        # Check for already placed positions
        if piece_key in list(self.piece_positions.keys()):
            print(f"{piece_key} already placed at {positions}")
            return False
        
        self.piece_positions[piece_key] = []

        # Place the piece on the board and update piece_positions
        for pos in positions:
            row, col = pos
            self.board[row][col] = piece_key  # Mark the position on the board

            # Add the position to piece_positions for tracking
            self.piece_positions[piece_key].append(pos)

        self.pieces_left.pop(piece_key)
        print(f"Placed {piece_key} at {self.piece_positions[piece_key]}")
        return True

    def remove_piece(self, piece_key):
        """
        Remove a piece from the board.

        Args:
            piece_key (str): The key of the piece.

        Returns:
            bool: True if the piece was successfully removed, False otherwise.
        """
        if piece_key not in list(self.piece_positions.keys()):
            print(f"Piece {piece_key} not in piece posistions")
            return  False # No such piece on the board

        # Get the positions occupied by the piece
        occupied_positions = self.piece_positions[piece_key]

        # Clear the positions on the board
        for pos in occupied_positions:
            row, col = pos
            self.board[row][col] = 0  # Mark as empty

        # Remove the piece from piece_positions
        print(f"Removed {piece_key} at {self.piece_positions[piece_key]}")
        del self.piece_positions[piece_key]

        self.pieces_left[piece_key] = self.pieces[piece_key]
        return True
    
    def is_board_filled(self):
        """
        Checks if all pieces have been placed on the board.

        Returns:
            bool: True if the board is filled, False otherwise.
        """
        if not self.pieces_left:
            return True
        return False
    
    def is_board_empty(self):
        """
        Checks if no pieces are placed on board.

        Returns:
            bool: True if the board is empty, False otherwise.
        """
        for row in self.board:
            for col in row:
                if col:
                    return False
        return True
    
    def is_valid_placement(self, positions):
        """
        Checks if piece position to be plaecd is not out of boards and
        no other pieces are placed in same position.

        Args:
            positions (list): List of (row, col) tuples where the piece is to be placed.

        Returns:
            bool: True if valid placemenet, False otherwise.
        """
        for pos in positions:
            row, col = pos
            # Check if the current position is out of bounds
            if row < 0 or row >= self.board_size[0] or col < 0 or col >= self.board_size[1]:
                return False
            
            # Check if the cell is already filled
            if self.board[row][col] == 1:
                return False
                
        # If all positions are valid, return True
        return True

    
    def rotate_piece(self, piece_key):
        """
        Rotates the piece 90 degrees and store it in the board.

        Args:
            piece_key (str): The key of the piece.

        Returns:
            bool: True if rotated successfully, False otherwise.
        """
        if piece_key not in self.pieces_left.keys() or piece_key in self.piece_positions.keys():
            print(f"Rotation {piece_key} Error")
            return False
        
        # Get the current piece matrix
        piece = self.pieces_left[piece_key]

        # Rotate the piece 90 degrees clockwise and store in pieces
        self.pieces_left[piece_key] = [list(reversed(col)) for col in zip(*piece)]
        print(f"Success: Rotation {piece_key} complete")

        return True
    
    def flip_piece(self, piece_key):
        """
        Flip the piece horizontally and store it in the board.

        Args:
            piece_key (str): The key of the piece.

        Returns:
            bool: True if flipped successfully, False otherwise.
        """
        if piece_key not in self.pieces_left.keys() or piece_key in self.piece_positions.keys():
            print(f"Flip {piece_key} Error")
            return False
        
        # Get the current piece matrix
        piece = self.pieces_left[piece_key]

        # Flip the piece vertically by reversing the order of the rows
        self.pieces_left[piece_key] = piece[::-1]
        print(f"Success: Flip {piece_key} complete")

        return True
    
    def reset_board(self):
        """
        Resets all the class attributes.
        """
        self.board = [[0 for _ in range(self.board_size[1])] for _ in range(self.board_size[0])]
        self.pieces_left = self.pieces.copy()
        self.piece_positions = {}
        self.all_solutions_partial_config = []
        return
    
    def solve_partial_config(self):
        """
        Gets a solution for the current board and stores it in self.board attribute.

        Returns:
            bool: True if solved successfully, False is no solutions found.
        """
        already_placed = board_conversion_from_letter_to_id(self.board)

        already_placed_ids = {id - 1 for row in already_placed for id in row if id}
        polys = []
        for i in range(12):
            if i in already_placed_ids:
                continue
            polys.append(matrix_polyominoes.Polyomino(matrix_polyominoes.POLYOMINOES[i]["tiles"], i + 1))
        id_conversions = []
        solver = matrix_solver.MatrixSolver()
        solution = solver.solve_packing(polys,11, 5, already_placed, id_conversions)
        if not solution:
            return False
        solution = solver.revert_ids(id_conversions, solution)
        solution = board_conversion_from_id_to_letter(solution)
        print(f"Solved after conversion to Letters: {solution}")
        self.board = solution

        piece_pos = get_pieces_positions_from_board(self.board)
        self.piece_positions = piece_pos.copy()
        self.pieces_left = {}
        return True
    
    def solve_all_partial_config(self):
        """
        Gets all solutions for the current board and stores it in 
        self.all_solutions_partial_config attribute.

        Returns:
            bool: True if solved successfully, False is no solutions found.
        """
        self.all_solutions_partial_config = []
        alreadyPlaced = board_conversion_from_letter_to_id(self.board)
        already_placed_ids = {id - 1 for row in alreadyPlaced for id in row if id}
        polys = []
        for i in range(12):
            if i in already_placed_ids:
                continue
            polys.append(matrix_polyominoes.Polyomino(matrix_polyominoes.POLYOMINOES[i]["tiles"], i + 1))

        s = matrix_solver.MatrixSolver()
        id_conversions = []

        for rows in s.generate_packing_solutions(polys, 11, 5, alreadyPlaced, id_conversions):
            # Have to now print packing separately from the solver solving function now it's a generator
            sol = s.print_packing(rows, 11, 5)

            sol_reverted = s.revert_ids(id_conversions, sol)
            if sol_reverted != None:
                sol_reverted = board_conversion_from_id_to_letter(sol_reverted)
                self.all_solutions_partial_config.append(sol_reverted)

        if not self.all_solutions_partial_config:
            return False
        return True
    
##########################################################################################
#                                  HELPER FUNCTIONS                                      #
##########################################################################################
    
def board_conversion_from_letter_to_id(board):
    ''' Function changes placed pieces from letters to ID '''
    rep = { 'A' : 1, 'B': 2, 'C' : 3, 'D' : 4, 'E' : 5, 'F' : 6, 
            'G': 7, 'H': 8, 'I': 9, 'J' : 10, 'K' : 11, 'L' : 12}
    new_board = [[0 for _ in range(11)] for _ in range(5)] # New Board to return

    for row_index, row in enumerate(board):
        for cell_index, cell in enumerate(row):
            if cell in rep:
                new_board[row_index][cell_index] = rep[cell]
    return new_board

def board_conversion_from_id_to_letter(board):
    ''' Function changes placed pieces from ID to letters '''
    rep = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 
           7: 'G', 8: 'H', 9: 'I', 10: 'J', 11: 'K', 12: 'L'}
    new_board = [[0 for _ in range(11)] for _ in range(5)] # New Board to return

    for row_index, row in enumerate(board):
        for cell_index, cell in enumerate(row):
            if cell in rep:
                new_board[row_index][cell_index] = rep[cell]
    return new_board


def get_pieces_positions_from_board(board):
    piecesPos = {}
    for row_index, row_data in enumerate(board):
        for col_index, col_data in enumerate(row_data):
            if col_data not in piecesPos.keys():
                piecesPos[col_data] = [(row_index, col_index)]
            else:
                piecesPos[col_data].append((row_index, col_index))

    return piecesPos


def get_all_solutions(solutions):
    ''' Function takes a list that will store the solutions in. See documentions on matrix_solver'''
    polys = []
    for p in matrix_polyominoes.POLYOMINOES:
        # Iterating over all polys to get them all in a list.
        poly = matrix_polyominoes.Polyomino(p["tiles"],p["poly_id"])
        polys.append(poly)

    s = matrix_solver.MatrixSolver()
    id_conversions = []
    solution_count = 0

    for rows in s.generate_packing_solutions(polys, 11, 5, None, id_conversions):
        # Have to now print packing separately from the solver solving function now it's a generator
            sol = s.print_packing(rows, 11, 5)

            sol_reverted = s.revert_ids(id_conversions, sol)

            if sol_reverted != None:
                solution_count += 1
                sol_reverted = board_conversion_from_id_to_letter(sol_reverted)
                solutions.append(sol_reverted)
            

