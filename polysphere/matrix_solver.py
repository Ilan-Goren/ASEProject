import time
from . import algorithm_x_functions, matrix_transformations

def packing_matrix(polys, w, h):
    """Construct the exact cover matrix for the packing problem."""
    matrix = algorithm_x_functions.Matrix(w * h + len(polys), 0)

    # Enumerate polyominoes from 1 to n
    for i, poly in enumerate(polys):
        poly.id = i + 1

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


def print_packing(rows, w, h):
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
                output[j // w][j % w] = chr(ord('A') + poly_id)

    for row in output:
        print(" ".join([c if c != 0 else ' ' for c in row]))


def solve_packing(polys, w, h):
    """Solve the packing problem and display the search time."""
    matrix = packing_matrix(polys, w, h)

    start = time.time()
    rows = algorithm_x_functions.find_rows(matrix)
    elapsed = time.time() - start

    print_packing(rows, w, h)
    print(f"Time: {elapsed:.4f} seconds")


def count_packing(polys, w, h):
    """Count the number of solutions to the packing problem and display the search time."""
    matrix = packing_matrix(polys, w, h)

    start = time.time()
    solutions = algorithm_x_functions.find_all(matrix)
    elapsed = time.time() - start

    print(f"Solutions: {len(solutions)}")
    print(f"Time: {elapsed:.4f} seconds")