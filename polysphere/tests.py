from django.test import TestCase
from . import solver, polyominoes, matrix_polyominoes, matrix_transformations, matrix_solver

class PolysphereTestCase(TestCase):
    def test_rotate_matrix_poly(self):
        for p in matrix_polyominoes.POLYOMINOES:
            poly = matrix_polyominoes.Polyomino(p["tiles"],p["poly_id"])
            coll = []
            ur = matrix_transformations.unique_rotations(coll, poly)
            for r in coll:
                print(r.poly_id)
                matrix_polyominoes.print_polyomino(r)

    def test_matrix_solver(self):
        polys = []
        for p in matrix_polyominoes.POLYOMINOES:
            poly = matrix_polyominoes.Polyomino(p["tiles"],p["poly_id"])
            polys.append(poly)
        s = matrix_solver.MatrixSolver()
        solution = s.solve_packing(polys,11,5)
        print(solution)

    def test_matrix_solver2(self):
        tiles1 = [[1,0,0],
                  [1,1,0],
                  [1,0,0]]
        tiles2 = [[0,2,2],
                  [0,0,2],
                  [0,2,2]]
        poly1 = matrix_polyominoes.Polyomino(tiles1,1)
        poly2 = matrix_polyominoes.Polyomino(tiles2,2)
        polys = [poly1,poly2]
        s = matrix_solver.MatrixSolver()
        s.solve_packing(polys, 3, 3)

    def test_matrix_solver_partial_config(self):
        p = matrix_polyominoes.Polyomino(matrix_polyominoes.POLYOMINOES[0]["tiles"], 3)
        polys = [p]
        board = [[2,2,2],
                 [0,2,0],
                 [0,0,0]]
        s = matrix_solver.MatrixSolver()
        id_conversions = []
        solution = s.solve_packing(polys,3,3,board, id_conversions)
        solution = s.revert_ids(id_conversions, solution)
        print(solution)

    def test_matrix_solver_partial_config2(self):
        p1 = matrix_polyominoes.Polyomino(matrix_polyominoes.POLYOMINOES[0]["tiles"],
                                         matrix_polyominoes.POLYOMINOES[0]["poly_id"])
        p2 = matrix_polyominoes.Polyomino(matrix_polyominoes.POLYOMINOES[3]["tiles"],
                                         matrix_polyominoes.POLYOMINOES[3]["poly_id"])
        polys = [p1,p2]
        board = [[0,0,0],
                 [0,0,0],
                 [0,0,0]]
        s = matrix_solver.MatrixSolver()
        id_conversions = []
        s.solve_packing(polys, 3, 3,None,id_conversions)
        solutions = s.count_packing(polys,3,3)
        for sol in solutions:
            s.revert_ids(id_conversions, sol)
            print(sol)

