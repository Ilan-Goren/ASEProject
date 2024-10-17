from django.test import TestCase
from . import solver
from . import polyominoes

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