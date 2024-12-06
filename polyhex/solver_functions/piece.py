import matplotlib.pyplot as plt

#hard-coded pieces for 3D board
'''
1:          2:          3:          4:          5:          6:
    X                         X
   X X         X X           X            X      X X           X
X X         X X X       X X X        X X X X    X X X       X X X X


7:          8:          9:          10:         11:         12:
              X
 X   X       X               X         X X       X X           X
X X X       X X X       X X X       X X         X X         X X X

'''
pieces  = { 1: [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 2, 0), (2, 1, 0)],
            2: [(0, 0, 0), (1, 0, 0), (1, 1, 0), (2, 0, 0), (2, 1, 0)],
            3: [(0, 0, 0), (1, 0, 0), (2, 0, 0), (2, 1, 0), (2, 2, 0)],
            4: [(0, 0, 0), (1, 0, 0), (2, 0, 0), (2, 1, 0), (3, 0, 0)],
            5: [(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 0), (2, 0, 0)],
            6: [(0, 0, 0), (1, 0, 0), (1, 1, 0), (2, 0, 0), (3, 0, 0)],
            7: [(0, 0, 0), (0, 1, 0), (1, 0, 0), (2, 0, 0), (2, 1, 0)],
            8: [(0, 0, 0), (0, 1, 0), (0, 2, 0), (1, 0, 0), (2, 0, 0)],
            9: [(0, 0, 0), (1, 0, 0), (2, 0, 0), (2, 1, 0)],
            10: [(0, 0, 0), (1, 0, 0), (1, 1, 0), (2, 1, 0)],
            11: [(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 0)],
            12: [(0, 0, 0), (1, 0, 0), (1, 1, 0), (2, 0, 0)]}

class Piece:
    """
    Represents a polyhex piece with all possible transformations.
    """
    def __init__(self, piece_id, custom_shape=None):
        """
        Initializes a Piece object with type, coordinates, and optionally transformations.

        Args:
            piece_type (str): The type or identifier of the piece.
            coordinates (list of tuple[int, int, int]): A list of coordinates representing the piece's shape.
            transformations (list of list[tuple[int, int, int]], optional): A list of transformations for the piece.
        """
        self.id = piece_id
        if custom_shape is None:
            self.transformations = build_transformations(pieces.get(piece_id))
        else:
            self.transformations = build_transformations(custom_shape)

def build_transformations(cells):
    """
    Generates all unique transformations (rotations, reflections, leans, transpositions) of a piece.

    Args:
        cells (list of tuple[int, int, int]): The initial list of cell coordinates for the piece.

    Returns:
        list of list[tuple[int, int, int]]: A list of unique transformations.
    """
    transformations = []
    for x in range(6):
        cells = sorted(normalize_transformation([rotate_xy(c) for c in cells]))
        transformations.append(cells)
        leaning_cells = sorted(normalize_transformation([lean(c) for c in cells]))
        transformations.append(leaning_cells)
        leaning_cells_trans_1 = sorted(normalize_transformation([transpose_lean_1(c) for c in leaning_cells]))
        transformations.append(leaning_cells_trans_1)
        leaning_cells_trans_2 = sorted(normalize_transformation([transpose_lean_2(c) for c in leaning_cells]))
        transformations.append(leaning_cells_trans_2)

        flipped_cells = sorted(normalize_transformation([reflect(c) for c in cells]))
        transformations.append(flipped_cells)
        flipped_leaning_cells = sorted(normalize_transformation([lean(c) for c in flipped_cells]))
        transformations.append(flipped_leaning_cells)
        flipped_leaning_cells_trans_1 = sorted(normalize_transformation([transpose_lean_1(c) for c in flipped_leaning_cells]))
        transformations.append(flipped_leaning_cells_trans_1)
        flipped_leaning_cells_trans_2 = sorted(normalize_transformation([transpose_lean_2(c) for c in flipped_leaning_cells]))
        transformations.append(flipped_leaning_cells_trans_2)
    # remove duplicates (if any) and return unique transformations
    unique_symmetries = [list(x) for x in set(tuple(s) for s in transformations)]
    return unique_symmetries

