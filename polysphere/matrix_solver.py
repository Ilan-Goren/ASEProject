import sys
import time
from . import algorithm_x_functions, matrix_transformations, matrix_polyominoes

class MatrixSolver:

    def packing_matrix(self, polys, w, h, id_conversions=None):
        """Construct the exact cover matrix for the packing problem."""
        if id_conversions is None:
            id_conversions = []

        matrix = algorithm_x_functions.Matrix(w * h + len(polys), 0)

        # Enumerate polyominoes from 1 to n
        for i, poly in enumerate(polys):
            id_conversions.append([poly.poly_id, i + 1])
            poly.poly_id = i + 1

        # Find all unique rotations and reflections of polyominoes
        options = []
        for poly in polys:
            matrix_transformations.unique_rotations(options, poly)

        # Populate the matrix
        for p in options:
            for p_col in range(w - len(p.tiles[0]) + 1):
                for p_row in range(h - len(p.tiles) + 1):
                    row = []

                    # Cover tile (j+p_col, i+p_row)
                    for i in range(len(p.tiles)):
                        for j in range(len(p.tiles[0])):
                            if p.tiles[i][j]:
                                row.append((j + p_col) + (i + p_row) * w + 1)

                    row.append(w * h + p.poly_id)  # id-th polyomino used
                    algorithm_x_functions.add_row(matrix, row)

        return matrix


    def print_packing(self, rows, w, h):
        """Print the packing solution."""
        output = [[0] * w for _ in range(h)]

        for i, row in enumerate(rows):
            # Find id of polyomino
            poly_id = -1
            for j in range(len(row) - 1, -1, -1):
                if row[j]:
                    poly_id = j - w * h
                    break

            for j in range(len(row)):
                if row[j] and j != poly_id + w * h:
                    # Reverse (x, y) -> x + y * w
                    output[j // w][j % w] = poly_id+1

        for row in output:
            print(" ".join([str(c) if c != 0 else ' ' for c in row]))

        return output


    def solve_packing(self, polys, w, h, b=None, id_conversions=None):
        """Solve the packing problem and display the search time."""
        if id_conversions is None:
            id_conversions = []

        if b is None:
            matrix = self.packing_matrix(polys, w, h, id_conversions)
        else:
            matrix = self.packing_matrix_partial_config(polys, w, h, b, id_conversions)

        start = time.time()
        rows = algorithm_x_functions.find_rows(matrix)
        elapsed = time.time() - start

        solution  = self.print_packing(rows, w, h)
        print(f"Time: {elapsed:.4f} seconds")
        return solution



    def count_packing(self, polys, w, h, b=None, id_conversions=None):
        """Count the number of solutions to the packing problem and display the search time."""
        if id_conversions is None:
            id_conversions = []

        if b is None:
            matrix = self.packing_matrix(polys, w, h, id_conversions)
        else:
            matrix = self.packing_matrix_partial_config(polys, w, h, b, id_conversions)

        start = time.time()
        solution_rows = algorithm_x_functions.find_all(matrix)
        elapsed = time.time() - start

        solutions = []
        for sr in solution_rows:
            solutions.append(self.print_packing(sr, w, h))

        print(f"Solutions: {len(solution_rows)}")
        print(f"Time: {elapsed:.4f} seconds")
        return solutions

    def generate_packing_solutions(self, polys, w, h, b=None, id_conversions=None):
        """Solve the packing problem and display the search time."""
        if id_conversions is None:
            id_conversions = []

        if b is None:
            matrix = self.packing_matrix(polys, w, h, id_conversions)
        else:
            matrix = self.packing_matrix_partial_config(polys, w, h, b, id_conversions)

        yield from algorithm_x_functions.generate_solutions(matrix)




    def packing_matrix_partial_config(self, polys, w, h, initial_board=None, id_conversions=None):

        if id_conversions is None:
            id_conversions = []

        # find the unique id's of pieces placed on the board
        placed_piece_ids = list(set(i for j in initial_board for i in j if i != 0))

        """Construct the exact cover matrix for the packing problem."""
        matrix = algorithm_x_functions.Matrix(w * h + (len(polys) + len(placed_piece_ids)), 0)

        # Enumerate polyominoes from 1 to n
        nextID = 1 #used for enumerating
        for i, poly in enumerate(polys):
            id_conversions.append([poly.poly_id, i + 1])
            poly.poly_id = i + 1
            nextID += 1

        # Find all unique rotations and reflections of polyominoes
        options = []
        for poly in polys:
            matrix_transformations.unique_rotations(options, poly)

        #build fixed versions of those pieces by making them the size of the board
        placed_pieces_fixed = []
        for id in placed_piece_ids:
            fixed_tiles = [[0 for _ in range(w)] for _ in range(h)]
            for i in range(len(initial_board)):
                for j in range(len(initial_board[0])):
                    if initial_board[i][j] == id:
                        fixed_tiles[i][j] = nextID
                    else:
                        fixed_tiles[i][j] = 0
            fixed_piece = matrix_polyominoes.Polyomino(fixed_tiles, nextID)
            placed_pieces_fixed.append(fixed_piece)
            id_conversions.append([id, nextID])
            nextID += 1

        options.extend(placed_pieces_fixed)

        # Populate the matrix
        for p in options:
            for p_col in range(w - len(p.tiles[0]) + 1):
                for p_row in range(h - len(p.tiles) + 1):
                    row = []

                    # Cover tile (j+p_col, i+p_row)
                    for i in range(len(p.tiles)):
                        for j in range(len(p.tiles[0])):
                            if p.tiles[i][j]:
                                row.append((j + p_col) + (i + p_row) * w + 1)

                    row.append(w * h + p.poly_id)  # id-th polyomino used
                    algorithm_x_functions.add_row(matrix, row)

        return matrix

    def revert_ids(self, id_conversions, solution):
        for i in range(len(solution)):
            for j in range(len(solution[0])):
                for c in id_conversions:
                    if solution[i][j] == c[1]:
                        solution[i][j] = c[0]
                        break
        return solution