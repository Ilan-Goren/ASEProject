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
    {'id': 1, 'shape': '111101', 'width':3, 'height':2},
    {'id': 2, 'shape': '00111110', 'width':4, 'height':2},
    {'id': 3, 'shape': '010110011', 'width':3, 'height':3},
    {'id': 4, 'shape': '010111', 'width':3, 'height':2},
    {'id': 5, 'shape': '01001111', 'width':4, 'height':2},
    {'id': 6, 'shape': '011111', 'width':3, 'height':2},
    {'id': 7, 'shape': '011110', 'width':3, 'height':2},
    {'id': 8, 'shape': '111010', 'width':2, 'height':3},
    {'id': 9, 'shape': '111001001', 'width':3, 'height':3},
    {'id': 10, 'shape': '10001111', 'width':2, 'height':4},
    {'id': 11, 'shape': '1011', 'width':2, 'height':2},
    {'id': 12, 'shape': '110011001', 'width':3, 'height':3}
]