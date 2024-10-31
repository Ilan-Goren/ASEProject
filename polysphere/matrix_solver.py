import time
from . import algorithm_x_functions, matrix_transformations, matrix_polyominoes

class MatrixSolver:

    def packing_matrix(self, polys, w, h, id_conversions=None):
        """Construct the exact cover matrix for the packing problem."""
        # For storing piece id conversions
        if id_conversions is None:
            id_conversions = []

        # Construct a blank matrix with the required number of columns
        matrix = algorithm_x_functions.Matrix(w * h + len(polys), 0)

        # Enumerate polyominoes from 1 to n
        for i, poly in enumerate(polys):
            # Keep track of original id's compared to enumerated ones
            id_conversions.append([poly.poly_id, i + 1])
            poly.poly_id = i + 1

        # Find all unique transformations (rotations/reflections) of all polyominoes, store them in options
        options = []
        for poly in polys:
            matrix_transformations.unique_rotations(options, poly)

        # Populate the matrix
        # Loop through each possible transformation of each polyomino
        for p in options:
            # Loop through each cell of the board that the polyomino can fit
            for p_col in range(w - len(p.tiles[0]) + 1):
                for p_row in range(h - len(p.tiles) + 1):
                    # Stores the indices required for a row of the matrix based on the current piece placement
                    row = []

                    # Cover tile (j+p_col, i+p_row)
                    # Loop through each cell of the transformed polyomino
                    for i in range(len(p.tiles)):
                        for j in range(len(p.tiles[0])):
                            # If the cell is part of the piece
                            if p.tiles[i][j]:
                                # Add the position of the cell within the row
                                row.append((j + p_col) + (i + p_row) * w + 1)
                    # Add an element to the row for the id of the piece used
                    row.append(w * h + p.poly_id)
                    # Add the row to the matrix
                    algorithm_x_functions.add_row(matrix, row)

        return matrix


    def print_packing(self, rows, w, h):
        """Return a list representation of a packing solution with enumerated piece ID's and print it for debugging."""
        # Initialise a 2D array of 0's the size of the board
        output = [[0] * w for _ in range(h)]

        # For each row in provided matrix solution
        for i, row in enumerate(rows):
            # Find id of polyomino from row
            poly_id = -1
            for j in range(len(row) - 1, -1, -1):
                if row[j]:
                    poly_id = j - w * h
                    break

            # Get where the piece has been placed on the board
            for j in range(len(row)):
                if row[j] and j != poly_id + w * h:
                    # Reverse (x, y) -> x + y * w
                    output[j // w][j % w] = poly_id+1

        # print out output for debugging
        for row in output:
            print(" ".join([str(c) if c != 0 else ' ' for c in row]))

        return output


    def solve_packing(self, polys, w, h, b=None, id_conversions=None):
        """Solve the packing problem (get first solution) and display the search time."""
        # For storing piece id conversions
        if id_conversions is None:
            id_conversions = []

        # Initialise matrix
        # If no board is provided then assume it is empty
        if b is None:
            matrix = self.packing_matrix(polys, w, h, id_conversions)
        # Else initialise the matrix with the partial configuration
        else:
            matrix = self.packing_matrix_partial_config(polys, w, h, b, id_conversions)

        # Track how long the solver takes
        start = time.time()
        # Get the first solution for the packing problem
        rows = algorithm_x_functions.find_rows(matrix)
        elapsed = time.time() - start

        # If no solution found
        if not rows:
            return False

        # Return solution
        solution  = self.print_packing(rows, w, h)
        print(f"Time: {elapsed:.4f} seconds")
        return solution


    def count_packing(self, polys, w, h, b=None, id_conversions=None):
        """Returns all solutions to the packing problem"""
        # For storing piece id conversions
        if id_conversions is None:
            id_conversions = []

        # Initialise matrix
        # If no board is provided then assume it is empty
        if b is None:
            matrix = self.packing_matrix(polys, w, h, id_conversions)
        # Else initialise the matrix with the partial configuration
        else:
            matrix = self.packing_matrix_partial_config(polys, w, h, b, id_conversions)

        # Track how long the solver takes
        start = time.time()
        # Get all solutions for the packing problem
        solution_rows = algorithm_x_functions.find_all(matrix)
        elapsed = time.time() - start

        # Get list representation of each solution
        solutions = []
        for sr in solution_rows:
            solutions.append(self.print_packing(sr, w, h))

        # Return all solutions
        print(f"Solutions: {len(solution_rows)}")
        print(f"Time: {elapsed:.4f} seconds")
        return solutions

    def generate_packing_solutions(self, polys, w, h, b=None, id_conversions=None):
        """ Generator function variation of count_packing
            yields all solutions to the packing problem"""
        # For storing piece id conversions
        if id_conversions is None:
            id_conversions = []

        # Initialise matrix
        # If no board is provided then assume it is empty
        if b is None:
            matrix = self.packing_matrix(polys, w, h, id_conversions)
        # Else initialise the matrix with the partial configuration
        else:
            matrix = self.packing_matrix_partial_config(polys, w, h, b, id_conversions)

        # yeild results from solver generator using the initialised matrix
        yield from algorithm_x_functions.generate_solutions(matrix)


    def packing_matrix_partial_config(self, polys, w, h, initial_board=None, id_conversions=None):
        """Construct the exact cover matrix for the packing problem, given a partially configured board"""
        # For storing piece id conversions
        if id_conversions is None:
            id_conversions = []

        # Find the unique id's of pieces already placed on the board
        placed_piece_ids = list(set(i for j in initial_board for i in j if i != 0))

        # Construct a blank matrix with the required number of columns
        matrix = algorithm_x_functions.Matrix(w * h + (len(polys) + len(placed_piece_ids)), 0)

        # Enumerate polyominoes from 1 to n
        # next ID is used to track what ID's to give for already placed pieces
        nextID = 1
        for i, poly in enumerate(polys):
            id_conversions.append([poly.poly_id, i + 1])
            poly.poly_id = i + 1
            nextID += 1

        # Find all unique transformations (rotations/reflections) of all polyominoes, store them in options
        options = []
        for poly in polys:
            matrix_transformations.unique_rotations(options, poly)

        # Build fixed versions of each placed piece by making them the size of the board
        placed_pieces_fixed = []
        # Loop through each placed piece
        for id in placed_piece_ids:
            # Create a new list the size of the board for the fixed placement
            fixed_tiles = [[0 for _ in range(w)] for _ in range(h)]
            for i in range(len(initial_board)):
                for j in range(len(initial_board[0])):
                    # Add piece placement to new fixed piece
                    if initial_board[i][j] == id:
                        fixed_tiles[i][j] = nextID
                    else:
                        fixed_tiles[i][j] = 0
            # Store new fixed piece as a polyomino object and track its ID conversion
            fixed_piece = matrix_polyominoes.Polyomino(fixed_tiles, nextID)
            placed_pieces_fixed.append(fixed_piece)
            id_conversions.append([id, nextID])
            nextID += 1
        # Add fixed pieces to array of piece placement options
        options.extend(placed_pieces_fixed)

        # Populate the matrix
        # Loop through each possible transformation of each polyomino
        for p in options:
            # Loop through each cell of the board that the polyomino can fit
            for p_col in range(w - len(p.tiles[0]) + 1):
                for p_row in range(h - len(p.tiles) + 1):
                    # Stores the indices required for a row of the matrix based on the current piece placement
                    row = []

                    # Cover tile (j+p_col, i+p_row)
                    # Loop through each cell of the transformed polyomino
                    for i in range(len(p.tiles)):
                        for j in range(len(p.tiles[0])):
                            # If the cell is part of the piece
                            if p.tiles[i][j]:
                                # Add the position of the cell within the row
                                row.append((j + p_col) + (i + p_row) * w + 1)
                    # Add an element to the row for the id of the piece used
                    row.append(w * h + p.poly_id)
                    # Add the row to the matrix
                    algorithm_x_functions.add_row(matrix, row)

        return matrix

    def revert_ids(self, id_conversions, solution):
        """Revert the ID's of the pieces placed on a solution list, to their original value, from their enumerated ID's"""
        for i in range(len(solution)):
            for j in range(len(solution[0])):
                for c in id_conversions:
                    if solution[i][j] == c[1]:
                        solution[i][j] = c[0]
                        break
        return solution