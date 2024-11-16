import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#hard-coded pieces for 3D board
'''
1:          2:          3:          4:          5:          6:
                         X
X X          XXX         XX          X           X          XX
XXX         XX          XX          XXX         XXXX        XXX

7:          8:          9:          10:         11:         12:
 X                      X                                     X
XX          X           X           X           X            XX
X           XXX         XXX         XXXX        XX          XX

'''
pieces  = { 1: [(0, 0, 0), (0, 2, 0), (0, 4, 0), (2, 0, 0), (2, 4, 0)],
            2: [(0, 0, 0), (0, 2, 0), (2, 2, 0), (2, 4, 0), (2, 6, 0)],
            3: [(0, 0, 0), (0, 2, 0), (2, 2, 0), (2, 4, 0), (4, 2, 0)],
            4: [(0, 0, 0), (0, 2, 0), (0, 4, 0), (2, 2, 0)],
            5: [(0, 0, 0), (0, 2, 0), (0, 4, 0), (0, 6, 0), (2, 2, 0)],
            6: [(0, 0, 0), (0, 2, 0), (0, 4, 0), (2, 0, 0), (2, 2, 0)],
            7: [(0, 0, 0), (2, 0, 0), (2, 2, 0), (4, 2, 0)],
            8: [(0, 0, 0), (0, 2, 0), (0, 4, 0), (2, 0, 0)],
            9: [(0, 0, 0), (0, 2, 0), (0, 4, 0), (2, 0, 0), (4, 0, 0)],
            10: [(0, 0, 0), (0, 2, 0), (0, 4, 0), (0, 6, 0), (2, 0, 0)],
            11: [(0, 0, 0), (0, 2, 0), (2, 0, 0)],
            12: [(0, 0, 0), (0, 2, 0), (2, 2, 0), (2, 4, 0), (4, 4, 0)]}


class Piece:
    def __init__(self, piece_id, custom_shape=None):
        self.id = piece_id
        if custom_shape is None:
            self.transformations = build_transformations(pieces.get(piece_id))
        else:
            self.transformations = build_transformations(custom_shape)



def build_transformations(cells):
    transformations = []
    initial = [cells]
    initial += rotate_z(normalize_transformation(cells))

    for next_cells in initial:
        next_cells = sorted(normalize_transformation(next_cells))

        while next_cells not in transformations:
            while next_cells not in transformations:
                transformations.append(next_cells)
                #apply rotatexy, normalize, and sort
                next_cells = sorted(normalize_transformation([(rotate_xy(cell)) for cell in next_cells]))

            #apply reflection, normalize, and sort
            next_cells = sorted(normalize_transformation([reflect(cell) for cell in next_cells]))

    #remove duplicates (if any) and return unique transformations
    unique_symmetries = [list(x) for x in set(tuple(s) for s in transformations)]
    return unique_symmetries


def rotate_z(cells):
    transformations = [[(int((c[0] - c[1]) / 2), int((c[0] - c[1]) / 2), int((c[0] + c[1]) / 2)) for c in cells],
                       [(int((c[0] - c[1]) / 2), int((c[0] - c[1]) / 2), int((-c[0] - c[1]) / 2)) for c in cells],
                       [(int((c[0] + c[1]) / 2), int((c[0] + c[1]) / 2), int((-c[0] + c[1]) / 2)) for c in cells],
                       [(int((c[0] + c[1]) / 2), int((c[0] + c[1]) / 2), int((c[0] - c[1]) / 2)) for c in cells]]
    return transformations

def rotate_xy(cell):
    vec = list(cell)
    vec[0], vec[1] = vec[1], -vec[0]
    return tuple(vec)

def reflect(cell):
    vec = list(cell)
    vec[0] = -vec[0]
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

    # Set labels for clarity
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Set the title
    ax.set_title("3D Coordinates Visualization")

    # Show the plot
    plt.show()