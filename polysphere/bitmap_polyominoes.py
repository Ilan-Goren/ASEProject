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
    {'id': 1, 'shape': [[1, 1, 1], [1, 0, 1]]},
    {'id': 2, 'shape': [[0, 0, 1, 1], [1, 1, 1,0]]},
    {'id': 3, 'shape': [[0, 1, 0], [1, 1, 0], [0, 1, 1]]},
    {'id': 4, 'shape': [[0, 1, 0], [1, 1, 1]]},
    {'id': 5, 'shape': [[0, 1, 0, 0], [1, 1, 1, 1]]},
    {'id': 6, 'shape': [[0, 1, 1], [1, 1, 1]]},
    {'id': 7, 'shape': [[0, 1, 1], [1, 1, 0]]},
    {'id': 8, 'shape': [[1, 1], [1, 0], [1, 0]]},
    {'id': 9, 'shape': [[1, 1, 1], [0, 0, 1], [0,0,1]]},
    {'id': 10, 'shape': [[1, 0, 0, 0], [1, 1, 1, 1]]},
    {'id': 11, 'shape': [[1, 0], [1, 1]]},
    {'id': 12, 'shape': [[1, 1, 0], [0, 1, 1], [0, 0, 1]]}
]