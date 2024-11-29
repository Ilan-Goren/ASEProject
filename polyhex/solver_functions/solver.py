import time

from . import  algorithm_x_functions, piece, board


class Solver:
    cell_to_index = {}
    index_to_cell = {}
    id_conversions = {}
    matrix = None

    def generate_board_cell_indexes(self, hex_board):
        i = 1
        for z in range(len(hex_board)):
            for y in range(len(hex_board[z])):
                for x in range(len(hex_board[z][y])):
                    self.cell_to_index[(x,y,z)] = i
                    self.index_to_cell[i] = (x,y,z)
                    i += 1

    def initialise_packing_matrix(self, hex_board, pieces):
        self.cell_to_index = {}
        self.index_to_cell = {}
        self.id_conversions = {}
        board_size = hex_board.count_cells()

        self.generate_board_cell_indexes(hex_board.board)

        self.matrix = algorithm_x_functions.Matrix(board_size + len(pieces), 0)

        for i, p in enumerate(pieces):
            self.id_conversions[i+1] = p.id
            p.id = i + 1

        for p in pieces:
            for t in p.transformations:
                for option in hex_board.get_matching_empty_regions(t):
                    row = []
                    for cell in option:
                        row.append(self.cell_to_index[cell])
                    row.sort()
                    row.append(p.id + board_size)
                    algorithm_x_functions.add_row(self.matrix, row)

        return self.matrix

    def initialise_packing_matrix_partial_config(self, hex_board, remaining_pieces):
        self.cell_to_index = {}
        self.index_to_cell = {}
        self.id_conversions = {}

        hb = hex_board.board

        self.generate_board_cell_indexes(hb)

        board_size = hex_board.count_cells()

        placed_pieces = {}

        for z in range(len(hb)):
            for y in range(len(hb[z])):
                for x in range(len(hb[z][y])):
                    cell_val = hb[z][y][x]
                    if cell_val != 0:
                        if cell_val not in placed_pieces:
                            placed_pieces[cell_val] = []
                        placed_pieces[cell_val].append((x,y,z))

        placed_pieces_count = len(placed_pieces)

        self.matrix = algorithm_x_functions.Matrix(board_size + len(remaining_pieces) + placed_pieces_count, 0)

        next_id = 1
        for i, p in enumerate(remaining_pieces):
            for placed_id in placed_pieces.keys():
                if placed_id == p.id:
                    raise Exception("Placed pieces cannot have same ID as remaining pieces")
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
                for option in hex_board.get_matching_empty_regions(t):
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

    def solve(self, pieces, hex_board=None):
        if hex_board is None:
            hex_board = board.Board()

        pieces_placed = False

        hb = hex_board.board

        for z in range(len(hb)):
            for y in range(len(hb[z])):
                for x in range(len(hb[z][y])):
                    if hb[z][y][x] != 0:
                        pieces_placed = True
                        break
                if pieces_placed:
                    break
            if pieces_placed:
                break

        if pieces_placed:
            self.initialise_packing_matrix_partial_config(hex_board, pieces)
        else:
            self.initialise_packing_matrix(hex_board, pieces)

        # Track how long the solver takes
        start = time.time()
        # Get the first solution for the packing problem
        rows = algorithm_x_functions.solve(self.matrix, [], True)
        elapsed = time.time() - start

        # If no solution found
        if not rows:
            return False

        return rows

    def rows_to_array_sol(self, rows, hex_board):
        solution_array = [
                [[0] * (6 - i) for i in range(6)],
                [[0] * (5 - i) for i in range(5)],
                [[0] * (4 - i) for i in range(4)],
                [[0] * (3 - i) for i in range(3)],
                [[0] * (2 - i) for i in range(2)],
                [[0] * (1 - i) for i in range(1)]
            ]

        board_cells_count = hex_board.count_cells()

        # For each row in provided matrix solution
        for i, row in enumerate(rows):

            # Find id of polyomino from row
            poly_id = -1
            for j in range(len(row) - 1, -1, -1):
                if row[j]:
                    poly_id = j - board_cells_count + 1
                    break

            for j in range(len(row)):
                if row[j] and j+1 != (poly_id + board_cells_count):
                    x, y, z = self.index_to_cell[j + 1]
                    solution_array[z][y][x] = self.id_conversions[poly_id]

        return solution_array