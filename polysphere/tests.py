from django.test import TestCase
from . import solver, polyominoes, bitmap_polyominoes, bitmap_transformations, bitmap_solver

class PolysphereTestCase(TestCase):
    # Create your tests here.
    def test_first_solution_empty_board(self):
        board = [[0 for _ in range(11)] for _ in range(5)]
        solver1 = solver.PuzzleSolver(board,polyominoes.POLYOMINOES)
        solver1.get_first_solution()
        print(solver1.solutions[0])

    def test_first_solution_non_empty_board(self):
        board = [['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A'],
                 ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A',  'A',  'A', 'A'],
                 ['A', 'A', 'A', 'A', 'A',  0,   0,   'A',   'A',  'A', 'A'],
                 ['A', 'A', 'A',  0,   0,   0,  'A', 'A',  'A',   'A',  'A'],
                 ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A']]
        pieces = [{"name": "B", "shape": [(0, 0), (1, 0), (2, 0), (2, 1),(3, 1)]}]
        solver1 = solver.PuzzleSolver(board, pieces)
        solver1.get_first_solution()
        print(solver1.solutions[0])

        # this orientation doesn't seem to be working, needs investigating
        board = [['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A'],
                 ['A', 'A', 'A', 'A', 'A', 'A', 'A', 0, 'A', 'A', 'A'],
                 ['A', 'A', 'A', 'A', 'A', 'A', 0, 0, 'A', 'A', 'A'],
                 ['A', 'A', 'A', 'A', 'A', 'A', 'A', 0, 0, 'A', 'A'],
                 ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A']]
        pieces = [{"name": "C", "shape": [(0, 1), (1, 0), (1, 1), (1, 2),(2, 0)]}]
        solver1 = solver.PuzzleSolver(board, pieces)
        solver1.get_first_solution()
        print(solver1.solutions[0])

    def test_rotating_bitmaps(self):
        pieces = bitmap_polyominoes.POLYOMINOES
        print("poloyomino 1:")
        for t in bitmap_transformations.generate_transformations(bitmap_transformations.list_to_bitmap(pieces[0]["shape"], pieces[0]["width"]), pieces[0]["width"], pieces[0]["height"]):
            print(bitmap_transformations.bitmap_to_list(t[0],t[1],t[2]),t[1],t[2])

        print("poloyomino 2:")
        for t in bitmap_transformations.generate_transformations(
                bitmap_transformations.list_to_bitmap(pieces[1]["shape"], pieces[1]["width"]), pieces[1]["width"],
                pieces[1]["height"]):
            print(bitmap_transformations.bitmap_to_list(t[0], t[1], t[2]), t[1], t[2])

        print("poloyomino 3:")
        for t in bitmap_transformations.generate_transformations(
                bitmap_transformations.list_to_bitmap(pieces[2]["shape"], pieces[2]["width"]), pieces[2]["width"],
                pieces[2]["height"]):
            print(bitmap_transformations.bitmap_to_list(t[0], t[1], t[2]), t[1], t[2])

    def test_bitmap_solver(self):
        board = [[0 for _ in range(11)] for _ in range(5)]  # 11x5 empty board
        polyominoes = bitmap_polyominoes.POLYOMINOES

        first_solution = bitmap_solver.find_first_solution(board, polyominoes, board_width=11, board_height=5)
        if first_solution:
            print("First solution found:")
            for row in first_solution:
                print(row)
        else:
            print("No solution exists.")

    def test_bitmap_solution_non_empty_board(self):
        board = [[1, 0, 1,],
                 [0, 0, 1,],
                 [1, 0, 0,]]
        polyominoes = [{'id': 3, 'shape': [[0, 1, 0], [1, 1, 0], [0, 1, 1]], 'width':3, 'height':3}]
        first_solution = bitmap_solver.find_first_solution(board, polyominoes, board_width=3, board_height=3)
        if first_solution:
            print("First solution found:")
            for row in first_solution:
                print(row)
        else:
            print("No solution exists.")
