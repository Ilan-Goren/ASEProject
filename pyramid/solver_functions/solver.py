import time

from . import algorithm_x_functions, piece, pyramid_board

class Solver:
    """
    Solver class for packing polyomino pieces onto a pyramid board using Algorithm X.
    """
    cell_to_index = {}
    index_to_cell = {}
    id_conversions = {}
    matrix = None

    def generate_board_cell_indexes(self, board):
        """
        Generates a mapping between board cell coordinates and column indexes in the matrix.

        :param board: The pyramid board object.
        :type board: pyramid_board
        """
        for i, cell in enumerate(board.cells, start=1):
            self.cell_to_index[cell] = i
            self.index_to_cell[i] = cell

    def initialise_packing_matrix(self, board, pieces):
        """
        Initializes the exact cover matrix for the packing problem.

        :param board: The pyramid board object.
        :type board: pyramid_board
        :param pieces: A list of pieces to pack onto the board.
        :type pieces: list[Piece]
        :return: The initialized matrix for the packing problem.
        :rtype: algorithm_x_functions.Matrix
        """
        self.cell_to_index = {}
        self.index_to_cell = {}
        self.id_conversions = {}

        self.generate_board_cell_indexes(board)

        board_size = board.count_cells()

        # Construct a blank matrix with the required number of columns
        self.matrix = algorithm_x_functions.Matrix(board_size + len(pieces), 0)

        # Enumerate pieces from 1 to n
        for i, p in enumerate(pieces):
            # Keep track of original id's compared to enumerated ones
            self.id_conversions[i+1] = p.id
            p.id = i + 1

        for p in pieces:
            for t in p.transformations:
                for option in board.get_matching_empty_regions(t):
                    row = []
                    for cell in option:
                        row.append(self.cell_to_index[cell])
                    row.sort()
                    row.append(p.id + board_size)
                    algorithm_x_functions.add_row(self.matrix, row)

        return self.matrix

    def initialise_packing_matrix_partial_config(self, board, remaining_pieces):
        """
        Initializes the exact cover matrix for a partially filled board configuration.

        :param board: The pyramid board, assumed to have some pieces placed.
        :type board: pyramid_board
        :param remaining_pieces: A list of pieces yet to be placed on the board.
        :type remaining_pieces: list[Piece]
        :return: The initialized matrix for the packing problem.
        :rtype: algorithm_x_functions.Matrix
        """
        self.cell_to_index = {}
        self.index_to_cell = {}
        self.id_conversions = {}

        self.generate_board_cell_indexes(board)

        board_size = board.count_cells()

        placed_pieces = {}
        for cell in board.cells.keys():
            piece_id = board.cells[cell]
            if piece_id != 0:
                if piece_id not in placed_pieces:
                    placed_pieces[piece_id] = []
                placed_pieces[piece_id].append(cell)

        placed_pieces_count = len(placed_pieces)

        # Construct a blank matrix with the required number of columns
        self.matrix = algorithm_x_functions.Matrix(board_size + len(remaining_pieces) + placed_pieces_count, 0)

        next_id = 1
        # Enumerate pieces from 1 to n
        for i, p in enumerate(remaining_pieces):
            for placed_id in placed_pieces.keys():
                if placed_id == p.id:
                    raise Exception("Placed pieces cannot have same ID as remaining pieces")
            # Keep track of original id's compared to enumerated ones
            self.id_conversions[i + 1] = p.id
            p.id = i + 1
            next_id = p.id + 1

        placed_pieces_renum = {}
        for p_id in placed_pieces.keys():
            self.id_conversions[next_id] = p_id
            placed_pieces_renum[next_id] = placed_pieces[p_id]
            next_id += 1

        for p in remaining_pieces:
            for t in p.transformations:
                for option in board.get_matching_empty_regions(t):
                    row = []
                    for cell in option:
                        row.append(self.cell_to_index[cell])
                    row.sort()
                    row.append(p.id + board_size)
                    algorithm_x_functions.add_row(self.matrix, row)

        for id, cells in placed_pieces_renum.items():
            row = []
            for cell in cells:
                row.append(self.cell_to_index[cell])
            row.sort()
            row.append(id + board_size)
            algorithm_x_functions.add_row(self.matrix, row)

        return self.matrix


    def solve(self, pieces, board=None):
        """
        Solves the packing problem for the given board and pieces.

        :param pieces: A list of pieces to place onto the board.
        :type pieces: list[Piece]
        :param board: The pyramid board object. If None, a default board is used.
        :type board: pyramid_board, optional
        :return: A list of rows of a solution matrix, or False if no solution exists.
        :rtype: list[list[int]] | bool
        """
        if board is None:
            board = pyramid_board.pyramid_board(5)

        pieces_placed = False

        for p_id in board.cells.values():
            if p_id != 0:
                pieces_placed = True
                break

        if pieces_placed:
            self.initialise_packing_matrix_partial_config(board, pieces)
        else:
            self.initialise_packing_matrix(board, pieces)

        # Track how long the solver takes
        start = time.time()
        # Get the first solution for the packing problem
        rows = algorithm_x_functions.solve(self.matrix, [], True)
        elapsed = time.time() - start

        # If no solution found
        if not rows:
            return False

        return rows

    def rows_to_array_sol(self, rows, board):
        """
        Converts a solution in matrix row format into a 3D array representation.

        :param rows: A list of rows representing the solution.
        :type rows: list[list[int]]
        :param board: The pyramid board object.
        :type board: pyramid_board
        :return: A 3D array representing the solution on the board.
        :rtype: list[list[list[int]]]
        """
        # build empty array to populate
        solution_array = [
            [[0 for x in range(z + 1)] for y in range(z + 1)]
            for z in range(board.layers - 1, -1, -1)
        ]

        board_cells_count = board.count_cells()

        # For each row in provided matrix solution
        for i, row in enumerate(rows):

            # Find id of polyomino from row
            poly_id = -1
            for j in range(len(row) - 1, -1, -1):
                if row[j]:
                    poly_id = j - board_cells_count + 1
                    break

            # Place piece on the solution array
            # Get where the piece has been placed on the board
            for j in range(len(row)):
                if row[j] and j+1 != (poly_id + board_cells_count):
                    x,y,z = self.index_to_cell[j+1]
                    solution_array[z][int((y-z)/2)][int((x-z)/2)] = self.id_conversions[poly_id]

        return solution_array

    def generate_solutions(self, pieces, board=None):
        """
        Generates all possible solutions for the given board and pieces.

        :param pieces: A list of pieces to place onto the board.
        :type pieces: list[Piece]
        :param board: The pyramid board object. If None, a default board is used.
        :type board: pyramid_board, optional
        :yield: Rows representing individual solution matrices.
        :rtype: generator[list[list[int]]]
        """
        if board is None:
            board = pyramid_board.pyramid_board(5)

        pieces_placed = False

        for p_id in board.cells.values():
            if p_id != 0:
                pieces_placed = True

        if pieces_placed:
            self.initialise_packing_matrix_partial_config(board, pieces)
        else:
            self.initialise_packing_matrix(board, pieces)

        yield from algorithm_x_functions.generate_solutions(self.matrix)














        





