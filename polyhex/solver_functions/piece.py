import matplotlib.pyplot as plt
from numpy.ma.core import transpose

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
    def __init__(self, piece_id, custom_shape=None):
        self.id = piece_id
        if custom_shape is None:
            self.transformations = build_transformations(pieces.get(piece_id))
        else:
            self.transformations = build_transformations(custom_shape)

'''
def build_transformations(cells):

    transformations = []
    y = 0
    for i in range(2):
        for x in range(6):
            cells = sorted(normalize_transformation([rotate_xy(c) for c in cells]))
            transformations.append(cells)
            leaning_cells = sorted(normalize_transformation([lean(c) for c in cells]))
            transformations.append(leaning_cells)
            leaning_cells_transposed_1 = sorted(normalize_transformation([transpose_lean_1(c) for c in leaning_cells]))
            transformations.append(leaning_cells_transposed_1)
            leaning_cells_transposed_2 = sorted(normalize_transformation([transpose_lean_2(c) for c in leaning_cells]))
            transformations.append(leaning_cells_transposed_2)
        cells = sorted(normalize_transformation([reflect(c) for c in cells]))

    # remove duplicates (if any) and return unique transformations
    unique_symmetries = [list(x) for x in set(tuple(s) for s in transformations)]
    return unique_symmetries
'''

def build_transformations(cells):
    transformations = []
    for x in range(6):
        cells = sorted(normalize_transformation([rotate_xy(c) for c in cells]))
        transformations.append(cells)
        print("base:")
        print(cells)
        leaning_cells = sorted(normalize_transformation([lean(c) for c in cells]))
        transformations.append(leaning_cells)
        print("lean:")
        print(leaning_cells)
        leaning_cells_trans_1 = sorted(normalize_transformation([transpose_lean_1(c) for c in leaning_cells]))
        transformations.append(leaning_cells_trans_1)
        print("trans1:")
        print(leaning_cells_trans_1)
        leaning_cells_trans_2 = sorted(normalize_transformation([transpose_lean_2(c) for c in leaning_cells]))
        transformations.append(leaning_cells_trans_2)
        print("trans2:")
        print(leaning_cells_trans_2)

        flipped_cells = sorted(normalize_transformation([reflect(c) for c in cells]))
        transformations.append(flipped_cells)
        print("fbase:")
        print(flipped_cells)
        flipped_leaning_cells = sorted(normalize_transformation([lean(c) for c in flipped_cells]))
        transformations.append(flipped_leaning_cells)
        print("flean:")
        print(flipped_leaning_cells)
        flipped_leaning_cells_trans_1 = sorted(normalize_transformation([transpose_lean_1(c) for c in flipped_leaning_cells]))
        transformations.append(flipped_leaning_cells_trans_1)
        print("ftrans1:")
        print(flipped_leaning_cells_trans_1)
        flipped_leaning_cells_trans_2 = sorted(normalize_transformation([transpose_lean_2(c) for c in flipped_leaning_cells]))
        transformations.append(flipped_leaning_cells_trans_2)
        print("ftrans2:")
        print(flipped_leaning_cells_trans_2)
    # remove duplicates (if any) and return unique transformations
    unique_symmetries = [list(x) for x in set(tuple(s) for s in transformations)]
    return unique_symmetries

'''
def build_transformations_fixed()
    (dont rotate reflections), build all base orientations
    reflect all orientations
    for all orinetations
        apply lean
            apply transpose
            apply other transpose
'''

def rotate_xy(cell):
    vec = list(cell)
    vec[0], vec[1] = -vec[1], vec[0] + vec[1]
    return tuple(vec)

def reflect(cell):
    vec = list(cell)
    vec[0] = -vec[0]
    vec[0] = vec[0] - vec[1]
    return tuple(vec)

def lean(cell):
    vec = list(cell)
    vec[1], vec[2] = 0, vec[1]
    return tuple(vec)

def transpose_lean_1(cell):
    vec = list(cell)
    vec[0], vec[1] = 5 - (vec[0] + vec[1] + vec[2]), vec[0]
    return tuple(vec)

def transpose_lean_2(cell):
    vec = list(cell)
    vec[0], vec[1] = vec[1], 5 - (vec[0] + vec[1] + vec[2])
    return tuple(vec)

def normalize_transformation(cells):
    # Find minimum values in each dimension
    min_x = min(cell[0] for cell in cells)
    min_y = min(cell[1] for cell in cells)
    min_z = min(cell[2] for cell in cells)

    # Shift each coordinate by the minimum values
    normalized_cells = [(cell[0] - min_x, cell[1] - min_y, cell[2] - min_z) for cell in cells]
    return normalized_cells

def visualise_piece(coords):
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