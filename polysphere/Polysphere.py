from copy import deepcopy

class Polysphere:
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
        self.piecesAvailabe = list(self.pieces.keys())
        self.piece_positions = {}

    def place_piece(self, piece_key, positions):
        """Place the piece on the board at the specified list of positions."""
        piece = self.pieces[piece_key]

        if not self.is_valid_placement(piece, positions):
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
        """Remove the piece from the board."""
        if piece_key not in list(self.piece_positions.keys()):
            print(f"Piece {piece_key} not in piece posistions")
            return  False# No such piece on the board

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
        """Check if no pieces are left and returns True else False"""
        if not self.pieces_left:
            return True
        return False
    
    def is_valid_placement(self, piece, positions):
        """Check if the piece can be placed on the board at the given positions."""
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
        """Rotate the specified piece 90 degrees."""
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
        self.board = [[0 for _ in range(self.board_size[1])] for _ in range(self.board_size[0])]
        self.pieces_left = self.pieces.copy()
        self.piece_positions = {}
        return
    
    def internalConversionFromLetterToPos(self, board):
        ''' Function changes placed pieces from letters to ID '''
        rep = { 'A' : 1, 'B': 2, 'C' : 3, 'D' : 4, 'E' : 5, 'F' : 6, 
               'G': 7, 'H': 8, 'I': 9, 'I': 10, 'J' : 11, 'K' : 12}
        for row in board:
            for cell in row:
                if cell in rep.keys():
                    cell = rep[cell]
        return board