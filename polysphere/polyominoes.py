# Hard-coded polyominoes as a list of dictionaries
'''
A:          B:          C:          D:          E:          F:
                         X
XXX           XX        XX           X           X           XX
X X         XXX          XX         XXX         XXXX        XXX

G:          H:          I:          J:          K:          L:
            XX          XXX                                 XX
 XX         X             X         X           X            XX
XX          X             X         XXXX        XX            X

'''
POLYOMINOES   = [
    {"name": "A", "shape": [(0, 0), (0, 1), (1, 1), (2, 1),(2, 0)]},
    {"name": "B", "shape": [(0, 0), (1, 0), (2, 0), (2, 1),(3, 1)]},
    {"name": "C", "shape": [(0, 1), (1, 0), (1, 1), (1, 2),(2, 0)]},
    {"name": "D", "shape": [(0, 0), (1, 0), (2, 0), (1, 1)]},
    {"name": "E", "shape": [(0, 0), (1, 0), (2, 0), (3, 0), (1, 1)]},
    {"name": "F", "shape": [(0, 0), (1, 0), (2, 0), (1, 1), (2, 1)]},
    {"name": "G", "shape": [(0, 0), (1, 0), (1, 1), (2, 1)]},
    {"name": "H", "shape": [(0, 0), (0, 1), (0, 2), (1, 2)]},
    {"name": "I", "shape": [(0, 2), (1, 2), (2, 2), (2, 1), (2, 0)]},
    {"name": "J", "shape": [(0, 0), (0, 1), (1, 0), (2, 0), (3, 0)]},
    {"name": "K", "shape": [(0, 0), (0, 1), (1, 0)]},
    {"name": "L", "shape": [(0, 2), (1, 2), (1, 1), (2, 1), (2, 0)]}
]