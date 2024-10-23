# Hard-coded polyominoes for bitwise comparison as a list of dictionaries
'''
1:          2:          3:          4:          5:          6:
                         X
XXX           XX        XX           X           X           XX
X X         XXX          XX         XXX         XXXX        XXX

7:          8:          9:          10:         11:         12:
            XX          XXX                                 XX
 XX         X             X         X           X            XX
XX          X             X         XXXX        XX            X

'''
POLYOMINOES   = [
    {'poly_id': 1, 'tiles': [[1, 1, 1], [1, 0, 1]]},
    {'poly_id': 2, 'tiles': [[0, 0, 1, 1], [1, 1, 1, 0]]},
    {'poly_id': 3, 'tiles': [[0, 1, 0], [1, 1, 0], [0, 1, 1]]},
    {'poly_id': 4, 'tiles': [[0, 1, 0], [1, 1, 1]]},
    {'poly_id': 5, 'tiles': [[0, 1, 0, 0], [1, 1, 1, 1]]},
    {'poly_id': 6, 'tiles': [[0, 1, 1], [1, 1, 1]]},
    {'poly_id': 7, 'tiles': [[0, 1, 1], [1, 1, 0]]},
    {'poly_id': 8, 'tiles': [[1, 1], [1, 0], [1, 0]]},
    {'poly_id': 9, 'tiles': [[1, 1, 1], [0, 0, 1], [0,0,1]]},
    {'poly_id': 10, 'tiles': [[1, 0, 0, 0], [1, 1, 1, 1]]},
    {'poly_id': 11, 'tiles': [[1, 0], [1, 1]]},
    {'poly_id': 12, 'tiles': [[1, 1, 0], [0, 1, 1], [0, 0, 1]]}
]

class Polyomino:
    def __init__(self, tiles, poly_id):
        self.tiles = tiles  # A 2D list of booleans representing the polyomino shape
        self.poly_id = poly_id  # ID for the polyomino

def print_polyomino(p):
    for row in p.tiles:
        for cell in row:
            if cell:
                print("X", end="")
            else:
                print(" ", end="")
        print("")  # Move to the next line after each row