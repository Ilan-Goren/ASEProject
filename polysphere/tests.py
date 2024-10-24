from django.test import TestCase
from . import solver
from . import polyominoes

class PolysphereTestCase(TestCase):
    # Create your tests here.
    def test_first_solution_empty_board(self):
        board = [[0 for _ in range(11)] for _ in range(5)]
        '''
        board = [[0,0,0,'A','A','A','A','A','A','A','A'],
                 ['A',0,'A','A','A','A','A','A','A','A','A'],
                 ['A','A','A','A','A','A','A','A','A','A','A'],
                 ['A','A','A','A','A','A','A','A','A','A','A'],
                 ['A','A','A','A','A','A','A','A','A','A','A']]
        piece = [{"name": "D", "shape": [(0, 0), (1, 0), (2, 0), (1, 1)]}]
        '''
        solver1 = solver.PuzzleSolver(board,polyominoes.POLYOMINOES)
        #solver1 = solver.PuzzleSolver(board, piece)
        solver1.get_first_solution()
        print(solver1.solutions[0])