def rotate_xy(cell):
    """
    Rotates a cell around the xy-plane.

    Args:
        cell (tuple[int, int, int]): The cell coordinates to rotate.

    Returns:
        tuple[int, int, int]: Rotated cell coordinates.
    """
    vec = list(cell)
    vec[0], vec[1] = -vec[1], vec[0] + vec[1]
    return tuple(vec)

def reflect(cell):
    """
    Reflects a cell across the xy-plane.
    Note: Our representation of the board is slanted to align layers on x, y 0, 0 
          instead of the center of the pyramid. To account for this, 'reflecting' a 
          cell also means shifting it in the -x direction by its y value.

    Args:
        cell (tuple[int, int, int]): The cell coordinates to reflect.

    Returns:
        tuple[int, int, int]: Reflected cell coordinates.
    """
    vec = list(cell)
    vec[0] = -vec[0]
    vec[0] = vec[0] - vec[1]
    return tuple(vec)

def lean(cell):
    """
    Transforms a cell to its leaning position.

    Args:
        cell (tuple[int, int, int]): The cell coordinates to transform.

    Returns:
        tuple[int, int, int]: Transformed cell coordinates.
    """
    vec = list(cell)
    vec[1], vec[2] = 0, vec[1]
    return tuple(vec)

def transpose_lean_1(cell):
    """
    Applies the first transposition to a leaned cell.

    Args:
        cell (tuple[int, int, int]): The cell coordinates to transpose.

    Returns:
        tuple[int, int, int]: Transposed cell coordinates.
    """
    vec = list(cell)
    vec[0], vec[1] = 5 - (vec[0] + vec[1] + vec[2]), vec[0]
    return tuple(vec)

def transpose_lean_2(cell):
    """
    Applies the second transposition to a leaned cell (not to be used on an already transposed cell).

    Args:
        cell (tuple[int, int, int]): The cell coordinates to transpose.

    Returns:
        tuple[int, int, int]: Transposed cell coordinates.
    """
    vec = list(cell)
    vec[0], vec[1] = vec[1], 5 - (vec[0] + vec[1] + vec[2])
    return tuple(vec)

def normalize_transformation(cells):
    """
    Normalizes a set of cell coordinates to their minimum values.

    Args:
        cells (list[tuple[int, int, int]]): A list of cell coordinates.

    Returns:
        list[tuple[int, int, int]]: Normalized cell coordinates.
    """
    # Find minimum values in each dimension
    min_x = min(cell[0] for cell in cells)
    min_y = min(cell[1] for cell in cells)
    min_z = min(cell[2] for cell in cells)

    # Shift each coordinate by the minimum values
    normalized_cells = [(cell[0] - min_x, cell[1] - min_y, cell[2] - min_z) for cell in cells]
    return normalized_cells

def visualise_piece(coords):
    """
    Visualizes a polyomino piece in 3D space using pyplot. For debugging and testing purposes.

    Args:
        coords (list[tuple[int, int, int]]): The cell coordinates to visualize.
    """
    if not coords:
        print("No coordinates to plot.")
        return

    # Extract x, y, and z values
    x_vals = [point[0] for point in coords]
    y_vals = [point[1] for point in coords]
    z_vals = [point[2] for point in coords]

    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the points
    ax.scatter(x_vals, y_vals, z_vals, c='b', marker='o')

    # Set fixed limits for x and y axes
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 6)
    ax.set_zlim(0, 6)

    # Set labels for clarity
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Set the title
    ax.set_title("3D Coordinates Visualization")

    # Show the plot
    plt.show()

def verify_placement(piece, coords):
    """
    Verifies whether a given set of coordinates match any transformation of a piece when normalized.

    Args:
        piece (Piece): The Piece object to verify.
        coords (list[tuple[int, int, int]]): The cell coordinates to verify.

    Returns:
        bool: True if the placement is valid, False otherwise.
    """
    coords = sorted(normalize_transformation(coords))
    options = piece.transformations
    valid = False
    for option in options:
        if option == coords:
            valid = True
            break
    return valid