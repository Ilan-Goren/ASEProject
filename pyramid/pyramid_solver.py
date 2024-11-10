class PyramidSolver:
    def __init__(self):
        # Initialize the board as a 3D grid to represent the level 5 pyramid
        self.levels = 5  # Number of levels in the pyramid
        self.board = self._initialize_board()
        self.pieces_left = self._initialize_pieces()
        self.piece_positions = {}  # To track the positions of placed pieces

    def _initialize_board(self):
        """
        Initializes a 3D list representing the board for the level 5 pyramid.
        Each level is a 2D grid with decreasing dimensions.
        """
        board = []
        for level in range(self.levels):
            # Create a 2D grid for each level with decreasing size
            grid_size = self.levels - level
            level_grid = [[None for _ in range(grid_size)] for _ in range(grid_size)]
            board.append(level_grid)
        return board

    def _initialize_pieces(self):
        """
        Initializes the list of pieces available for placement.
        For now, this can be a placeholder that returns a simple set of pieces.
        """
        # Example placeholder for pieces: List of dictionaries representing piece data
        return [
            {"id": 1, "shape": "T", "color": "red"},
            {"id": 2, "shape": "L", "color": "green"},
            {"id": 3, "shape": "Z", "color": "blue"},
            # Add more piece representations as needed
        ]

    def place_piece(self, piece_id, level, row, col):
        """
        Places a piece on the board at the specified level, row, and column.
        """
        # Check if the piece exists and is available
        piece = next((p for p in self.pieces_left if p["id"] == piece_id), None)
        if not piece:
            return False  # Piece not found or already placed
        
        # Example logic to place the piece (simplified, expand as needed)
        if self._can_place(piece, level, row, col):
            self.board[level][row][col] = piece["id"]  # Place the piece
            self.pieces_left.remove(piece)  # Remove from available pieces
            self.piece_positions[piece_id] = (level, row, col)
            return True
        return False

    def _can_place(self, piece, level, row, col):
        """
        Checks if a piece can be placed at the specified location.
        """
        # Check if the position is within bounds
        if level < 0 or level >= self.levels:
            return False
        if row < 0 or row >= len(self.board[level]):
            return False
        if col < 0 or col >= len(self.board[level][row]):
            return False
        
        # Check if the space is empty
        if self.board[level][row][col] is not None:
            return False
        
        # Additional placement logic can be added here (e.g., shape fitting)
        return True

    def remove_piece(self, piece_id):
        """
        Removes a piece from the board and returns it to the available pieces.
        """
        if piece_id in self.piece_positions:
            level, row, col = self.piece_positions[piece_id]
            self.board[level][row][col] = None  # Clear the spot
            piece = {"id": piece_id, "shape": "Unknown", "color": "Unknown"}  # Example placeholder
            self.pieces_left.append(piece)  # Return to available pieces
            del self.piece_positions[piece_id]  # Remove from positions tracking
            return True
        return False

    def is_board_empty(self):
        """
        Checks if the board is empty (no pieces placed).
        """
        for level in self.board:
            for row in level:
                for cell in row:
                    if cell is not None:
                        return False
        return True