from . import piece

class Board:
    """
    Represents a 3D board with layers and cells for placing polyhex pieces.
    """
    def __init__(self, board=None):
        """
        Initializes the Board object. If no board is provided, creates a default 6-layer board.

        Args:
            board (list[list[list[int]]], optional): A nested list representing the initial state of the board, or None for a default board.
        """
        if board is None:
            self.board = [
                [[0] * (6 - i) for i in range(6)],
                [[0] * (5 - i) for i in range(5)],
                [[0] * (4 - i) for i in range(4)],
                [[0] * (3 - i) for i in range(3)],
                [[0] * (2 - i) for i in range(2)],
                [[0] * (1 - i) for i in range(1)]
            ]
        else:
            self.board = board

    def count_cells(self):
        """
        Counts the total number of cells in the board.

        Returns:
            int: The total number of cells.
        """
        return sum(len(row) for layer in self.board for row in layer)

    def is_region_free(self, region):
        """
        Checks if a given region of cells is free on the board.

        Args:
            region (list[tuple[int, int, int]]): A list of tuples representing cell coordinates (x, y, z).

        Returns:
            bool: True if the region is free, False otherwise.
        """
        for cell in region:
            if cell[2] > len(self.board) - 1:
                return False
            if cell[1] > len(self.board[cell[2]]) - 1:
                return False
            if cell[0] > len(self.board[cell[2]][cell[1]]) - 1:
                return False
            if self.board[cell[2]][cell[1]][cell[0]] != 0:
                return False
        return True

    def get_matching_empty_regions(self, region):
        """
        Finds all regions on the board that match the given region and are free.

        Args:
            region (list[tuple[int, int, int]]): A list of tuples representing cell coordinates (x, y, z).

        Returns:
            list[list[tuple[int, int, int]]]: A list of matching empty regions.
        """
        matching_empty_regions = []
        for z in range(len(self.board)):
            for y in range(len(self.board[z])):
                for x in range(len(self.board[z][y])):
                    translated_region = []
                    for i,j,k in region:
                        translated_region.append((i+x, j+y, k+z))
                    if self.is_region_free(translated_region):
                        matching_empty_regions.append(translated_region)
        return matching_empty_regions

    def get_piece_locations(self):
        """
        Retrieves the locations of all placed pieces on the board.

        Returns:
            dict[int, list[tuple[int, int, int]]]: A dictionary where keys are piece IDs and values are lists of their cell coordinates.
        """
        placed_pieces = {}

        for z in range(len(self.board)):
            for y in range(len(self.board[z])):
                for x in range(len(self.board[z][y])):
                    cell_val = self.board[z][y][x]
                    if cell_val != 0:
                        if cell_val not in placed_pieces:
                            placed_pieces[cell_val] = []
                        placed_pieces[cell_val].append((x,y,z))

        return placed_pieces

    def verify_board(self):
        """
        Verifies the validity of the board by checking the placement of all pieces.

        Returns:
            bool: True if the board is valid, False otherwise.
        """
        piece_locations = self.get_piece_locations()
        valid = True
        for id in piece_locations:
            cells = piece_locations[id]
            p = piece.Piece(id)
            if not piece.verify_placement(p, cells):
                valid = False
        return valid
