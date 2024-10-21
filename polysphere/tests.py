from django.test import TestCase
from . import solver, polyominoes, matrix_polyominoes, matrix_transformations, matrix_solver

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


    def test_rotate_matrix_poly(self):
        for p in matrix_polyominoes.POLYOMINOES:
            poly = matrix_polyominoes.Polyomino(p["tiles"],p["id"])
            coll = []
            ur = matrix_transformations.unique_rotations(coll, poly)
            for r in coll:
                print(r.poly_id)
                matrix_polyominoes.print_polyomino(r)

    def test_matrix_solver(self):
        polys = []
        for p in matrix_polyominoes.POLYOMINOES:
            poly = matrix_polyominoes.Polyomino(p["tiles"],p["id"])
            polys.append(poly)
        matrix_solver.solve_packing(polys,11,5)

