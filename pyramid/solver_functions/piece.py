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
            2: [(0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 2, 0), (1, 3, 0)],
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


class piece:
    def __init__(self, id):
        self.id = id
        self.transformations = build_transformations(pieces.get(id))

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
    print("original")
    print(cells)
    # Find minimum values in each dimension
    min_x = min(cell[0] for cell in cells)
    min_y = min(cell[1] for cell in cells)
    min_z = min(cell[2] for cell in cells)

    # Print minimum values for debugging
    print(f"Minimum x: {min_x}, Minimum y: {min_y}, Minimum z: {min_z}")

    # Shift each coordinate by the minimum values
    normalized_cells = [(cell[0] - min_x, cell[1] - min_y, cell[2] - min_z) for cell in cells]
    print("normalised")
    print(cells)
    return normalized_cells